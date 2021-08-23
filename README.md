![Version 3.0](http://img.shields.io/badge/version-v3.0-orange.svg)
![Python 3.9](http://img.shields.io/badge/python-3.9-blue.svg)
![Latest Commit](https://img.shields.io/github/last-commit/kyletimmermans/wicked?color=green)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">Wicked</div>

This program scrapes Instagram web pages that contain the usernames of the people the you follow and who are following you. By comparing the two lists, it returns all the usernames that are in the "Following" list and are not in your "Followers" list. Essentially, showing you who has not followed you back. This program does not use the Instagram API.

## How to run it:
1. In order to make this work, you must have python3 on your system
2. Run: **pip3 install -r requirements.txt**
3. Download the [Chrome Webdriver](https://chromedriver.chromium.org/downloads "Chrome Webdriver")
 for your current version of Chrome (check by visiting chrome://version in your browser) and for your respective system (Windows, MacOSX, Linux) and place it in the same folder / directory as _Wicked.py_
4. Finally, run with admin/root permissions: **sudo python3 Wicked.py**
5. Input your username and password for Instagram, and wait a few minutes for it to print to the console. Run time is dependant on how many people you follow / follow you

_Note:_ 

_1. This program does not log your username or password, it simply passes it to the Instagram login form._    
_2. This program uses HTTPS and TLSv1.2 to send information to Instagram._ \
_3. The program will also **temporarily** add the line, if not already present, "127.0.0.1 localhost" to your hosts file to help fix some issues with Selenium. Program will automatically remove the line if added by the program, once finished._


<p>&nbsp;</p>

### Sample Program Output
![alt text](https://github.com/kyletimmermans/wicked/blob/master/output_screenshot1.png "Sample Program Output")

</br>

### Changelog
<div>v1.0: Initial-Release</div>
<div>v2.0:<div>
<div>&ensp;&ensp;-Handle for possible incorrect username and password and re-input them if their incorrect</div>
<div>&ensp;&ensp;-Handle path change for different Operating Systems (Windows, OSX, Linux)</div>
<div>&ensp;&ensp;-Automatically add and then remove a line from 'hosts' file to fix selenium error</div>
<div>v2.1: Added progress bars while loading results</div>
<div>v2.2:</div>
<div>&ensp;&ensp;-Added error handling for not being able to find the host file</div>
<div>&ensp;&ensp;-Added error handling for not finding chromedriver in the same folder as itself</div>
<div>&ensp;&ensp;-Added "Establishing Connection" print line
<div>&ensp;&ensp;-Removed logs showing up in console for Windows</div>
<div>v2.3:</div>
<div>&ensp;&ensp;-Added error handling for no internet connection</div>
<div>&ensp;&ensp;-Added better error handling for chromedriver not found in 'Wicked.py' directory</div> 
<div>&ensp;&ensp;-Better error handling for hosts file not found</div>
<div>&ensp;&ensp;-Syntax sugar added, small code cleanup</div> 
<div>v2.4:</div>
<div>&ensp;&ensp;-Fixed JavascriptException: Cannot read property 'scrollTo' of null</div>
<div>&ensp;&ensp;-Fixed issue where selenium couldn't find user profile div</div>
<div>&ensp;&ensp;-Fixed issue with output where '1' would randomly show up
<div>v2.5:</div>
<div>&ensp;&ensp;-Added final count of usernames along with Results</div>
<div>&ensp;&ensp;-Fixed issue with accounts that have a 'K' or 'M' in their following/followers number</div>
<div>&ensp;&ensp;-Login page needed to have 'react-root' replaced with 'loginForm'</div>
<div>&ensp;&ensp;-Automatically remove "Headless" from user agent string for the driver (Instagram can block headless ones)</div>
<div>&ensp;&ensp;-Fixed bs4 list iterator</div>
<div>&ensp;&ensp;-Logic for (following - followers) detailed in comments</div>
<div>v3.0:</div>
<div>&ensp;&ensp;-Using TLSv1.2 to send information</div>
<div>&ensp;&ensp;-Added MFA Support</div>
<div>&ensp;&ensp;-Added better correct-login checking</div>
<div>&ensp;&ensp;-Added v3 to the ASCII art title</div>
<div>&ensp;&ensp;-Removed JavaScript that scrolls div (was always changing) and sends scroll key instead</div>
