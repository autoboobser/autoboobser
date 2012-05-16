#!/usr/bin/env python
# -*- coding: UTF-8

import shutil, os, xml.dom.minidom, binascii, struct, sys, json, codecs, re, shlex, subprocess, ctypes, zipfile, plistlib
from abc import ABCMeta, abstractmethod, abstractproperty

def deleteEmptyDirs(dir):
	files = os.listdir(dir)
	for filename in files:
		path = os.path.join(dir, filename)
		if os.path.isdir(path):
			try:
				os.rmdir(path)
			except OSError:
				#deleteEmptyDirs(path)
				pass
		

def copyDirContents(src, dst, ignore=None):
	names = os.listdir(src)
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()

	try:
		os.makedirs(dst)
	except:
		pass
		
	for name in names:
		if name in ignored_names:
			continue
		#print name
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		
		if os.path.isdir(srcname):
			copyDirContents(srcname, dstname, ignore)
		else:
			try:
				shutil.copy(srcname, dstname)
			except:
				pass

def moveDirContents(src, dst, ignore=None):
	names = os.listdir(src)
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()

	try:
		os.makedirs(dst)
	except:
		pass
	
	for name in names:
		if name in ignored_names:
			continue
		#print name
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			shutil.move(srcname, dstname)
		except:
			pass

def readFilesInString(files, delimeter):
	file_contents = []
	for file in files:
		fin = codecs.open(file, 'r', 'utf-8-sig')
		file_contents.append(fin.read())
		fin.close()
	return delimeter.join(file_contents)
	
def deleteFiles(fileList):
	for file in fileList:
		os.remove(file)

def readJSON(filename):
	f = open(filename, 'rt')
	jsonObj = json.loads(f.read())
	f.close()
	return jsonObj
	
def writeJSON(filename, jsonObj):
	f = open(filename, 'wt')
	f.write(json.dumps(jsonObj, skipkeys=True, indent=2))
	f.close()
	
def getPrefixFromName(name):
	return filter(lambda x: x.isalpha(), name)
	
def getExtensionPackageName(info):
	return (getPrefixFromName(info.name) + '_' + info.version).lower()

class ZipDirectoryArchiver(object):

	def _makeArchive(self, zip, arcname, src):
		files = os.listdir(src)
		for filename in files:
			path = os.path.join(src, filename)
			name = os.path.join(arcname, filename)
			if os.path.isdir(path):
				self._makeArchive(zip, name, path)
			else:
				zip.write(path, name)
	
	def makeArchive(self, dst, src):
		zip = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
		self._makeArchive(zip, '', src)
		zip.close()

class ExtensionBuilder(object):
	__metaclass__ = ABCMeta
	
	key = ''

	@abstractmethod
	def build(self, outDir):
		pass
	
	@abstractmethod	
	def pack(self, dst, src):
		pass

class ChromeExtensionBuilder(ExtensionBuilder):
	
	key = 'chrome'
	
	_manifestFileName = 'manifest.json'
		
	bckgrPageName = 'background.html'
	scriptContainerTagName = 'head'
	
	def __init__(self, info):
		return
	
	def get_chrome_path(self):
		path = ''
		try:
			import ctypes.wintypes
			CSIDL_LOCAL_APPDATA = 0x001c
			_SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathW
			_SHGetFolderPath.argtypes = [ctypes.wintypes.HWND, ctypes.c_int,
										ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD,
										ctypes.wintypes.LPCWSTR]
			path_buf = ctypes.wintypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
			result = _SHGetFolderPath(0, CSIDL_LOCAL_APPDATA, 0, 0, path_buf)
			path = os.path.join(path_buf.value, 'Google', 'Chrome', 'Application', 'chrome.exe')
		except:
			pass
		return path	

	def build(self):
		print "Building chrome..."
		self.pack()
		
	def pack(self):
		chrome_path = self.get_chrome_path()
		if(chrome_path != ''):
			src = os.path.join(sys.path[0], "tmp")
			out = os.path.join(sys.path[0], "output\\chrome.crx")
			extension_path = os.path.abspath(src)
			certificate_path = os.path.join(sys.path[0], "certificates/chrome.pem")
			
			cmd = chrome_path + ' --pack-extension="' + extension_path + '" '
			if os.path.isfile(certificate_path):
				cmd += '--pack-extension-key="' + certificate_path + '"'
			cmd += ' --no-message-box'
			os.system(cmd)
			try:
				crxFile = sys.path[0] + '\\tmp.crx'
				if os.path.exists(out):
					os.remove(out)
					
				shutil.move(crxFile, out )
				print 'Done.'
			except:
				print 'Can\'t move extension to dest folder.'
				pass
			
		else:
			print 'Chrome is not installed, can\'t pack chrome extension.'
			
def main():
	__title__ = 'Browser extension builder'
	__version__ = '0.1'

	print __title__, 'version', __version__, '\n'
	
	#Build chrome extension	
	cBuilder = ChromeExtensionBuilder(ChromeExtensionBuilder)
	cBuilder.build()
	

if __name__ == '__main__':
    main()