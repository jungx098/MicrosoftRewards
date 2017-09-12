import googleTrends as gt
import auth
import common as c
import random
import sys
import urllib
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

email = sys.argv[1].split(">")[0]
password = sys.argv[1].split(">")[1]
desktop_ua = sys.argv[1].split(">")[2]
mobile_ua = sys.argv[1].split(">")[3]
try:
	proxy = sys.argv[1].split(">")[4]
except IndexError:
	proxy = "127.0.0.1:8080"

#wait random amount before logging in
wait_secs = random.randint(c.new_thread_low,c.new_thread_high)
print("sleeping for " + str(wait_secs))

#login mobile and desktop
desktop = auth.Account(email, password, desktop_ua, proxy)
desktop.login()
mobile = auth.Account(email, password, mobile_ua, proxy)
print email + ": logged in"

#searches throughout the period of time 6-8 hours default
mobile_left = 20
desktop_left = 30
querytime = random.randint(c.querytime_low,c.querytime_high)
querysalt = random.randint(c.querysalt_low,c.querysalt_high)
querytimes = random.sample(range(1,int(querytime)),int(desktop_left + mobile_left + querysalt) - 1)
printed = False
mobile_searches = 0
desktop_searches = 0
lasttype = random.choice(["desktop","mobile"])
for i in range(0,int(querytime)+1):
	time.sleep(1)
	try:
		if not printed:
			print(email + ": next search in: " + str(min(filter(lambda x: x > i,querytimes)) - i) + " seconds")
			printed = True
	except ValueError:
		print(email + ": searches done")
		sys.exit(1)
	if i in querytimes:
		if mobile_searches > mobile_left and desktop_searches > desktop_left:
			pass
		elif desktop_searches > desktop_left and mobile_searches < mobile_left:
			lasttype = "mobile"
		elif desktop_searches < desktop_left and mobile_searches > mobile_left:
			lasttype = "desktop"
		types = []
		num = int(c.last_type_chance * 10)
		count = 0
		while count != num:
			types.append(lasttype)
			count += 1
		count = 0
		num = int((1 - c.last_type_chance) * 10)
		while count != num:
			if "desktop" in lasttype:
				types.append("mobile")
			else:
				types.append("desktop")
			count += 1
		lasttype = random.choice(types)
		gen = gt.queryGenerator(1)
		query = gen.generateQueries(1,set())
		if "desktop" in lasttype:
			account = auth.Account(email, password, desktop_ua, proxy)
			desktop_searches += 1
			desktop.get(c.searchURL + str(query.pop()), cookies=desktop.cookies)
		if "mobile" in lasttype:
			account = auth.Account(email, password, mobile_ua, proxy)
			mobile_searches += 1
			mobile.get(c.searchURL + str(query.pop()), cookies=desktop.cookies)
		print email + ": " + lasttype + " search"
		printed = False



  
