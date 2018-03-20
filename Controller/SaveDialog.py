#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GLib
import os

from shutil import copyfile


class ExportDialog(Gtk.Dialog):
	def __init__(self,db,exportdbfile,exportlist,totalcount,destnation):
		Gtk.Dialog.__init__(self, "Exporting...", None, Gtk.DialogFlags.MODAL)

		self.set_size_request(300,-1)
		self.mydb 			= db
		self.exportdbfile 	= exportdbfile
		self.exportlist 	= exportlist
		self.totalcount 	= totalcount
		self.destnation 	= destnation

		#----updated -----#
		self.cancelAction = False

		box = Gtk.VBox()
		self.lbl_done 		= Gtk.Label("0/0 done",xalign=0.0)
		self.progressbar 	= Gtk.LevelBar()
		self.CancelBtn 		= Gtk.Button("Cancel")
		self.CancelBtn.connect("clicked", self.doCandel)
		box.pack_start(self.lbl_done,True,True,5)
		box.pack_start(self.progressbar,True,True,5)
		box.pack_start(self.CancelBtn,True,True,5)
		self.progressbar.set_max_value(totalcount)
		self.lbl_done.set_text("0/%i exported"%(self.totalcount))
		box_area = self.get_content_area()
		box_area.add(box)

	def doCandel(self, *args, **kwargs):
		self.cancelAction = True

	def run(self):
		self.show_all()
		self.run_generator(self.Active_loop)

	def run_generator(self, func):
		gen = func()
		GLib.idle_add(lambda: next(gen, False), priority=GLib.PRIORITY_LOW)
	def Active_loop(self):
		idx = 0
		for moviefile in self.exportlist:
			if self.cancelAction:
				break
			if moviefile.exported:
				dirname = os.path.dirname(moviefile.filepath)
				dirname = os.path.basename(dirname)
				parent_dirname = "%s/%s" % (self.destnation, dirname)
				if not os.path.exists(parent_dirname):
					os.makedirs(parent_dirname)
				# moviefile.filepath =
				self.exportdbfile.Add(moviefile)
				copyfile(moviefile.filepath, parent_dirname+"/"+moviefile.filename)

				self.mydb.DB_Save(self.exportdbfile)
				idx += 1
				self.lbl_done.set_text("%i/%i exported"%(idx,self.totalcount))
				self.progressbar.set_value(idx)
				yield True
		self.destroy()
			

			
		

