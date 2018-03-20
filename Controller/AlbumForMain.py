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
	def __init__(self, album,idx):
		super(CreateListBoxRow,self).__init__()
		self.index 	= idx
		self.album = album
		frame = Gtk.Frame()
		hbox = Gtk.HBox()
		frame.add(hbox)

		self.Char_Label = Gtk.Label(self.album.short_albumname[0].upper())
		self.Char_Label.set_size_request(50,50)
		self.Fullname_Label = Gtk.Label(self.album.albumname)
		
		hbox.pack_start(self.Char_Label,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		
		self.add(frame)
	

	

class AlbumForMain:
	def __init__(self,parent, albumslist):
		self.parent 			= parent
		self.current_mediafile 	= None
		self.AlbumsList 	= albumslist
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/main_album.ui")
		self.album_panel 	= builder.get_object("frame1")
		self.parent.pack_start(self.album_panel, True, True,0)
		
		self.up_list_albums	 	= builder.get_object("up_album_list")
		self.up_list_albums.connect("row-selected",self.UpListBoxRowSelected)

		self.down_list_albums	 	= builder.get_object("down_album_list")
		self.down_list_albums.connect("row-selected",self.DownListBoxRowSelected)

		
		self.btn_up 			= builder.get_object("btn_up")
		self.btn_down			= builder.get_object("btn_down")
		self.btn_add			= builder.get_object("btn_add")


		self.txt_search 		= builder.get_object("text_search")

				
		
		
		self.txt_search.connect("changed", self.search_changed)


		self.DrawListBox(self.up_list_albums, self.AlbumsList.All())

		
	


	def clear_row(self,listbox):
		for row in listbox.get_children():
			row.destroy()
	def DrawListBox(self,listbox, albumslist):
		self.clear_row(listbox)
		idx = 0
		for album in albumslist:
			list_row 	= CreateListBoxRow(album,idx)
			listbox.add(list_row)
			idx += 1
		listbox.show_all()

	def UpListBoxRowSelected(self,*arg):
		row = self.up_list_albums.get_selected_row()
		if row:
			pass
			

	def DownListBoxRowSelected(self,*arg):
		row = self.down_list_albums.get_selected_row()
		if row:
			pass
	def search_changed(self, widget, event=None):
		tmp = widget.get_text()
		result = self.AlbumsList.SearchByName(tmp)
		self.DrawListBox(self.up_list_albums, result)

	