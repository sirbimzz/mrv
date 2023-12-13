#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-

# PI server connectivity related library
from win32com.client.dynamic import Dispatch

# Library for handling datetime data
from datetime import datetime, timedelta
import pandas as pd
from os import path
import smtplib
import math
import pyodbc
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from datetime import timedelta
from email.mime.text import MIMEText
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta

def conn_sql_server(server, db, user, pwd, sql_string):
    """
    Establish connection to SQL Server and return data as DataFrame
    Parameters
    ----------
    server : TYPE
        DESCRIPTION.
    db : TYPE
        DESCRIPTION.
    user : TYPE
        DESCRIPTION.
    pwd : TYPE
        DESCRIPTION.
    sql_string : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    df = pd.DataFrame()
    try:
        conn = pyodbc.connect(Driver="{SQL Server}", Server=server, Database=db, Trusted_Connection="NO", User=user, Password=pwd)
        print("connection with {} successful".format(db))
        df = pd.read_sql_query(sql_string, conn)
        success = True
    except Exception as e:
        print("connection with {} failed: ->{}".format(db, str(e)))   
        success = False
    return df, success

def insert_SQL(server,db,user,pwd,tbl,cols,vals):
    conn = pyodbc.connect(Driver="{SQL Server}", Server=server, Database=db, Trusted_Connection="NO", User=user, Password=pwd)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO """ + tbl + """ (""" + cols + """)""" + """ VALUES(""" + vals + """);""")
    conn.commit()
    
def update_SQL(server,db,user,pwd,tbl,cols_vals,row_id):
    conn = pyodbc.connect(Driver="{SQL Server}", Server=server, Database=db, Trusted_Connection="NO", User=user, Password=pwd)
    cursor = conn.cursor()
    cursor.execute("""UPDATE """ + tbl + """ SET """ + cols_vals + """ WHERE id = """ + row_id + """;""")
    conn.commit()

def tag_list(kpi, trains):
    tags = []
    for kpi_tags in kpi:
        for train_num in trains:
            tags = tags + [
                str(train_num) + kpi_tags.split(':')[0] + ':' + str(train_num) + kpi_tags.split(':')[1]
                ]
    return tags

def iferror(success, failure, *exceptions):
    try:
        return success()
    except Exception as e:
        return failure    


# In[2]:


# Getting GHG Factors from Datatbase
df_Factors, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Factors"""
        )
df_Factors = df_Factors.set_index('Factor_Name')


# In[4]:


# Getting Projects data from Datatbase
GHG_Projects, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Projects"""
        )


# In[5]:


# Getting GHG_Projects_Monthly data from Datatbase
df_GHG_Projects_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Projects_Monthly"""
        )


# In[6]:


df_GHG_Projects_Monthly.columns


# In[7]:


# Creating a new dataframe to store GHG output
GHG_Projects_Monthly = pd.DataFrame(columns = ['RecordDate', 'UpdatedDate', 'UpdatedBy', 'Diesel_CO2e', 'Petrol_CO2e', 'Projects_CO2e'])


# In[8]:


# Calculating emissions for Diesel_CO2e and storing to dataframe for all months
for i in range(GHG_Projects.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Projects['Diesel'][i]),0)
    Diesel_CO2e = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Projects_Monthly.loc[i, 'Diesel_CO2e'] = Diesel_CO2e
    GHG_Projects_Monthly.loc[i, "RecordDate"] = GHG_Projects['RecordDate'][i]
    GHG_Projects_Monthly.loc[i, "UpdatedDate"] = datetime.today().strftime('%Y-%m-%d')
    GHG_Projects_Monthly.loc[i, "UpdatedBy"] = 'Admin'


# In[9]:


# Calculating emissions for Petrol_CO2e and storing to dataframe for all months
for i in range(GHG_Projects.shape[0]):
    Gasoline_Density = iferror(lambda: float(df_Factors['Factor_Value']['Gasoline_Density']),0)
    Petrol_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Petrol_CO2']),0)
    Petrol = iferror(lambda: float(GHG_Projects['Petrol'][i]),0)
    Petrol_CO2e = iferror(lambda: Petrol/1000 * Gasoline_Density/1000 * Petrol_CO2,0)
    GHG_Projects_Monthly.loc[i, 'Petrol_CO2e'] = Petrol_CO2e


# In[10]:


# Calculating emissions for Total CO2e and storing to dataframe for all months
for i in range(GHG_Projects.shape[0]):
    Diesel_CO2e = GHG_Projects_Monthly.loc[i, 'Diesel_CO2e']
    Petrol_CO2e = GHG_Projects_Monthly.loc[i, 'Petrol_CO2e']
    GHG_Projects_Monthly.loc[i, 'Projects_CO2e'] = Diesel_CO2e + Petrol_CO2e


# In[12]:


# Posting all GHG entries to database
col_list = GHG_Projects_Monthly.columns
for i, row in GHG_Projects_Monthly.iterrows():
    record_date = GHG_Projects_Monthly.at[i, 'RecordDate']
    if df_GHG_Projects_Monthly.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in df_GHG_Projects_Monthly.iterrows():
            new_date = df_GHG_Projects_Monthly.at[j, 'RecordDate'] 
            if record_date.month==new_date.month and record_date.year==new_date.year:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Projects_Monthly.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        row_id = str(df_GHG_Projects_Monthly.at[j, 'id'])
        update_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Projects_Monthly",cols_vals=cols_vals,row_id = row_id)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Projects_Monthly.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Projects_Monthly",cols=cols,vals=vals)


# In[ ]:




