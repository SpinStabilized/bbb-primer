import wx
import wx.lib.agw.pygauge as PG

class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "PyGauge Demo")

        panel = wx.Panel(self)

        gauge1 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
        gauge1.SetValue(80)
        gauge1.SetBackgroundColour(wx.WHITE)
        gauge1.SetBorderColor(wx.BLACK)

        gauge2 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
        gauge2.SetValue([20, 80])
        gauge2.SetBarColor([wx.Colour(162, 255, 178), wx.Colour(159, 176, 255)])
        gauge2.SetBackgroundColour(wx.WHITE)
        gauge2.SetBorderColor(wx.BLACK)
        gauge2.SetBorderPadding(2)
        gauge2.Update([30, 0], 2000)

        gauge3 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
        gauge3.SetValue(50)
        gauge3.SetBarColor(wx.GREEN)
        gauge3.SetBackgroundColour(wx.WHITE)
        gauge3.SetBorderColor(wx.BLACK)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gauge1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
        sizer.Add(gauge2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
        sizer.Add(gauge3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)

        panel.SetSizer(sizer)
        sizer.Layout()


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()
