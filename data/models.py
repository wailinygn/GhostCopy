# -*- coding: utf-8 -*-
import uuid
from config import *
def newid():
	newid = uuid.uuid4()
	return str(newid)
class Title:
	"""	There is a Title Class.
		This has uuid, name, photo path.
	"""
	def __init__(self,  title=UNKNOWN, uid=None, short_name=UNKNOWN):
		if uid == None:
			self.uid = newid()
		else:
			self.uid 		= uid
		self.title 			= title
		self.short_name 	= short_name

	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]
		return None
	def get(self, attr):
		return getattr(self,attr)

	def __repr__(self):
		return self.title
	def __str__(self):
		return self.title


class Artist:
	"""	There is a Artist Class.
		This has uuid, name, photo path.
	"""
	def __init__(self, uid=None, name=UNKNOWN,gender=None,photo_path=None):
		if uid == None:
			self.uid 	= newid()
		else:
			self.uid 	= uid
		self.name 		= name
		self.short_name = UNKNOWN
		self.gender 	= gender
		self.photo  	= photo_path
		self.songs 		= []
	def __getattr__(self, attr):
		print(self.__dict__)
		if attr in self.__dict__:
			return self.__dict__[attr]
		return None
	def get(self, attr):
		return getattr(self,attr)
	def __repr__(self):
		return self.name
	def __str__(self):
		return self.name

class Album:
	"""	There is a Album Class.
		This has uuid, albumname, albumphoto path, published date.
	"""
	def __init__(self, uid=None, albumname=UNKNOWN,photo_path=None,pub_date=None):
		if uid == None:
			self.uid = newid()
		else:
			self.uid 	= uid
		self.albumname = albumname
		self.short_albumname = UNKNOWN
		self.photo  	= photo_path
		self.published 	= pub_date
	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]
		return None
	def get(self, attr):
		return getattr(self,attr)
		
	def __repr__(self):
		return self.albumname
	def __str__(self):
		return self.albumname


class Category:
	"""	There is a Category Class.
		This has uid, categoryname, published date.
	"""
	def __init__(self, uid=None, categoryname=UNKNOWN,photo_path=None,pub_date=None):
		if uid == None:
			self.uid = newid()
		else:
			self.uid 			= uid
		self.categoryname 		= categoryname
		self.short_categoryname = UNKNOWN
		self.published 			= pub_date
	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]
		return None
	def get(self, attr):
		return getattr(self,attr)
		
	def __repr__(self):
		return self.categoryname
	def __str__(self):
		return self.categoryname



class Titles:
	def __init__(self, *args):
		self.Titles = list(args)
		
	def Add(self, *args):
		for title in args:
			self.Titles.append(title)

	def __repr__(self):
		if len(self.Titles)>0:
			return "%s"%self.Titles[0]
		return ""
		
	def All(self):
		return self.Titles

	def length(self):
		return len(self.Titles)

	def sort(self):
		tmpdict 	= {}
		tmptitles = []
		for title in self.Titles:
			tmpdict[title.short_name.lower()+title.uid.lower()] = title

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			tmptitles.append(tmpdict[key])
		self.Titles = tmptitles

	def SearchByName(self, fltr_txt,limit=200):
		fltr_txt = fltr_txt.lower()
		result = []
		for title in self.Titles:
			field_value1 = title.title.lower()
			field_value2 = title.short_name.lower()
			if fltr_txt == field_value1[:len(fltr_txt)] or fltr_txt == field_value2[:len(fltr_txt)]:
				result.append(title)
				if len(result)==limit:
					break
		return result
	def isexists(self,title):
		for tit in self.Titles:
			if tit.title == title.title:
				return True
		return False

	def get_by_uid(self, uuid):
		for title in self.Titles:
			if title.uid == uuid:
				return title

		return Title(uid=uuid)

class Artists:
	def __init__(self, *args):
		self.artists = list(args)

	def new(self, *arg):
		return Artist()
	def Remove(self, oldartist):
		idx = 0
		delidx = None 
		for artist in self.artists:
			if artist == oldartist:
				delidx = idx 
				break 
			idx += 1
		if delidx is not None:
			del self.artists[delidx]

	def Add(self, *args):
		for newartist in args:
			self.artists.append(newartist)

		# To Delete Unknown artist already set.
		self.check_and_remove_unknown()

	def check_exists(self, newartist):
		for artist in self.artists:
			if artist == newartist:
				return True 

		return False

	def __repr__(self):
		if len(self.artists)>0:
			return "%s"%self.artists[0]
		return ""
		
	def All(self):
		return self.artists

	def length(self):
		return len(self.artists)


	def get_by_oldid(self,oldid):
		for artist in self.artists:
			if oldid == artist.old_id:
				return artist
		return None

	def get_by_uid(self, uuid):
		for artist in self.artists:
			if artist.uid == uuid:
				return artist

		return Artist(uid=uuid)

	def sort(self):
		tmpdict 	= {}
		tmpartists = []
		for artist in self.artists:
			tmpdict[artist.short_name.lower()+artist.uid.lower()] = artist

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			tmpartists.append(tmpdict[key])
		self.artists = tmpartists

	def SearchByName(self, fltr_txt):
		fltr_txt = fltr_txt.lower()
		fltr_list = fltr_txt.split("+")
		result = []
		for artist in self.artists:
			field_value1 = artist.name.lower()
			field_value2 = artist.short_name.lower()
			for fltr_txt in fltr_list:
				if fltr_txt == field_value1[:len(fltr_txt)] or fltr_txt == field_value2[:len(fltr_txt)]:
					result.append(artist)
		return list(set(result))

	def get_all_artists_string(self):
		all_artists_string = " | ".join(artist.name for artist in self.artists)
		return all_artists_string

	# To Delete unknown artist
	def check_and_remove_unknown(self, *arg):
		if len(self.artists) > 1:
			idx = 0
			delidx = None
			for artist in self.artists:
				if artist.name == UNKNOWN:
					delidx 	= idx
					break
				idx += 1
			if delidx is not None:
				del self.artists[delidx]
	# Checking existing for new or edit artist
	def isexists(self,newartist,editmode=False):
		for artist in self.artists:
			if artist.uid != newartist.uid and artist.name == newartist.name :
				return True
		return False

		
class Albums:
	def __init__(self, *args):
		self.albums = list(args)
		
	def Add(self, *args):
		for album in args:
			self.albums.append(album)

	def __repr__(self):
		if len(self.albums)>0:
			return "%s"%self.albums[0].albumname
		return ""

		
	def All(self):
		return self.albums

	def length(self):
		return len(self.albums)

	def get_by_oldid(self,oldid):
		for album in self.albums:
			if oldid == album.old_id:
				return album
		return None

	def sort(self):
		tmpdict 	= {}
		tmpalbums = []
		for album in self.albums:
			tmpdict[album.short_albumname.lower()+album.uid.lower()] = album

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			tmpalbums.append(tmpdict[key])
		self.albums = tmpalbums

	def SearchByName(self, fltr_txt,limit=200):
		fltr_txt = fltr_txt.lower()
		result = []
		for album in self.albums:
			field_value1 = album.albumname.lower()
			field_value2 = album.short_albumname.lower()
			if fltr_txt == field_value1[:len(fltr_txt)] or fltr_txt == field_value2[:len(fltr_txt)]:
				result.append(album)
				if len(result)==limit:
					break
		return result

	def isexists(self,album):
		for alb in self.albums:
			if alb.uid != album.uid and alb.albumname == album.albumname :
				return True
		return False

	def get_by_uid(self, uuid):
		for album in self.albums:
			if album.uid == uuid:
				return album

		return Album(uid=uuid)


class Categories:
	def __init__(self, *args):
		self.categories = list(args)

	def new(self, *arg):
		return Category()
	def Remove(self, odlcategory):
		idx = 0
		delidx = None 
		for category in self.categories:
			if category == odlcategory:
				delidx = idx 
				break 
			idx += 1
		if delidx is not None:
			del self.categories[delidx]
		
	def Add(self, *args):
		for category in args:
			self.categories.append(category)
		# To Delete Unknown artist already set.
		self.check_and_remove_unknown()


	def check_exists(self, newcategory):
		for category in self.categories:
			if category == newcategory:
				return True 

		return False

	def __repr__(self):
		if len(self.categories)>0:
			return "%s"%self.categories[0].categoryname
		return ""
		
	def All(self):
		return self.categories

	def length(self):
		return len(self.categories)

	def get_by_oldid(self,oldid):
		for category in self.categories:
			if oldid == category.old_id:
				return category
		return None

	def get_by_uid(self, uuid):
		for category in self.categories:
			if category.uid == uuid:
				return category

		return Category(uid=uuid)

	def sort(self):
		tmpdict 	= {}
		tmpcategories = []
		for category in self.categories:
			tmpdict[category.short_categoryname.lower()+category.uid.lower()] = category

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			tmpcategories.append(tmpdict[key])
		self.categories = tmpcategories

	def SearchByName(self, fltr_txt,limit=200):
		fltr_txt = fltr_txt.lower()
		result = []
		for category in self.categories:
			field_value1 = category.categoryname.lower()
			field_value2 = category.short_categoryname.lower()
			if fltr_txt == field_value1[:len(fltr_txt)] or fltr_txt == field_value2[:len(fltr_txt)]:
				result.append(category)
				if len(result)==limit:
					break
		return result
	def isexists(self,category):
		for cat in self.categories:
			if cat.categoryname == category.categoryname:
				return True
		return False

	def get_all_categories_string(self):
		all_categories_string = " | ".join(category.categoryname for category in self.categories)
		return all_categories_string

	# To Delete unknown artist
	def check_and_remove_unknown(self, *arg):
		if len(self.categories) > 1:
			idx = 0
			delidx = None
			for category in self.categories:
				if category.categoryname == UNKNOWN:
					delidx 	= idx
					break
				idx += 1
			if delidx is not None:
				del self.categories[delidx]



class MediaFile:
	"""	
	There is a MediaFile Class.
	"""
	def __init__(self, filepath,duration=None):
		self.uid 		= None
		self.filepath 	= filepath
		self.duration 	= duration
		self.active 	= True

	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]
		return None
	def get(self, attr):
		return getattr(self,attr)
	def __str__(self):
		return self.Title
	def __repr__(self):
		return self.Title
	def get_uid(self):
		return self.uid

	def newTitle(self):
		return Title(UNKNOWN)

	def newAlbum(self):
		return Album()
	
	def check_title_exists(self,newtitle):
		if self.Title == newtitle:
			return True
		else:
			return False

	def check_album_exists(self,newalbum):
		if self.Album == newalbum:
			return True
		else:
			return False

class MediaFiles:
	def __init__(self, *args):
		self.mediafiles = list(args)
		self.searchbytitles 	= {}
		self.sortedtitles 		= []
		self.searchbyartists 	= {}
		self.sortedartists 		= []
		self.searchbyalbums		= {}
		self.sortedalbums 		= []
		self.searchbycategories	= {}
		self.sortedcategories	= []
	def Add(self, *args):
		for mediafile in args:
			self.mediafiles.append(mediafile)

	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]
		return None
	def get(self, attr):
		return getattr(self,attr)

	def Newuid(self):
		return newid()

	def __repr__(self):
		# if len(self.mediafiles)>0:
		# 	return "%s"%self.mediafiles[0]
		# return ""
		return self.mediafiles

	def sort_founded_title(self):
		tmpdict 			= {}
		sortedtitles  		= []
		for title in self.searchbytitles.keys():
			tmpdict[title.title.lower()] = title

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			sortedtitle_key = tmpdict[key]
			sortedtitles.append((sortedtitle_key,self.searchbytitles[sortedtitle_key]))
			
		self.sortedtitles = sortedtitles

	def sort_founded_artist(self):
		tmpdict 			= {}
		sortedartists  		= []
		for artist in self.searchbyartists.keys():
			tmpdict[artist.name.lower()] = artist

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			sortedartist_key = tmpdict[key]
			sortedartists.append((sortedartist_key,self.searchbyartists[sortedartist_key]))
			
		self.sortedartists = sortedartists

	def sort_founded_album(self):
		tmpdict 			= {}
		sortedalbums  		= []
		for album in self.searchbyalbums.keys():
			tmpdict[album.albumname.lower()] = album

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			sortedalbum_key = tmpdict[key]
			sortedalbums.append((sortedalbum_key,self.searchbyalbums[sortedalbum_key]))
			
		self.sortedalbums = sortedalbums

	def sort_founded_category(self):
		tmpdict 			= {}
		tmpsortedcategory	= {}
		sortedcategories	= []
		for category in self.searchbycategories.keys():
			tmpdict[category.categoryname.lower()] = category

		tmplist = list(tmpdict.keys())
		tmplist.sort()
		for key in tmplist:
			sortedcategory_key = tmpdict[key]
			sortedcategories.append((sortedcategory_key,self.searchbycategories[sortedcategory_key]))
			
		self.sortedcategories = sortedcategories

	
	def All(self):
		return self.mediafiles

	def length(self):
		return len(self.mediafiles)

	def delete_by_uid(self, uid):
		idx = 0
		for mediafile in self.mediafiles:
			if mediafile.uid == uid:
				del self.mediafiles[idx]
				break
			idx += 1

	# For Songs by Atrist's list
	def get_by_indexid(self,idx):
		result = []
		for mediafile in self.mediafiles:
			if mediafile.indexid == idx:
				result.append(mediafile)
		return result

	# Getting by row index
	def GetByIndex(self, idx):
		return self.mediafiles[idx]

	def SearchByTitle(self, fltr_txt):
		idx = 0
		result = []
		for mediafile in self.mediafiles:
			fname		= mediafile.filename.lower()
			field_value1 = mediafile.Title.title
			field_value2 = mediafile.Title.short_name
			if fltr_txt == field_value1[:len(fltr_txt)] or fltr_txt == field_value2[:len(fltr_txt)] or fltr_txt.lower() == fname[:len(fltr_txt)]:
				result.append(mediafile)
		return result
	def SearchByTitleForExported(self, fltr_txt):
		result = []
		for mediafile in self.mediafiles:
			if mediafile.exported:
				field_value1 = mediafile.Title.title
				field_value2 = mediafile.Title.short_name
				if fltr_txt == field_value1[:len(fltr_txt)] or fltr_txt == field_value2[:len(fltr_txt)]:
					result.append(mediafile)
				
		return result

	def get_All_by_ArtistUid(self, fltr_txt):
		idx = 0
		result = []
		for artist in self.searchbyartists:
			if fltr_txt == artist.uid :
				# List of mediafile index_id
				for mediafile in self.searchbyartists[artist]:
					result.append(mediafile)
		return result

	def get_All_by_AlbumUid(self, fltr_txt):
		idx = 0
		result = []
		for album in self.searchbyalbums:
			if fltr_txt == album.uid :
				# List of mediafile index_id
				for mediafile in self.searchbyalbums[album]:
					result.append(mediafile)
		return result

	def get_All_by_CategoryUid(self, fltr_txt):
		idx = 0
		result = []
		for category in self.searchbycategories:
			if fltr_txt == category.uid :
				# List of mediafile index_id
				for mediafile in self.searchbycategories[category]:
					result.append(mediafile)
		return result

	def SearchByFilename(self,fltr_txt):
		result = []
		for mediafile in self.mediafiles:
			field_value = mediafile.get("filename")
			if fltr_txt == field_value[:len(fltr_txt)]:
				result.append(mediafile)
		return result
	def get_bypath(self, path):
		for mediafile in self.mediafiles:
			print(path, mediafile.filepath)
			if path == mediafile.filepath :
				print("founded")
				return mediafile

	def create_counted_title(self,*arg):
		# set same unknown title
		unknown_title = Title(UNKNOWN)
		self.searchbytitles = {}
		tmpsearchbytitles = {}
		for mediafile in self.mediafiles:
			if UNKNOWN == mediafile.Title.title:
				self.set_key_value(tmpsearchbytitles,unknown_title,mediafile)
			else:
				self.set_key_value(tmpsearchbytitles,mediafile.Title,mediafile)

		for key in tmpsearchbytitles.keys():	
			if len(tmpsearchbytitles[key])> 1:
				self.searchbytitles[key] = tmpsearchbytitles[key]


	def create_counted_artist(self,*arg):
		# set same unknown artist
		unknown_artist = Artist()
		self.searchbyartists = {}
		for mediafile in self.mediafiles:
			for artist in mediafile.Artists.All():
				if UNKNOWN == artist.name:
					self.set_key_value(self.searchbyartists,unknown_artist,mediafile)
				else:
					self.set_key_value(self.searchbyartists,artist,mediafile)	

	def create_counted_album(self,*arg):
		# set same unknown category
		unknown_album = Album()
		self.searchbyalbums = {}
		for mediafile in self.mediafiles:
			if UNKNOWN == mediafile.Album.albumname:
				self.set_key_value(self.searchbyalbums,unknown_album,mediafile)
			else:
				self.set_key_value(self.searchbyalbums,mediafile.Album,mediafile)	


	def create_counted_category(self,*arg):
		# set same unknown category
		unknown_category = Category()
		self.searchbycategories = {}
		for mediafile in self.mediafiles:
			for category in mediafile.Categories.All():
				if UNKNOWN == category.categoryname:
					self.set_key_value(self.searchbycategories,unknown_category,mediafile)
				else:
					self.set_key_value(self.searchbycategories,category,mediafile)	


	def set_key_value(self,data, key, value):
		try:
			data[key] += [value]
		except KeyError:
			data[key] = [value]
		return True

