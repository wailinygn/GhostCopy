#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gdk,GObject,GLib

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

	@property
	def fullname(self):
		return self.title.title

	@fullname.setter 
	def fullname(self,name):
		if name != self.fullname:
			self.title.title = name 
			self.Fullname_Label.set_text(name)

	@property
	def shortname(self):
		return self.title.short_name

	@shortname.setter 
	def shortname(self,shortname):
		if shortname != self.shortname:
			self.title.short_name = shortname
			self.Char_Label.set_text(shortname[0])
	

class TitleEntry(Gtk.Dialog):
	def __init__(self,parent,titlelist,searchtext=""):
		super(TitleEntry,self).__init__(self,title="Title",parent=parent)
		self.connect("key_press_event",self.on_key_press_event)

		self.TitlesList 	= titlelist
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/title_panel.ui")
		self.title_panel 	= builder.get_object("panel_entry_title")
		box = self.get_content_area()
		box.pack_start(self.title_panel,True,True,0)
		
		self.list_titles	 	= builder.get_object("title_list")
		self.list_titles.connect("row-selected",self.ListBoxRowSelected)

		self.lbl_total	 	= builder.get_object("lbl_total")
		
		self.btn_new 			= builder.get_object("btn_new")
		self.btn_edit 			= builder.get_object("btn_edit")
		self.btn_save 			= builder.get_object("btn_save")
		self.btn_remove 		= builder.get_object("btn_remove")

		self.txt_search 		= builder.get_object("text_search")
		

		self.txt_uuid 			= builder.get_object("text_uuid")
		self.txt_name 			= builder.get_object("text_name")
		self.txt_short_name 	= builder.get_object("text_short_name")

		
		self.btn_new.connect("clicked",self.new)
		self.btn_edit.connect("clicked",self.edit)
		self.btn_save.connect("clicked",self.save)

		self.txt_search.connect("changed", self.search_changed)
		self.txt_name.connect("changed", self.name_changed)

		self.edit_state 	= False
		self.new_state 		= False

		if len(searchtext)>0:
			self.txt_search.set_text(searchtext)
		self.search_changed(self.txt_search)

		# self.run_generator(self._DrawListBox,self.TitlesList.All())

	def on_key_press_event(self, widget, event):
		key = event.keyval
		if key == Gdk.KEY_F6:
			self.new()
		elif key == Gdk.KEY_F2:
			self.edit()
		elif key == Gdk.KEY_F10:
			self.save()

	def clear_row(self):
		for row in self.list_titles.get_children():
			row.destroy()
	def _DrawListBox(self,titleslist):
		self.clear_row()
		idx = 0
		for title in titleslist:
			if idx <200:
				list_row 	= CreateListBoxRow(title,idx)
				self.list_titles.add(list_row)
				self.list_titles.show_all()
			idx += 1
			self.lbl_total.set_text("Total : %i"%idx)
			yield True
		self.lbl_total.set_text("Total : %i"%self.TitlesList.length())

	def ListBoxRowSelected(self,*arg):
		row = self.list_titles.get_selected_row()
		if row:
			self.txt_uuid.set_text(row.title.uid)
			self.txt_name.set_editable(False)
			self.txt_name.set_text(row.title.title)
			self.txt_short_name.set_text(row.title.short_name)
			
			self.edit_state = False
			self.new_state 	= False


	def search_changed(self, widget, event=None):
		tmp = widget.get_text()
		result = self.TitlesList.SearchByName(tmp)
		self.run_generator(self._DrawListBox,result)

	def name_changed(self,widget,event=None):
		tmp= widget.get_text()

		# tmp = tmp.decode('UTF-8')
		# print(tmp,len(tmp))
		if len(tmp)>0:
			short_txt = SplitConsonant(tmp)
			self.txt_short_name.set_text(short_txt)
		else:
			self.txt_short_name.set_text("")

	def new(self,*arg):
		txt = self.txt_search.get_text()
		if len(txt) >0:
			self.txt_name.set_text(txt)
			short_txt = SplitConsonant(txt)
			self.txt_short_name.set_text(short_txt)
		else:
			self.txt_name.set_text("")
			self.txt_short_name.set_text("")
		self.txt_name.set_editable(True)
		self.txt_name.set_visibility(True)

		self.txt_name.set_can_focus(True)
		self.txt_uuid.set_text(newid())
		self.new_state 		= True
		self.edit_state  	= False
		

	def edit(self,*arg):
		self.edit_state = True
		self.new_state 		= False
		self.txt_name.set_editable(True)
		self.txt_name.set_visibility(True)

	def save(self, *arg):
		if self.edit_state:
			titleid 		= self.txt_uuid.get_text()
			titlename 		= self.txt_name.get_text()
			titleshortname 	= self.txt_short_name.get_text()
			title = Title(uid=titleid,title=titlename,short_name=titleshortname)
			if not self.TitlesList.isexists(title):
				row 				= self.list_titles.get_selected_row()
				row.fullname 		= titlename
				row.shortname 		= titleshortname
				# row.title.uid 		= titleid

				self.SavetoFile()
			else:
				print("editing is exists title")

		elif self.new_state :
			uuid 	= self.txt_uuid.get_text()
			name 	= self.txt_name.get_text()
			short_name 	= self.txt_short_name.get_text()
			if name != "" and short_name != "" and uuid != "":
				title 				= Title(uid=uuid,title=name)
				title.short_name 	= short_name

				if not self.TitlesList.isexists(title):
					self.TitlesList.Add(title)
					self.SavetoFile()
					self.txt_search.set_text("")
					self.txt_search.grab_focus_without_selecting()
				else:
					print("new title is existing...")

				

		self.edit_state = False
		self.new_state 	= False


		
	def SavetoFile(self):
		db = []
		for title in self.TitlesList.All():
			db.append([title.uid,title.title,title.short_name])
		wfile = open(BASE_DIR+"/data/DB/DBTITLE", 'wb')
		pickle.dump(db,wfile)
		wfile.close()

	def run_generator(self,func,arg=None):
		gen = func(arg)
		GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)