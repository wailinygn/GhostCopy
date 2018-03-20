import time, threading
import gi
gi.require_version("Gst","1.0")
gi.require_version("GstVideo","1.0")
from gi.repository import Gst, GObject, GLib
from gi.repository import GstVideo


# from config import *
import time



Gst.init(None)





class Player(GObject.GObject):

	
	
	def __init__(self):
		super(Player,self).__init__()

		self.ratio_str 	= "1/1"
		self.vol 	= 5
		self.dur_int  = 0.0
		self.createPipeLine()

		self.MousePress  = False

		
		
	def createPipeLine(self):
		# Create GStreamer pipeline
		self.player = Gst.Pipeline()
		# Create bus to get events from GStreamer pipeline
		self.bus = self.player.get_bus()
		self.bus.add_signal_watch()
		self.bus.connect('message::eos', self.on_eos)
		self.bus.connect('message::error', self.on_error)

		# This is needed to make the video output in our DrawingArea:
		self.bus.enable_sync_message_emission()
		self.bus.connect('sync-message::element', self.on_sync_message)



		self.filesrc  =Gst.ElementFactory.make("filesrc","filesource")
		self.decodebin =Gst.ElementFactory.make("decodebin","decodebin")
		self.decodebin.connect("pad_added",self.decodebin_pad_added)

		#--------------Audio Session -------------------#

		self.audioQueue =Gst.ElementFactory.make("queue","audioqueue")
		self.audioconvert =Gst.ElementFactory.make("audioconvert","audioconvert")
		self.audiocapfilter =Gst.ElementFactory.make("capsfilter","audiocapfilter")
		audiocaps = Gst.Caps.from_string("audio/x-raw,channels=1")
		self.audiocapfilter.set_property("caps",audiocaps)
		self.audiosink =Gst.ElementFactory.make("autoaudiosink","alsasink")
		


		#--------------Video Session -------------------#
		self.videoQueue =Gst.ElementFactory.make("queue","videoqueue")
		self.videoconvert =Gst.ElementFactory.make("videoconvert","videoconvert")
		self.scale =Gst.ElementFactory.make("videoscale","videoscale")
		self.videosink  =Gst.ElementFactory.make("xvimagesink","videosink")
		
		#---------------- Text Overlay ----------------#
		self.OSD_Text =Gst.ElementFactory.make("textoverlay")
		self.OSD_Text.set_property("text","Triple111")
		self.OSD_Text.set_property("halignment","left")
		self.OSD_Text.set_property("valignment","top")
		# self.OSD_Text.set_property("shaded-background",True)


		self.player.add(self.filesrc)
		self.player.add(self.decodebin)

		self.player.add(self.audioQueue)
		self.player.add(self.audioconvert)
		self.player.add(self.audiocapfilter)
		self.player.add(self.audiosink)

		self.player.add(self.videoQueue)
		self.player.add(self.videoconvert)
		self.player.add(self.OSD_Text)
		self.player.add(self.scale)
		self.player.add(self.videosink)


		self.filesrc.link(self.decodebin)
		#---------- For Audio -----------------#
		self.audioQueue.link(self.audioconvert)
		self.audioconvert.link(self.audiocapfilter)
		self.audiocapfilter.link(self.audiosink)
		#---------- For Video -----------------#
		self.videoQueue.link(self.videoconvert)
		self.videoconvert.link(self.OSD_Text)
		self.OSD_Text.link(self.scale)
		self.scale.link(self.videosink)

		self.player.set_state(Gst.State.READY)
		
	def compare_state(self,pipeline, state):
		return pipeline.get_state(1)[1] == state

	def on_sync_message(self, bus, msg):
		self.msg = msg
		if msg.get_structure().get_name() == 'prepare-window-handle':            
			msg.src.set_window_handle(self.xid)

	def on_eos(self,*args):
		self.play_thread_id = None
		self.player.set_state(Gst.State.NULL)
					

	def on_error(self, bus, msg):
		self.play_thread_id = None
		self.player.set_state(Gst.State.NULL)
	
	def decodebin_pad_added(self, decodebin, pad):
		compatible_pad = None
		caps = pad.query_caps(None)
		name = caps.to_string()
		if name.startswith('video/'):
			compatible_pad = (self.videoQueue.get_compatible_pad(pad, caps))
		elif name.startswith('audio/'):
			compatible_pad = (self.audioQueue.get_compatible_pad(pad, caps))
		if compatible_pad:
			pad.link(compatible_pad)

	# ------------------ PLAYER CONTROL ------------------- #
	def convert_ns(self,t):
		s, ns = divmod(t, 1000000000)
		m, s = divmod(s, 60)
		if m<60:
			return "%02i:%02i" %(m, s)
		else:
			h, m = divmod(m, 60)
			return "%i:%02i:%02i" %(h, m, s)
	def ToDoPlayState(self):
		self.filesrc.set_property("location",self.current_mediafile.filepath)
		self.OSD_Text.set_property("text",self.current_mediafile.filename)
		self.player.set_state(Gst.State.PLAYING)
		self.dur_int = 0
		self.pos_int = 0
		self.dur_str = "00:00"
		self.pos_str = "00:00"


	def play(self,*arg):
		if self.compare_state(self.player,Gst.State.PAUSED):
			if self.current_mediafile != None:
				self.player.set_state(Gst.State.PLAYING)
		else:
			if self.current_mediafile != None:
				self.ToDoPlayState()
				self.play_thread_id = threading.Thread(target=self.play_thread)
				self.play_thread_id.start()
		
	def play_thread(self):
		play_thread_id = self.play_thread_id
		while play_thread_id == self.play_thread_id:
			time.sleep(0.02)
			self.dur_int = self.player.query_duration(Gst.Format.TIME)[1]
			if self.dur_int <= 0:
				continue
			self.dur_str = self.convert_ns(self.dur_int)
			
			self.adjustment.set_value(0.0)
			self.adjustment.set_upper(float(self.dur_int))
			break
			
		time.sleep(0.02)
		while play_thread_id == self.play_thread_id:
			self.pos_int = self.player.query_position(Gst.Format.TIME)[1]
			
			if self.pos_int < self.dur_int+Gst.SECOND:
				self.pos_str = self.convert_ns(self.pos_int)
				try:
					GLib.idle_add(self.set_scale_and_text, priority=GLib.PRIORITY_LOW)

				except:
					pass
			else:
				self.stop()
			time.sleep(1)

	def set_scale_and_text(self, *arg):
		self.adjustment.set_value(float(self.pos_int))
		settxt = "{0}/{1}".format(self.pos_str,self.dur_str)
		self.lbl_time.set_text(settxt)

	def pause(self, *arg):
		if self.compare_state(self.player,Gst.State.PLAYING):
			self.player.set_state(Gst.State.PAUSED)
	def stop(self, *arg):
		self.play_thread_id = None
		self.player.set_state(Gst.State.NULL)

	def do_scale_press(self, widget=None, event=None):
		self.pause()
		self.MousePress  = True
	
	def do_scale_release(self, widget=None, event=None):
		self.MousePress  = False
		if self.current_mediafile != None:
			self.player.set_state(Gst.State.PLAYING)

	def do_change_seek(self,vol):
		if self.MousePress and self.current_mediafile != None:
			seek_val = int(self.adjustment.get_value())
			if seek_val:
				self.player.seek_simple(
	                Gst.Format.TIME,        
	                Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
	                seek_val
	            )  

	