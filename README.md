# MicrosoftRewards
## About
MicrosoftRewards is an automated point earning script that works with bing.com to earn points that can be redeemed for giftcards.

## Requirements
Python 2.7

## Running The Script
Copy *accounts.txt.dist* to *accounts.txt*  

Linux/Mac
```bash
$ cd path/to/microsoftrewards
$ ./bing.py
```
Windows
```
> cd path\to\microsoftrewards
> python bing.py
```
## Config

### General


### Accounts
You can have as many accounts as you need, one account per line in *accounts.txt*. 
**Note**: Proxies are optional and are on a per account basis. 
**Note**: User-Agent fields are NOT optional.
**Note**: Two-Factor Authentication (2FA) is not supported.
```
email>password>desktop_ua>mobile_ua>proxy
```

### Query Generators
- googleTrends
- wikipedia
