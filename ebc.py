import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import cfscrape
from bs4 import BeautifulSoup
import sys
from termcolor import colored
vip = ''
def data(string):
	dat=colored('[+] ', 'green', None, ['bold'])+colored(string, 'white', None, ['bold'])
	print(dat)

def info(string):
	info=colored('[*] ', 'blue', None, ['bold'])+colored(string, 'white', None, ['bold'])
	print(info)

def error(string):
	error=colored('[+] ', 'red', None, ['bold'])+colored(string, 'white', None, ['bold'])
	print(error)
try:
	emails=sys.argv[1]
except Exception as e:
	error('No arguments given...')
	sys.exit(1)
if len(sys.argv) == 0:
	error('No email/account given..')
	sys.exit(1)
elif len(sys.argv) > 2:
	error('Too much arguments given..')
	sys.exit(1)
headers = {'user-agent': 'Email-breach-checker-h0nus/py3.7'}
print("     Email breach cheacker v0.1 by H0nus")
info('Getting {} breaches..'.format(emails))
r = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/{}'.format(emails),headers=headers)
if r.json() == '' or r.status_code == 404:
	error('No data or failed to connect to HaveIBeenPwnd')
else:
	f = r.json()
	i = 0
	for x in f:
	 		data('Target: {}, Domain:  {}, Breach Date: {}, Leaked: {}'.format(x['Name'],x['Domain'],x['BreachDate'], x['DataClasses']))
info('Getting {} pastes..'.format(emails))
p = requests.get('https://haveibeenpwned.com/api/pasteaccount/{}'.format(emails),headers=headers)
if p.text == '' or p.status_code == 404:
	error('No data or failed to connect to HaveIBeenPwnd')
	pass
else:
	f = p.json()
	a = f[0]
	for x in a:
		data('{} : {}'.format(x,a[x]))
time.sleep(2)
info('Searching for cleartext passwords..')
s = cfscrape.create_scraper()
datas={'param':'{}'.format(emails)}
if vip == '':
	data("I'm using normal research")
	final = s.post('https://ghostproject.fr/search.php',data=datas,headers=headers)
else:
	data("I'm using VIP research")
	cook={'mtusr':'{}'.format(vip)}
	final = s.post('https://ghostproject.fr/search.php',data=datas,headers=headers,cookies=cook)
if 'Error: No results found' in final.text:
	error('No results found')
	pass
else:
	info('Opening Firefox to get credentials..')
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)
	time.sleep(1)
	info('Remember to put your VIP (line 7) email to have passwords in cleartext')
	if vip == '':
		try:
			driver.get("https://ghostproject.fr/")
			info('Waiting 20 seconds to bypass cloudlare bot detection!')
			driver.implicitly_wait(20)
			search = driver.find_element_by_id('searchStr')
			search.click()
			search.clear()
			search.send_keys(emails)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(5)
			test = driver.find_element_by_xpath("//button[@onclick=\"search()\"]")
			test.click()
			time.sleep(3)
			info('Time to save the passwords! Saved to {}-passwords.png'.format(emails))
			driver.save_screenshot('{}-passwords.png'.format(emails.strip()))
			time.sleep(5)
		except Exception as e:
			driver.quit()
			error('Got an error: {}'.format(e))
			sys.exit(1)
	else:
		try:
			driver.get("https://ghostproject.fr/vip")
			info('Waiting 20 seconds to bypass cloudlare bot detection!')
			driver.implicitly_wait(20)
			login = driver.find_element_by_name('mtusr')
			driver.implicitly_wait(5)
			login.send_keys(vip)
			login.send_keys(Keys.ENTER)
			search = driver.find_element_by_id('searchStr')
			search.click()
			search.clear()
			search.send_keys(emails)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(5)
			test = driver.find_element_by_xpath("//button[@onclick=\"search()\"]")
			test.click()
			time.sleep(3)
			info('Time to save the passwords! Saved to {}-passwords.png'.format(emails))
			driver.save_screenshot('{}-passwords.png'.format(emails.strip()))
			time.sleep(5)
		except Exception as e:
			driver.quit()
			error('Got an error: {}'.format(e))
			sys.exit(1)
	driver.quit()
info('Enough for today!')
time.sleep(2)
