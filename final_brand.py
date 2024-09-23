# Required Libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
from gnews import GNews
#from bardapi import Bard
import os
from datetime import datetime
import urllib.request
import shutil
import zipfile
import io

warnings.filterwarnings('ignore')

# Function to scrape the logo of the company
def scrape_logo(search_name):
    search_input = '+'.join(search_name.split())
    url = f'https://www.google.com/search?q={search_input}+logo&tbm=isch'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    if len(images) > 1:
        logo_url = images[1].get("src")
        return logo_url
    return None

# Function to pull the website information using URL
def scrape_website_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    lists = soup.find_all('li')
    paragraphs_text = [p.text.strip() for p in paragraphs]
    lists_text = [li.text.strip() for li in lists]
    return paragraphs_text, lists_text

# Function to get company news
def get_company_news(company_name):
    google_news = GNews()
    news = google_news.get_news(company_name)
    news_df = pd.DataFrame(news)
    return news_df

# Function to get company reviews
# def get_company_reviews(company_name, location):
#     pass
#     # text = "Give me top 10 good and bad reviews and overall summary and suggestions of " + company_name + " "+ location
#     # os.environ['_BARD_API_KEY']="YQhFyqz3tSmDGji1cuBr6nNH5x_hy8e5_oKo32_zSaef85lFVfG2Vwp5g_QIHqInLLCzig."
#     # answer = Bard().get_answer(text)['content']
#     # return answer

# Updated function to save custom Google reviews text
def get_company_reviews(company_name, location):
    # Custom placeholder text for reviews
    reviews_text = f"Google Reviews for {company_name} in {location}:\n"
    reviews_text += "This is a placeholder for reviews. Actual Google Reviews require access to Google services via API.\n\n"
    reviews_text += "Example Reviews:\n"
    reviews_text += "1. Great service and products!\n"
    reviews_text += "2. Had a wonderful experience with the customer support team.\n"
    reviews_text += "3. Delivery was a bit delayed but overall happy with the service."
    
    return reviews_text


# Function to save image from URL
def save_image(url, path):
    with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

# # Function to generate the report and save it in specified location
# def generate_report(company_name, website_url, location, get_logo, get_website_info, get_reviews, get_news):
#     dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
#     os.makedirs(dt_string)

#     if get_logo:
#         logo_url = scrape_logo(company_name)
#         if logo_url:
#             save_image(logo_url, f'{dt_string}/logo.png')
#             st.info("Logo has been saved.")

#     if get_website_info:
#         if website_url:
#             paragraphs_text, lists_text = scrape_website_info(website_url)
#             with open(f'{dt_string}/website_info.txt', 'w', encoding='utf-8') as f:
#                 f.write('Paragraphs:\n')
#                 for paragraph in paragraphs_text:
#                     f.write(f'{paragraph}\n')
#                 f.write('Lists:\n')
#                 for item in lists_text:
#                     f.write(f'- {item}\n')
#             st.info("Website information has been saved.")

#     if get_reviews:
#         reviews_text = get_company_reviews(company_name, location)
#         with open(f'{dt_string}/reviews.txt', 'w', encoding='utf-8') as f:
#             f.write(reviews_text)
#         st.info("Reviews have been saved.")

#     if get_news:
#         news_df = get_company_news(company_name)
#         news_df.to_csv(f'{dt_string}/news.csv')
#         st.info("News has been saved.")

# # Streamlit Application
# st.set_page_config(page_title='Brand Research App', page_icon=':mag:')
# st.title("Brand Research App")
# st.sidebar.image("logo.png", width=300) 
# st.sidebar.title('About App')
# st.sidebar.write('This application allows you to gather information about a company, including its logo, website, Google reviews, and recent news.')
# #st.sidebar.image("logo.png", width=300) 

# company_name = st.text_input("Enter the company name:")
# website_url = st.text_input("Enter the website URL:")
# location = st.text_input("Enter the location:")

# get_logo = st.checkbox("Get Logo")
# get_website_info = st.checkbox("Get Website Information")
# get_reviews = st.checkbox("Get Google Reviews")
# get_news = st.checkbox("Get Company News")

# if st.button("Generate Report"):
#     generate_report(company_name, website_url, location, get_logo, get_website_info, get_reviews, get_news)
#     st.write("Report has been generated.")




# Function to generate the report and zip it
def generate_report(company_name, website_url, location, get_logo, get_website_info, get_reviews, get_news):
    dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    os.makedirs(dt_string)

    if get_logo:
        logo_url = scrape_logo(company_name)
        if logo_url:
            save_image(logo_url, f'{dt_string}/logo.png')
            st.info("Logo has been saved.")

    if get_website_info:
        if website_url:
            paragraphs_text, lists_text = scrape_website_info(website_url)
            with open(f'{dt_string}/website_info.txt', 'w', encoding='utf-8') as f:
                f.write('Paragraphs:\n')
                for paragraph in paragraphs_text:
                    f.write(f'{paragraph}\n')
                f.write('Lists:\n')
                for item in lists_text:
                    f.write(f'- {item}\n')
            st.info("Website information has been saved.")

    if get_reviews:
        reviews_text = get_company_reviews(company_name, location)
        with open(f'{dt_string}/reviews.txt', 'w', encoding='utf-8') as f:
            f.write(reviews_text)
        st.info("Reviews have been saved.")

    if get_news:
        news_df = get_company_news(company_name)
        news_df.to_csv(f'{dt_string}/news.csv')
        st.info("News has been saved.")
    
    # Zip the folder
    zip_filename = f"{dt_string}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(dt_string):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, dt_string))
    
    # Return the path of the zip file
    return zip_filename

# Streamlit Application with download option
st.set_page_config(page_title='APCO Insight Research App', page_icon=':mag:')
st.title("APCO Insight Research App")
st.sidebar.image("logo3.png", width=300)
st.sidebar.title('About App')
st.sidebar.write('This application allows you to gather information about a company, including its logo, website, Google reviews, and recent news.')

company_name = st.text_input("Enter the company name:")
website_url = st.text_input("Enter the website URL:")
location = st.text_input("Enter the location:")

get_logo = st.checkbox("Get Logo")
get_website_info = st.checkbox("Get Website Information")
get_reviews = st.checkbox("Get Google Reviews")
get_news = st.checkbox("Get Company News")

if st.button("Generate Report"):
    zip_file_path = generate_report(company_name, website_url, location, get_logo, get_website_info, get_reviews, get_news)
    
    # Read the zip file for download
    with open(zip_file_path, "rb") as f:
        st.download_button(
            label="Download Report as ZIP",
            data=f,
            file_name=zip_file_path,
            mime="application/zip"
        )
    
    st.write("Report has been generated and is ready for download.")
