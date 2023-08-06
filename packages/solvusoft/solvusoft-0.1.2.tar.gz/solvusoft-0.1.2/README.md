# Solvusoft Lib
## Solvusoft(solvusoft.com)
Solvusoft provides a number of databases with extensions, companies and applications.We use the Requests engine and the BeautifulSoup engine to extract content, clean data, and get tuple data.

## Install
```commandline
pip install solvusoftlib
```
## Extensions Data
Extension Interface in `solvusoftlib.extensions`

```python
from solvusoftlib import extensions
print(extensions.get_extension_details(str(
"html"
)))
```

```
('The HTML File Extension has one primary file type, Hypertext Markup Language File format, and can be opened with seventeen distinctive software programs, with the dominant related application developed by Microsoft Corporation(Microsoft Notepad software).
HTML files are categorized ordinarily as Web Files.
File Extension HTML files have been identified on both desktop and mobile devices.
They are fully or partially supported by Windows, Mac, and Linux.HTML files have a "Low" Popularity Rating;
this means that they are not present on most devices.
Interested to learn more about the HTML File Extension? We encourage you to view the detailed file information below to learn about the software that opens HTML files, and other troubleshooting tips.', 'Hypertext Markup Language File', [['Microsoft Notepad', 'Microsoft Corporation'], ['Internet Explorer', 'Microsoft Corporation'], ['Mozilla Firefox', 'Mozilla'], ['Google Chrome', 'Google'], ['Opera', 'Opera Software'], ['Microsoft Edge', 'Microsoft Corporation'], ['Adobe Dreamweaver', 'Adobe Systems Incorporated'], ['Apple Safari', 'Apple'], ['AbiWord', 'Open Source'], ['<a href="/en/file-extensions/software/open-source/notepad2/">Notepad2', 'Open Source'], ['WeBuilder', 'Blumentals Software'], ['Visual Studio Code', 'Microsoft Corporation'], ['Textastic Code Editor', 'Alexander Blach'], ['Amaya', 'Open Source'], ['KompoZer', 'Open Source'], ['SCREEM', 'David A Knight']])
```

If Can't Find , Return `None` Like This:
```python
from solvusoftlib import extensions
print(extensions.get_extension_details(str(
"qwerty"
)))
```
```
None
```


### Use Other Language
Use Chinese, Like This
```python
from  solvusoftlib import extensions
print(extensions.get_extension_details(str("html"), str("zh-cn")))
```
Use Japanese Like This:
```python
from  solvusoftlib import extensions
print(extensions.get_extension_details(str("html"), str("jp")))

```
If use a invalid lang, like this.
```python
from  solvusoftlib import extensions
print(extensions.get_extension_details(str("html"), str("qwety")))
```
```
None
```
> Very occasionally (such as making a lot of calls or using a computer with a virus), using a valid call statement also returns None because inside the function when the HTTP return code is Not 200 (OK), 304 (cache) returns None, including 404 (Not Found), 500 (Server Error), and 403(Forbidden)

## Company Data
Company Data in `solvusoftlib.company`
```python
from solvusoftlib import company
print(company.get_company_details(str('kingsoft')))
```
```
('Kingsoft is a Chinese software company founded in 1989 by Pak Kwan Kau. Aside from developing the WPS, Kingsoft is also an Internet service provider, created a mobile internet subsidiary (Cheetah) and security software products.', ['Kingsoft Office', 'Kingsoft Presentation', 'Kingsoft Writer', 'WPS Office'])
```
Usage similar to above

## Application Data
```python
from solvusoftlib import application
print(application.get_application_details(str('kingsoft'), str('wps-office')))
```

There is no guarantee that the set language results will be correct.
