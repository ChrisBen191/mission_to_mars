# declare dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup

from splinter import Browser
import re
import time
browser = Browser('chrome',headless=False)


def get_mars_headline():

    # visited mars news through the splinter module
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(2)

    # created an html object to obtain html content
    news_html = browser.html

    # parsing through html using beautiful soup
    soup = BeautifulSoup(news_html, 'html.parser')

    # assigned the title and paragraph text to variables
    news_title = soup.find('div', {'class': 'content_title'}).find('a').text
    news_p = soup.find('div', {'class': 'article_teaser_body'}).text
    
    # function will return the news_title / news_p variables in a dict format
    return {'news_title':news_title, 'news_paragraph': news_p}



def get_featured_image_url():

    # visited mars space images through the splinter module
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)

    # created an html object to obtain html content
    image_html = browser.html

    # parsing through html using beautiful soup
    soup = BeautifulSoup(image_html, 'html.parser')

    # retrieved background-image url from article > style tag
    article = soup.find('article')['style']

    # sliced the image url to only include the path to the image
    image_url = article[23:-3]

    # website url 
    main_url = 'https://www.jpl.nasa.gov'

    # combined the website url with the spliced image url
    featured_image_url = main_url + image_url
    
    # function will return the full image url in dict format
    return {'image_url': featured_image_url}


def get_mars_weather():

    # visited mars weather through the splinter module
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(2)

    # created an html object to obtain html content
    weather_html = browser.html

    # parsing through html using beautiful soup
    soup = BeautifulSoup(weather_html, 'html.parser')

    # retrieved html content containing tweet information
    latest_tweets = soup.find_all('div', {'class':'js-tweet-text-container'})

    # for loop to loop through tweets and to retrieve the first tweet  
    # with weather information 
    for tweet in latest_tweets:
        weather_tweet = tweet.find('p').text
        # two strings found in every weather-related tweet
        if 'sol' and 'low' in weather_tweet:
            
            # function will return mars weather tweet in dict format
            return {'mars_weather': weather_tweet}
            break
            
        else:
            pass


def get_mars_facts():

    # visited mars facts through the splinter module
    fact_url = "https://space-facts.com/mars/"
    browser.visit(fact_url)
    time.sleep(2)
    
    # parsed the html using pandas
    mars_facts = pd.read_html(fact_url)

    # assigned the facts dataframe to mars_df
    mars_df = mars_facts[0]

    # assigned the column names in the mars_df
    mars_df.columns = ['Description', 'Measurement']
    formatted = mars_df.to_html(classes=["table-dark", "table-hover"])
    
    # function will return mars facts html table in dict format
    return {"html_table_facts": formatted}


def get_mars_hemispheres():
    
    # visited mars hemispheres through the splinter module
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(2)

    # created an html object to obtain html content
    hemi_html = browser.html

    # parsing through html using beautiful soup
    soup = BeautifulSoup(hemi_html, 'html.parser')

    # retrieved container holding hemi info
    products = soup.find_all('div', {'class': 'item'})

    # created empty list for hemisphere urls
    hemi_image_urls = []

    # stored the main url
    hemi_main_url = 'https://astrogeology.usgs.gov'

    # for loop to find hemi info
    for p in products:

        # stored hemi title as object
        title = p.find('h3').text

        # stored link that leads to full image website
        partial_img_url = p.find('a', {'class': 'itemLink product-item'})['href']

        # visited the link that contains the full image website
        browser.visit(hemi_main_url + partial_img_url)

        # created an html object to obtain html content
        partial_img_html = browser.html

        # parsing through html using beautiful soup
        soup = BeautifulSoup(partial_img_html, 'html.parser')

        # stored full image url as object
        img_url = hemi_main_url + soup.find('img', {'class': 'wide-image'})['src']

        # appended the retreived information into hemi_image_urls list
        hemi_image_urls.append({"title": title, "img_url": img_url})

    # function will return mars hemisphere image urls in a list of dicts format
    return {'hemi_image_urls':hemi_image_urls}


def scrape_master():
    print('scraping stuff')

    # assigned the get_mars_headline() function to a variable
    headlines_dict = get_mars_headline()

    # assigned the get_featured_image_url() function to a variable
    featured_image_dict = get_featured_image_url()

    # assigned the get_mars_weather() function to a variable
    mars_weather_dict = get_mars_weather()

    # assigned the get_mars_facts() function to a variable
    mars_facts_dict = get_mars_facts()

    # assigned the get_mars_hemispheres() function to a variable
    mars_hemi_dict = get_mars_hemispheres()

    # Insert the dicts into Mongo - but first merge our dictionaries into one dict
    merged_dict = {**headlines_dict, **featured_image_dict,**mars_facts_dict, **mars_weather_dict, **mars_hemi_dict}
    print('done merging')

    # merged dict will be the new data in mongodb
    return merged_dict
