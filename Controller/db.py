# -*- coding: utf-8 -*-

import os
import pickle, json
from data.models import *
from config import *


class DB:
	def __init__(self):
		self.dbpath 	= "%s/data/DB"%BASE_DIR
		self.TITLES_LIST 	= self.get_titles()
		self.ARTISTS_LIST 	= self.get_artists()
		self.ALBUMS_LIST  	= self.get_albums()
		self.CATEGORIES_LIST 	= self.get_categories()
		self.MEDIA_LIBRARY = {}
		# print("db",self.ARTISTS_LIST.All()[0].albumname)
	def get_titles(self):
		data = self.OpenFile("%s/DBTITLE"%self.dbpath)
		titles = Titles()
		for row in data:
			title = Title(uid=row[0],title=row[1],short_name=row[2])
			if not titles.isexists(title):
				titles.Add(title)
		titles.sort()
		return titles
	def get_artists(self):
		data = self.OpenFile("%s/DBARTIST"%self.dbpath)
		artists = Artists()
		for row in data:
			artist = Artist(uid=row[0],name=row[1])
			artist.short_name 	= row[2]
			artist.gender 	 	= row[3]
			artist.photo 	 	= row[4]
			artists.Add(artist)
		artists.sort()

		return artists

	def get_albums(self):
		data = self.OpenFile("%s/DBALBUM"%self.dbpath)
		albums = Albums()
		for row in data:
			album = Album(uid=row[0],albumname=row[1])
			album.short_albumname 	= row[2]
			albums.Add(album)

		albums.sort()
		return albums

	def get_categories(self):
		data = self.OpenFile("%s/DBCATEGORY"%self.dbpath)
		categories = Categories()
		for row in data:
			category = Category(uid=row[0],categoryname=row[1])
			category.short_categoryname 	= row[2]
			categories.Add(category)
		categories.sort()
		return categories

	def get_AllFileInDirectory(self, rootDir):
		fileSet = []
		for dir_, _, files in os.walk(rootDir):
			for fileName in files:
				relDir = os.path.relpath(dir_, rootDir)
				if relDir == '.':
					relDir = ''
				relFile = os.path.join(relDir, fileName)
				fileSet.append({'parent':relDir,'filename':fileName, 'relFile':relFile})
		return fileSet

	def get_AllFileInDirectory2(self,path):
		allfile = []
		try:
			allfile = [ {'parent':path, 'filename':f} if os.path.isfile(path+f) else self.get_AllFileInDirectory(path+f) for f in os.listdir(path)]
		except:
			pass
		finally:
			print(allfile)
			return allfile

	#----  BACKUP  ----#
	# def get_AllFileInDirectory(self,path):
	# 	allfile = []
	# 	try:
	# 		allfile = [ f for f in os.listdir(path) if os.path.isfile(path+f)]
	# 	except:
	# 		pass
	# 	finally:
	# 		return allfile

	def set_uuid(self,db):
		rdb = {}
		for idx in db:
			uid = str(uuid.uuid4())
			old_id = idx
			rdb[idx] = [uid,db[idx][0],db[idx][1],old_id]
		return rdb
	
	def OpenFile(self,dbfile):
		data = {}
		if os.path.isfile(dbfile):
			try:
				rfile = open(dbfile, "rb")
				data = pickle.load(rfile)
			except:
				print("File sources reading error...")
			finally:
				rfile.close()
				return data
		return data

	def DB_Save(self, moviefiles):
		if moviefiles:
			save_DB 	= {}
			moviesdb 	= {}
			# (
			#	filename,
			# 	titleuuid,
			# 	albumuuid,
			# 	[artistuuid,artistuuid],
			# 	[categoryuid,categoryuid]
			# )
			for moviefile in moviefiles.All():
				tmpartists 		= []
				tmpcategories 	= []

				filename 	= moviefile.filename
				titleuid 	= moviefile.Title.uid
				albumuid 	= moviefile.Album.uid
				for artist in moviefile.Artists.All():
					tmpartists.append(artist.uid)

				for category in moviefile.Categories.All():
					tmpcategories.append(category.uid)

				moviesdb[filename] = (titleuid,albumuid,tmpartists,tmpcategories)

			save_DB["tblmovies"] = moviesdb
			self.SavetoFile(moviefiles.savefilepath,save_DB)
			return True

	def exportDBtomyplayer(self, moviefiles):
		if moviefiles:
			save_DB 	= {}
			moviesdb 	= {}

			for moviefile in moviefiles.All():
				tmpartists 		= []
				tmpcategories 	= []

				if moviefile.Title.title.lower() == "unknown":
					continue
				relName		= moviefile.relName
				filename 	= moviefile.filename
				title_name 	= moviefile.Title.title
				title_shortname = moviefile.Title.short_name
				title = {
					'title_name': title_name,
					'title_shortname': title_shortname,
				}

				albumname 	= moviefile.Album.albumname
				albumshortname = moviefile.Album.short_albumname

				album ={
					'album_name':albumname,
					'album_shortname':albumshortname
				}

				for artist in moviefile.Artists.All():
					new_artist = {
						'artist_name':artist.name,
						'artist_shortname': artist.short_name,
						'gender': artist.gender,
						'photo': artist.photo
					}
					tmpartists.append(new_artist)

				for category in moviefile.Categories.All():
					new_cat = {
						'category_name': category.categoryname,
						'category_shortname': category.short_categoryname,
					}
					tmpcategories.append(new_cat)

				moviesdb[filename] = {
										'relname':relName,
									  'title':title,
										'album':album,
										'artists':tmpartists,
										'categories':tmpcategories
				}

			save_DB["myplayerdb"] = moviesdb
			print(moviefiles.savefilepath, save_DB)
			self.SavetoExportFile(moviefiles.exportfilepath,save_DB)
			return True

	def SavetoFile(self, filename, data):
		print(data)
		wfile = open(filename, 'wb')
		pickle.dump(data,wfile,pickle.HIGHEST_PROTOCOL)
		wfile.close()

	def SavetoExportFile(self, filename, data):
		print(data)
		wfile = open(filename, 'w')
		jsonfile = json.dumps(data)
		wfile.write(jsonfile)
		wfile.close()

	def open_dbfile(self,dbfile=None,path=None):
		self.MAINDB = {}
		self.opendirpath 	= "%s/"%path
		self.exportfile		= "%s/mp.db"%path
		self.DBFILE 		= "%s/%s"%(path,dbfile)
		print("dbfile>",self.DBFILE)
		MEDIA_LIBRARY = MediaFiles()
		if os.path.isfile(self.DBFILE):
			self.MAINDB = self.OpenFile(self.DBFILE)
		
			if "tblmovies" not in self.MAINDB:
				self.MAINDB['tblmovies'] = {}
			LOCAL_DB 	= self.MAINDB['tblmovies']
			#Getting existing files [{parent:parentparth,filename:moviefilename},{}
			AllFileInLib = self.get_AllFileInDirectory(self.opendirpath)


			# Create Media Library Class

			MEDIA_LIBRARY.searchbytitles 		= {}
			MEDIA_LIBRARY.searchbyartists 		= {}
			MEDIA_LIBRARY.searchbyalbums 		= {}
			MEDIA_LIBRARY.searchbycategories	= {}
			MEDIA_LIBRARY.savefilepath 			= self.DBFILE
			MEDIA_LIBRARY.exportfilepath		= self.exportfile
			index_id = 0 # for index no. 
			for mediafile in AllFileInLib:
				fname = mediafile['filename']
				parent = mediafile['parent']
				relFile = mediafile['relFile']


				idx = len(fname) - fname.rfind('.')
				filetype = fname[-idx:].lower()
				if filetype in FILE_TYPE:
					media_file = MediaFile(self.opendirpath+relFile) # create / set filename
					media_file.indexid 	= index_id # Set the No. For idx Artist songs
					media_file.uid 		= newid()
					media_file.parent	= parent
					media_file.relName	= relFile
					media_file.filename = fname
					media_file.size 	= os.path.getsize(media_file.filepath)		
					media_file.duration = 0 # call get_duration()
					media_file.filetype = filetype
					media_file.active 	= True
					media_file.exported = False

					
					if fname in LOCAL_DB:
						dbtitle_uid 			= LOCAL_DB[fname][0]
						dbalbum_uid 			= LOCAL_DB[fname][1]
						dbartists_list			= LOCAL_DB[fname][2]
						dbcategories_list		= LOCAL_DB[fname][3]


						media_file.Title 		= self.TITLES_LIST.get_by_uid(dbtitle_uid)
						media_file.Album 		= self.ALBUMS_LIST.get_by_uid(dbalbum_uid)

						#Artist Session
						media_file.Artists = Artists()
						for dbartist_uid in dbartists_list:
							artist = self.ARTISTS_LIST.get_by_uid(dbartist_uid)
							media_file.Artists.Add(artist)
							# self.set_key_value(MEDIA_LIBRARY.searchbyartists,artist,index_id)

						#Category Session
						media_file.Categories = Categories()
						for dbcategory_uid in dbcategories_list:
							category = self.CATEGORIES_LIST.get_by_uid(dbcategory_uid)
							media_file.Categories.Add(category)
							# self.set_key_value(MEDIA_LIBRARY.searchbycategories,category,index_id)


					else:
						media_file.Title 		= Title(UNKNOWN)					
						artist 					= Artist(newid(),UNKNOWN)
						media_file.Artists 		= Artists(artist)
						# self.set_key_value(MEDIA_LIBRARY.searchbyartists,artist,index_id)

						album 					= Album()
						media_file.Album 		= album
						# self.set_key_value(MEDIA_LIBRARY.searchbyalbums,album,index_id)

						category 				= Category(newid(),UNKNOWN)
						media_file.Categories	= Categories(category)
						# self.set_key_value(MEDIA_LIBRARY.searchbycategories,category,index_id)
					MEDIA_LIBRARY.Add(media_file)
					index_id += 1

			MEDIA_LIBRARY.create_counted_artist()
			MEDIA_LIBRARY.create_counted_album()
			MEDIA_LIBRARY.create_counted_category()

			MEDIA_LIBRARY.sort_founded_artist()
			MEDIA_LIBRARY.sort_founded_album()
			MEDIA_LIBRARY.sort_founded_category()


		return MEDIA_LIBRARY


	def set_key_value(self,data, key, value):
		try:
			data[key] += [value]
		except KeyError:
			data[key] = [value]
		return True

	def NewMediafiles(self):
		return MediaFiles()
