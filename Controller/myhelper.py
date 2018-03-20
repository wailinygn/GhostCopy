# -*- coding: UTF-8 -*-

# import pickle
# import os
# import time
# import sys
# sys.path.append('./Resources')
# from resources import *

# import uuid
#web access signals



# from properties import *
MMENG_map= [u'က', u'ခ', u'ဂ', u'ဃ', u'င',
        u'စ', u'ဆ', u'ဇ', u'ဈ', u'ည',
        u'ဋ', u'ဌ', u'ဍ', u'ဎ', u'ဏ',
        u'တ', u'ထ', u'ဒ', u'ဓ', u'န',
        u'ပ', u'ဖ', u'ဗ', u'ဘ', u'မ',
        u'ယ', u'ရ', u'လ', u'ဝ', u'သ',
        u'ဟ', u'ဠ', u'အ', u'၏', u'ဤ',
        u'ဥ', u'၌', u'ဉ', u'ဧ', u'ဩ', 
        u'\u1090',u'၍',u'ဣ',
        u'a', u'b', u'c', u'd', u'e',
        u'f', u'g', u'h', u'i', u'j',
        u'k', u'l', u'm', u'n', u'o',
        u'p', u'q', u'r', u's', u't',
        u'u', u'v', u'w', u'x', u'y',
        u'z',
        u'1', u'2', u'3', u'4', u'5',
        u'6', u'7', u'8', u'9', u'0',
        u'၁', u'၂', u'၃', u'၄', u'၅',
        u'၆', u'၇', u'၈', u'၉', u'၀',] 
        
find_map = [u'\u1039',u'\u1060', u'\u1062', u'\u1063', u'\u1067', u'\u1068', u'\u1069', 
            u'\u106C', u'\u106D', u'\u1071', u'\u1072', u'\u1073', u'\u1074', u'\u1085']

FILE_TYPE 			= ['.avi','.mpg','.mp4', '.dat','.flv','.mkv','.vob','.divx']


class Helper:
	def __init__(self):
		pass

	def OpenFile(self,dbfile):
		if os.path.isfile(dbfile):
			rfile = open(dbfile, "rb")
			data = pickle.load(rfile)
			rfile.close()
			return data
		return None

	def set_uuid(self,db):
		rdb = []
		for idx in db:
			uid = str(uuid.uuid4())
			old_id = idx
			rdb.append([uid,db[idx][0],db[idx][1],old_id])

		return rdb

	def SavetoFile(self, filename, data):
		rdb = []
		for idx in db:
			uid = str(uuid.uuid4())
			old_id = idx
			rdb.append([uid,db[idx][0],db[idx][1],old_id])

		return rdb

		wfile = open(filename, 'wb')
		pickle.dump(data,wfile)
		wfile.close()
		# pass
	def chkExistData(self, datatbl, txt):
		for data in datatbl.values():
			if txt in data[0]:
				return True

	
	def FindDuplicatedFiles(self, maindb):
		finddb = {}
		cpymaindb = maindb.copy()
		for vcd in maindb:
			title = maindb[vcd][TITLE][0]
			if vcd in cpymaindb:
				del cpymaindb[vcd]
				# print vcd,'deleted'
			tmp = []
			for vcd2 in cpymaindb:
				title2 = cpymaindb[vcd2][TITLE][0]
				# print 'title1', title, 'title2', title2
				if title== title2:
					tmp.append(vcd2)
			# print 'len tmp>', tmp
			if len(tmp)>1:
				for id in tmp:
					finddb[id] = cpymaindb.pop(id)
			elif len(tmp) == 1:
				cpymaindb.pop(tmp[0])
		cpymaindb = None
		return finddb        
	def FindSupportedFile(self):
		d = {}
		for l in file('/proc/mounts'):
			if l[0] == '/':
				l = l.split()
				d[l[0]] = l[1]
		d['media'] = "/media/PLAN_B"
		return d

	def SplitConsonant(self, txt):
		splited_consonant = ''
		i = 0
		txt_length = len(txt)
		txt = txt.lower()
		for c in txt:
			i += 1
			if c in MMENG_map:
				if i < txt_length:
					if txt[i] != u'\u103a' and txt[i] not in find_map:
						splited_consonant = '%s%s'%(splited_consonant, c)
				elif txt[i-1] != u'\u103a':# and txt[i] not in find_map::
					splited_consonant = '%s%s'%(splited_consonant, c)
		
		return splited_consonant
	

	def hp_find_db_path(self):        
		i = 0
		while not self.found_Media:
			result = self.FindSupportedFile()
			if len(result) > 0 :
				for key in result:
					if result[key] != '/':
						#findfile = result[key].replace("\\040", ' ')
						findfile = result[key] 
						findfile_pb = '%s/PLAN_B'%result[key]
						# print key,'key',  findfile
						if os.path.exists('%s/.mdb'%result[key]):
							self.path = result[key]
							self.found_Media = True
							break
						elif os.path.exists('%s/.mdb'%findfile_pb):
							self.path = findfile_pb
							self.found_Media = True
							break
			i += 1
			# print 'Searching media... %i times'%i
			time.sleep(2)
		self.On_LoadData()



def SavetoFile(filename, data):
	rdb = []
	for idx in db:
		uid = str(uuid.uuid4())
		old_id = idx
		rdb.append([uid,db[idx][0],db[idx][1],old_id])

	return rdb

	wfile = open(filename, 'wb')
	pickle.dump(data,wfile)
	wfile.close()

def SplitConsonant(txt):
	splited_consonant = ''
	i = 0
	txt_length = len(txt)
	txt = txt.lower()
	for c in txt:
		i += 1
		if c in MMENG_map:
			if i < txt_length:
				if txt[i] != u'\u103a' and txt[i] not in find_map:
					splited_consonant = '%s%s'%(splited_consonant, c)
			elif txt[i-1] != u'\u103a':# and txt[i] not in find_map::
				splited_consonant = '%s%s'%(splited_consonant, c)
	
	return splited_consonant