import wx
import threading
from SeChainUI.MainUI import MainApp

app = MainApp(0)
t = threading.Thread(target=app.MainLoop())
t.setDaemon(1)
t.start()
# app.MainLoop()