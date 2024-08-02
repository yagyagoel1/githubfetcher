import sys
import os


import streamlit as st
import pandas as pd
import sqlite3


#appending path to able to access the logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
from logger import logger


# Function to fetch data from SQLite database
def fetch_data(query,params=()):
    try:
        #establishing a connection with db
        conn = sqlite3.connect('data/github_data.db')
        cursor = conn.cursor()
        cursor.execute(query,params) #executing the query with the given parameters
        data = cursor.fetchall() 
        #taking only the first coulm as it is the necessary one
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(data, columns=columns)#creating dataframe with the data
        conn.close()#closing the connection
        return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()


def main():
    st.title('GitHub Repositories Dashboard')

    #total no of entries
    st.header('Total Number of Entries')
    total_entries = fetch_data('SELECT COUNT(*) AS count FROM repositories')['count'][0]
    st.write(total_entries)

    #top 10 entries by size 
    st.header('Top 10 Entries by Size')
    top_10_entries = fetch_data('SELECT name, size FROM repositories ORDER BY size DESC LIMIT 10')
    st.bar_chart(top_10_entries.set_index('name'))

    #repos created over time
    st.header('Repos Created Over Time')
    entries_over_time = fetch_data('SELECT DATE(created_at) AS date, COUNT(*) AS count FROM repositories GROUP BY DATE(created_at)')
    st.scatter_chart(entries_over_time.set_index('date'))

    #discription of entries by language
    st.header('Distribution of Entries by Language')
    language_distribution = fetch_data('SELECT language, COUNT(*) AS count FROM repositories GROUP BY language')
    st.bar_chart(language_distribution.set_index('language'))

    #top 10 enteris
    st.header('Top 10 Entries by Last Updated')
    top_10_entries = fetch_data('SELECT * FROM repositories ORDER BY updated_at DESC LIMIT 10')
    st.write(top_10_entries)



    #search
    st.header('Search')
    search_by = st.selectbox('Search by', ['ID','Name', 'Full Name',"Description","Language"])
    search_query = st.text_input(f'Enter {search_by}')
    if st.button('Search'):
        query = f"SELECT * FROM repositories WHERE {search_by.lower().replace(' ', '_')} LIKE ?"
        search_results = fetch_data(query, (f'%{search_query}%',)) # using like ? to take a parameter 
        st.write(search_results)


if __name__ == '__main__':
    main()
