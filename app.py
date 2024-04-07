import asyncio
import streamlit as st
import pandas as pd
import sqlite3
import os
from icecream import ic 

import logging
logging.basicConfig(level=logging.INFO)


db_name = 'test_db.sqlite'

# Function to read all CSV files from a directory and load them into a SQLite database
def load_csv_to_sqlite(csv_dir, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for file_name in os.listdir(csv_dir):
        if file_name.endswith('.csv'):
            table_name = os.path.splitext(file_name)[0]
            # Replace hyphens with underscores to create valid table names
            table_name = table_name.replace('-', '_')
            file_path = os.path.join(csv_dir, file_name)
            df = pd.read_csv(file_path, encoding='latin-1')  # Use 'latin-1' encoding
            df.to_sql(table_name, conn, index=False, if_exists='append')

    conn.commit()
    conn.close()


# Function to read tables from SQLite database into DataFrames
def read_tables_from_sqlite(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    tables = {}
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    for table_name in table_names:
        # Replace underscores with hyphens to get the original table name
        original_table_name = table_name[0].replace('_', '-')
        df = pd.read_sql_query(f"SELECT * FROM \"{table_name[0]}\"", conn)
        tables[original_table_name] = df

    conn.close()
    return tables

# Function to find column names mentioned in the question
def find_column_names(question, dfs):
    column_names = {}
    for table_name, df in dfs.items():
        matching_columns = []
        for column in df.columns:
            if column.lower() in question.lower():
                matching_columns.append(column)
        if matching_columns:
            column_names[table_name] = matching_columns
    return column_names

# Function to answer questions
async def answer_question(question, dfs):
    ic("Inside answer_question")
    column_names = find_column_names(question, dfs)
    ic(column_names)
    results = {}
    for table_name, df in dfs.items():
        if table_name in column_names:
            for column_name in column_names[table_name]:
                result = df[df[column_name] == 'desired_value']  # Modify as needed
                results[(table_name, column_name)] = result
    ic(results)
    return results

# Streamlit UI
st.title('Database Query Tool')

csv_dir = st.text_input('Enter directory path containing CSV files')

if st.button('Load CSV files'):
    if csv_dir and os.path.isdir(csv_dir):
        load_csv_to_sqlite(csv_dir, db_name)
        st.write("CSV files loaded into SQLite database successfully!")
    else:
        st.write("Please provide a valid directory path containing CSV files")

if st.button('Ask a question'):
    question = st.text_input('Ask a question')

    if os.path.isdir(csv_dir):
        dfs = read_tables_from_sqlite(db_name)
        answer = asyncio.run(answer_question(question, dfs))
        ic(answer)
        st.write(answer)
        
        for (table_name, column_name), result in answer.items():
            st.write(f"Results for {table_name} - {column_name}")
            st.write(result)
    else:
        st.write("Please provide a valid directory path containing CSV files")
