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
	def __init__(self, artist,idx):
		super(CreateListBoxRow,self).__init__()
		self.index 	= idx
		self.artist = artist
		frame = Gtk.Frame()
		hbox = Gtk.HBox()
		frame.add(hbox)

		self.Char_Label = Gtk.Label(self.artist.short_name[0].upper())
		self.Char_Label.set_size_request(50,50)
		self.Fullname_Label = Gtk.Label(self.artist.name)
		
		hbox.pack_start(self.Char_Label,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		
		self.add(frame)

	@property
	def fullname(self):
		return self.artist.name

	@fullname.setter 
	def fullname(self,name):
		if name != self.fullname:
			self.artist.name = name 
			self.Fullname_Label.set_text(name)

	@property
	def shortname(self):
		return self.artist.short_name

	@shortname.setter 
	def shortname(self,shortname):
		if shortname != self.shortname:
			self.artist.short_name = shortname
			self.Char_Label.set_text(shortname[0])
	

class ArtistEntry(Gtk.Dialog):
	def __init__(self,parent,artistlist,searchtext=""):
		super(ArtistEntry,self).__init__(self,title="Artist",parent=parent)
		self.connect("key_press_event",self.on_key_press_event)
		self.ArtistsList 	= artistlist
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/artist_panel.ui")
		self.artist_panel 	= builder.get_object("panel_entry_artist")
		box = self.get_content_area()
		box.pack_start(self.artist_panel,True,True,0)
		
		self.list_artists	 	= builder.get_object("artist_list")
		self.list_artists.connect("row-selected",self.ListBoxRowSelected)

		self.lbl_total	 	= builder.get_object("lbl_total")
		
		self.btn_new 			= builder.get_object("btn_new")
		self.btn_edit 			= builder.get_object("btn_edit")
		self.btn_save 			= builder.get_object("btn_save")
		self.btn_remove 		= builder.get_object("btn_remove")

		self.txt_search 		= builder.get_object("text_search")
		

		self.txt_uuid 			= builder.get_object("text_uuid")
		self.txt_name 			= builder.get_object("text_name")
		self.txt_short_name 	= builder.get_object("text_short_name")
		self.radio_notset		= builder.get_object("radio_notset")
		self.radio_male			= builder.get_object("radio_male")
		self.radio_female		= builder.get_object("radio_female")
		self.radio_group		= builder.get_object("radio_group")
		
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
		for row in self.list_artists.get_children():
			row.destroy()
	def _DrawListBox(self,artistslist):
		self.clear_row()
		idx = 0
		for artist in artistslist:
			if idx < 200:
				list_row 	= CreateListBoxRow(artist,idx)
				self.list_artists.add(list_row)
				self.list_artists.show_all()
			idx += 1
			self.lbl_total.set_text("Total : %i"%idx)
			yield True
		self.lbl_total.set_text("Total : %i"%self.ArtistsList.length())


	def ListBoxRowSelected(self,*arg):
		row = self.list_artists.get_selected_row()
		if row:
			self.txt_uuid.set_text(row.artist.uid)
			self.txt_name.set_editable(False)
			self.txt_name.set_text(row.artist.name)
			self.txt_short_name.set_text(row.artist.short_name)
			sex = row.artist.gender
			if sex == "M":
				self.radio_male.set_active(True)
			elif sex == "F":
				self.radio_female.set_active(True)
			elif sex == "G":
				self.radio_group.set_active(True)
			else:
				self.radio_notset.set_active(True)
			self.edit_state = False
			self.new_state 	= False
			print("Gender : ",sex)

	def search_changed(self, widget, event=None):
		tmp = widget.get_text()
		result = self.ArtistsList.SearchByName(tmp)
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
		sex = "N"
		if self.radio_male.get_active():
			sex = "M"
		elif self.radio_female.get_active():
			sex = "F"
		elif self.radio_group.get_active():
			sex = "G"
		if self.edit_state:
			artistid 		= self.txt_uuid.get_text()
			artistname 		= self.txt_name.get_text()
			shortname 		= self.txt_short_name.get_text()
			# Artist will not check exiting artist, because Artists can be same name but not same uid
			if artistname != "" and shortname != "" and artistid != "":
				row 				= self.list_artists.get_selected_row()
				row.fullname 		= artistname
				row.shortname 		= shortname
				row.artist.gender 	= sex
				self.SavetoFile()
		elif self.new_state :
			uuid 	= self.txt_uuid.get_text()
			artistname 	= self.txt_name.get_text()
			short_name 	= self.txt_short_name.get_text()
			if artistname != "" and short_name != "" and uuid != "":
				artist 				= Artist(uid=uuid,name=artistname)
				artist.short_name 	= short_name
				artist.gender 		= sex
				if not self.ArtistsList.isexists(artist):
					self.ArtistsList.Add(artist)
					self.SavetoFile()
					self.txt_search.set_text("")
					self.txt_search.grab_focus_without_selecting()


		self.edit_state = False
		self.new_state 	= False


		
	def SavetoFile(self):
		db = []
		for artist in self.ArtistsList.All():
			db.append([artist.uid,artist.name,artist.short_name,artist.gender,artist.photo])
		wfile = open(BASE_DIR+"/data/DB/DBARTIST", 'wb')
		pickle.dump(db,wfile)
		wfile.close()

	def run_generator(self,func,arg=None):
		gen = func(arg)
		GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)