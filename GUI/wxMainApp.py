# -*- coding: utf-8 -*- ############################################################################# Python code generated with wxFormBuilder (version Nov 27 2012)## http://www.wxformbuilder.org/#### PLEASE DO "NOT" EDIT THIS FILE!###########################################################################import wximport wx.xrc############################################################################# Class MyFrame1###########################################################################class MyFrame1 ( wx.Frame ):		def __init__( self, parent ):		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"wxGestalt", pos = wx.DefaultPosition, size = wx.Size( 900,700 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CLIP_CHILDREN|wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )				self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )				self.m_menubar1 = wx.MenuBar( 0 )		self.m_menu1 = wx.Menu()		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"New Machine", wx.EmptyString, wx.ITEM_NORMAL )		self.m_menu1.AppendItem( self.m_menuItem1 )				self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Open a Machine", wx.EmptyString, wx.ITEM_NORMAL )		self.m_menu1.AppendItem( self.m_menuItem2 )				self.m_menuItem7 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Save a Machine", wx.EmptyString, wx.ITEM_NORMAL )		self.m_menu1.AppendItem( self.m_menuItem7 )				self.m_menuItem8 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )		self.m_menu1.AppendItem( self.m_menuItem8 )				self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Quit", wx.EmptyString, wx.ITEM_NORMAL )		self.m_menu1.AppendItem( self.m_menuItem3 )				self.m_menubar1.Append( self.m_menu1, u"File" ) 				self.SetMenuBar( self.m_menubar1 )				self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )		self.bSizer1 = wx.BoxSizer( wx.VERTICAL )				self.fgSizer1 = wx.FlexGridSizer( 2, 1, 0, 0 )		self.fgSizer1.SetFlexibleDirection( wx.BOTH )		self.fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )				self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 900,650 ), 0 )				self.fgSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )						self.bSizer1.Add( self.fgSizer1, 1, wx.EXPAND, 5 )						self.SetSizer( self.bSizer1 )		self.Layout()				self.Centre( wx.BOTH )				# Connect Events		self.Bind( wx.EVT_MENU, self.On_NewMachine, id = self.m_menuItem1.GetId() )		self.Bind( wx.EVT_MENU, self.On_OpenMachine, id = self.m_menuItem2.GetId() )		self.Bind( wx.EVT_MENU, self.On_SaveMachine, id = self.m_menuItem7.GetId() )		self.Bind( wx.EVT_UPDATE_UI, self.On_About, id = self.m_menuItem8.GetId() )		self.Bind( wx.EVT_MENU, self.On_Quit, id = self.m_menuItem3.GetId() )		self.m_notebook1.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.On_SelectNotebookPage )		def __del__( self ):		pass			# Virtual event handlers, overide them in your derived class	def On_NewMachine( self, event ):		event.Skip()		def On_OpenMachine( self, event ):		event.Skip()		def On_SaveMachine( self, event ):		event.Skip()		def On_About( self, event ):		event.Skip()		def On_Quit( self, event ):		event.Skip()		def On_SelectNotebookPage( self, event ):		event.Skip()	