# -*- coding: utf-8 -*-

# Modules
# Modules for the wx GUI
import wx
import wx.stc as stc
import GUI.wxMainApp as wxMainApp
import GUI.wxTabSetup as wxTabSetup
import GUI.wxNodeTab as wxNodeTab
import GUI.wxTabIdentify as wxTabIdentify
import GUI.wxTabTest as wxTabTest
import GUI.wxTabCAM as wxTabCAM
import GUI.wxCodeEditor as wxCodeEditor
# Various functions
import Functions.wxFunctions as wxFunctions
import Functions.wxSubThread as wxSubThread
# Module for log
import sys
# Modules for temp file
import os
import codecs
from unidecode import unidecode
# Module for Gestalt Machines
import Machines.wxMachines as wxMachines
# sleep
from time import sleep
# Import gestalt
from gestalt import utilities


# Variables
# The current machine edited in the app
currentMachine = wxMachines.wxMachine(persistenceFile="debug.vmp")
GUImachine = wxMachines.wxMachineGUI()
terminal = sys.stdout
path_file_opened = ""


# Classes
# Class for redirecting the terminal to the log screen
class RedirectText():
    # Redirect the print message to the Status log area
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    #def write(self,string):
    #    self.out.WriteText(string)
    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)


# Class for threading: for managing the gestalt nodes, which is a long process
class InitThread(wxSubThread.SimpleThread):

    def run(self):
        global currentMachine
        currentMachine.initMachine()

        # Test node
        number = currentMachine.nodesNumber
        print "Number of nodes:",number
        if number == 1:
            moves = [[10],[20],[10],[0]]
        elif number == 2:
            moves = [[10,10],[20,20],[10,10],[0,0]]
        elif number == 3:
            moves = [[10,10,10],[20,20,20],[10,10,10],[0,0,0]]
        elif number == 4:
            moves = [[10,10,10,10],[20,20,20,20],[10,10,10,10],[0,0,0,0]]

        print
        print "Testing the nodes..."

        currentMachine.machineNodes.setVelocityRequest(8)

        # #Test move
        for coords in moves:
            currentMachine.move(coords, 0)
            status = currentMachine.machineNodes.spinStatusRequest()
            while status[0]['stepsRemaining'] > 0:
                  sleep(0.001)
                  status = currentMachine.machineNodes.spinStatusRequest()

        print
        print "Nodes tested successfully."


# The class for the Setup tab
class wxTabSetup(wxTabSetup.MyPanel1):

    def On_OrganizeNodes( self, event ):

        global GUImachine

        # Add or remove nodes and therefore their GUI editing part
        if self.m_spinCtrl1.GetValue() < GUImachine.nodesNumber:
            self.m_notebook_nodes.DeletePage(self.m_spinCtrl1.GetValue())
            GUImachine.nodesNumber -=1
        else:
            nodePage = wxNodeTabSetup(self.m_notebook_nodes)
            self.m_notebook_nodes.AddPage(nodePage,u"Node #"+str(GUImachine.nodesNumber+1))
            GUImachine.nodesNumber += 1

        # Feedback on the status bar
        if GUImachine.nodesNumber == 1:
            message = "The Machine now has " + str(GUImachine.nodesNumber) + " Gestalt node."
        else:
            message = "The Machine now has " + str(GUImachine.nodesNumber) + " Gestalt nodes."
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)

        # Update the virtual class for the machine in the GUI
        GUImachine.initNodesGUI(GUImachine.nodesNumber)
        currentMachine.nodesNumber = GUImachine.nodesNumber


# The class for the Node tab
class wxNodeTabSetup(wxNodeTab.MyPanel1):

    def On_ChooseNodeType( self, event):
        global GUImachine

        currentNode = self.GetParent().GetSelection()
        currentType = self.m_radioBox1.GetSelection()
        if currentType == 0:
            message = "Node #" + str(currentNode+1) + " is linear."
            self.GetParent().GetParent().GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
            GUImachine.nodesGUI[currentNode]["linear"] = True
            GUImachine.nodesGUI[currentNode]["rotary"] = False
            currentMachine.linear = True
            currentMachine.rotary = False
        else:
            message = "Node #" + str(currentNode+1) + " is rotary."
            self.GetParent().GetParent().GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
            GUImachine.nodesGUI[currentNode]["linear"] = False
            GUImachine.nodesGUI[currentNode]["rotary"] = True
            currentMachine.linear = False
            currentMachine.rotary = True


# The class for the Identify tab
class wxTabIdentify(wxTabIdentify.MyPanel1):

    def On_InitializeMachine( self, event ):
        global currentMachine
        global GUImachine
        message = "Initializing the nodes..."
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
        currentMachine = wxMachines.wxMachine(nodesNumber = GUImachine.nodesNumber, interfaceType = currentMachine.interfaceType, portName = currentMachine.portName, persistence="debug.vmp")
        print "---------------------------------------------------------------------------------------------------------------"
        print "Please identify each Gestalt node by pressing on their buttons when asked here:"
        print
        initialize = InitThread()
        event.Skip()


# The class for the Test tab
class wxTabTest(wxTabTest.MyPanel1):

    def InitUI(self):
        global currentMachine
        # Clean previous interface
        for k in range(len(self.control)):
            self.controlSizer.Hide(self.control[k])
            self.controlSizer.Remove(self.control[k])
            self.controlSizer.Hide(self.label[k])
            self.controlSizer.Remove(self.label[k])
            self.controlSizer.Hide(self.button[k])
            self.controlSizer.Remove(self.button[k])
        del self.control
        del self.label
        del self.button
        self.control = {}
        self.label = {}
        self.button = {}

        # Create the new interface
        for g in range(currentMachine.nodesNumber):
            self.label[g] = wx.StaticText( self, wx.ID_ANY, "Node #"+str(g+1), (10, 50+100*g), wx.DefaultSize, 0 )
            self.label[g].Wrap( -1 )
            self.controlSizer.Add( self.label[g], 0, wx.ALL, 5 )
            self.control[g] = wx.Slider( self, wx.ID_ANY, 50, 0, 100, (100, 50+100*g), wx.DefaultSize, wx.SL_HORIZONTAL )
            self.controlSizer.Add( self.control[g], 0, wx.ALL, 5 )
            self.button[g] = wx.Button( self, wx.ID_ANY, u"Test this node", (300, 50+100*g-5), wx.DefaultSize, 0 )
            self.controlSizer.Add( self.button[g], 0, wx.ALL, 5 )
            self.button[g].Bind( wx.EVT_BUTTON, self.On_TestNode )

    def On_TestNode(self, event):
        global currentMachine
        message = "Testing... Not working at the moment"
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)


# The class for the CAM tab
class wxTabCAM(wxTabCAM.MyPanel1):

    def __init__(self, *args, **kw):
        super(wxTabCAM, self).__init__(*args, **kw)
        # Get rid of the TextCtrl added in the wxFormBuilder file
        self.bSizer2.Hide(self.m_textCtrl1)
        self.bSizer2.Remove(self.m_textCtrl1)
        # Add a styled text editor
        self.editor = wxCodeEditor.codeEditor(self, -1)
        self.bSizer2.Add(self.editor, 1, wx.EXPAND)
        self.editor.EmptyUndoBuffer()
        self.editor.Colourise(0, -1)
        self.editor.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.editor.SetMarginWidth(1, 25)
        # Load basic template.py file at startup
        self.editor.SetText(open(os.getcwd() + "/CAM/template.py").read())

    def On_LoadFile( self, event ):
        global path_file_opened
        path_file_opened = event.GetPath()
        self.editor.SetText(open(path_file_opened).read())
        message = "File loaded:"
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
        event.Skip()

    def On_SaveCAM( self, event ):
        global path_file_opened
        file_to_save = self.editor.GetValue()
        fo = open(path_file_opened, "w+")
        fo.write(file_to_save.encode('utf8'));
        fo.close()
        message = "File saved"
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
        event.Skip()

    def On_LaunchCAM( self, event ):
        # Save a temporary file
        file_to_save = self.editor.GetValue()
        temp_path = os.getcwd() + "/temp_temp.py"
        fo_temp = codecs.open(temp_path, "w+",'utf-8')
        fo_temp.write(unidecode(file_to_save));
        fo_temp.close()
        # Create the tab
        import temp_temp
        self.GetParent().GetParent().tab_go = temp_temp.MyPanel1(self.GetParent().GetParent().m_notebook1)
        self.GetParent().GetParent().m_notebook1.AddPage(self.GetParent().GetParent().tab_go, "5. Run the machine")
        message = "Launch tab created"
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
        event.Skip()


# The class for the main app
class wxGestaltApp(wxMainApp.MyFrame1):

    def __init__(self, *args, **kw):
        super(wxGestaltApp, self).__init__(*args, **kw)
        global currentMachine

        self.InitUI()

    def InitUI(self):

        # Add Setup Tab
        self.tab_setup = wxTabSetup(self.m_notebook1)
        # Serial port setup
        self.tab_setup.m_listBox_serialPorts.Bind( wx.EVT_LISTBOX, self.On_ChooseSerialPort )
        SerialPortsAvailable = wxFunctions.ScanSerialPorts()
        self.tab_setup.m_listBox_serialPorts.Set(SerialPortsAvailable)
        # Baudrate setup
        self.tab_setup.m_listBox_baudrates.Set(wxMachines.baudratesListStrings)
        self.tab_setup.m_listBox_baudrates.SetSelection(16)
        self.tab_setup.m_listBox_baudrates.Bind( wx.EVT_LISTBOX, self.On_ChooseBaudrate )
        # Interface setup
        self.tab_setup.m_listBox_interfaceType.Set(wxMachines.interfacesList)
        self.tab_setup.m_listBox_interfaceType.SetSelection(0)
        self.tab_setup.m_listBox_interfaceType.Bind( wx.EVT_LISTBOX, self.On_ChooseInterface )

        # Add tab
        self.m_notebook1.AddPage(self.tab_setup, "1. Machine Setup")

        # Add Identify Tab
        self.tab_identify = wxTabIdentify(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_identify, "2. Identify the nodes")

        # Add Test Tab
        self.tab_test = wxTabTest(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_test, "3. Test the Machine")

        # Add CAM Tab
        self.tab_cam = wxTabCAM(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_cam, "4. CAM")


    def On_Quit( self, event ):
        self.Close(True)

    def On_ChooseSerialPort( self, event ):
        global currentMachine
        currentMachine.portName = event.GetString()
        message = "Connecting to " + currentMachine.portName + " ..."
        self.m_statusBar1.SetStatusText(message, 0)

    def On_ChooseBaudrate( self, event ):
        global currentMachine
        currentMachine.baudRate = wxMachines.baudratesList[event.GetSelection()]
        message = "Connecting with a baudrate of " + str(currentMachine.baudRate) + "..."
        self.m_statusBar1.SetStatusText(message, 0)

    def On_ChooseInterface( self, event ):
        global currentMachine
        currentMachine.interfaceType = wxMachines.interfacesList[event.GetSelection()]
        message = "Connecting with the " + currentMachine.interfaceType + " protocol..."
        self.m_statusBar1.SetStatusText(message, 0)

    def On_SelectNotebookPage( self, event):
        currentMainTab = event.GetSelection()
        if currentMainTab == 2 and currentMachine.nodesNumber != 0:
            self.tab_test.InitUI()
        event.Skip()

    def On_Message(self, title, content):
        # Open up a dialog
        dlg = wx.MessageDialog(self, content, title, wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    ex = wx.App()
    ex1 = wxGestaltApp(None)
    ex1.Show()
    # Starting the log
    # Redirect text here
    redir=RedirectText(ex1.tab_identify.wxLog)
    sys.stdout=redir
    ex.MainLoop()
