import requests
import common as c
import time
import random
from bs4 import BeautifulSoup
from random import randint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Account:

    headers = c.headers
    params = {}
    data = {"i13":"0", "type":"11", "LoginOptions":"3", "lrt":"", "ps":"2", "psRNGCDefaultType":"", "psRNGCEntropy":"", "psRNGCSLK":"", "canary":"", "ctx":"", "NewUser":"1", "FoundMSAs":"", "fspost":"0", "i21":"0", "i2":"1", "i17":"0", "i18":"__ConvergedLoginPaginatedStrings%7C1%2C__ConvergedLogin_PCore%7C1%2C", "i19":"2" + str(randint(0, 5000))}
    proxies = {"http":"127.0.0.1:8080", "https":"127.0.0.1:8080"}

    def __init__(self, email, password, ua, proxy):
        self.data["login"] = email
        self.data["loginfmt"] = email
        self.data["passwd"] = password
        self.headers["User-Agent"] = ua
        if proxy != "127.0.0.1:8080":
            self.proxies["http"] = proxy
            self.proxies["https"] = proxy
        
    def login(self, mobile=False):
        postURL = self.preLogin()
        res = self.post(postURL, cookies=self.cookies, data=self.data)
        # Parse HTML Form
        form = BeautifulSoup(res.text, "html.parser").findAll("form")[0] # Get Form
        params = dict()
        for field in form:
            params[field["name"]] = field["value"] # Add each field to params
        self.headers["Host"] = c.host # Set Host to Bing Server
        res = self.post(form.get("action"), cookies=self.cookies, data=params)
        self.cookies = res.cookies # Set Cookies
        
    def preLogin(self):
        res = self.get(c.hostURL)
        # Get Login URL
        index = res.text.index("WindowsLiveId") # Find URL
        cutText = res.text[index + 16:] # Cut Text at Start of URL
        loginURL = cutText[:cutText.index("\"")] # Cut at End of URL
        loginURL = bytes(loginURL).encode("utf-8").decode("unicode_escape") # Unescape URL
        # Get Login Cookies
        self.headers["Host"] = c.loginHost # Set Host to Login Server
        res = self.get(loginURL)
        self.cookies = res.cookies # Set Cookies
        self.cookies["CkTst"] = "G" + str(int(time.time() * 1000)) # Add Time Cookie
        # Get Post URL
        index = res.text.index(c.loginPostURL) # Find URL
        cutText = res.text[index:] # Cut Text at Start of URL
        postURL = cutText[:cutText.index("\'")] # Cut at End of URL
        # Get PPFT
        index = res.text.index("sFTTag") # Find PPFT
        cutText = res.text[index:] # Cut Text Near PPFT
        PPFT = cutText[cutText.index("value=") + 7:cutText.index("\"/>")] # Cut PPFT
        self.data["PPFT"] = PPFT
        # Get PPSX
        PPSXs = ["P","Pa","Pas","Pass","Passp","Passpo","Passpor","Passport","PassportR","PassportRN"]
        PPSX = random.choice(PPSXs)
        self.data["PPSX"] = PPSX
        # Finish Up
        self.cookies["wlidperf"] = "FR=L&ST=" + str(int(time.time() * 1000)) # Add Another Time Cookie
        return postURL
    
    def logout(self):
        pass
    
    def get(self, URL, params=None, cookies=None, data=None, extra_offer=False):
        if(extra_offer):
             self.headers["User-Agent"] = self.headers["User-Agent"] + " Edge/12.10136"
        if(self.proxies["http"] != "127.0.0.1:8080"):
            res = requests.get(URL, headers=self.headers, params=params, cookies=cookies, data=data, proxies=self.proxies, verify=False)
        else:
            res = requests.get(URL, headers=self.headers, params=params, cookies=cookies, data=data, verify=False)
        self.headers["Referer"] = URL
        return res
    
    def post(self, URL, params=None, cookies=None, data=None):
        if(self.proxies["http"] != "127.0.0.1:8080"):
            res = requests.post(URL, headers=self.headers, params=params, cookies=cookies, data=data, proxies=self.proxies, verify=False)
        else:
            res = requests.post(URL, headers=self.headers, params=params, cookies=cookies, data=data, verify=False)
        self.headers["Referer"] = URL
        return res