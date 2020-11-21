# =============================================================================
# File name: create_tables.py
# Author: Andy Ortiz
# Date created: 11/17/2020
# Date last modified: 11/73/2020
# Python Version: 3.8.5
# =============================================================================

# =============================================================================
# Imports
# =============================================================================

import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# id INTEGER PRIMARY KEY means it will be an auto-incrementing id
create_table = "CREATE TABLE if NOT EXISTS students (id INTEGER PRIMARY KEY)"
cursor.execute(create_table)

# To work with SQLAlchemy, we must run python create_tables.py in its same directory
connection.commit()
connection.close()
