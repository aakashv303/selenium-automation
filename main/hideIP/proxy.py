import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

from scrap.survayfiller import automate

import config

WEB_DRIVER = config.WEB_DRIVER
PROXY_LIST = config.PROXY_LIST
USED_PROXY_LIST = config.USED_PROXY_LIST

co = webdriver.ChromeOptions()
co.add_argument("log-level=3")
# co.add_argument("--headless")

def get_proxies(co=co):
    # driver = webdriver.Chrome(chrome_options=co,executable_path=os.path.join(WEB_DRIVER))
    # driver.get("https://free-proxy-list.net/")
    import requests
    from lxml.html import fromstring
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = list()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies


ALL_PROXIES = get_proxies()


def proxy_driver(PROXIES, co=co):
    prox = Proxy()
    pxy = ''
    if PROXIES:
        pxy = PROXIES[-1]
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(
        chrome_options=co,
        executable_path=os.path.join(WEB_DRIVER),
        desired_capabilities=capabilities
        )

    return driver,pxy

def get_proxy_file():
    lines = open(PROXY_LIST).readlines()
    for i, proxy in enumerate(lines[:]):
        prox_driver, pxy = proxy_driver([proxy])
        del lines[i]
        break
    open(PROXY_LIST, 'w').writelines(lines)
    open(USED_PROXY_LIST, 'a').writelines(proxy)
    return prox_driver, pxy
# code must be in a while loop with a try to keep trying with different proxies
running = True

def maskIP(text_partition,typeID):
    while running:
        prox_driver, proxy = get_proxy_file()
        try:
            # if statement to terminate loop if code working properly
            coupon_text = automate(prox_driver,text_partition,typeID)
            if coupon_text:
                return coupon_text, proxy

        except Exception as e:
            
            # reassign driver if fail to switch proxy
            print("---proxy %s is not working" % proxy)
            time.sleep(1)
