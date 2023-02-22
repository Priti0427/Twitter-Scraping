import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import datetime
client = pymongo.MongoClient("mongodb+srv://priti:priti@cluster0.i3rg0rm.mongodb.net/?retryWrites=true&w=majority")
db = client["Projectwitter"]
records = db['scraping']

# taking input from user
username = st.text_input('Enter Scraped Word : ' )
st.write('Scraped Word : ', username)


number = st.slider("Pick Count of Tweets: ",0, 500, 20, 20)
st.write("Number of Tweets:", number)

d1 = st.date_input(
    "Enter Start date of tweet",
    )
st.write('Start Date:', d1)

d2 = st.date_input(
    " Enter End  date of tweet",
    )
st.write('Till Date:', d2)


tweets_list2 = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{username} since:{d1} until:{d2}').get_items()):
    if i > number:
        break
    tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating a dataframe from the tweets list above
tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# button for scraping data
result = st.button("CLick here to see Data")
if result:
    st.dataframe(tweets_df2)

#one more button for uploading data in database
result1 = st.button("CLick here to upload Data")
if result1:
    
    timenow = datetime.datetime.now()
    mongo_database = {"Scraped Word": username , "Scrapped Date": timenow.strftime("%Y-%m-%d"),
                      "Scrapped Data": tweets_df2.to_json()}
    records.insert_one(mongo_database)


#dowloading the file as CSV or JSON
file_format = st.radio(
    "Download as ?",
    ('CSV', 'JSON'))

if file_format == 'CSV':
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')


    csv = convert_df(tweets_df2)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='tweets_df2.csv',
        mime='text/csv',
    )
else:
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_json().encode('utf-8')


    json = convert_df(tweets_df2)

    st.download_button(
        label="Download data as JSON",
        data=json,
        file_name='tweets_df2.json',
        mime='json',
    )






