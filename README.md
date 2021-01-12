## About Grabster

Very often in process of external/internal penetration testing after primare port scans of network you have huge count of web services. The main difficulty - find the most interesting services for further work with them. Collecting information about every web service by hand can take a lot of time.

**Grabster** - tool, that can be used for collecting information about web services and searching the most interesting for primary analyze.

Also the tool can be very useful for OSINT in process of external penetration testing. 

**It is not fully automated scanner. It collects information and generates readable output for manual analysis.** 

## What it already can

- Trying to get access to service with HTTP/HTTPS and automatically skips in case of fail;
- Collects headers from response;
- Gets URLs from SSL certificate;
- Makes screenshots of every domain/web-service;
- Enumerates known virtual hosts (VHosts) for every service
- Identifies web technologies using Wappalyzer 

## What will be in future

- Crawling functionality;
- More settings and customize features (custom headers, regexps, ...);
- Custom macroses;
- Light dirbusting functionality;
- ...

## Installing

Initially required python3 and pip3. 

1. Installing requirements

```
pip3 install -r requirements.txt
./main.py --help
```

2. Installing **chromedriver** (For screenshots)

Firstly you have to download chromedriver binary file from https://chromedriver.chromium.org/downloads with version that matches chrome version. After that you should make it available from PATH environment variable.

3. Установка **wappalyzer** (For identifies web technologies)

```
npm i -g wappalyzer@5.9.34
```

## Possible installing problems

### Problems with m2crypto install

**Mac**: https://stackoverflow.com/questions/33005354/trouble-installing-m2crypto-with-pip-on-os-x-macos

**Linux**: ?

### Сhromedriver stopped working or didn't work initially

Likely you updated your chrome browser or installed chromedriver with incorrect version. Chromedriver and Chrome should have the same version.

Solves by reinstalling of **chromedriver** the same version that has chrome browser. 

## Usage examples:

```
python3 main.py -f input.txt --vhosts vhosts.txt --screenshots 
```

input.txt:

```
test.local
192.168.1.1:1234
192.168.1.2
```

vhosts.txt:

```
www.test.local
admin.test.local
qweqwe.test.local
```
