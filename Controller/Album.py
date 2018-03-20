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

	@property
	def fullname(self):
		return self.album.albumname

	@fullname.setter 
	def fullname(self,name):
		if name != self.fullname:
			self.album.albumname = name 
			self.Fullname_Label.set_text(name)

	@property
	def shortname(self):
		return self.album.short_albumname

	@shortname.setter 
	def shortname(self,shortname):
		if shortname != self.shortname:
			self.album.short_albumname = shortname
			self.Char_Label.set_text(shortname[0])
	

class AlbumEntry(Gtk.Dialog):
	def __init__(self,parent,albumlist,searchtext=""):
		super(AlbumEntry,self).__init__(self,title="Album",parent=parent)
		self.connect("key_press_event",self.on_key_press_event)

		self.AlbumsList 	= albumlist
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/album_panel.ui")
		self.album_panel 	= builder.get_object("panel_entry_album")
		box = self.get_content_area()
		box.add(self.album_panel)
		
		self.list_albums	 	= builder.get_object("album_list")
		self.list_albums.connect("row-selected",self.ListBoxRowSelected)

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

	def on_key_press_event(self, widget, event):
		key = event.keyval
		if key == Gdk.KEY_F6:
			self.new()
		elif key == Gdk.KEY_F2:
			self.edit()
		elif key == Gdk.KEY_F10:
			self.save()

	def clear_row(self):
		for row in self.list_albums.get_children():
			row.destroy()
	def _DrawListBox(self,albumslist):
		self.clear_row()
		idx = 0
		for album in albumslist:
			if idx < 200:
				list_row 	= CreateListBoxRow(album,idx)
				self.list_albums.add(list_row)
				self.list_albums.show_all()
			idx += 1
			self.lbl_total.set_text("Total : %i"%idx)
			yield True
		self.lbl_total.set_text("Total : %i"%self.AlbumsList.length())

	def ListBoxRowSelected(self,*arg):
		row = self.list_albums.get_selected_row()
		if row:
			self.txt_uuid.set_text(row.album.uid)
			self.txt_name.set_editable(False)
			self.txt_name.set_text(row.album.albumname)
			self.txt_short_name.set_text(row.album.short_albumname)
			
			self.edit_state = False
			self.new_state 	= False


	def search_changed(self, widget, event=None):
		tmp = widget.get_text()
		result = self.AlbumsList.SearchByName(tmp)
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
			albumid 		= self.txt_uuid.get_text()
			albumname 		= self.txt_name.get_text()
			albumshortname 	= self.txt_short_name.get_text()
			album = Album(uid=albumid,albumname=albumname)
			album.short_albumname = albumshortname
			if not self.AlbumsList.isexists(album):
				row 				= self.list_albums.get_selected_row()
				row.fullname 		= albumname
				row.shortname 		= albumshortname
				# row.album.uid 		= albumid

				self.SavetoFile()
			else:
				print("editing is exists album")

		elif self.new_state :
			uuid 	= self.txt_uuid.get_text()
			name 	= self.txt_name.get_text()
			short_name 	= self.txt_short_name.get_text()
			if name != "" and short_name != "" and uuid != "":
				album 				= Album(uid=uuid,albumname=name)
				album.short_albumname 	= short_name

				if not self.AlbumsList.isexists(album):
					self.AlbumsList.Add(album)
					self.SavetoFile()
					self.txt_search.set_text("")
					self.txt_search.grab_focus_without_selecting()
				else:
					print("new album is existing...")

				

		self.edit_state = False
		self.new_state 	= False


		
	def SavetoFile(self):
		db = []
		for album in self.AlbumsList.All():
			db.append([album.uid,album.albumname,album.short_albumname])
		wfile = open(BASE_DIR+"/data/DB/DBALBUM", 'wb')
		pickle.dump(db,wfile)
		wfile.close()

	def run_generator(self,func,arg=None):
		gen = func(arg)
		GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)