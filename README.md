![Version 1.1](http://img.shields.io/badge/version-v1.1-orange.svg)
![Python 3.8](http://img.shields.io/badge/python-3.8-blue.svg)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">Wicked</div>

This program scrapes Instagram web pages that contain the usernames of the people the you follow and who are following you. By comparing the two lists, it returns all the usernames that are in the "Following" list and are not in your "Followers" list. Essentially, showing you who has not followed you back. This program does not use the Instagram API.

## How to run it:
1. In order to make this work, you must have python3 on your system.
2. Run: **pip3 install -r requirements.txt**
3. Download the [Chrome Webdriver](https://chromedriver.chromium.org/downloads "Chrome Webdriver")
 for the your current version of Chrome and for your respective system (Windows, MacOSX, Linux) place it in the same folder as `Wicked.py'
4. Finally, run **python3 Wicked.py**
5. Input your username and password for Instagram, and wait a few minutes for it to print to the console, depending on how many people you follow / follow you

_Note: This program does not log your username or password, it simply passes it to the Instagram log-in form_

<p>&nbsp;</p>

### Sample Program Output
![alt text](https://github.com/kyletimmermans/wicked/blob/master/output_screenshot.png "Sample Program Output")

</br>

### Changelog
<div>v1.0: Initial-Release</div>
<div>v1.1: Handle for possible incorrect username and password</div>
