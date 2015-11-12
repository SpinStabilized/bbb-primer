import wx


class OBDApp(wx.App):

    def OnInit(self):
        frame = MainWindow(parent=None)
        frame.Show()
        return True


class MainWindow(wx.Frame):
    def __init__(self, parent):
        self.title = 'Virtual Instrument Cluster'
        wx.Frame.__init__(self, parent, title=self.title, size=(640, 400))

        # Create File Menu
        filemenu = wx.Menu()
        menuAbout_txt = ' About' + self.title
        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About', menuAbout_txt)
        menuExit = filemenu.Append(wx.ID_EXIT, 'E&xit', ' Quit')

        # Create Menubar & Add Menus
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, '&File')
        self.SetMenuBar(menuBar)

        # Bind events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.notebook = ModifiedNotebook(self)
        self.notebook.AddPage(RawPanel(self.notebook), 'Raw Control')

        self.statusbar = self.CreateStatusBar()

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


class DisplayPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.notebook = parent
        self.main_frame = parent.parent
        grid = wx.GridBadSizer(hgap=5, vgap=6)

        self.lbl_throttle = wx.StaticText(self, -1, 'Throttle Position:')
        grid.Add(self.lbl_throttle, pos=(0, 0))

        self.gauge_throttle = wx.Gauge(self, )


class RawPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.notebook = parent
        self.main_frame = parent.parent
        grid = wx.GridBagSizer(hgap=5, vgap=6)

        self.cmd_line = wx.TextCtrl(self, size=(530, 20), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSend, self.cmd_line)
        grid.Add(self.cmd_line, pos=(0, 0))

        self.btn_send_cmd = wx.Button(self, label='Send')
        self.Bind(wx.EVT_BUTTON, self.OnSend, self.btn_send_cmd)
        grid.Add(self.btn_send_cmd, pos=(0, 1))

        self.out = wx.TextCtrl(self, size=(620, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        grid.Add(self.out, pos=(1, 0), span=(1, 2))

        self.SetSizerAndFit(grid)

    def OnSend(self, event):
        cmd = self.cmd_line.GetValue().encode('ascii')
        cmd = cmd + '\r'
        self.out.AppendText(repr(cmd) + '\n')
        self.cmd_line.Clear()
        self.main_frame.statusbar.SetStatusText('Last Command: {}'.format(cmd))


if __name__ == '__main__':
    app = OBDApp()
    app.MainLoop()
