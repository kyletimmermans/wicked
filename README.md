![Version 2.4](http://img.shields.io/badge/version-v2.4-orange.svg)
![Python 3.8](http://img.shields.io/badge/python-3.8-blue.svg)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">Wicked</div>

This program scrapes Instagram web pages that contain the usernames of the people the you follow and who are following you. By comparing the two lists, it returns all the usernames that are in the "Following" list and are not in your "Followers" list. Essentially, showing you who has not followed you back. This program does not use the Instagram API.

## How to run it:
1. In order to make this work, you must have python3 on your system.
2. Run: **pip3 install -r requirements.txt**
3. Download the [Chrome Webdriver](https://chromedriver.chromium.org/downloads "Chrome Webdriver")
 for the your current version of Chrome and for your respective system (Windows, MacOSX, Linux) and place it in the same folder as _Wicked.py_
4. Finally, run with admin/root permissions **python3 Wicked.py**
5. Input your username and password for Instagram, and wait a few minutes for it to print to the console. Run time is dependant on how many people you follow / follow you

_Note:_ 

_1. This program does not log your username or password, it simply passes it to the Instagram log-in form_                        
_2. The program will also **temporarily** add the line, if not already present, "127.0.0.1 localhost" to your hosts file to help fix some issues with Selenium. Program will automatically remove the line if added by the program, once finished._


<p>&nbsp;</p>

### Sample Program Output
![alt text](https://github.com/kyletimmermans/wicked/blob/master/output_screenshot.png "Sample Program Output")

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
 
 
