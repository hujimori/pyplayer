# coding: utf-8
import main_frame
import wx
class Application(wx.App):
	def OnInit(self):
		frame = main_frame.MainFrame(None, -1)
		frame.Show(True)
		self.SetTopWindow(frame)
		return True 

if __name__ == "__main__":	
	app = Application()
	app.MainLoop()