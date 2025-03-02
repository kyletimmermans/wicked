![Version 6.4](http://img.shields.io/badge/Version-6.4-orange.svg)
![Python 3.12](http://img.shields.io/badge/Python-3.12-blue.svg)
![Latest Commit](https://img.shields.io/github/last-commit/kyletimmermans/wicked?color=green&label=Latest%20Commit)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">Wicked</div>

A program that prints two lists: a list of people that you follow, but don't follow you back, and a list of people that follow you, but that you don't follow back on Instagram, using Selenium

<div>&#8203;</div>

![Sample Program Output](/media/results_screenshot.png?raw=true)

<div>&#8203;</div>

## How it works
This program scrapes Instagram web pages and uses that data to make requests to Instagram's GraphQL API (no need for an API key!), in order to create lists of the usernames that follow you and that you follow. By comparing the two lists, it returns all the usernames that are in the "Following" list and are not in your "Followers" list. Essentially, showing you who has not followed you back. It does the same process for showing you who follows you, but you aren't following them back.

Wicked uses several evasion/masquerading techniques, including throttling, to appear as a legitimate user and to prevent being seen as a bot/web scraper.

<div>&#8203;</div>

## How to run it
1. Prerequisite: Must have Python3
2. `git clone https://github.com/kyletimmermans/wicked.git && cd wicked`
3. `pip3 install -r requirements.txt`
4. `python3 Wicked.py`
5. Input your username/email/phone # and password for Instagram (MFA code too, if enabled), and wait a few minutes for it to return the results. Run time is dependent on how many people you follow / follow you

_Note:_

* This program does not log your username or password, it simply passes it to the Instagram login form
* This program uses HTTPS and TLSv1.3 to send information to Instagram

<div>&#8203;</div>

### Program Flags

```text
-h, --help, -u, --usage         Show usage/help menu

-v, --version                   Print program version

-o, --output                    Write results (both lists) to file
                                E.g. python3 Wicked.py -o results.txt
```

<div>&#8203;</div>

### Changelog
<div><b>v1.0:</b> Initial-Release</div>
<div><b>v2.0:</b><div>
<div>&ensp;&ensp;-Handle for possible incorrect username and password and re-input them if their incorrect</div>
<div>&ensp;&ensp;-Handle path change for different Operating Systems (Windows, OSX, Linux)</div>
<div>&ensp;&ensp;-Automatically add and then remove a line from 'hosts' file to fix selenium error</div>
<div><b>v2.1:</b> Added progress bars while loading results</div>
<div><b>v2.2:</b></div>
<div>&ensp;&ensp;-Added error handling for not being able to find the host file</div>
<div>&ensp;&ensp;-Added error handling for not finding chromedriver in the same folder as itself</div>
<div>&ensp;&ensp;-Added "Establishing Connection" print line
<div>&ensp;&ensp;-Removed logs showing up in console for Windows</div>
<div><b>v2.3:</b></div>
<div>&ensp;&ensp;-Added error handling for no internet connection</div>
<div>&ensp;&ensp;-Added better error handling for chromedriver not found in 'Wicked.py' directory</div>
<div>&ensp;&ensp;-Better error handling for hosts file not found</div>
<div>&ensp;&ensp;-Syntax sugar added, small code cleanup</div>
<div><b>v2.4:</b></div>
<div>&ensp;&ensp;-Fixed JavascriptException: Cannot read property 'scrollTo' of null</div>
<div>&ensp;&ensp;-Fixed issue where selenium couldn't find user profile div</div>
<div>&ensp;&ensp;-Fixed issue with output where '1' would randomly show up
<div><b>v2.5:</b></div>
<div>&ensp;&ensp;-Added final count of usernames along with Results</div>
<div>&ensp;&ensp;-Fixed issue with accounts that have a 'K' or 'M' in their following/followers number</div>
<div>&ensp;&ensp;-Login page needed to have 'react-root' replaced with 'loginForm'</div>
<div>&ensp;&ensp;-Automatically remove "Headless" from user agent string for the driver (Instagram can block headless ones)</div>
<div>&ensp;&ensp;-Fixed bs4 list iterator</div>
<div>&ensp;&ensp;-Logic for (following - followers) detailed in comments</div>
<div><b>v3.0:</b></div>
<div>&ensp;&ensp;-Using TLSv1.2 to send information</div>
<div>&ensp;&ensp;-Added MFA Support</div>
<div>&ensp;&ensp;-Added better correct-login checking</div>
<div>&ensp;&ensp;-Added v3 to the ASCII art title</div>
<div>&ensp;&ensp;-Removed JavaScript that scrolls div (was always changing) and sends scroll key instead</div>
<div><b>v3.1:</b></div>
<div>&ensp;&ensp;-Added Python Shebang</div>
<div>&ensp;&ensp;-Added if __name__ == "__main__":</div>
<div>&ensp;&ensp;-Refactor / Moved code into main</div>
<div>&ensp;&ensp;-Removed hard-coded XPATHs</div>
<div>&ensp;&ensp;-Added language chromedriver flag to force en-US</div>
<div>&ensp;&ensp;-Added --version and -v command line flag<div>
<div><b>v4.0:</b></div>
<div>&ensp;&ensp;-Added option to take email or phone number instead of just Instagram username<div>
<div>&ensp;&ensp;-Added support for million(s) and just 0 followers / following<div>
<div>&ensp;&ensp;-Using wakepy to prevent program from sleeping and crashing<div>
<div>&ensp;&ensp;-Deal with "Suggested for you" accounts in following modal</div>
<div>&ensp;&ensp;-Bug & Logic fixes</div>
<div>&ensp;&ensp;-Selenium:</div>
<div>&ensp;&ensp;&ensp;&ensp;-Switched from executable_path to "service" model</div>
<div>&ensp;&ensp;&ensp;&ensp;-Switched to new "find_element(By.)" model</div>
<div>&ensp;&ensp;&ensp;&ensp;-No longer clicking follower / following modal, now visits links: instagram.com/{username}/followers</div>
<div>&ensp;&ensp;&ensp;&ensp;-Removed hard-coded cursor coordinates system for scrolling modal</div>
<div>&ensp;&ensp;&ensp;&ensp;-Using WebDriverWait to wait for elements to show up</div>
<div><b>v4.1:</b> Print results to a .txt file</div>
<div><b>v4.5:</b> Now using <a href="https://pypi.org/project/webdriver-manager/">webdriver-manager</a> to automatically install chromedriver</div>
<div><b>v4.6:</b></div>
<div>&ensp;&ensp;-Removed host file manipulation files<div>
<div>&ensp;&ensp;-Regex fixes<div>
<div><b>v4.7:</b></div>
<div>&ensp;&ensp;-Switched from getpass to pwinput for password masking<div>
<div>&ensp;&ensp;-Fix failed MFA retry support<div>
<div>&ensp;&ensp;-Scrolling method now requires window resize event to open each time to load followers/following</div>
<div>&ensp;&ensp;-Using TLSv1.3 to send information</div>
<div><b>v5.0:</b></div>
<div>&ensp;&ensp;-Added feature to see who you don't follow back<div>
<div>&ensp;&ensp;&ensp;&ensp;-Updated banner with new program description</div>
<div>&ensp;&ensp;-Added: -h, -u, --help, --usage flags</div>
<div>&ensp;&ensp;-Fixes to ensure that all following/followers are retrieved properly<div>
<div>&ensp;&ensp;&ensp;&ensp;-Removed scrolling method - Switched to intercept & replay XHR</div>
<div><b>v6.0:</b></div>
<div>&ensp;&ensp;-Now using GraphQL API endpoints to get follower and following username lists</div>
<div>&ensp;&ensp;&ensp;&ensp;-Getting follower and following count done through this API as well</div>
<div><b>v6.1:</b></div>
<div>&ensp;&ensp;-Fixed issue where webdriver-manager would cause a crash</div>
<div>&ensp;&ensp;&ensp;&ensp;-Catch error and let user know that Chrome needs to be updated</div>
<div>&ensp;&ensp;-Fixed method for grabbing user_id</div>
<div>&ensp;&ensp;-Deprecated unused 'dpr' key in 'headers' key-value store</div>
<div>&ensp;&ensp;-Switched to f-strings from string concatenation for error messages and ASCII art</div>
<div>&ensp;&ensp;-Removed "DevTools listening on ws://" and TensorFlow debug logs showing up in Windows stdout</div>
<div>&ensp;&ensp;-Updated dependencies (requirements.txt)</div>
<div><b>v6.4:</b></div>
<div>&ensp;&ensp;-Fixed: Now using CREATE_NO_WINDOW (subprocess) to prevent unnecessary logging on Windows (DevTools listening, TensorFlow), the flags added in the last version did not work</div>
<div>&ensp;&ensp;-Removed: No longer using webdriver_manager library, Selenium's webdriver.chrome.service handles getting the chromedriver</div>
<div>&ensp;&ensp;-Added: -o / --output flag - Results file no longer created by default, need to provide this flag and a filename to get a results file now</div>
<div>&ensp;&ensp;-Added: Extra chromedriver flags to further prevent automation detection</div>
<div>&ensp;&ensp;-Changed: All flags/args being parsed with argparse now</div>
