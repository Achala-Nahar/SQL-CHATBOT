# import sqlite3

# connection=sqlite3.connect('student.db')
# cursor=connection.cursor() ##cursor object to insert record,create table

# table_info="""

# create table Student(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT))

# """

# cursor.execute(table_info)
# # Insert some more records
# cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
# cursor.execute('''Insert Into STUDENT values('John','Data Science','B',100)''')
# cursor.execute('''Insert Into STUDENT values('Mukesh','Data Science','A',86)''')
# cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
# cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''') 

# ##Display all the records
# print("The inserted records are: ")
# rows = cursor.execute('''Selcect * FROM STUDENT''')

# for row in rows:
#     print(row)

# connection.commit()
# connection.close()

import sqlite3

# Connect to the database (or create it)
connection = sqlite3.connect('student.db')
cursor = connection.cursor()

# Create table (only once)
table_info = """    
CREATE TABLE IF NOT EXISTS Student (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""
cursor.execute(table_info)

# Insert records
cursor.execute('''INSERT INTO Student VALUES ('Krish', 'Data Science', 'A', 90)''')
cursor.execute('''INSERT INTO Student VALUES ('John', 'Data Science', 'B', 100)''')
cursor.execute('''INSERT INTO Student VALUES ('John', 'Data Science', 'B', 100)''')
cursor.execute('''INSERT INTO Student VALUES ('Jacob', 'DEVOPS', 'A', 50)''')
cursor.execute('''INSERT INTO Student VALUES ('Dipesh', 'DEVOPS', 'A', 35)''')
print("The inserted records are:")
rows = cursor.execute('''SELECT * FROM Student''')
for row in rows:
    print(row)

# Save changes and close connection
connection.commit()
connection.close()