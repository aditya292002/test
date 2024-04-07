from dotenv import load_dotenv
load_dotenv()  #load all the environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

#configure our api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load local Gemini model and provide sql query as response
def get_gemini_response(question,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    return response.text

#function to retrieve query from sql database
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

#define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL databse has the name Test and has the following columns - user_id, product_id, product_name,
    brand, category and price \n\n For example, \nExample 1 - How many entries of records are present in 
    the SQL command will be something like this SELECT COUNT(*) FROM TEST;
    \nExample 2 - Tell me the price of all the products with id 1,
    the sql command will be something like this SELECT PRICE FROM TEST
    WHERE PRODUCT_ID=1;
    also the sql code should not have ''' in the beginning or end and sql word in the output.
    
    """
]

##initialize our streamlit app
st.set_page_config(page_title="I can retrieve any SQL query")
st.header("SQL Data Retrieval")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

## If submit button is clicked
if submit:
    
    response=get_gemini_response(question,prompt)
    print(response)
    data = read_sql_query(response,'test_db.sqlite')
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.write(row) 
