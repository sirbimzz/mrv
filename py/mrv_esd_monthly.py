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


# In[3]:


# Getting Non-Bonny Offices data from Datatbase
df_Non_Bny_Off, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.Non_Bonny_Offices"""
        )


# In[4]:


# Getting Non-Bonny Offices data from Datatbase
df_GHG_Offices_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Offices_Monthly"""
        )


# In[5]:


for col in df_Non_Bny_Off.columns:
    df_Non_Bny_Off.loc[df_Non_Bny_Off[col] == 'nan', col] = 0


# In[6]:


# Creating a new dataframe to store GHG output
GHG_Offices_Monthly = pd.DataFrame(columns = ['RecordDate', 'UpdatedDate', 'UpdatedBy', 'PHC_NG_CO2e','PHC_Diesel_CO2e', 'PHC_CO2e', 'ABJ_NG_CO2e', 'ABJ_Diesel_CO2e','ABJ_CO2e', 'LTO_NG_CO2e', 'LTO_Diesel_CO2e', 'LTO_CO2e','LON_NG_CO2e'])


# In[7]:


# Calculating emissions for PHC_NG_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    NG_Conversion = iferror(lambda: float(df_Factors['Factor_Value']['NG_Conversion']),0)
    NG_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['NG_CO2']),0)
    PHC_NG = iferror(lambda: float(df_Non_Bny_Off['PHC_NG'][i]),0)
    PHC_NG_CO2e = iferror(lambda: PHC_NG * NG_Conversion * NG_CO2,0)
    GHG_Offices_Monthly.loc[i, 'PHC_NG_CO2e'] = PHC_NG_CO2e
    GHG_Offices_Monthly.loc[i, "RecordDate"] = df_Non_Bny_Off['RecordDate'][i]
    GHG_Offices_Monthly.loc[i, "UpdatedDate"] = datetime.today().strftime('%Y-%m-%d')
    GHG_Offices_Monthly.loc[i, "UpdatedBy"] = 'Admin'


# In[8]:


# Calculating emissions for PHC_Diesel_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    PHC_Diesel = iferror(lambda: float(df_Non_Bny_Off['PHC_Diesel'][i]),0)
    PHC_Diesel_CO2e = iferror(lambda: PHC_Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Offices_Monthly.loc[i, 'PHC_Diesel_CO2e'] = PHC_Diesel_CO2e


# In[9]:


# Calculating emissions for total PHC_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    GHG_Offices_Monthly.loc[i, 'PHC_CO2e'] = GHG_Offices_Monthly.loc[i, 'PHC_NG_CO2e'] + GHG_Offices_Monthly.loc[i, 'PHC_Diesel_CO2e']


# In[10]:


# Calculating emissions for ABJ_NG_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    GT_Efficiency = iferror(lambda: float(df_Factors['Factor_Value']['GT_Efficiency']),0)
    NG_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['NG_CO2']),0)
    ABJ_NG = iferror(lambda: float(df_Non_Bny_Off['ABJ_NG'][i]),0)
    ABJ_NG_CO2e = iferror(lambda: ABJ_NG/24 * GT_Efficiency * NG_CO2,0)
    GHG_Offices_Monthly.loc[i, 'ABJ_NG_CO2e'] = ABJ_NG_CO2e


# In[11]:


# Calculating emissions for ABJ_Diesel_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    ABJ_Diesel = iferror(lambda: float(df_Non_Bny_Off['ABJ_Diesel'][i]),0)
    ABJ_Diesel_CO2e = iferror(lambda: ABJ_Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Offices_Monthly.loc[i, 'ABJ_Diesel_CO2e'] = ABJ_Diesel_CO2e


# In[12]:


# Calculating emissions for total ABJ_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    GHG_Offices_Monthly.loc[i, 'ABJ_CO2e'] = GHG_Offices_Monthly.loc[i, 'ABJ_NG_CO2e'] + GHG_Offices_Monthly.loc[i, 'ABJ_Diesel_CO2e']


# In[13]:


# Calculating emissions for LTO_NG_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    NG_Conversion = iferror(lambda: float(df_Factors['Factor_Value']['NG_Conversion']),0)
    NG_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['NG_CO2']),0)
    LTO_NG = iferror(lambda: float(df_Non_Bny_Off['LTO_NG'][i]),0)
    LTO_NG_CO2e = iferror(lambda: LTO_NG * NG_Conversion * NG_CO2,0)
    GHG_Offices_Monthly.loc[i, 'LTO_NG_CO2e'] = LTO_NG_CO2e


# In[14]:


# Calculating emissions for LTO_Diesel_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    LTO_Diesel = iferror(lambda: float(df_Non_Bny_Off['LTO_Diesel'][i]),0)
    LTO_Diesel_CO2e = iferror(lambda: LTO_Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Offices_Monthly.loc[i, 'LTO_Diesel_CO2e'] = LTO_Diesel_CO2e


# In[15]:


# Calculating emissions for total LTO_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    GHG_Offices_Monthly.loc[i, 'LTO_CO2e'] = GHG_Offices_Monthly.loc[i, 'LTO_NG_CO2e'] + GHG_Offices_Monthly.loc[i, 'LTO_Diesel_CO2e']


# In[16]:


# Calculating emissions for LON_NG_CO2e and storing to dataframe for all months
for i in range(df_Non_Bny_Off.shape[0]):
    GT_Efficiency = iferror(lambda: float(df_Factors['Factor_Value']['GT_Efficiency']),0)
    NG_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['NG_CO2']),0)
    LON_NG = iferror(lambda: float(df_Non_Bny_Off['LON_NG'][i]),0)
    LON_NG_CO2e = iferror(lambda: LON_NG/24 * GT_Efficiency * NG_CO2,0)
    GHG_Offices_Monthly.loc[i, 'LON_NG_CO2e'] = LON_NG_CO2e


# In[17]:


# Posting all GHG entries to database
col_list = GHG_Offices_Monthly.columns
for i, row in GHG_Offices_Monthly.iterrows():
    record_date = GHG_Offices_Monthly.at[i, 'RecordDate']
    if df_GHG_Offices_Monthly.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in df_GHG_Offices_Monthly.iterrows():
            new_date = df_GHG_Offices_Monthly.at[j, 'RecordDate'] 
            if record_date.month==new_date.month and record_date.year==new_date.year:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Offices_Monthly.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        row_id = str(df_GHG_Offices_Monthly.at[j, 'id'])
        update_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Offices_Monthly",cols_vals=cols_vals,row_id = row_id)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Offices_Monthly.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Offices_Monthly",cols=cols,vals=vals)

