import wx
import wx.lib.agw.speedmeter as SM
import Adafruit_BBIO.UART as UART
import obd
import logging
import sys

logger = logging.getLogger(__name__)


class OBDApp(wx.App):

    def OnInit(self, car=None):
        UART.setup('UART2')
        port = '/dev/ttyO2'
        baud = 38400

        try:
            msg = 'Attempting to connect to {} at rate {}'
            logging.info(msg.format(port, baud))
            obd_connect = obd.OBDToUART(port=port, baud=baud)
        except Exception as e:
            msg = 'Unable to open connection to OBD hardware on port {}. Exiting.'
            logging.error(msg.format(port))
            print(msg.format(port))
            sys.exit()
        car = obd.Car(obd_connect)
        frame = MainWindow(parent=None, car=car)
        frame.SetTitle('Virtual Instrument Cluster')
        frame.Show()
        return True


class MainWindow(wx.Frame):
    def __init__(self, parent, car=None):
        self.car = car
        self.title = 'Virtual Instrument Cluster'
        wx.Frame.__init__(self, parent, title=self.title, size=(640, 400))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        self.notebook = ModifiedNotebook(self)
        self.display_panel = DisplayPanel(self.notebook)
        self.notebook.AddPage(self.display_panel, 'Instruments')

        self.statusbar = self.CreateStatusBar()

        wx.CallLater(500, self.Start)

    def Start(self):
        self.timer.Start(1000 // 10)            # 2 fps

    def update(self):
        throttle = car.mnemonic_cmd('throttle_position')
        temp = self.car.mnemonic_cmd('ambient_temp')
        tach = self.car.mnemonic_cmd('tach')
        self.display_panel.throttle.update(throttle)
        self.display_panel.temperature.update(temp)
        self.display_panel.meter.SetSpeedValue(tach)

    def OnAbout(self, event):
        text = 'A BeagleBone Black based\nCar Virtual Instrument Cluster'
        dlg = wx.MessageDialog(self, text, 'About ' + self.title, wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)


class ModifiedNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.parent = parent


class InstrumentsGaugePanel(wx.Panel):
    def __init__(self, parent, label, units='', full_range=(0, 100)):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.value = 0
        self.units = units
        self.full_range = full_range
        range = self.map_range(self.full_range[1])
        text_box = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.BoxSizer(wx.VERTICAL)

        self.lbl = wx.StaticText(self, label=label)
        text_box.Add(self.lbl, 0, wx.EXPAND)
        self.val = wx.StaticText(self, label='')
        text_box.Add(self.val, 0, wx.EXPAND)

        box.Add(text_box, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        self.gauge = wx.Gauge(self, range=range, size=(250, 25))
        box.Add(self.gauge, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)

        self.SetSizer(box)

    def update(self, value):
        self.value = value
        self.val.SetLabel('{} {}'.format(self.value, self.units))
        self.gauge.SetValue(self.map_range(self.value))

    def map_range(self, value):
        negative = 0 - self.full_range[0]
        return value + negative


class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        box = wx.BoxSizer(wx.VERTICAL)

        self.throttle = InstrumentsGaugePanel(self, 'Throttle: ', units='%')
        box.Add(self.throttle, 0, wx.EXPAND)

        self.temperature = InstrumentsGaugePanel(self, 'Temp: ', units='dgC', full_range=(-40, 215))
        box.Add(self.temperature, 0, wx.EXPAND)

        self.meter = SM.SpeedMeter(self,
                                   agwStyle=SM.SM_DRAW_HAND |
                                   SM.SM_DRAW_FANCY_TICKS)
        self.meter.SetIntervals(range(0, 12000, 12))
        # self.meter.SetIntervalColours([wx.BLACK] * 12)
        self.meter.SetTicks([str(interval) for interval in range(0, 12001, 12)])
        self.meter.SetTicksColour(wx.BLACK)
        # self.meter.SetNumberOfSecondaryTicks(4)
        # Set The Font For The Ticks Markers
        self.meter.SetTicksFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # Set The Colour For The Hand Indicator
        self.meter.SetHandColour(wx.Colour(255, 50, 0))

        # Do Not Draw The External (Container) Arc. Drawing The External Arc
        # May Sometimes Create Uglier Controls. Try To Comment This Line And
        # See It For Yourself!
        self.meter.DrawExternalArc(False)

        # Set The Current Value For The SpeedMeter
        self.meter.SetSpeedValue(44)
        box.Add(self.meter, 1, wx.EXPAND)
        self.SetSizer(box)


if __name__ == '__main__':
    logging_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logging_format,
                        datefmt='%m-%d %H:%M',
                        filename='obd_basic.log',
                        filemode='w')

    app = OBDApp(redirect=False)
    app.MainLoop()
