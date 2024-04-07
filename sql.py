import sqlite3
import pandas as pd
import os

# #connect to sqlite
# connection = sqlite3.connect('student.db')

df = pd.read_csv("test_data.csv")

conn = sqlite3.connect('test_db.sqlite')
c = conn.cursor()

# # Iterate over each CSV file
# csv_folder = "C:\Users\admin2\Desktop\Swati\soc_usecase\Sample_Data_TCS_SOC (1)"
# for file in os.listdir(csv_folder):
#     if file.endswith(".csv"):
#         file_path = os.path.join(csv_folder, file)
#         table_name = os.path.splitext(file)[0]  # Use CSV file name as table name

#         # Read CSV into pandas DataFrame
#         df = pd.read_csv(file_path)

#         df.to_sql('Test', conn, if_exists='replace', index=False)

# #creating cursor object to insert, record, create table, retrieve
# cursor = connection.cursor()

# #create the table
# table_info = """
# Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), 
# SECTION VARCHAR(25), MARKS INT);
# """

# cursor.execute(table_info)

#display all the records
print("The inserted records are")

data = c.execute('''Select * from Test''')
# for table_name in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
#     data = c.execute(f"SELECT * FROM {table_name[0]}")
#     print(f"Records from table: {table_name[0]}")

for row in data:
    print(row)

conn.commit()
conn.close()