#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, Gdk,GObject

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11


import subprocess as sp

from Controller.db import DB
from config import *
from player import *

from Controller.SaveDialog import ExportDialog as SD
from Controller.RenameWindow import RenameWindow as rnwindow

from Controller.Artist import ArtistEntry
from Controller.Title import TitleEntry
from Controller.Album import AlbumEntry
from Controller.Category import CategoryEntry

from Controller.TitleForMain import TitleForMain 
from Controller.ArtistForMain import ArtistForMain 
from Controller.AlbumForMain import AlbumForMain 
from Controller.CategoryForMain import CategoryForMain 

from datetime import datetime

class CreateListBoxRow(Gtk.ListBoxRow):
	def __init__(self, moviefile,idx):
		super(CreateListBoxRow,self).__init__()
		self.set_margin_top(4)
		self.set_margin_right(8)
		self.set_margin_bottom(4)
		self.set_margin_left(8)
		self.index 	= idx
		self.moviefile = moviefile

		
		hbox = Gtk.HBox()
		

		img 		= Gtk.Image.new_from_file(BASE_DIR+"/UI/images/movie.png")
		img.set_tooltip_markup(self.moviefile.filename)
		img.set_size_request(100,100)	
		hbox.pack_start(img,False,False,0)

		vbox 		= Gtk.VBox()
		hbox.pack_start(vbox,True,True,10)
		row0 		= Gtk.HBox()
		row1 		= Gtk.HBox() 		
		row2 		= Gtk.HBox() 		
		row3 		= Gtk.HBox()

		
		titleimg 		= Gtk.Image.new_from_file(BASE_DIR+"/UI/images/title.png")
		self.lbl_title 		= Gtk.Label("",xalign=0)

		artistimg 		= Gtk.Image.new_from_file(BASE_DIR+"/UI/images/artist.png")
		self.lbl_artist 	= Gtk.Label("",xalign=0)

		albumimg 		= Gtk.Image.new_from_file(BASE_DIR+"/UI/images/album.png")
		self.lbl_album 		= Gtk.Label("",xalign=0)

		categoryimg 		= Gtk.Image.new_from_file(BASE_DIR+"/UI/images/category.png")
		self.lbl_category 	= Gtk.Label("",xalign=0)


		lbl_filename 		= Gtk.Label(moviefile.filename,xalign=0)
		
		row0.pack_start(titleimg,False,False,2)
		row0.pack_start(self.lbl_title,False,False,2)

		row1.pack_start(artistimg,False,False,2)
		row1.pack_start(self.lbl_artist,False,False,2)
		
		row2.pack_start(albumimg,False,False,2)
		row2.pack_start(self.lbl_album,False,False,2)

		row3.pack_start(categoryimg,False,False,2)
		row3.pack_start(self.lbl_category,False,False,2)

		
		# vbox.add(lbl_filename)
		vbox.add(row0)
		vbox.add(row1)
		vbox.add(row2)
		vbox.add(row3)
		# vbox.pack_end(self.toggle_more,False,False,2)
		
		self.add(hbox)
		self.update_label()

	def update_label(self):
		if self.moviefile.Title.title == 'unknown':
			self.lbl_title.set_text(self.moviefile.relName)
		else:
			self.lbl_title.set_text(self.moviefile.Title.title)
		self.lbl_artist.set_text(self.moviefile.Artists.get_all_artists_string())
		self.lbl_album.set_text(self.moviefile.Album.albumname)
		self.lbl_category.set_text(self.moviefile.Categories.get_all_categories_string())

	


class myWindow(Player):
	def __init__(self):
		super(myWindow,self).__init__()
		self.current_mediafile = None
		self.mydb 	 	= DB()
		builder = Gtk.Builder()
		builder.add_from_file(BASE_DIR+ "/UI/main.ui")
		
		self.window 	= builder.get_object("mainwindow")
		self.window.show_all()
		self.window.maximize()

		self.window.connect("delete-event", self.quit)
		self.window.connect("key_press_event",self.on_key_press_event)

		

		# Menu Session
		self.fileopen 	= builder.get_object("FileOpen")
		self.fileopen.connect("activate", self.openlocation)

		self.filesave 	= builder.get_object("FileSave")
		self.filesave.connect("activate", self.save)

		self.fileexit 	= builder.get_object("FileExit")
		self.fileexit.connect("activate", self.quit)

		self.helpabout 	= builder.get_object("HelpAbout")
		self.helpabout.connect("activate", self.about_dlg)

		self.leftpanel 		= builder.get_object("left_panel")
		self.filterpanel 		= builder.get_object("filter_panel")
		self.exportpanel 		= builder.get_object("export_panel")

		self.filterpanel.set_position(0)
		

		self.showleftpanel 	= builder.get_object("ViewShowLeftPanel")
		self.showleftpanel.connect("toggled", self.toggled_for_leftpanel)

		self.showfilterpanel 	= builder.get_object("ViewShowFilterPanel")
		self.showfilterpanel.connect("toggled", self.toggled_for_filterpanel)

		self.showexportpanel 	= builder.get_object("ViewShowExportPanel")
		self.showexportpanel.connect("toggled", self.toggled_for_exportpanel)


		
		


		self.btn_open 			= builder.get_object("btn_location")
		self.btn_open.connect("clicked", self.openlocation)
		self.btn_reload 		= builder.get_object("btn_reload")
		self.btn_reload.connect("clicked", self.reloadlocation)
		self.txt_location 		= builder.get_object("text_location")
		self.text_main_search 	= builder.get_object("text_main_search")
		self.text_main_search.connect("changed", self.main_search)

		# Delete file and remove from library
		self.btn_delete 			= builder.get_object("btn_delete")
		self.btn_delete.connect("clicked", self.delete_file)

		# Save Database file
		self.btn_save 			= builder.get_object("btn_save")
		self.btn_save.connect("clicked", self.save)

		# Save Database file
		self.btn_export = builder.get_object("btn_export")
		self.btn_export.connect("clicked", self.exportfor_myplayer)

		# Rename file
		self.btn_rename 		= builder.get_object("btn_rename")
		self.btn_rename.connect("clicked", self.renamefile)
		self.renamewindow 		= rnwindow(self.mydb)
				

		self.exportbtn_open 			= builder.get_object("exportbtn_location")
		self.exportbtn_open.connect("clicked", self.ExportLocation)
		self.exporttext_location 	= builder.get_object("exporttext_location")
		self.btn_sendtoexport	= builder.get_object("btn_sendtoexport")
		self.btn_sendtoexport.connect("clicked", self.SendToExport)
		self.exportbtn_remove	= builder.get_object("exportbtn_remove")
		self.exportbtn_remove.connect("clicked", self.RemoveFromExport)
		self.exportbtn_save	= builder.get_object("exportbtn_save")
		self.exportbtn_save.connect("clicked", self.SaveExportList)
		self.export_list 	= builder.get_object("to_export_list")
		self.export_list.connect("button_press_event",self.exportlistbox_key_press_event)
		self.exportlbl_total_media 	= builder.get_object("exportlbl_total_media")
		self.exportlbl_total_size 	= builder.get_object("exportlbl_total_size")
		self.space_level 	= builder.get_object("space_level")
		self.exportlbl_usage 	= builder.get_object("exportlbl_usage")
		self.exporttext_main_search 	= builder.get_object("exporttext_main_search")
		self.exporttext_main_search.connect("changed", self.Exportmain_search)
		



		self.library_list 	= builder.get_object("library_list")
		self.library_list.connect("selected-rows-changed",self.MainListBoxRowSelected)
		self.library_list.connect("button_press_event",self.librarylistbox_key_press_event)

		self.founded_notebook 		= builder.get_object("founded_notebook")
		self.founded_notebook.connect("switch-page", self.founded_notebook_changepaged)


		self.founded_title_list 	= builder.get_object("founded_titles_list")
		self.founded_artist_list 	= builder.get_object("founded_artists_list")
		self.founded_album_list 	= builder.get_object("founded_album_list")
		self.founded_category_list 	= builder.get_object("founded_category_list")

		self.lbl_total_media 	= builder.get_object("lbl_total_media")
		self.lbl_total_size 	= builder.get_object("lbl_total_size")
		self.lbl_selected_size 	= builder.get_object("lbl_selected_size")
		self.lbl_save			= builder.get_object("lbl_save")


		
		
		# There must be called after self.mydb are called
		self.Do_For_Title(builder)
		self.Do_For_Artsit(builder)
		self.Do_For_Album(builder)
		self.Do_For_Category(builder)

		self.Do_For_Preview(builder)

		self.exportsize = 0
		self.founded_notebook_index = 0
		self.library 		= None
		self.SAVE_STATE 	= False
		
		self.FoundedTitleEdited 	= True
		self.FoundedArtistEdited 	= False
		self.FoundedAlbumEdited 	= False
		self.FoundedCategoryEdited 	= False



	def Do_For_Title(self,builder):
		titlebox 	= builder.get_object("titlebox")
		self.main_title 	= TitleForMain(titlebox,self.mydb.TITLES_LIST)
		self.main_title.btn_up.connect("clicked",self.title_btn_up_press)
		self.main_title.btn_down.connect("clicked",self.title_btn_down_press)
		self.main_title.btn_add.connect("clicked",self.title_btn_add_press)
		self.main_title.up_list_titles.connect("button_press_event",self.on_mouse_press_event_Title)

	def Do_For_Artsit(self,builder):
		artistbox 	= builder.get_object("artistbox")
		self.main_artist 	= ArtistForMain(artistbox,self.mydb.ARTISTS_LIST)
		self.main_artist.btn_up.connect("clicked",self.artist_btn_up_press)
		self.main_artist.btn_down.connect("clicked",self.artist_btn_down_press)
		self.main_artist.btn_add.connect("clicked",self.artist_btn_add_press)
		self.main_artist.up_list_artists.connect("button_press_event",self.on_mouse_press_event_Artist)

	def Do_For_Album(self,builder):
		albumbox 	= builder.get_object("albumbox")
		self.main_album 	= AlbumForMain(albumbox,self.mydb.ALBUMS_LIST)
		self.main_album.btn_up.connect("clicked",self.album_btn_up_press)
		self.main_album.btn_down.connect("clicked",self.album_btn_down_press)
		self.main_album.btn_add.connect("clicked",self.album_btn_add_press)
		self.main_album.up_list_albums.connect("button_press_event",self.on_mouse_press_event_Album)

	def Do_For_Category(self,builder):
		categorybox 	= builder.get_object("categorybox")
		self.main_category 	= CategoryForMain(categorybox,self.mydb.CATEGORIES_LIST)
		self.main_category.btn_up.connect("clicked",self.category_btn_up_press)
		self.main_category.btn_down.connect("clicked",self.category_btn_down_press)
		self.main_category.btn_add.connect("clicked",self.category_btn_add_press)
		self.main_category.up_list_categories.connect("button_press_event",self.on_mouse_press_event_Category)

	def Do_For_Preview(self,builder):
		display 		= builder.get_object("moviedisplay")
		self.scalebar 		= builder.get_object("scalebar")
		self.lbl_time 		= builder.get_object("lbl_time")

		self.btn_play 	= builder.get_object("btn_play")
		self.btn_pause 	= builder.get_object("btn_pause")
		self.btn_stop	= builder.get_object("btn_stop")

		self.btn_play.connect("clicked", self.play)
		self.btn_pause.connect("clicked", self.pause)
		self.btn_stop.connect("clicked", self.stop)

		self.xid = display.get_property('window').get_xid()
		# self 	= Player(xid)
		self.scalebar.connect("button-press-event",self.do_scale_press)
		self.scalebar.connect("button-release-event",self.do_scale_release)
		self.scalebar.connect("value-changed",self.do_change_seek)
		self.adjustment = self.scalebar.get_adjustment()

		
	# Menu Session
	def toggled_for_leftpanel(self,*arg):
		menuitem = arg[0]
		if menuitem.get_active():
			self.leftpanel.set_position(300)
		else:
			self.leftpanel.set_position(0)

	def toggled_for_filterpanel(self,*arg):
		menuitem = arg[0]
		if menuitem.get_active():
			self.filterpanel.set_position(400)
		else:
			self.filterpanel.set_position(0)

	def toggled_for_exportpanel(self,*arg):
		menuitem = arg[0]
		if menuitem.get_active():
			self.exportpanel.set_position(400)
		else:
			self.exportpanel.set_position(0)

	def about_dlg(self,*arg):
		dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK, "About")
		dialog.format_secondary_text(
		"Name:\nn o t s e t\nVersion:\ntrial version 1.0\nRelease Date:\nnot set\n\nLicense:\nNot Set\n\nDeveloped by:\nWai Lin\nwailinygn@gmail.com\nhttp://www.n o t s e t.com")
		dialog.run()
		dialog.destroy()


	def quit(self,*arg):
		if self.SAVE_STATE:
			dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
					Gtk.ButtonsType.OK_CANCEL, "You need to save!")
			dialog.format_secondary_text(
			"Database are edited. If you press OK, Database will not be saved.")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				self.stop()
				Gtk.main_quit()
			dialog.destroy()

		else:
			self.stop()
			Gtk.main_quit()



	def UpdateUI(self):

		if self.SAVE_STATE:
			self.lbl_save.set_text("Save: [Ctrl+S/F10]")
			self.btn_save.set_visible(True)
		else:
			self.lbl_save.set_text("")
			self.btn_save.set_visible(False)

		if self.library != None:
			self.btn_rename.set_visible(True)
			self.btn_delete.set_visible(True)
		else:
			self.btn_rename.set_visible(False)
			self.btn_delete.set_visible(False)





	def on_key_press_event(self, widget, event):
		# Control Key + key, eg. ctrl + a
		key = event.keyval
		if event.state == Gdk.ModifierType.CONTROL_MASK:
			if key == Gdk.KEY_s:
				self.save()
			elif key == Gdk.KEY_Delete:
				self.delete_file()
					
		elif key == Gdk.KEY_F10:
			self.save()
		

	def librarylistbox_key_press_event(self, widget, event):
		# Mouse Double Click
		if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
			row = widget.get_selected_row()
			if row:
				if self.current_mediafile != row.moviefile:
					self.stop()
					self.current_mediafile = row.moviefile
					self.play()

	# Mouse Press Event
	def on_mouse_press_event_Title(self, widget=None, event=None):
		# Mouse Double Click
		if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
			self.title_btn_down_press()

	def on_mouse_press_event_Artist(self, widget=None, event=None):
		# Mouse Double Click
		if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
			self.artist_btn_down_press()

	def on_mouse_press_event_Album(self, widget=None, event=None):
		# Mouse Double Click
		if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
			self.album_btn_down_press()

	def on_mouse_press_event_Category(self, widget=None, event=None):
		# Mouse Double Click
		if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
			self.category_btn_down_press()


	def delete_file(self, *arg):
		rows = self.library_list.get_selected_rows()
		if rows:
			dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
					Gtk.ButtonsType.OK_CANCEL, "!!!WARNING!!!")
			dialog.format_secondary_text(
			"Original soruce file(s) will be deleted.\nAre you sure?")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				self.stop()
				self.current_mediafile = None
				for row in rows:
					filepath = row.moviefile.filepath
					os.remove(filepath)
					if not os.path.exists(filepath):
						self.library.delete_by_uid(row.moviefile.uid)
				run_generator(self.DrawListBox)

				
				self.SAVE_STATE = True
				self.FoundedTitleEdited 	= True
				self.FoundedArtistEdited	= True
				self.FoundedAlbumEdited 	= True 
				self.FoundedCategoryEdited 	= True
				idx = self.founded_notebook.get_current_page()
				self.founded_notebook_changepaged(None,None,idx)
				self.UpdateUI()

			dialog.destroy()

	def founded_notebook_changepaged(self, notebookwidget, scrollwidget, page_idx):
		self.founded_notebook_index = page_idx
		# For Founded Notebook list update
		if self.founded_notebook_index == 0 and self.FoundedTitleEdited:
			self.TitleUPDATE_UI()
		elif self.founded_notebook_index == 1 and self.FoundedArtistEdited:
			self.ArtistUPDATE_UI()
		elif self.founded_notebook_index == 2 and self.FoundedAlbumEdited:
			self.AlbumUPDATE_UI()
		elif self.founded_notebook_index == 3 and self.FoundedCategoryEdited:
			self.CategoryUPDATE_UI()
	
	def save(self, *arg):
		location = self.txt_location.get_text()
		if location != "":
			result = self.mydb.DB_Save(self.library)
			if result:
				self.SAVE_STATE 	= False
				dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK, "DB Save")
				dialog.format_secondary_text(
				"Success!")
				dialog.run()
				dialog.destroy()
				self.UpdateUI()

	def exportfor_myplayer(self, *arg):
		location = self.txt_location.get_text()
		if location != "":
			result = self.mydb.exportDBtomyplayer(self.library)
			if result:
				self.SAVE_STATE 	= False
				dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
						Gtk.ButtonsType.OK, "DB export")
				dialog.format_secondary_text(
				"Success!")
				dialog.run()
				dialog.destroy()
				self.UpdateUI()

	def renamefile(self, *arg):
		location = self.txt_location.get_text()
		if location != "":
			self.stop()
			self.renamewindow.load(self.library)


	def reloadlocation(self, *arg):
		if self.SAVE_STATE:
			dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
					Gtk.ButtonsType.OK_CANCEL, "Need to save!")
			dialog.format_secondary_text(
			"Database are edited. If you press OK, Database will not be saved.")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				location = self.txt_location.get_text()
				if location != "":
					self.loadData(location)
			dialog.destroy()

		else:
			location = self.txt_location.get_text()
			if location != "":
				self.loadData(location)

	# Export Session
	def SendToExport(self, *arg):
		rows = self.library_list.get_selected_rows()
		if rows and self.library != None:
			for row in rows:
				if not row.moviefile.exported :
					row.moviefile.exported = True

		run_generator(self.DrawExportListBox)

	def DrawExportListBox(self, foundedlist=None):
		listbox 	= self.export_list
		if foundedlist == None:
			datas 		= self.library.All()
		else:
			datas 		= foundedlist
		
		# listbox.moviefiles_list = datas
		self.clear_row(listbox)
		idx = 0
		self.exportsize = 0
		for data in datas:
			if data.exported:
				if idx < 500:
					list_row 	= CreateListBoxRow(data,idx)
					listbox.add(list_row)
					listbox.show_all()
				idx += 1
				self.exportsize += data.size
				
			
			
				self.exportlbl_total_media.set_text("Total: %i"%idx)
				self.exportlbl_total_size.set_text("Total: %s"%self.size_format(self.exportsize))
				if foundedlist == None:
					self.loadfreespace()
				yield True
		self.exportlist_count = idx
		self.exportlbl_total_media.set_text("Total: %i"%idx)
		self.exportlbl_total_size.set_text("Total: %s"%self.size_format(self.exportsize))

	def getDirNameString(self, text):
		tmp = ""
		for c in text:
			if c.isdigit():
				tmp += c
		return tmp


	def RemoveFromExport(self, *arg):
		rows = self.export_list.get_selected_rows()
		if rows:
			for row in rows:
				row.moviefile.exported = False
		run_generator(self.DrawExportListBox)

	def SaveExportList(self, *arg):
		destnation = self.exporttext_location.get_text()
		sdate = str(datetime.now())
		self.curdirname = self.getDirNameString(sdate)
		if destnation != "":
			destnation = "%s/ghostcopy_%s"%(destnation, self.curdirname)
			if not os.path.exists(destnation):
				os.makedirs(destnation)
			# self.window.set_sensitive(False)
			export_moviefiles = self.mydb.NewMediafiles()
			export_moviefiles.savefilepath = destnation+"/ghost.db"
			idx = 0

			dbSaveDialog = SD(self.mydb,export_moviefiles,self.library.All(), self.exportlist_count,destnation)
			dbSaveDialog.run()
			
			


	def exportlistbox_key_press_event(self, widget, event):
		# Mouse Double Click
		if event.type == Gdk.EventType._2BUTTON_PRESS and event.button == 1:
			row = widget.get_selected_row()
			if row:
				if self.current_mediafile != row.moviefile:
					self.stop()
					self.current_mediafile = row.moviefile
					self.play()

	def ExportLocation(self, *arg):
		dialog = Gtk.FileChooserDialog("Please choose export location", self.window,
					Gtk.FileChooserAction.SELECT_FOLDER,
					(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
					"Select", Gtk.ResponseType.OK))
		dialog.set_default_size(600, 300)

		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			dbfilepath 	= dialog.get_filename()
			self.exporttext_location.set_text(dbfilepath)
			self.loadfreespace()
		dialog.destroy()

	def loadfreespace(self):
		location = self.exporttext_location.get_text()
		if location != "":
			df = sp.Popen(["df",location], stdout=sp.PIPE)
			output = df.communicate()[0]
			newoutput = str(output).split("\\n")[1].split()
			# [device,size, used, available, percent, mountpoint,...]
			size = newoutput[1]
			used = newoutput[2]
			size = float(size) * 1000.0
			value = (float(used)  * 1000.0) + float(self.exportsize)
			self.space_level.set_max_value(size)
			self.space_level.set_value(value)
			self.exportlbl_usage.set_text("Storage: %s/%s"%(self.size_format(value),self.size_format(size)))



	def Exportmain_search(self, widget=None, event=None):
		txt = self.txt_location.get_text()
		if txt != "":
			tmp = widget.get_text()
			foundedlist = self.library.SearchByTitleForExported(tmp)
			run_generator(self.DrawExportListBox,foundedlist)

	# -------------------------------------------

	def openlocation(self, *arg):
		if self.SAVE_STATE:
			dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
					Gtk.ButtonsType.OK_CANCEL, "Need to save!")
			dialog.format_secondary_text(
			"Database are edited. If you press OK, Database will not be saved.")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				dialog.destroy()
				filedialog = Gtk.FileChooserDialog("Please choose media location", self.window,
					Gtk.FileChooserAction.SELECT_FOLDER,
					(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
					"Select", Gtk.ResponseType.OK))
				filedialog.set_default_size(600, 300)

				response = filedialog.run()
				if response == Gtk.ResponseType.OK:
					dbfilepath 	= filedialog.get_filename()
					filedialog.destroy()
					GLib.idle_add(self.loadData,dbfilepath, priority=GLib.PRIORITY_LOW)
				else:
					filedialog.destroy()
			else:
				dialog.destroy()
				
		else:
			filedialog = Gtk.FileChooserDialog("Please choose media location", self.window,
					Gtk.FileChooserAction.SELECT_FOLDER,
					(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
					"Select", Gtk.ResponseType.OK))
			filedialog.set_default_size(600, 300)

			response = filedialog.run()
			if response == Gtk.ResponseType.OK:
				dbfilepath 	= filedialog.get_filename()
				filedialog.destroy()
				GLib.idle_add(self.loadData,dbfilepath, priority=GLib.PRIORITY_LOW)		
			else:
				filedialog.destroy()
			
	def loadData(self, dbfilepath):
		self.txt_location.set_text(dbfilepath)
		dbfile 		= "%s/ghost.db"%dbfilepath
		if not os.path.exists(dbfile):
			dirname = os.path.dirname(dbfile)
			if os.path.exists(dirname):
				wfile = open(dbfile,"wb")
				wfile.close()
		self.library = self.mydb.open_dbfile("ghost.db",dbfilepath)

		# self.DrawListBox()
		if self.library != None:
			run_generator(self.DrawListBox)
			self.SAVE_STATE = False
			self.FoundedTitleEdited 	= True
			self.FoundedArtistEdited	= True
			self.FoundedAlbumEdited 	= True 
			self.FoundedCategoryEdited 	= True
			idx = self.founded_notebook.get_current_page()
			self.founded_notebook_changepaged(None,None,idx)
			self.UpdateUI()


	def clear_row(self,listbox):
		for row in listbox.get_children():
			row.destroy()

	def DrawListBox(self, searchlist=None):
		listbox 	= self.library_list
		if searchlist == None:
			datas 		= self.library.All()
		else:
			datas 		= searchlist

		# listbox.moviefiles_list = datas
		self.clear_row(listbox)
		idx = 0
		size = 0
		for data in datas:
			if data.active:
				if idx < len(datas) :
					list_row 	= CreateListBoxRow(data,idx)
					listbox.add(list_row)
					listbox.show_all()
				idx += 1
				size += data.size	
				self.lbl_total_media.set_text("Total: %i"%idx)
				self.lbl_total_size.set_text("Total: %s"%self.size_format(size))
				yield True

		self.lbl_total_media.set_text("Total: %i"%idx)
		self.lbl_total_size.set_text("Total: %s"%self.size_format(size))


	def main_search(self, widget=None, event=None):
		txt = self.txt_location.get_text()
		self.foundedlist = []
		if txt != "":
			tmp = widget.get_text()
			self.foundedlist = self.library.SearchByTitle(tmp)
			run_generator(self.DrawListBox, self.foundedlist)

	def size_format(self,num,suffix='B'):
		for unit in ['','K','M','G','T','P','E','Z']:
			if abs(num)<1000.0:
				return "%3.1f%s%s"%(num, unit, suffix)
			num /= 1000.0
		return "%.1f%s%s"%(num, 'Wi', suffix)

	def MainListBoxRowSelected(self,*arg):
		rows = self.library_list.get_selected_rows()
		if rows:
			sizes = 0
			for row in rows:
				sizes += row.moviefile.size
			self.lbl_selected_size.set_text("Selected Size: %s"%self.size_format(sizes))
			self.ArtistListBoxRowSelected()
			self.AlbumListBoxRowSelected()
			self.CategoryListBoxRowSelected()
		else:
			self.lbl_selected_size.set_text("Selected Size: 0")
		if len(rows) == 1:
			self.TitleListBoxRowSelected()
			# self.current_mediafile = rows[0].moviefile

		self.UpdateUI()
		


	# Main Title Session
	def TitleListBoxRowSelected(self,*arg):
		row = self.library_list.get_selected_row()
		if row:
			title = row.moviefile.Title
			self.main_title.DrawListBox(self.main_title.down_list_titles,[title])


	def title_btn_up_press(self,*arg):
		media_row 		= self.library_list.get_selected_row()
		title_row		= self.main_title.down_list_titles.get_selected_row()
		if title_row and media_row:
			media_row.moviefile.Title = media_row.moviefile.newTitle()
			media_row.update_label()
			self.main_title.DrawListBox(self.main_title.down_list_titles,[media_row.moviefile.Title])
			self.SAVE_STATE = True
			self.FoundedTitleEdited = True # For redraw founded title list
			if self.founded_notebook.get_current_page() != 0:
				self.founded_notebook.set_current_page(0)
			else:
				self.TitleUPDATE_UI()
			self.UpdateUI()

	def title_btn_down_press(self,*arg):
		media_row 		= self.library_list.get_selected_row()
		title_row		= self.main_title.up_list_titles.get_selected_row()
		if title_row and media_row:
			if not media_row.moviefile.check_title_exists(title_row.title):
				media_row.moviefile.Title = title_row.title
				media_row.update_label()
				self.main_title.DrawListBox(self.main_title.down_list_titles,[title_row.title])
				self.SAVE_STATE = True
				self.FoundedTitleEdited = True # For redraw founded title list
				if self.founded_notebook.get_current_page() != 0:
					self.founded_notebook.set_current_page(0)
				else:
					self.TitleUPDATE_UI()
				self.UpdateUI()
			else:
				print("already exist")

	def title_btn_add_press(self, *arg):
		search_text = self.main_title.txt_search.get_text()

		Title_Entry = TitleEntry(self.window,self.mydb.TITLES_LIST,search_text)
		response = Title_Entry.run()
		Title_Entry.destroy()

		self.main_title.search_changed(self.main_title.txt_search)


	# Mainf Artist Session
	def ArtistListBoxRowSelected(self,*arg):
		rows = self.library_list.get_selected_rows()
		artistlist = []
		if rows:
			for row in rows:
				artistlist += row.moviefile.Artists.All()
			# filter dublicate artist
			artistlist = list(set(artistlist))
			self.main_artist.DrawListBox(self.main_artist.down_list_artists,artistlist)


	def artist_btn_up_press(self,*arg):
		media_rows 		= self.library_list.get_selected_rows()
		artist_row		= self.main_artist.down_list_artists.get_selected_row()
		if artist_row and media_rows:
			artistlist = []
			for media_row in media_rows:
				if len(media_row.moviefile.Artists.All())>1 :
					media_row.moviefile.Artists.Remove(artist_row.artist)
				else:
					media_row.moviefile.Artists.Remove(artist_row.artist)
					media_row.moviefile.Artists.Add(media_row.moviefile.Artists.new())
				media_row.update_label()
				artistlist += media_row.moviefile.Artists.All()
			artistlist = list(set(artistlist))
			self.main_artist.DrawListBox(self.main_artist.down_list_artists,artistlist)
			self.SAVE_STATE = True
			self.FoundedArtistEdited = True # For redraw founded Artist list
			if self.founded_notebook.get_current_page() != 1:
				self.founded_notebook.set_current_page(1)
			else:
				self.ArtistUPDATE_UI()
			
			self.UpdateUI()

	def artist_btn_down_press(self,*arg):
		media_rows 		= self.library_list.get_selected_rows()
		artist_row		= self.main_artist.up_list_artists.get_selected_row()
		if artist_row and media_rows:
			artistlist = []
			for media_row in media_rows:
				if not media_row.moviefile.Artists.check_exists(artist_row.artist):
					media_row.moviefile.Artists.Add(artist_row.artist)
					media_row.update_label()
				else:
					print("already exist")
				artistlist += media_row.moviefile.Artists.All()
			artistlist = list(set(artistlist))
			self.main_artist.DrawListBox(self.main_artist.down_list_artists,artistlist)
			self.SAVE_STATE = True
			self.FoundedArtistEdited = True # For redraw founded Artist list
			if self.founded_notebook.get_current_page() != 1:
				self.founded_notebook.set_current_page(1)
			else:
				self.ArtistUPDATE_UI()
			
			self.UpdateUI()
	def artist_btn_add_press(self, *arg):
		search_text = self.main_artist.txt_search.get_text()

		Artist_Entry = ArtistEntry(self.window,self.mydb.ARTISTS_LIST,search_text)
		response = Artist_Entry.run()
		Artist_Entry.destroy()

		self.main_artist.search_changed(self.main_artist.txt_search)


	# Main Album Session
	def AlbumListBoxRowSelected(self,*arg):
		rows = self.library_list.get_selected_rows()
		albumslist = []
		if rows:
			for row in rows:
				album = row.moviefile.Album
				albumslist += [album]
			# filter dublicate album
			albumslist = list(set(albumslist))
			self.main_album.DrawListBox(self.main_album.down_list_albums,albumslist)


	def album_btn_up_press(self,*arg):
		media_rows 		= self.library_list.get_selected_rows()
		album_row		= self.main_album.down_list_albums.get_selected_row()
		if album_row and media_rows:
			albumslist 	= []
			for media_row in media_rows:
				if album_row.album == media_row.moviefile.Album :
					print("same")
					media_row.moviefile.Album = media_row.moviefile.newAlbum()
					media_row.update_label()
				albumslist += [media_row.moviefile.Album]
			albumslist = list(set(albumslist))
			self.main_album.DrawListBox(self.main_album.down_list_albums,albumslist)
			self.SAVE_STATE = True
			self.FoundedAlbumEdited = True # For redraw founded Album list
			if self.founded_notebook.get_current_page() != 2:
				self.founded_notebook.set_current_page(2)
			else:
				self.AlbumUPDATE_UI()
			
			self.UpdateUI()

	def album_btn_down_press(self,*arg):
		media_rows 		= self.library_list.get_selected_rows()
		album_row		= self.main_album.up_list_albums.get_selected_row()
		if album_row and media_rows:
			albumslist 	= []
			for media_row in media_rows:
				if not media_row.moviefile.check_album_exists(album_row.album):
					media_row.moviefile.Album = album_row.album
					media_row.update_label()
				albumslist += [album_row.album]
			albumslist = list(set(albumslist))
			self.main_album.DrawListBox(self.main_album.down_list_albums,albumslist)
			self.SAVE_STATE = True
			self.FoundedAlbumEdited = True # For redraw founded Album list
			if self.founded_notebook.get_current_page() != 2:
				self.founded_notebook.set_current_page(2)
			else:
				self.AlbumUPDATE_UI()
			
			self.UpdateUI()

	def album_btn_add_press(self, *arg):
		search_text = self.main_album.txt_search.get_text()

		Album_Entry = AlbumEntry(self.window,self.mydb.ALBUMS_LIST,search_text)
		response = Album_Entry.run()
		Album_Entry.destroy()

		self.main_album.search_changed(self.main_album.txt_search)


	# Main Cateogry Session
	def CategoryListBoxRowSelected(self,*arg):
		rows = self.library_list.get_selected_rows()
		categorieslist 	= []
		if rows:
			for row in rows:
				categorieslist += row.moviefile.Categories.All()
			# filter dublicate category
			categorieslist = list(set(categorieslist))
			self.main_category.DrawListBox(self.main_category.down_list_categories,categorieslist)


	def category_btn_up_press(self,*arg):
		media_rows 		= self.library_list.get_selected_rows()
		category_row		= self.main_category.down_list_categories.get_selected_row()
		if category_row and media_rows:
			categorieslist 	= []
			for media_row in media_rows:
				if len(media_row.moviefile.Categories.All())>1 :
					media_row.moviefile.Categories.Remove(category_row.category)
				else:
					media_row.moviefile.Categories.Remove(category_row.category)
					media_row.moviefile.Categories.Add(media_row.moviefile.Categories.new())
				media_row.update_label()
				categorieslist += media_row.moviefile.Categories.All()
			categorieslist = list(set(categorieslist))
			self.main_category.DrawListBox(self.main_category.down_list_categories,categorieslist)
			self.SAVE_STATE = True
			self.FoundedCategoryEdited = True # For redraw founded Category list
			if self.founded_notebook.get_current_page() != 3:
				self.founded_notebook.set_current_page(3)
			else:
				self.CategoryUPDATE_UI()
			
			self.UpdateUI()

	def category_btn_down_press(self,*arg):
		media_rows 		= self.library_list.get_selected_rows()
		category_row		= self.main_category.up_list_categories.get_selected_row()
		if category_row and media_rows:
			categorieslist = []
			for media_row in media_rows:
				# check already exists
				if not media_row.moviefile.Categories.check_exists(category_row.category):
					media_row.moviefile.Categories.Add(category_row.category)
					media_row.update_label()

				categorieslist += media_row.moviefile.Categories.All()
			categorieslist = list(set(categorieslist))
			self.main_category.DrawListBox(self.main_category.down_list_categories,categorieslist)
			self.SAVE_STATE = True
			self.FoundedCategoryEdited = True # For redraw founded Category list
			if self.founded_notebook.get_current_page() != 3:
				self.founded_notebook.set_current_page(3)
			else:
				self.CategoryUPDATE_UI()
			
			self.UpdateUI()

	def category_btn_add_press(self, *arg):
		search_text = self.main_category.txt_search.get_text()

		Category_Entry = CategoryEntry(self.window,self.mydb.CATEGORIES_LIST,search_text)
		response = Category_Entry.run()
		Category_Entry.destroy()

		self.main_category.search_changed(self.main_category.txt_search)

	def TitleUPDATE_UI(self,*arg):
		if self.library != None:
			self.library.create_counted_title()
			self.library.sort_founded_title()
			run_generator(self.DrawTitleFoundedListBox,(self.founded_title_list,self.library.sortedtitles))
			self.FoundedTitleEdited = False
		

	def DrawTitleFoundedListBox(self,datas):
		listbox = datas[0]
		datas 	= datas[1]
		self.clear_row(listbox)
		idx = 0
		for data in datas:
			list_row 	= Title_CreateFoundedListBoxRow(data[0],data[1],idx,self.library.All(),self.DrawListBox)
			listbox.add(list_row)
			idx += 1
			listbox.show_all()
			yield True


	# Filterd for Artists
	def ArtistUPDATE_UI(self,*arg):
		if self.library != None:
			self.library.create_counted_artist()
			self.library.sort_founded_artist()
			run_generator(self.DrawArtistFoundedListBox,(self.founded_artist_list,self.library.sortedartists))
			self.FoundedArtistEdited = False
		

	def DrawArtistFoundedListBox(self,datas):
		listbox = datas[0]
		datas 	= datas[1]
		self.clear_row(listbox)
		idx = 0
		for data in datas:
			list_row 	= Artist_CreateFoundedListBoxRow(data[0],data[1],idx,self.library.All(),self.DrawListBox)
			listbox.add(list_row)
			idx += 1
			listbox.show_all()
			yield True

	# Filterd for Albums
	def AlbumUPDATE_UI(self,*arg):
		if self.library != None:
			self.library.create_counted_album()
			self.library.sort_founded_album()
			run_generator(self.DrawAlbumFoundedListBox,(self.founded_album_list,self.library.sortedalbums))
			self.FoundedAlbumEdited = False
		

	def DrawAlbumFoundedListBox(self,datas):
		listbox = datas[0]
		datas 	= datas[1]
		self.clear_row(listbox)
		idx = 0
		for data in datas:
			list_row 	= Album_CreateFoundedListBoxRow(data[0],data[1],idx, self.library.All(),self.DrawListBox)
			listbox.add(list_row)
			idx += 1
			listbox.show_all()
			yield True


	# Filterd for Categories
	def CategoryUPDATE_UI(self,*arg):
		if self.library != None:
			self.library.create_counted_category()
			self.library.sort_founded_category()
			run_generator(self.DrawCategoryFoundedListBox,(self.founded_category_list,self.library.sortedcategories))
			self.FoundedCategoryEdited = False
		

	def DrawCategoryFoundedListBox(self,datas):
		listbox = datas[0]
		datas 	= datas[1]
		self.clear_row(listbox)
		idx = 0
		for data in datas:
			list_row 	= Category_CreateFoundedListBoxRow(data[0],data[1],idx, self.library.All(),self.DrawListBox)
			listbox.add(list_row)
			idx += 1
			listbox.show_all()
			yield True

class Title_CreateFoundedListBoxRow(Gtk.ListBoxRow):
	def __init__(self, key,values,idx,library_list, redrawlistmethod):
		super(Title_CreateFoundedListBoxRow,self).__init__()
		self.RedrawMainListBox = redrawlistmethod
		self.MainList = library_list
		self.index 	= idx
		self.Foundedkey 	= key    # key is key = string 
		self.Foundedvalues 	= values # values is list = []

		hbox = Gtk.HBox()

		self.check_selectbox = Gtk.CheckButton()
		self.check_selectbox.connect("toggled", self.on_checkbox_toggled)

		self.Char_Label = Gtk.Label(str(len(values)),xalign=1.0)
		self.Fullname_Label = Gtk.Label(key.title)
		
		hbox.pack_start(self.check_selectbox,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		hbox.pack_end(self.Char_Label,False,False,5)
		
		self.add(hbox)

	def on_checkbox_toggled(self, widget=None, event=None):
		parent = self.get_parent()
		self.DrawListBox(parent)

	def clear_row(self,moviefiles):
		for moviefile in moviefiles:
			moviefile.active = False

	def DrawListBox(self,listbox):
		self.clear_row(self.MainList)
		idx = 0
		for row in listbox.get_children():
			check_state = row.check_selectbox.get_active()
			if check_state :
				for moviefile in row.Foundedvalues:
					moviefile.active = True
		run_generator(self.RedrawMainListBox)

class Artist_CreateFoundedListBoxRow(Gtk.ListBoxRow):
	def __init__(self, key,values,idx,library_list, redrawlistmethod):
		super(Artist_CreateFoundedListBoxRow,self).__init__()
		self.RedrawMainListBox = redrawlistmethod
		self.MainList = library_list
		self.index 	= idx
		self.Foundedkey 	= key    # key is key = string 
		self.Foundedvalues 	= values # values is list = []

		hbox = Gtk.HBox()

		self.check_selectbox = Gtk.CheckButton()
		self.check_selectbox.connect("toggled", self.on_checkbox_toggled)

		self.Char_Label = Gtk.Label(str(len(values)),xalign=1.0)
		self.Fullname_Label = Gtk.Label(key.name)
		
		hbox.pack_start(self.check_selectbox,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		hbox.pack_end(self.Char_Label,False,False,5)
		
		self.add(hbox)
	def on_checkbox_toggled(self, widget=None, event=None):
		parent = self.get_parent()
		self.DrawListBox(parent)

	def clear_row(self,moviefiles):
		for moviefile in moviefiles:
			moviefile.active = False


	def DrawListBox(self,listbox):
		self.clear_row(self.MainList)
		idx = 0
		for row in listbox.get_children():
			check_state = row.check_selectbox.get_active()
			if check_state :
				for moviefile in row.Foundedvalues:
					moviefile.active = True
		run_generator(self.RedrawMainListBox)

class Album_CreateFoundedListBoxRow(Gtk.ListBoxRow):
	def __init__(self, key,values,idx,library_list, redrawlistmethod):
		super(Album_CreateFoundedListBoxRow,self).__init__()
		self.RedrawMainListBox = redrawlistmethod
		self.MainList = library_list
		self.index 	= idx
		self.Foundedkey 	= key    # key is key = string 
		self.Foundedvalues 	= values # values is list = []
		
		hbox = Gtk.HBox()

		self.check_selectbox = Gtk.CheckButton()
		self.check_selectbox.connect("toggled", self.on_checkbox_toggled)

		self.Char_Label = Gtk.Label(str(len(values)),xalign=1.0)
		self.Fullname_Label = Gtk.Label(key.albumname)
		
		hbox.pack_start(self.check_selectbox,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		hbox.pack_end(self.Char_Label,False,False,5)
		
		self.add(hbox)

	def on_checkbox_toggled(self, widget=None, event=None):
		parent = self.get_parent()
		self.DrawListBox(parent)

	def clear_row(self,moviefiles):
		for moviefile in moviefiles:
			moviefile.active = False

	def DrawListBox(self,listbox):
		self.clear_row(self.MainList)
		idx = 0
		for row in listbox.get_children():
			check_state = row.check_selectbox.get_active()
			if check_state :
				for moviefile in row.Foundedvalues:
					moviefile.active = True
		run_generator(self.RedrawMainListBox)


class Category_CreateFoundedListBoxRow(Gtk.ListBoxRow):
	def __init__(self, key,values,idx, library_list, redrawlistmethod):
		super(Category_CreateFoundedListBoxRow,self).__init__()
		self.RedrawMainListBox = redrawlistmethod
		self.MainList = library_list
		self.index 	= idx
		self.Foundedkey 	= key    # key is key = string 
		self.Foundedvalues 	= values # values is list = []
		hbox = Gtk.HBox()

		self.check_selectbox = Gtk.CheckButton()
		self.check_selectbox.connect("toggled", self.on_checkbox_toggled)

		self.Char_Label = Gtk.Label(str(len(values)),xalign=1.0)
		self.Fullname_Label = Gtk.Label(key.categoryname)
		
		hbox.pack_start(self.check_selectbox,False,False,0)
		hbox.pack_start(self.Fullname_Label,False,False,5)
		hbox.pack_end(self.Char_Label,False,False,5)
		
		self.add(hbox)

	def on_checkbox_toggled(self, widget=None, event=None):
		parent = self.get_parent()
		self.DrawListBox(parent)

	def clear_row(self,moviefiles):
		for moviefile in moviefiles:
			moviefile.active = False


	def DrawListBox(self,listbox):
		self.clear_row(self.MainList)
		idx = 0
		for row in listbox.get_children():
			check_state = row.check_selectbox.get_active()
			if check_state :
				for moviefile in row.Foundedvalues:
					moviefile.active = True
		run_generator(self.RedrawMainListBox)


def run_generator(func,arg=None):
	gen = func(arg)
	GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)

def load_css():
	style_provider = Gtk.CssProvider()

	css = open(BASE_DIR+'/css/mycss.css', 'rb') # rb needed for python 3 support
	css_data = css.read()
	css.close()

	style_provider.load_from_data(css_data)

	Gtk.StyleContext.add_provider_for_screen(
		Gdk.Screen.get_default(), style_provider,     
		Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)


if __name__ == '__main__':
	load_css()
	mainwindow = myWindow()
	# mydb 	 	= DB()

	# album_entry = CategoryEntry(mainwindow,mydb.CATEGORIES_LIST)
	
	# response = album_entry.run()
	# print(response)

	# album_entry.destroy()


	Gtk.main()
