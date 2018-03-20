#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GObject

from config import *
from Controller.myhelper import *
import pickle
from data.models import *

class CreateListBoxRow(Gtk.ListBoxRow):
	def __init__(self, title,idx):
		super(CreateListBoxRow,self).__init__()
		self.index 	= idx
		self.title = title
		frame = Gtk.Frame()
		hbox = Gtk.HBox()
		frame.add(hbox)

		self.Char_Label = Gtk.Label(self.title.short_name[0].upper())
		self.Char_Label.set_size_request(50,50)
		self.Fullname_Label = Gtk.Label(self.title.title)
		
		hbox.pack_start(self.Char_Label,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		
		self.add(frame)
	

	

class TitleForMain:
	def __init__(self,parent, titleslist):
		self.parent 			= parent
		self.current_mediafile 	= None
		self.TitlesList 	= titleslist
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/main_title.ui")
		self.title_panel 	= builder.get_object("frame1")
		self.parent.pack_start(self.title_panel, True, True,0)
		
		self.up_list_titles	 	= builder.get_object("up_title_list")
		self.up_list_titles.connect("row-selected",self.UpListBoxRowSelected)

		self.down_list_titles	 	= builder.get_object("down_title_list")
		self.down_list_titles.connect("row-selected",self.DownListBoxRowSelected)

		
		self.btn_up 			= builder.get_object("btn_up")
		self.btn_down			= builder.get_object("btn_down")
		self.btn_add 			= builder.get_object("btn_add")


		self.txt_search 		= builder.get_object("text_search")

				
		
		
		self.txt_search.connect("changed", self.search_changed)


		self.DrawListBox(self.up_list_titles, self.TitlesList.All())

		
	


	def clear_row(self,listbox):
		for row in listbox.get_children():
			row.destroy()
	def DrawListBox(self,listbox, titleslist):
		self.clear_row(listbox)
		idx = 0
		for title in titleslist:
			list_row 	= CreateListBoxRow(title,idx)
			listbox.add(list_row)
			idx += 1
		listbox.show_all()

	def UpListBoxRowSelected(self,*arg):
		row = self.up_list_titles.get_selected_row()
		if row:
			pass
			

	def DownListBoxRowSelected(self,*arg):
		row = self.down_list_titles.get_selected_row()
		if row:
			pass
	def search_changed(self, widget, event=None):
		tmp = widget.get_text()
		result = self.TitlesList.SearchByName(tmp)
		self.DrawListBox(self.up_list_titles, result)

	