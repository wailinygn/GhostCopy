#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GLib
from config import *


from shutil import copyfile

class RenameWindow:
	def __init__(self,mydb):
		self.mydb = mydb
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/rename_window.ui")
		self.window = builder.get_object("renamewindow")

		self.radio_frame		= builder.get_object("radio_frame")

		self.radio_uuid			= builder.get_object("radio_uuid")
		self.radio_no			= builder.get_object("radio_no")
		self.radio_serial		= builder.get_object("radio_serial")
		self.radio_title		= builder.get_object("radio_title")
		self.radio_title_artist	= builder.get_object("radio_title_artist")
		self.radio_title_album	= builder.get_object("radio_title_album")
		self.radio_artist		= builder.get_object("radio_artist")
		self.radio_artist_title	= builder.get_object("radio_artist_title")
		

		self.lbl_status			= builder.get_object("lbl_status")
		self.statusbar			= builder.get_object("statusbar")

		self.btn_cancel			= builder.get_object("btn_cancel")
		self.btn_rename			= builder.get_object("btn_rename")

		self.btn_cancel.connect("clicked", self.btn_cancel_press)
		self.btn_rename.connect("clicked", self.btn_rename_press)

		self.Cancel_State = False

		
	def load(self,mediafiles):
		self.btn_cancel.set_label("Cancel")
		self.btn_rename.set_sensitive(True)
		self.radio_frame.set_visible(True)
		self.statusbar.set_value(0)
		self.statusbar.set_max_value(mediafiles.length())
		self.window.show_all()
		self.mediafiles =mediafiles

	def run_generator(self, func):
		gen = func()
		GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)


	def btn_cancel_press(self,*arg):
		self.Cancel_State = True
		self.window.hide()


	def btn_rename_press(self, *arg):
		self.Cancel_State = False
		self.btn_rename.set_sensitive(False)
		self.radio_frame.set_visible(False)
		

		if self.radio_uuid.get_active():
			self.run_generator(self.rename_uuid)

		elif self.radio_no.get_active():
			self.run_generator(self.rename_no)

		elif self.radio_serial.get_active():
			self.run_generator(self.rename_serial)

		elif self.radio_title.get_active():
			self.run_generator(self.rename_title)

		elif self.radio_title_artist.get_active():
			self.run_generator(self.rename_title_artist)

		elif self.radio_title_album.get_active():
			self.run_generator(self.rename_title_album)

		elif self.radio_artist.get_active():
			self.run_generator(self.rename_artist)

		elif self.radio_artist_title.get_active():
			self.run_generator(self.rename_artist_title)
		

	def rename_uuid(self):
		count = 1
		for moviefile in self.mediafiles.All():
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					newuuid = self.mediafiles.Newuid()
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")


	def rename_no(self):
		idx = 0
		count = 1
		for moviefile in self.mediafiles.All():
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					idx += 1
					newuuid = str(idx)
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")


	def rename_serial(self):
		idx = 0
		count = 1
		for moviefile in self.mediafiles.All():
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					idx += 1
					newuuid = "%09i"%idx
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")


	def rename_title(self):
		count = 1
		for moviefile in self.mediafiles.All():
			idx = 0
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					idx += 1
					newuuid = moviefile.Title.title + "_%i"%idx
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")


	def rename_title_artist(self):
		count = 1
		for moviefile in self.mediafiles.All():
			idx = 0
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					all_artists_string = "+".join(artist.name for artist in moviefile.Artists.All())
					idx += 1
					newuuid = "%s_%s_%i"%(moviefile.Title.title,all_artists_string,idx)
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")


	def rename_title_album(self):
		count = 1
		for moviefile in self.mediafiles.All():
			idx = 0
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					idx += 1
					newuuid = "%s__%s_%i"%(moviefile.Title.title,moviefile.Album.albumname,idx)
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")


	def rename_artist(self):
		count = 1
		for moviefile in self.mediafiles.All():
			idx = 0
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					all_artists_string = "+".join(artist.name for artist in moviefile.Artists.All())
					idx += 1
					newuuid = "%s__%i"%(all_artists_string,idx)
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")
		

	def rename_artist_title(self):
		count = 1
		for moviefile in self.mediafiles.All():
			idx = 0
			if self.Cancel_State:
				break
			else:
				fileexists = True
				while fileexists:
					all_artists_string = "+".join(artist.name for artist in moviefile.Artists.All())
					idx += 1
					newuuid = "%s_%s__%i"%(all_artists_string,moviefile.Title.title,idx)
					newfilename = os.path.dirname(moviefile.filepath)+"/"+newuuid+moviefile.filetype
					if not os.path.exists(newfilename):
						os.rename(moviefile.filepath,newfilename)
						moviefile.filename = newuuid+moviefile.filetype
						moviefile.filepath = newfilename
						self.mydb.DB_Save(self.mediafiles)
						break
				self.lbl_status.set_text(moviefile.filename)
				self.statusbar.set_value(count)
				count += 1
				yield True
		self.lbl_status.set_text("done!")
		self.btn_cancel.set_label("Close")
		
	