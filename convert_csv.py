import sqlite3
import pandas as pd
import numpy as np
import time
import csv


con= sqlite3.connect("db.sqlite3")
data= pd.read_sql_query("SELECT * FROM blog_rating",con)
#print(data)
data.to_csv('output.csv')
