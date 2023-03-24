# Necessary modules are imported
import streamlit as st
import snscrape.modules.twitter as sntwitter
from pymongo import MongoClient
import pandas as pd
import pymongo
import datetime

client = pymongo.MongoClient("mongodb+srv://priti:priti@cluster0.i3rg0rm.mongodb.net/?retryWrites=true&w=majority")
db = client["Projectwitter"]
coll = db['scraping']

st.title('Twitter Scraping')
menu = ["Home","About","Scraping Data"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.write('''This is **Twitter Scraping web app created using Streamlit**. Data is scraped from twitter based on keyword and date provided. The scraped data is stored in Mongodb and can be downloaded in CSV or
JSON format ''')

elif choice == "About":

# Info about Snscraper
    with st.expander("Snscrape"):
        st.write('''Snscrape is a scraper for *social networking services (SNS)*. 
        It scrapes things like user profiles, hashtags, or searches and returns the discovered items, e.g. the relevant posts.''')

# Info about MongoDB database
    with st.expander("Mongodb"):
        st.write('''MongoDB is an open source document database used for
storing unstructured data. The data is stored as JSON like documents called
BSON. It is used by developers to work easily with real time data analytics, content management and lot of other web
applications.''')

# Info about Streamlit framework
    with st.expander("Streamlit"):
        st.write('''Streamlit is a free and open-source framework to
**rapidly build and share beautiful machine learning and data science web
apps**. It is a Python-based library specifically *designed for machine
learning engineers*.''')

# Scraping data based on keyword and date range

elif choice == "Scraping Data":
    username = st.text_input('Enter the keyword : ' )
    st.write('Scraped Word : ', username)

    number = st.slider("Pick Count of Tweets: ",0, 500, 20, 20)
    st.write("Number of Tweets:", number)
    start_date = st.date_input(
         "Enter Start date of tweet",
         )

    st.write('Start Date:', start_date)
    end_date = st.date_input(
         " Enter End date of tweet",
        )
    st.write('Till Date:', end_date)

    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{username} since:{start_date} until:{end_date}').get_items()):
        if i > number:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
# Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
# button for scraping data
    result = st.button("CLick here to see Data")
    if result:
        st.dataframe(tweets_df)
# button for uploading data in Mongodb
    result1 = st.button("CLick here to upload Data")
    if result1:
        timenow = datetime.datetime.now()
        mongo_database = {"Scraped Word": username , "Scrapped Date": timenow.strftime("%Y-%m-%d"), "Scrapped Data": tweets_df.to_json()}

        coll.insert_one(mongo_database)


    file_format = st.radio(
        "Download as ?",
        ('CSV', 'JSON'))
    if file_format == 'CSV':
        @st.cache
        def convert_df(df):
# Cache the conversion to prevent computation on every rerun

            return df.to_csv().encode('utf-8')
        csv = convert_df(tweets_df)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='tweets_df.csv',
            mime='text/csv',
        )
    else:
        @st.cache
        def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun

            return df.to_json().encode('utf-8')
        json = convert_df(tweets_df)
        st.download_button(
            label="Download data as JSON",
            data=json,
            file_name='tweets_df.json',
            mime='json',
        )