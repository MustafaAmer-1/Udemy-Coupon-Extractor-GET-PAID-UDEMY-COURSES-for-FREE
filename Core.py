import requests, bs4
from requests.models import PreparedRequest
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def tutorialbar(CourseName):
    DOMAIN = "https://www.tutorialbar.com/"
    params = {'s':CourseName,
    'post_type':'post',
    'cat': ''}

    res = requests.get(DOMAIN, params=params)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    try:
        link = soup.find_all('article')[0]
    except:
        return ""
    courseLink = link.find("a").get("href")

    res = requests.get(courseLink)
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    udemy_link = soup.find("span", class_="rh_button_wrapper").find("a").get("href")
    return udemy_link

def couponscorpion(CourseName):
    global browser
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser =  webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    browser.set_page_load_timeout(4)

    DOMAIN = 'https://couponscorpion.com/'
    params = {'s':CourseName,
    'post_type':'post%2Cpage'}

    res = requests.get(DOMAIN, params=params)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    try:
        link = soup.find('div', class_='rh_gr_right_sec').find('a').get('href')
        browser.get(link)
        udemy_link = browser.find_element_by_class_name('re_track_btn').get_attribute('href')
    except TimeoutException:
        elementLink = browser.find_element_by_class_name('re_track_btn')
        udemy_link = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 're_track_btn'))).get_attribute("href")
    except:
        return ''
    return udemy_link


def realdiscount(CourseName):
    DOMAIN = 'https://www.real.discount/'
    req = PreparedRequest()
    params = {'s':CourseName,
    'post_type':'product',
    'product_cat': '0'}
    req.prepare_url(DOMAIN, params)
    search_url = req.url

    try:
        browser.set_page_load_timeout(10)
        browser.get(search_url)
    except TimeoutException:
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'retina-logo')))

    status = browser.find_elements_by_class_name('status')

    links = []
    if len(status):
        for state in status:
            if state.text == "Expired":
                continue
            links.append(state.find_element_by_xpath('..').get_attribute('href'))
    else:
        browser.close()
        return []
    
    udemy_links = []
    for link in links:
        browser.get(link)
        if browser.title != CourseName:
            continue
        udemy_links.append(browser.find_element_by_class_name('single_add_to_cart_button').find_element_by_xpath('..').get_attribute('href'))
    browser.close()
    return udemy_links

def smartybro(CourseName):
    DOMAIN = 'https://smartybro.com/'
    params={'s':CourseName}

    res = requests.get(DOMAIN, params=params)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    try:
        link = soup.select_one('#post-164902 > h2 > a')
    except:
        return ''
    courseLink = link.get('href')

    res = requests.get(courseLink)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    udemy_link = soup.find('a', class_='fasc-type-flat').get('href')
    return udemy_link

def discudemy(CourseName):
    DOMAIN = 'https://www.discudemy.com/s-r/'
    for i in range(5):
        res = requests.get(DOMAIN + CourseName.replace(' ', '-') + '.jsf')
        if res.status_code == 200:
            break
    if res.status_code != 200:
        return ''
    
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    ancherElements = soup.find_all('a', class_='card-header')
    link = ''
    for element in ancherElements:
        if CourseName in element.getText():
            link = element.get('href')
            break
    
    res = requests.get(link)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    courseLink = soup.find('a', class_='discBtn').get('href')

    res = requests.get(courseLink)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    udemy_link = soup.select('body > div.ui.container.mt10 > div:nth-child(3) > div > a')[0].get('href')
    return udemy_link

def getCoupon(CourseName):
    try:
        TB = tutorialbar(CourseName)
    except:
       TB = []
    try:
        CS = couponscorpion(CourseName)
    except:
       CS = []
    try:
        RD = realdiscount(CourseName)
    except:
        RD = []
    try:
        SB = smartybro(CourseName)
    except:
        SB = []
    try:
        DU = discudemy(CourseName)
    except:
        DU = []
    
    return [TB] + [CS] + RD + [SB] + [DU]
