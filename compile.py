#!/usr/bin/python
#coding:utf-8
#python2.6

import json, sys, re, os, shutil, platform, commands, time, getopt

# 获取svn版本的正则
revFieldP = re.compile('Last Changed Rev\:\s*(\d+)\s*')
# 获取js中key的正则
jsKeyP = re.compile('([^"\s]\S+[^"])\s*:')
# 获取修改日期的正则
dateFieldP = re.compile('Last Changed Date\:\s*(.+)\n*')

# 子文件类型 (文件内容中含有下列子文件类型，需要级联更新版本)
subtypes = {
	'image' : re.compile('url\((.*)\)'),
	'css' : re.compile('\<link.*rel=\"stylesheet\".*href=\"(.*)\".*\/\>'),
	'js' : re.compile('\<script.*type=\"text\/javascript\".*src=\"(.*)\".*\>\<\/script\>'),
	'json' : re.compile('[^"\s]\S+[^"]\s*:\s*\'(.*)\'')
}

# 支持的标记
marks = {}
# 自定义标记
cmarks = {}

# 临时文件列表
tmpfiles = []

# 配置文件json对象
jsonConfig = {}

# 默认白名单
allowext = []
# 平文本类型扩展名
plaintext = []
# 输出的文件target会相对于此目录，每次生成均会先删除此文件夹
relpath = ''
# 编译规则
rules = {}
# 编译模式
modes = {}
# js压缩工具, css压缩工具
tools = {
	'googleclosurePath' : './tools/compiler.jar',
	'yuicompiressorPath' : './tools/yuicompressor-2.4.6.jar'
}

# 默认配置文件
defaultConfig = './config.json'


class Compile(object):
	def __init__(self, rule, name):
		print 'Complie ', name, 60*'+'
		self.markreplace = rule.get('markreplace', 0)
		self.target = rule['target'] if not self.markreplace else self.replace(name, rule['target'])
		self.source = rule['source']
		self.version = rule.get('version')
		self.subversion = rule.get('subversion')
		self.subtype = rule.get('subtype')
		self.ifcompress = rule.get('compress', 1) if rule.get('compress') else ifCompress
		self.name = name
		self.compressfiles = []

		# 默认值处理
		# if not self.subtype:
		# 	self.subversion = False
		# else:
		# 	self.subreg = [v for k, v in subtypes.items()]
		if not self.subtype:
			self.subreg = [v for k, v in subtypes.items()]
			
		# 文件夹的basename为空
		self.sourcename = os.path.basename(self.source)
		if not self.sourcename:
			# 文件夹 扩展名为空
			self.ext = None
		else:
			self.ext = os.path.splitext(self.sourcename)[1][1:]
		
		
		# 合并规则qzmin
		if self.ext == 'qzmin':
			self.loadQzmin()
		# 文件夹规则			
		elif self.ext is None:
			self.recursive = rule.get('recursive')
			self.allowext = rule.get('ext')
			self.blacklist = rule.get('blacklist')
			self.whitelist = rule.get('whitelist')
			if not self.allowext:
				self.allowext = allowext
			self.moveFiles()
		# 文件规则
		else:
			self.moveFile(self.source, self.target)
			
		self.compressor(self.compressfiles)
		
	def loadQzmin(self, format=True):
		print 'load qzmin start', self.name
		f = open(self.source)
		ll = [];
		for l in f.xreadlines():
			if format:
				ll.append(js2json(l))
			else:
				ll.append(l)
		print 'load qzmin finish', self.name
		self.combine(json.loads("".join(ll)))
		
	def combine(self, j):
		print 'combine start', self.name
		projects = j["projects"]
		results = []
		for p in projects:
			target = p["target"]
			files =  p["include"]
			spath = self.source
			tpath = self.target
			ver = 0
			t = []
			combineContent = []
			for f in files:
				fileName = os.path.basename(f)
				filepath = os.path.join(os.path.dirname(self.source), f)
				fileVer = self.getFileVer(filepath)
				#if self.version and fileVer > ver:
				if fileVer > ver:
					ver = fileVer
				for line in open(filepath).xreadlines():
					t.append(line);
				t.append('\r\n');
				combineContent.append("".join(t))
				del t[:]
			results.append("".join(combineContent))
			print 'combine finish', self.name
		
			if not self.version:
				pass
			else:
				selfver = self.getFileVer(spath)
				ver = '%s-%s' % (selfver, ver)
				self.createTmpVerFile(tpath, ver)
				tpath = self.getVersionName(spath, tpath, ver)
			self.createFile(tpath, results)
			
	def moveFiles(self):
		if not self.recursive:
			for f in os.listdir(self.source):
				ext = os.path.splitext(f)[1][1:]
				if not self.allowext or self.allowext and ext in self.allowext:
					sourcefile = os.path.join(self.source, f)
					if os.path.isfile(sourcefile):
						self.moveFile(sourcefile, os.path.join(self.target, f))
		else:
			for root, dirs, files in os.walk(self.source, True):
				for f in files:
					ext = os.path.splitext(f)[1][1:]
					if not self.allowext or self.allowext and ext in self.allowext:
						spath = os.path.join(root, f)
						tpath = os.path.join(self.target, os.path.relpath(root, self.source), f)
						self.moveFile(spath, tpath)
		
	def moveFile(self, spath, tpath):
		# 文件夹规则
		if self.ext is None:
			# 白名单
			if not self.whitelist or self.whitelist and os.path.basename(spath) in self.whitelist:
				pass
			else:
				return
			
			# 黑名单
			if self.blacklist and os.path.basename(spath) in self.blacklist:
				return
		
		# 需要更新版本号 并且 需要更新文件内容自版本
		# 非平文本文件忽略subversion
		ext = os.path.splitext(tpath)[1][1:]
		if ext not in plaintext:
			self.subversion = False
		
		if self.version and self.subversion:
			self.createSubRevFile(spath, tpath, self.subreg, True)
		elif not self.version and self.subversion:
			self.createSubRevFile(spath, tpath, self.subreg, False)
		elif self.version and not self.subversion:
			tpath = self.getVersionName(spath, tpath)
			self.doMoveFile(spath, tpath)
		elif not self.version and not self.subversion:
			self.doMoveFile(spath, tpath)
		
	def doMoveFile(self, source, target):
		ext = os.path.splitext(target)[1][1:]
		if ext not in plaintext or not self.markreplace:
			print 'copyfile %s to %s ' % (source, target)
			mkdir(target)
			shutil.copy(source, target)
			self.compressfiles.append(target)
		else:
			self.createFile(target, open(source).xreadlines())

	
	def replace(self, target, output):
		print 'replace', target
		for m in marks:
			print 'replace', m, marks.get(m)
			output = output.replace(m, marks.get(m))
		return output
		print 'replace finish', target	
		
	def getVersionName(self, spath, tpath, ver = ''):
		filename = os.path.splitext(tpath)[0]
		ext = os.path.splitext(tpath)[1]
		if ver != '':
			pass
		else:
			if "Windows" not in platform.platform():
				ver = self.getFileVer(spath)
			else:
				ver = time.strftime("%Y-%m-%d",time.localtime())
		return '%s.%s%s' % (filename, ver, ext)
	
	def getFileVer(self, path):
		ver = self.getVerFromTmpFile(path)
		if ver is None:
			output = commands.getoutput("svn info %s" % path)
			ver = revFieldP.search(output)
			if ver:
				ver = ver.group(1)
			else:
				ver = ''
		return ver
		
	def getVerFromTmpFile(self, path):
		tpath = self.getTmpVerFileName(path)
		t = []
		if os.path.exists(tpath):
			for line in open(tpath).xreadlines():
				t.append(line);
			return "".join(t)
		else:
			return None
		
	def createFile(self, tpath, contents):
		mkdir(tpath)
		print "Create File", tpath
		if self.markreplace:
			output = self.replace(tpath, "".join([l for l in contents]))
		else:
			output = "".join([l for l in contents])
		open(tpath, "w").write(output)
		self.compressfiles.append(tpath)
		
	def createTmpVerFile(self, tpath, ver):
		tpath = self.getTmpVerFileName(tpath)
		contents = []
		contents.append(str(ver))
		tmpfiles.append(tpath)
		self.createFile(tpath, contents)
	
	def getTmpVerFileName(self, tpath):
		filename = os.path.splitext(tpath)[0]
		tpath = '%s.ver' % (filename)
		return tpath
		
	def createSubRevFile(self, spath, tpath, regs, isVersion):
		contents = []
		selfver = self.getFileVer(spath)
		subver = 0
		for line in open(spath).xreadlines():
			for reg in regs:
				urlline = reg.search(line)
				if urlline:
					break
					
			if urlline:
				#imgurl = urlline.group(1).replace('"', '')
				imgurl = urlline.group(1)
				imgpath = os.path.join(os.path.dirname(spath), imgurl)
				imgver = self.getFileVer(imgpath)
				if imgver > subver:
					subver = imgver
				filename = os.path.splitext(imgurl)[0]
				ext = os.path.splitext(imgurl)[1]
				newname = '%s.%s%s' % (filename, imgver, ext)
				contents.append(line.replace(imgurl, newname))
			else:
				contents.append(line)
		
		if not isVersion:
			pass
		else:
			ver = '%s-%s' % (selfver, subver)
			tpath = self.getVersionName(spath, tpath, ver)
			self.createTmpVerFile(spath, ver)
			
		self.createFile(tpath, contents)
	
	def compressor(self, files):
		print 'compressor start', "-"*40
		if self.ifcompress:
			for f in files:
				filetype = os.path.splitext(f)[1][1:]
				if filetype in ["js", "css"]:
					print 'compressor start', self.name, "-"*40
					if filetype == "js":
						cmd = 'java -jar %s --%s %s --%s_output_file %s.min' % (tools['googleclosurePath'], filetype, f, filetype, f)
					elif filetype == "css":
						cmd = 'java -jar %s %s -o %s.min --charset utf-8' % (tools['yuicompiressorPath'], f, f)
					print cmd
					os.system(cmd)
					t = []
					for line in open(f+".min").xreadlines():
						t.append(line);
					open(f,"w").write("".join(t))
					os.remove(f+".min")
					print 'compressor finish', self.name, "-"*40
		print 'compressor end', "-"*40



def pickMode(modeRules):
	for ruleName in modeRules:
		v = rules[ruleName]
		if v.get("relpath"):
			v['target'] = os.path.join(v['relpath'], v['target'])
		else:
			v['target'] = os.path.join(relpath, v['target'])
		Compile(v, ruleName)
		
def js2json(fileline):
	l = jsKeyP.sub(lambda l:'"%s" : ' % l.group(1), fileline)
	return '"'.join(l.split('\''))
			
def mkdir(path):
	path = os.path.dirname(path)
	if not os.path.exists(path):
		os.makedirs(path)
		print "Create path", path
		
def rmdir(path):
	if os.path.exists(path):
		shutil.rmtree(path)
		print "rmdir dir", path

def cleanup():
	print "CleanUp start", 60 * '-'
	for file in tmpfiles:
		if os.path.exists(file):
			os.remove(file)
			print "removefile path", file
	print "CleanUp end", 60 * '-'
	
def parseConfig():
	print "Parse Config start", 60 * '-'
	global allowext, plaintext, relpath, rules, modes, tools, cmarks
	jsonConfig = json.loads(open(pyConfig).read())
	allowext = jsonConfig.get('allowext')
	plaintext = jsonConfig.get('plaintext')
	relpath = jsonConfig.get('relpath')
	rules = jsonConfig.get('rules')
	modes = jsonConfig.get('modes')
	cmarks = jsonConfig.get('cmarks') if jsonConfig.get('cmarks') else cmarks
	if jsonConfig.get('tools') is None:
		pass
	else:
		tools = jsonConfig.get('tools')
	print "Parse Config end", 60 * '-'

def usage():
	print '''Options and arguments:
help           : Help
noup           : Publish without svn up
nocompress     : Publish without google closure
debug    	   : Complie with Debug Mode Rules
-f             : Config File, default as 'config.json'
--config       : Config File, default as 'config.json'

For example:
	python compile.py -noup -nocompress 
	python compile.py -debug 
		'''	
	sys.exit()

def parseMarks():
	global marks, cmarks
	if "Windows" not in platform.platform():
		output = commands.getoutput("svn info")
		REV = revFieldP.search(output).group(1)
		LASTUPDATE = dateFieldP.search(output).group(1)[:19]
		DATE = time.strftime('%Y-%m-%d %H:%M:%S')
	else:
		REV = DATE = LASTUPDATE = str(time.time())
	marks['%Date%'] = DATE
	marks['%LastUpdate%'] = LASTUPDATE
	marks['%Version%'] = REV
	marks = marks.copy()
	marks.update(cmarks)

	
if __name__ == '__main__':
	print platform.platform()
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:", ["config="])
	except getopt.GetoptError, err:
		print str(err)
		usage()
        
    # 运行参数    
	if len(args) >= 1:
		argS = (" ").join(args)
	else:
		argS = ""
	argS = argS.lower()
	
	if "help" in argS:
		usage()

	if "noup" in argS:
		pass
	else:
		if "Windows" not in platform.platform():
			os.system("svn up")
			
	if "nocompress" in argS:
		ifCompress = False
	else:
		ifCompress = True
	
	# 解析配置项	
	pyConfig = defaultConfig
	for o, a in opts:
		if o in ("-f", "--config"):
			pyConfig = a
	parseConfig()
	
	# 准备替换标记 
	parseMarks()

	# 默认编译模式
	mode = 'default'
	for cmd in args:
		if modes.get(cmd):
			mode = cmd
			break
	
	if modes.get(mode):
		rmdir(relpath)
		print mode, "Compile Mode on ", "-"*60
		pickMode(modes.get(mode))
			
	# 删除临时ver文件	
	cleanup()
	sys.exit()