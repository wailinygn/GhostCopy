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
	def __init__(self, category,idx):
		super(CreateListBoxRow,self).__init__()
		self.index 	= idx
		self.category = category
		frame = Gtk.Frame()
		hbox = Gtk.HBox()
		frame.add(hbox)

		self.Char_Label = Gtk.Label(self.category.short_categoryname[0].upper())
		self.Char_Label.set_size_request(50,50)
		self.Fullname_Label = Gtk.Label(self.category.categoryname)
		
		hbox.pack_start(self.Char_Label,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		
		self.add(frame)
	

	

class CategoryForMain:
	def __init__(self,parent, categorieslist):
		self.parent 			= parent
		self.current_mediafile 	= None
		self.CategoriesList 	= categorieslist
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/main_category.ui")
		self.category_panel 	= builder.get_object("frame1")
		self.parent.pack_start(self.category_panel, True, True,0)
		
		self.up_list_categories	 	= builder.get_object("up_category_list")
		self.up_list_categories.connect("row-selected",self.UpListBoxRowSelected)

		self.down_list_categories	 	= builder.get_object("down_category_list")
		self.down_list_categories.connect("row-selected",self.DownListBoxRowSelected)

		
		self.btn_up 			= builder.get_object("btn_up")
		self.btn_down			= builder.get_object("btn_down")
		self.btn_add 			= builder.get_object("btn_add")


		self.txt_search 		= builder.get_object("text_search")

				
		
		
		self.txt_search.connect("changed", self.search_changed)


		self.DrawListBox(self.up_list_categories, self.CategoriesList.All())

		
	


	def clear_row(self,listbox):
		for row in listbox.get_children():
			row.destroy()
	def DrawListBox(self,listbox, categorieslist):
		self.clear_row(listbox)
		idx = 0
		for category in categorieslist:
			list_row 	= CreateListBoxRow(category,idx)
			listbox.add(list_row)
			idx += 1
		listbox.show_all()

	def UpListBoxRowSelected(self,*arg):
		row = self.up_list_categories.get_selected_row()
		if row:
			pass
			

	def DownListBoxRowSelected(self,*arg):
		row = self.down_list_categories.get_selected_row()
		if row:
			pass
	def search_changed(self, widget, event=None):
		tmp = widget.get_text()
		result = self.CategoriesList.SearchByName(tmp)
		self.DrawListBox(self.up_list_categories, result)

	