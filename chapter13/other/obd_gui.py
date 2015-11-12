import wx
import wx.lib.agw.speedmeter as SM
#import Adafruit_BBIO.UART as UART
import obd
import logging
import sys
import math

logger = logging.getLogger(__name__)


class OBDApp(wx.App):

    def OnInit(self):
        # UART.setup('UART2')
        # port = '/dev/ttyO2'
        # baud = 38400

        # try:
        #     msg = 'Attempting to connect to {} at rate {}'
        #     logging.info(msg.format(port, baud))
        #     obd_connect = obd.OBDToUART(port=port, baud=baud)
        # except Exception as e:
        #     msg = 'Unable to open connection to OBD hardware on port {}. Exiting.'
        #     logging.error(msg.format(port))
        #     print(msg.format(port))
        #     sys.exit()
        # self.car = obd.Car(obd_connect)
        frame = MainWindow(None, car=None)
        frame.SetTitle('Virtual Instrument Cluster')
        frame.Show()
        return True


class MainWindow(wx.Frame):
    def __init__(self, parent, car=None):
        self.car = car
        self.title = 'Virtual Instrument Cluster'
        wx.Frame.__init__(self, parent, title=self.title, size=(640, 400))
        box = wx.BoxSizer(wx.VERTICAL)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        line1_sizer = box = wx.BoxSizer(wx.HORIZONTAL)
        self.info_pnl = InfoPanel(self, style=wx.SIMPLE_BORDER)
        line1_sizer.Add(self.info_pnl, 0, wx.EXPAND)

        box.Add(line1_sizer, 0, wx.EXPAND)
        self.SetSizer(box)
        self.Layout()

        wx.CallLater(500, self.Start)

    def Start(self):
        self.timer.Start(1000 // 3)            # 2 fps

    def Update(self, event):
        pass

    def OnExit(self, event):
        self.Close(True)


class InfoPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """Create the DemoPanel."""
        wx.Panel.__init__(self, *args, **kwargs)
        lbl_format = '{:<10}'

        box = wx.BoxSizer(wx.VERTICAL)
        lbl_panel_txt = 'General Information:'
        lbl_panel = wx.StaticText(self, -1, lbl_panel_txt, (30, 15), style=wx.ALIGN_LEFT)
        box.Add(lbl_panel, 0, wx.EXPAND)

        vin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_vin_txt = lbl_format.format('VIN:')
        lbl_vin = wx.StaticText(self, -1, lbl_vin_txt, (30, 15), style=wx.ALIGN_LEFT)
        vin_sizer.Add(lbl_vin, 0, wx.EXPAND)

        self.vin = wx.StaticText(self, -1, '', (30, 15), style=wx.ALIGN_LEFT)
        vin_sizer.Add(self.vin, 0, wx.EXPAND)

        box.Add(vin_sizer, 0, wx.EXPAND)

        ecm_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_ecm_txt = lbl_format.format('ECM Name:')
        lbl_ecm = wx.StaticText(self, -1, lbl_ecm_txt, (30, 15), style=wx.ALIGN_LEFT)
        ecm_sizer.Add(lbl_ecm)

        self.ecm = wx.StaticText(self, -1, '', (30, 15), style=wx.ALIGN_LEFT)
        ecm_sizer.Add(self.ecm)

        box.Add(ecm_sizer, 0, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()

        self.Update(vin='2C4RDGEG5DR661979', ecm='PCM-PowertrainCtrl')

    def Update(self, vin='', ecm=''):
        self.vin.SetLabel('{:<20}'.format(vin))
        self.ecm.SetLabel('{:<20}'.format(ecm))


class RPMPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """Create the DemoPanel."""
        wx.Panel.__init__(self, *args, **kwargs)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.rpm = SM.SpeedMeter(self, agwStyle=SM.SM_DRAW_HAND|SM.SM_DRAW_SECTORS|SM.SM_DRAW_MIDDLE_TEXT|SM.SM_DRAW_SECONDARY_TICKS)

        dial_range = (0, 7001)
        dial_major = 1000
        # Set The Region Of Existence Of SpeedMeter (Always In Radians!!!!)
        self.rpm.SetAngleRange(math.radians(0), math.radians(180))

        # Create The Intervals That Will Divide Our SpeedMeter In Sectors
        intervals = range(dial_range[0], dial_range[1]+1, dial_major)
        self.rpm.SetIntervals(intervals)

        # Assign The Same Colours To All Sectors (We Simulate A Car Control For Speed)
        # Usually This Is Black
        colours = [wx.BLACK] * (int(dial_range[1] / dial_major) - 1)
        colours.append(wx.RED)
        print len(intervals), len(colours)
        self.rpm.SetIntervalColours(colours)

        # Assign The Ticks: Here They Are Simply The String Equivalent Of The Intervals
        ticks = [str(interval) for interval in intervals]
        self.rpm.SetTicks(ticks)
        # Set The Ticks/Tick Markers Colour
        self.rpm.SetTicksColour(wx.WHITE)
        # We Want To Draw 5 Secondary Ticks Between The Principal Ticks
        self.rpm.SetNumberOfSecondaryTicks(1)

        # Set The Font For The Ticks Markers
        self.rpm.SetTicksFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # Set The Text In The Center Of SpeedMeter
        self.rpm.SetMiddleText("RPM")
        # Assign The Colour To The Center Text
        self.rpm.SetMiddleTextColour(wx.WHITE)
        # Assign A Font To The Center Text
        self.rpm.SetMiddleTextFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))

        # Set The Colour For The Hand Indicator
        self.rpm.SetHandColour(wx.Colour(255, 50, 0))

        # Do Not Draw The External (Container) Arc. Drawing The External Arc May
        # Sometimes Create Uglier Controls. Try To Comment This Line And See It
        # For Yourself!
        self.rpm.DrawExternalArc(False)

        # Set The Current Value For The SpeedMeter
        self.rpm.SetSpeedValue(2000)

        box.Add(self.rpm, 0, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()



    def Update(self, speed=0):
        self.rpm.SetSpeedValue(speed)


if __name__ == '__main__':
    logging_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logging_format,
                        datefmt='%m-%d %H:%M',
                        filename='obd_basic.log',
                        filemode='w')

    app = OBDApp()
    app.MainLoop()
