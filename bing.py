import googleTrends as gt
import auth
import common as c
import sys
from time import sleep
from random import uniform

email = sys.argv[1].split(">")[0]
password = sys.argv[1].split(">")[1]
desktop_ua = sys.argv[1].split(">")[2]
mobile_ua = sys.argv[1].split(">")[3]
try:
    proxy = sys.argv[1].split(">")[4]
except IndexError:
    proxy = "127.0.0.1:8080"
cur = 1 # Current Query Number
account = auth.Account(config["email"], config["password"], desktop_ua, proxy) # Init Account
# Generate PC Queries
gen = gt.queryGenerator(1)
querySet = gen.generateQueries(count, set())
account.login() # Login Account on PC
# Do Searches
for query in querySet:
    print("PC Query " + str(cur) + " / " + str(count) + " : " + query)
    account.get(c.searchURL + query, cookies=account.cookies)
    sleep(delay + uniform(0, delayRandom))
    cur += 1
account.logout() # Logout
sleep(config["accountDelay"])
cur = 1 # Reset Current Query Number
# Generate Mobile Queries
gen = gt.queryGenerator(1)
querySet = gen.generateQueries(mobileCount, set())
account = auth.Account(config["email"], config["password"], mobile_ua, proxy) # Init Account
account.login(mobile=True) # Login Account on Mobile
# Do Searches
for query in querySet:
    print("Mobile Query " + str(cur) + " / " + str(mobileCount) + " : " + query)
    account.get(c.searchURL + query, cookies=account.cookies)
    sleep(delay + uniform(0, delayRandom))
    cur += 1
account.logout() # Logout


  
