import wx
from SeChainController.MainController import MainController
from SeChainController import NodeInformation

class MainApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.drow_frame(None, -1, 'Se-Chain')
        frame.Show(True)
        NodeInformation.ui_frame = frame
        self.SetTopWindow(frame)
        return True

class MainFrame(wx.Frame):
    trust_node_panel = None
    console_panel = None
    console_text = ""

    def __init__(self):
        return None


    def drow_frame(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(500, 250))

        # console
        self.console_panel = wx.Panel(self, -1)
        self.console_text = wx.StaticText(self.console_panel, 9, "Console", (30, 15), (500, 15), style=wx.LEFT)

        # Welcome message
        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_panel = wx.Panel(self, -1)
        wx.StaticText(welcome_panel, 1, "Welcome Se-Chain", (30, 15), style=wx.LEFT)
        vbox.Add(welcome_panel, 1, wx.EXPAND)

        # IP address
        ip_panel = wx.Panel(self, -1)
        ip_address = MainController.get_ip_address()
        wx.StaticText(ip_panel, 1, "Your IP Address:"+ip_address, (30, 30), style=wx.LEFT)
        vbox.Add(ip_panel, 1, wx.EXPAND)

        # Setting Trust Node Box
        trust_node_box = wx.BoxSizer(wx.HORIZONTAL)
        self.trust_node_panel = wx.Panel(self, -1)
        self.set_trust_node_text()
        trust_node_box.Add(self.trust_node_panel, 1, wx.EXPAND)

        trust_node_text = wx.TextEntryDialog(self, '', 'Text Entry')
        trust_node_text.SetValue("Default")
        trust_node_box.Add(trust_node_text, 1, wx.EXPAND)

        trust_node_button = wx.Button(self, 1, '1. Set Trust Node')
        trust_node_box.Add(trust_node_button, 1, wx.EXPAND)
        vbox.Add(trust_node_box, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.set_trust_node, id=1)

        #start
        start_button = wx.Button(self, 3, "4. Se Chain Start")
        vbox.Add(start_button, 3, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.start_sechain, id=3)

        #start
        trust_start_button = wx.Button(self, 4, "*. Start Trust Node (if this is trust node)")
        vbox.Add(trust_start_button, 4, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.start_trust_node, id=4)

        self.SetSizer(vbox)
        self.Center()

        #console
        vbox.Add(self.console_panel, 1, wx.EXPAND)

    def set_trust_node_text(self):
        from SeChainController import NodeInformation

        my_ip = NodeInformation.trust_node_ip

        wx.StaticText(self.trust_node_panel, 1, "TrustNode : " + my_ip, (30, 30), style=wx.LEFT)

    def set_trust_node(self, event):
        import NodeInformation
        dlg = wx.TextEntryDialog(self, '', 'Text Entry')
        dlg.SetValue(NodeInformation.trust_node_ip)
        if dlg.ShowModal() == wx.ID_OK:
            # need to validation check (IP format)
            NodeInformation.trust_node_ip = dlg.GetValue()
            self.set_trust_node_text()
        dlg.Destroy()
        self.write_console("Trust node is set")

    def write_console(self, message):
        NodeInformation.ui_frame.console_text.SetLabel(message)

    def start_sechain(self, event):
        MainController.initiate_node()

    def start_trust_node(self, event):
        from MainController import NodeInformation
        if NodeInformation.my_ip_address == NodeInformation.trust_node_ip :
            self.write_console("start trust node")
            MainController.node_start()
        else:
            self.write_console("This IP and trust node IP is not same")
