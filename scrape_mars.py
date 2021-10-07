# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random


def extractPageSource(URL):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe", options=chrome_options)
    # get source code
    driver.get(URL)
    html = driver.page_source
    time.sleep(2)
    driver.close()
    return html


def scrape():
    URL = "https://redplanetscience.com/"
    html = extractPageSource(URL)
    soup = BeautifulSoup(html, features="lxml")
    title_elements = soup.findAll('div', attrs={'class': 'content_title'})
    description_elements = soup.findAll(
        'div', attrs={'class': 'article_teaser_body'})
    news_title = []
    news_p = []
    for title_element, description_element in zip(title_elements, description_elements):
        news_title.append(title_element.text)
        news_p.append(description_element.text)

    URL = "https://spaceimages-mars.com/"
    html = extractPageSource(URL)
    soup = BeautifulSoup(html, features="lxml")
    img_src = soup.find('img', attrs={'class': 'headerimage fade-in'})['src']
    featured_image_url = f"{URL}{img_src}"

    URL = "https://galaxyfacts-mars.com/"
    table_MN = pd.read_html(URL)
    info_table = pd.DataFrame(
        {'Feature': table_MN[1][0], 'Value': table_MN[1][1]})
    html_table_string = info_table.to_html()

    URL = "https://marshemispheres.com/"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe", options=chrome_options)
    # get source code
    driver.get(URL)
    hemisphere_image_urls = []
    for i in range(1, 5):
        fastrack = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, f'//*[@id="product-section"]/div[2]/div[{i}]/a/img')))
        fastrack.click()
        img_src = driver.find_element_by_xpath(
            '//*[@id="wide-image"]/div/ul/li[1]/a').get_attribute("href")
        img_title = driver.find_element_by_xpath(
            '//*[@id="results"]/div[1]/div/div[3]/h2').text
        hemisphere_image_urls.append({'title': img_title, 'img_url': img_src})
        driver.back()

    driver.close()
    return {"data": {'hemisphere_image_urls': hemisphere_image_urls, 'html_table_string': html_table_string, 'featured_image_url': featured_image_url, 'news_title': random.choice(news_title), 'news_p': random.choice(news_p)}}
    # close web browser
