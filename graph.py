#!/usr/bin/env python2.7

debug = True

import numpy as np
import matplotlib as mp

mp.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx
import glob

class mainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=None, title='Main frame', size=(800,600))

        #### make menu bar and menu

        self.filemenu = wx.Menu()
        self.exitId, self.aboutId = wx.NewId(), wx.NewId()
        # TODO: why do these texts/shortcuts not show up in the same way in the actual menu?
        self.menuAbout = self.filemenu.Append(id=self.aboutId, text='About\tCtrl+a', help='Informations')
        self.menuExit = self.filemenu.Append(id=self.exitId, text='Exit\tCtrl+w', help='Quit')

        self.menubar = wx.MenuBar()
        self.menubar.Append(self.filemenu, title='File')
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, self.onAbout, source=self.menuAbout)
        self.Bind(wx.EVT_MENU, self.onExit, source=self.menuExit)

    def onAbout(self, e):
        dlg = wx.MessageDialog(self, 'A data explorer.', 'About the data explorer', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, e):
        self.Close(True)


class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #### make sizers

        self.topSizer = wx.BoxSizer(wx.VERTICAL)
        self.plotSizer = wx.BoxSizer(wx.VERTICAL)
        self.inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.textInputSizer = wx.GridSizer(0, 2, 5, 5)

        #### add sizers to each other

        self.topSizer.Add(self.plotSizer, 1, wx.EXPAND)
        self.topSizer.Add(self.inputSizer, 0, wx.EXPAND)
        self.inputSizer.Add(self.textInputSizer, 1, wx.EXPAND)

        #### make objects

        # mp figure object for 1D plot
        self.figure1D = Figure()
        gs = mp.gridspec.GridSpec(1, 2, width_ratios=[1,1.618])
        self.axes2D = self.figure1D.add_subplot(gs[0])
        self.axes1D = self.figure1D.add_subplot(gs[1])
        self.plot1D = FigureCanvas(self, -1, self.figure1D)
        self.drawPlot1D('data/d1_1_d2_1/pts.dat')
        self.drawPlot2D()

        # text input objects
        self.baseText = wx.StaticText(self, -1, "base pathname")
        self.middleText = wx.StaticText(self, -1, "middle of pathname")
        self.endText = wx.StaticText(self, -1, "end of pathname")
        self.text1D = wx.StaticText(self, -1, "1D data file")
        self.text2D = wx.StaticText(self, -1, "2D data file")
        self.baseInput = wx.TextCtrl(self, -1, "")
        self.middleInput = wx.TextCtrl(self, -1, "")
        self.endInput = wx.TextCtrl(self, -1, "")
        self.text1DInput = wx.TextCtrl(self, -1, "")
        self.text2DInput = wx.TextCtrl(self, -1, "")

        loadBtn = wx.Button(self, -1, "Load Data")
        self.Bind(wx.EVT_BUTTON, self.onLoad, id=loadBtn.GetId())

        #### add objects to sizers

        self.plotSizer.Add(self.plot1D, 1, wx.EXPAND)
        self.textInputSizer.Add(self.baseText, 1, wx.ALIGN_LEFT)
        self.textInputSizer.Add(self.baseInput, 2, wx.EXPAND)
        self.textInputSizer.Add(self.middleText, 1, wx.ALIGN_LEFT)
        self.textInputSizer.Add(self.middleInput, 2, wx.EXPAND)
        self.textInputSizer.Add(self.endText, 1, wx.ALIGN_LEFT)
        self.textInputSizer.Add(self.endInput, 2, wx.EXPAND)
        self.textInputSizer.Add(self.text1D, 1, wx.ALIGN_LEFT)
        self.textInputSizer.Add(self.text1DInput, 2, wx.EXPAND)
        self.textInputSizer.Add(self.text2D, 1, wx.ALIGN_LEFT)
        self.textInputSizer.Add(self.text2DInput, 2, wx.EXPAND)
        self.inputSizer.Add(loadBtn, 0, wx.EXPAND)

        #### set sizer for panel

        self.SetSizer(self.topSizer)
        self.Fit()

    def onLoad(self, e):
        '''
        1. Regex to find directories with data
         a. Assume rectangular data set, i.e. all y values for all x values
        2. Find which files exist
        3. Add files to map, read 2D data into array
        '''

        basePath = self.baseInput.GetValue()
        midPath = self.middleInput.GetValue()
        endPath = self.endInput.GetValue()

        globber = basePath + '*' + midPath + '*' + endPath
        if (debug):
            print globber
        globs = glob.glob(globber)
        print globs

    def getDirs(self, basePath, midPath, endPath):
        pass

    def drawPlot1D(self, fileName=None):
        if (fileName):
            data = np.loadtxt(fileName)
            self.axes1D.plot(data[:,0], data[:,1])
        else:
            t = np.arange(0.0, 3.0, 0.01)
            s = np.sin(2 * np.pi * t)
            self.axes2D.plot(t, s)

    def drawPlot2D(self, fileName=None):
        if (fileName):
            data = np.loadtxt(fileName)
            self.axes2D.plot(data[:,0], data[:,1])
        else:
            xdata = np.arange(10)
            ydata = np.arange(10)
            X, Y = np.meshgrid(xdata, ydata)
            Z = np.arange(100).reshape(10,10)
            self.axes2D.matshow(Z)


if __name__ == "__main__":
    app = wx.App(False)
    fr = mainFrame(None)
    panel = CanvasPanel(fr)
    fr.Show()
    # start with focus on first input text box
    panel.baseInput.SetFocus()
    app.MainLoop()
