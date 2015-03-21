# -*- coding: utf-8 -*-
import wx
import wx.grid

from gdata import *
import gdata.youtube
import gdata.youtube.service

class MainFrame(wx.Frame):
	def __init__(self, id, title):
		wx.Frame.__init__(self, id, title = "Youtube Player", size = wx.Size(1000, 400))
		pan = wx.Panel(self, -1)
		
		# 検索結果を表示するテーブル
		self.table = DataTable(pan)

		# 検索ワードを入力するボックス
		self.text = wx.TextCtrl(pan, wx.ID_ANY, size = (200, 20))
		self.btn = wx.Button(pan, -1, "この名前で検索する")
		self.btn2 = wx.Button(pan, -1, "番目の動画を再生する")
		self.st_txt = wx.StaticText(pan, -1, "上のテーブルで")
		self.spn = wx.SpinCtrl(pan, -1, "1", min = 1, max = 25)

		vsizer = wx.BoxSizer(wx.VERTICAL)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		vsizer.Add(self.text, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer.Add(self.btn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer.Add(self.table, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		hsizer.Add(self.st_txt, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		hsizer.Add(self.spn, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		hsizer.Add(self.btn2, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		vsizer.Add(hsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		pan.SetSizer(vsizer)
		vsizer.Fit(pan)

		self.btn.Bind(wx.EVT_BUTTON, self.search_youtube)


	# youtubeの動画を検索 
	def search_youtube(self, event):	
		self.search_word = self.text.GetValue()
		self.client = gdata.youtube.service.YouTubeService()


		self.query = gdata.youtube.service.YouTubeVideoQuery()
		# 検索ワード
		self.query.vq = "冴えない彼女の育て方"
		# 何番目の動画から取得するか
		self.query.start_index = 1
		# 検索件数
		self.query.max_results = 10
		# 最後の動画を含めるかどうか
		self.query.racy = "exclude"
		# 検索結果の順番
		self.query.orderby = "relevance"

		feed = self.client.YouTubeQuery(self.query)
		self.feed_list = []
		self.table.number = 0
		for entry in feed.entry:
			self.table.number += 1
			feed_dict = {} 
			feed_dict["title"] = entry.media.title.text
			feed_dict["page"] = entry.GetSwfUrl()
			feed_dict["time"] = entry.media.duration.seconds
			self.feed_list.append(feed_dict)

		self.table.update_table(self.feed_list)
		


# 検索結果の一覧を表示するテーブル
class DataTable(wx.grid.Grid):
	def __init__(self, parent):
		wx.grid.Grid.__init__(self, parent, -1)

		self.InitRow= 10
		self.CreateGrid(self.InitRow, 2)
		self.SetColLabelValue(0, "動画のタイトル")		
		self.SetColLabelValue(1, "再生時間[秒]")
		self.SetColSize(0, 800)
		self.SetColSize(1, 100)
	

	def update_table(self, list):
		# 検索結果をリストに表示
		row_num = len(list)
		if row_num > self.InitRow:
			self.AppendRows(row_num-self.InitRow)
			self.InitRow = row_num 

		for i, result in enumerate(list):
			if "title" in result:
				self.SetCellValue(i, 0, result["title"])
				self.SetCellValue(i, 1, result["time"])


def main():
	ex = wx.App()
	MainFrame(None, -1)
	ex.MainLoop()

if __name__ == '__main__':
	main()