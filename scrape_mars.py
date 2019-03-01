#!/usr/bin/env python
# coding: utf-8

# In[39]:


# declare dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from splinter import Browser


# In[40]:


browser = Browser('chrome',headless=False)


# ## NASA Mars News

# In[41]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[42]:


# created an html object to obtain html content
html = browser.html

# parsing through html using beautiful soup
soup = BeautifulSoup(html, 'html.parser')

# assigned the title and paragraph text to variables
news_title = soup.find('div', {'class': 'content_title'}).find('a').text
news_p = soup.find('div', {'class': 'article_teaser_body'}).text


# printed the variables from the latest article
print(news_title)
print(news_p)


# ## JPL Mars Space Images - Featured Image

# In[43]:


# Visit Mars Space Images through splinter module
image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url_featured)


# In[44]:


# HTML Object
html_image = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_image, 'html.parser')

# Retrieve background-image url from style tag
featured_image_url = soup.find('article')['style'].replace(
    'background-image: url(', '').replace(');', '')[1:-1]

# Website Url
main_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route
featured_image_url = main_url + featured_image_url

# Display full link to featured image
featured_image_url


# In[ ]:




