import wx
from SeChainController.MainController import MainController
from SeChainController import Property

class MainApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.drow_frame(None, -1, 'Se-Chain')
        frame.Show(True)
        Property.ui_frame = frame
        self.SetTopWindow(frame)
        return True

class MainFrame(wx.Frame):
    trust_node_panel = None
    console_panel = None
    console_text = ""

    def __init__(self):
        return None


    def drow_frame(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(700, 350))

        vbox = wx.BoxSizer(wx.VERTICAL)

        # console
        self.console_panel = wx.Panel(self, -1)
        self.console_text = wx.StaticText(self.console_panel, 9, "Console", (30, 15), (500, 90), style=wx.LEFT)

        # menu
        menubar = wx.MenuBar()
        trx_menu = wx.Menu()
        menubar.Append(trx_menu, '&Send Transaction')
        trx_menu.Append(1, '&Send Data Transaction')
        trx_menu.Append(2, '&Deploy Smart Contract')
        trx_menu.Append(3, '&Run Smart Contract')
        self.Bind(wx.EVT_MENU, self.send_transaction, id=1)
        self.Bind(wx.EVT_MENU, self.deploy_contract, id=2)
        self.Bind(wx.EVT_MENU, self.run_contract, id=3)
        self.SetMenuBar(menubar)

        # Welcome message
        welcome_panel = wx.Panel(self, -1)
        wx.StaticText(welcome_panel, 1, "Welcome to Se-Chain", (30, 15), style=wx.LEFT)
        vbox.Add(welcome_panel, 0, wx.EXPAND)

        # IP address
        ip_panel = wx.Panel(self, -1)
        ip_address = MainController.get_ip_address()
        wx.StaticText(ip_panel, 1, "Your IP Address:" + Property.my_ip_address, (30, 30), style=wx.LEFT)
        vbox.Add(ip_panel, 0, wx.EXPAND)

        # Setting Trust Node Box
        trust_node_box = wx.BoxSizer(wx.HORIZONTAL)
        self.trust_node_panel = wx.Panel(self, -1)
        self.set_trust_node_text()
        trust_node_box.Add(self.trust_node_panel, 0, wx.EXPAND)

        trust_node_text = wx.TextEntryDialog(self, '', 'Setting Trust Node')
        trust_node_text.SetValue("Default")
        trust_node_box.Add(trust_node_text, 0, wx.EXPAND)

        trust_node_button = wx.Button(self, 1, '1. Set Trust Node')
        trust_node_box.Add(trust_node_button, 1, wx.EXPAND)
        vbox.Add(trust_node_box, 0, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.set_trust_node, id=1)

        #start
        start_button = wx.Button(self, 3, "4. Se Chain Start")
        vbox.Add(start_button, 0, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.start_sechain, id=3)

        #start
        trust_start_button = wx.Button(self, 4, "*. Start Trust Node (if this is trust node)")
        vbox.Add(trust_start_button, 0, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.start_trust_node, id=4)

        self.SetSizer(vbox)
        self.Center()

        #console
        vbox.Add(self.console_panel, 1, wx.EXPAND)

    def set_trust_node_text(self):
        from SeChainController import Property

        my_ip = Property.trust_node_ip

        wx.StaticText(self.trust_node_panel, 1, "TrustNode : " + my_ip, (30, 30), style=wx.LEFT)

    def set_trust_node(self, event):
        from SeChainController import Property
        dlg = wx.TextEntryDialog(self, '', 'Setting Trust Node')
        dlg.SetValue(Property.trust_node_ip)
        if dlg.ShowModal() == wx.ID_OK:
            # need to validation check (IP format)
            Property.trust_node_ip = dlg.GetValue()
            self.set_trust_node_text()
        dlg.Destroy()
        self.write_console("Trust node is set")

    def write_console(self, message):
        Property.ui_frame.console_text.SetLabel(message)

    def start_sechain(self, event):
        # import thread
        # thread.start_new_thread(MainController.initiate_node(), ("start_main_controller", 1))
        MainController.initiate_node()

    def start_trust_node(self, event):
        print "My_ip : " + Property.my_ip_address
        print "Trust_ip : " + Property.trust_node_ip
        if Property.my_ip_address == Property.trust_node_ip :
            self.write_console("start trust node")
            MainController.node_start()

        else:
            self.write_console("This IP and trust node IP is not same")

    def send_transaction(self, event):
        if (Property.node_started == True):
            trx_drg = wx.Dialog(None, title='Sending Transaction')
            trx_drg.SetSize((500, 300))
            trx_drg.SetTitle('Sending Transaction')

            pnl = wx.Panel(trx_drg)
            vbox = wx.BoxSizer(wx.VERTICAL)

            wx.StaticText(pnl, 1, 'Receiver address', (5, 5), style=wx.LEFT)
            receiver_text = wx.TextCtrl(pnl, pos = (5, 25))
            wx.StaticText(pnl, 2, 'Amount', (5, 60), style=wx.LEFT)
            amount_text = wx.TextCtrl(pnl, pos = (5, 80))
            wx.StaticText(pnl, 3, 'Message', (5, 120), style=wx.LEFT)
            message_text = wx.TextCtrl(pnl, pos = (5, 140), size = (200, 25))

            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
            okButton = wx.Button(trx_drg, wx.ID_OK)
            hbox2.Add(okButton)

            vbox.Add(pnl, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
            vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

            trx_drg.SetSizer(vbox)

            if trx_drg.ShowModal() == wx.ID_OK:
                from SeChainController import FunctionAPIs
                # need to validation check (IP format)
                FunctionAPIs.send_transaction(receiver_text.GetValue(), amount_text.GetValue(), message_text.GetValue())

            trx_drg.Destroy()
        else:
            print "Node is not started, Start node first"
            self.write_console("Node is not started, Start node first")

    def deploy_contract(self, event):
        if (Property.node_started == True):
            trx_drg = wx.Dialog(None, title='Deploying Contract')
            trx_drg.SetSize((500, 400))
            trx_drg.SetTitle('Sending Transaction')

            pnl = wx.Panel(trx_drg)
            vbox = wx.BoxSizer(wx.VERTICAL)

            wx.StaticText(pnl, 1, 'Receiver address', (5, 5), style=wx.LEFT)
            receiver_text = wx.TextCtrl(pnl, pos = (5, 25))
            wx.StaticText(pnl, 2, 'Amount', (5, 60), style=wx.LEFT)
            amount_text = wx.TextCtrl(pnl, pos = (5, 80))
            wx.StaticText(pnl, 3, 'Message', (5, 120), style=wx.LEFT)
            message_text = wx.TextCtrl(pnl, pos = (5, 140), size = (200, 25))
            wx.StaticText(pnl, 4, 'Source File (ex : Addition)', (5, 180), style=wx.LEFT)
            source_text = wx.TextCtrl(pnl, pos = (5, 200), size = (200, 25))
            wx.StaticText(pnl, 4, 'Arguments (split by ' ', ex : 1 b)', (5, 240), style=wx.LEFT)
            arg_text = wx.TextCtrl(pnl, pos=(5, 260), size=(200, 25))


            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
            okButton = wx.Button(trx_drg, wx.ID_OK)
            hbox2.Add(okButton)

            vbox.Add(pnl, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
            vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

            trx_drg.SetSizer(vbox)

            if trx_drg.ShowModal() == wx.ID_OK:
                from SeChainController import FunctionAPIs
                contract_source = {'source': source_text.GetValue(), 'args': arg_text.GetValue()}
                trx_json = FunctionAPIs.deploy_contract(Property.myNode['public_key'],
                                                                    Property.myNode['private_key'],
                                                                    'CT',
                                                                    receiver_text.GetValue(),
                                                                    amount_text.GetValue(),
                                                                    message_text.GetValue(),
                                                                    contract_source)

            trx_drg.Destroy()
        else:
            print "Node is not started, Start node first"
            self.write_console("Node is not started, Start node first")


    def run_contract(self, event):
        if (Property.node_started == True):
            trx_drg = wx.Dialog(None, title='Run Contract')
            trx_drg.SetSize((500, 450))
            trx_drg.SetTitle('Sending Transaction')

            pnl = wx.Panel(trx_drg)
            vbox = wx.BoxSizer(wx.VERTICAL)

            wx.StaticText(pnl, 1, 'Receiver IP', (5, 5), style=wx.LEFT)
            receiver_text = wx.TextCtrl(pnl, pos=(5, 25))
            wx.StaticText(pnl, 2, 'Amount', (5, 60), style=wx.LEFT)
            amount_text = wx.TextCtrl(pnl, pos=(5, 80))
            wx.StaticText(pnl, 3, 'Message', (5, 120), style=wx.LEFT)
            message_text = wx.TextCtrl(pnl, pos=(5, 140), size=(200, 25))
            wx.StaticText(pnl, 4, 'Contract Address', (5, 180), style=wx.LEFT)
            address_text = wx.TextCtrl(pnl, pos=(5, 200), size=(200, 25))
            wx.StaticText(pnl, 5, 'Function Name', (5, 240), style=wx.LEFT)
            function_text = wx.TextCtrl(pnl, pos=(5, 260), size=(200, 25))
            wx.StaticText(pnl, 6, 'Arguments (split by ' ', ex : 1 b)', (5, 300), style=wx.LEFT)
            arg_text = wx.TextCtrl(pnl, pos=(5, 320), size=(200, 25))

            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
            okButton = wx.Button(trx_drg, wx.ID_OK)
            hbox2.Add(okButton)

            vbox.Add(pnl, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
            vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

            trx_drg.SetSizer(vbox)

            if trx_drg.ShowModal() == wx.ID_OK:
                from SeChainController import FunctionAPIs
                contract_data = {'contractAddr': address_text.GetValue(),
                                 'function': function_text.GetValue(),
                                 'args': arg_text.GetValue()}
                trx_json = FunctionAPIs.run_contract(Property.myNode['public_key'],
                                                     Property.myNode['private_key'],
                                                     'RT',
                                                     receiver_text.GetValue(),
                                                     amount_text.GetValue(),
                                                     message_text.GetValue(),
                                                     contract_data)

            trx_drg.Destroy()
        else:
            print "Node is not started, Start node first"
            self.write_console("Node is not started, Start node first")