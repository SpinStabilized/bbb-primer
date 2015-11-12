import wx
import math
import wx.lib.agw.speedmeter as SM

class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, "SpeedMeter Demo")

        speed = SM.SpeedMeter(self, agwStyle=
                              SM.SM_DRAW_HAND |
                                                                    SM.SM_DRAW_SECTORS |
                                                                    SM.SM_DRAW_MIDDLE_TEXT|SM.SM_DRAW_SECONDARY_TICKS)

        dial_range = (0, 7000)
        dial_major = 1000
        # Set The Region Of Existence Of SpeedMeter (Always In Radians!!!!)
        speed.SetAngleRange(-math.pi/6, 7*math.pi/6)

        # Create The Intervals That Will Divide Our SpeedMeter In Sectors
        intervals = range(dial_range[0], dial_range[1]+1, dial_major)
        speed.SetIntervals(intervals)

        # Assign The Same Colours To All Sectors (We Simulate A Car Control For Speed)
        # Usually This Is Black
        colours = [wx.BLACK] * (int(dial_range[1] / dial_major) - 1)
        colours.append(wx.RED)
        print len(intervals), len(colours)
        speed.SetIntervalColours(colours)

        # Assign The Ticks: Here They Are Simply The String Equivalent Of The Intervals
        ticks = [str(interval) for interval in intervals]
        speed.SetTicks(ticks)
        # Set The Ticks/Tick Markers Colour
        speed.SetTicksColour(wx.WHITE)
        # We Want To Draw 5 Secondary Ticks Between The Principal Ticks
        speed.SetNumberOfSecondaryTicks(1)

        # Set The Font For The Ticks Markers
        speed.SetTicksFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # Set The Text In The Center Of SpeedMeter
        speed.SetMiddleText("Km/h")
        # Assign The Colour To The Center Text
        speed.SetMiddleTextColour(wx.WHITE)
        # Assign A Font To The Center Text
        speed.SetMiddleTextFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))

        # Set The Colour For The Hand Indicator
        speed.SetHandColour(wx.Colour(255, 50, 0))

        # Do Not Draw The External (Container) Arc. Drawing The External Arc May
        # Sometimes Create Uglier Controls. Try To Comment This Line And See It
        # For Yourself!
        speed.DrawExternalArc(False)

        # Set The Current Value For The SpeedMeter
        speed.SetSpeedValue(44)


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()
