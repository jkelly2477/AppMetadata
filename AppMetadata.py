# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import urllib2
import sys
import json
from pprint import pprint

def get_app_url(package_name):
    prefix = "https://play.google.com/store/apps/details?id="
    prefix += package_name + "&hl=en"
    return prefix


def is_free_app(package_name, soup):
    if (soup == None):
        return None
    button_line = soup.find_all(class_="price buy id-track-click id-track-impression")[0]
    button_meta_data = button_line.get_text().strip()
    if (button_meta_data == 'Install'):
        return True
    return False

def is_freemium(package_name, soup):
    if (soup == None):
        return None
    pay_line = soup.find_all(class_="inapp-msg")
    if not pay_line:
        return False
    return True


def has_ads(package_name, soup):
    if (soup == None):
        return None
    pay_line = soup.find_all(class_="ads-supported-label-msg")
    if not pay_line:
        return False
    return True


'''
    text = pay_line.get_text().strip()
    if ('ads' in text):
        return True
    return False
'''


def get_category(package_name, soup):
    if (soup == None):
        return None
    cat_line = soup.find_all(class_="document-subtitle category")[0]
    return cat_line.get_text().strip()


def get_rating(package_name, soup):
    if (soup == None):
        return None
    rating_line = soup.find_all(class_="score")[0]
    return float(rating_line.get_text().strip())


# get the upper bound on the downloads
def get_downloads_ub(package_name, soup):
    if (soup == None):
        return None
    download_line = soup.find_all(class_="content", itemprop="numDownloads")[0]
    text = download_line.get_text().strip()
    downloads_ub = text[text.find('-') + 2:]
    return int(downloads_ub.replace(',', ''))


def connect(package_name):
    try:
        url = get_app_url(package_name)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except urllib2.URLError as e:
        print ("Error in Connecting: ", e.reason)
        if (e.reason == 'Not Found'):
            print ("Please check the package name. If the package name is valid, then it can be a system app")
            return None
        elif (e.reason == 'Forbidden'):
            return None
        return None


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print ('Usage: Package name is needed as an argument')
        sys.exit(1)
    # print (get_available_countries('com.SecUpwN.AIMSICD'))
    package_name = sys.argv[1]
    soup = connect(package_name)
    print ('Rating of the app %s' % get_rating(package_name, soup))
    print ('Category of the app %s' % get_category(package_name, soup))
    print ('Downloads UB %s ' % get_downloads_ub(package_name, soup))
    print ('Has Ads? %s' % has_ads(package_name, soup))
    print ('Is Freemium? %s' % is_freemium(package_name, soup))
    print ('Is Free? %s' % is_free_app(package_name, soup))

# wait for some time before making repeated request

# vim: set ts=8 sw=4 expandtab softtabstop=4