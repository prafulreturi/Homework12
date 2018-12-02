
from bs4 import BeautifulSoup as bs
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    local_nasa_file = "News_NASA_Mars_Exploration_Program.html"
    nasa_html = open(local_nasa_file, "r").read()
    news_soup = bs(nasa_html, "html.parser")

    news_title = news_soup.find('div', class_ ='content_title').text
    news_p = news_soup.find('div', class_ = 'article_teaser_body').text

    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    # Mars twitter
    mars_tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_tweet_url)
    mars_tweet_html = browser.html
    mars_tweet_soup = bs(mars_tweet_html, 'html.parser')
    
    mars_weather = mars_tweet_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    # Add the Mars weather to the dictionary

    mars_data["mars_weather"] = mars_weather

    # Mars Facts

    mars_facts_url = 'https://space-facts.com/mars/'

    mars_facts_tables = pd.read_html(mars_facts_url)

    mars_info = pd.DataFrame(mars_facts_tables[0])

    mars_info.columns=['Mars','Data']
    mars_table=mars_info.set_index("Mars")
    mars_html = mars_table.to_html(classes='marsinformation')
    mars_html =mars_html.replace('\n', ' ')

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = mars_html

    # Mars Hemispheres

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    hemisphere_results = hemisphere_soup.find_all('div', class_ = 'item')

    hemisphere_image_urls = []

    for hemisphere in hemisphere_results:

        result = hemisphere.find('div', class_='description')
    
        title = result.a.h3.text
    
        img_url = result.a['href']
    
        img_url = 'https://astrogeology.usgs.gov' + img_url
    
        browser.visit(img_url)
    
        html = browser.html
    
        soup = bs(html, 'html.parser')
    
        img_download = soup.find('div', class_ ='downloads')
    
        img_url_download = img_download.ul.li.a['href']
    
        hemisphere_image_url = {'title' : title, 'img_url' : img_url_download}

        hemisphere_image_urls.append(hemisphere_image_url)

   # Add the Mars hemisphere to the dictionary
    mars_data['mars_hemis'] = hemisphere_image_urls
    
    return mars_data
