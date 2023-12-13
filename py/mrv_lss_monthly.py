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


# In[3]:


df_Factors


# In[4]:


# Getting Aviation data from Datatbase
GHG_Aviation, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Aviation"""
        )


# In[5]:


# Getting Passenger boats data from Datatbase
GHG_Passenger_Boats, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Passenger_Boats"""
        )


# In[6]:


# Getting Tug boats data from Datatbase
GHG_Tug_Boats, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Tug_Boats"""
        )


# In[7]:


# Getting Escort boats data from Datatbase
GHG_Escort_Boats, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Escort_Boats"""
        )


# In[8]:


# Getting Bonny Fleet boats data from Datatbase
GHG_Bonny_Fleet, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Bonny_Fleet"""
        )


# In[9]:


# Getting Non-Bonny Fleet boats data from Datatbase
GHG_Non_Bonny_Fleet, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Non_Bonny_Fleet"""
        )


# In[10]:


# Getting Non-Bonny Logistics data from Datatbase
df_GHG_Logistics_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Logistics_Monthly"""
        )


# In[11]:


df_GHG_Logistics_Monthly.columns


# In[12]:


# Creating a new dataframe to store GHG output
GHG_Logistics_Monthly = pd.DataFrame(columns = ['RecordDate', 'UpdatedDate', 'UpdatedBy', 'Aviation_CO2e',
       'Av_Per_Passenger', 'Av_Per_Distance', 'Passenger_Boats_CO2e',
       'P_Boats_Per_Passenger', 'P_Boats_Per_Distance', 'Tug_Boats_CO2e',
       'T_Boats_Per_Passenger', 'T_Boats_Per_Distance', 'Long_Escort_CO2e',
       'L_Escort_Per_Passenger', 'L_Escort_Per_Distance',
       'Passenger_Escort_CO2e', 'P_Escort_Per_Passenger',
       'P_Escort_Per_Distance', 'Escort_CO2e', 'Bny_Fleet_Diesel_CO2e',
       'Bny_Fleet_Petrol_CO2e', 'Bny_Fleet_CO2e', 'Bny_Fleet_Per_Passenger',
       'Bny_Fleet_Per_Distance', 'Non_Bny_Fleet_Diesel_CO2e',
       'Non_Bny_Fleet_Petrol_CO2e', 'Non_Bny_Fleet_CO2e',
       'Non_Bny_Fleet_Per_Passenger', 'Non_Bny_Fleet_Per_Distance'])


# In[13]:


# Calculating emissions for Aviation_CO2e and storing to dataframe for all months
for i, row in GHG_Aviation.iterrows():
    Jet_Fuel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Jet_Fuel_Density']),0)
    Jet_Fuel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Jet_Fuel_CO2']),0)
    Jet_Fuel = iferror(lambda: float(GHG_Aviation['Jet_Fuel'][i]),0)
    Tot_Passengers = iferror(lambda: float(GHG_Aviation['Tot_Passengers'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Aviation['Tot_Distance'][i]),0)
    Aviation_CO2e = iferror(lambda: Jet_Fuel/1000 * Jet_Fuel_Density/1000 * Jet_Fuel_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Aviation_CO2e'] = Aviation_CO2e
    GHG_Logistics_Monthly.loc[i, 'Av_Per_Passenger'] = iferror(lambda: Aviation_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'Av_Per_Distance'] = iferror(lambda: Aviation_CO2e/Tot_Distance,0)
    GHG_Logistics_Monthly.loc[i, "RecordDate"] = GHG_Aviation['RecordDate'][i]
    GHG_Logistics_Monthly.loc[i, "UpdatedDate"] = datetime.today().strftime('%Y-%m-%d')
    GHG_Logistics_Monthly.loc[i, "UpdatedBy"] = 'Admin'


# In[14]:


# Calculating emissions for Passenger_Boats_CO2e and storing to dataframe for all months
for i, row in GHG_Passenger_Boats.iterrows():
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Passenger_Boats['Diesel'][i]),0)
    Tot_Passengers = iferror(lambda: float(GHG_Passenger_Boats['Tot_Passengers'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Passenger_Boats['Tot_Distance'][i]),0)
    Passenger_Boats_CO2e = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Passenger_Boats_CO2e'] = Passenger_Boats_CO2e
    GHG_Logistics_Monthly.loc[i, 'P_Boats_Per_Passenger'] = iferror(lambda: Passenger_Boats_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'P_Boats_Per_Distance'] = iferror(lambda: Passenger_Boats_CO2e/Tot_Distance,0)


# In[15]:


GHG_Tug_Boats


# In[16]:


# Calculating emissions for Tug_Boats_CO2e and storing to dataframe for all months
for i, row in GHG_Tug_Boats.iterrows():
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Tug_Boats['Diesel'][i]),0)
    Tot_Passengers = iferror(lambda: float(GHG_Tug_Boats['Tot_Passengers'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Tug_Boats['Tot_Distance'][i]),0)
    Tug_Boats_CO2e = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Tug_Boats_CO2e'] = Tug_Boats_CO2e
    GHG_Logistics_Monthly.loc[i, 'T_Boats_Per_Passenger'] = iferror(lambda: Tug_Boats_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'T_Boats_Per_Distance'] = iferror(lambda: Tug_Boats_CO2e/Tot_Distance,0)


# In[17]:


# Calculating emissions for Escort_CO2e and storing to dataframe for all months
for i, row in GHG_Escort_Boats.iterrows():
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Escort_Boats['Long_Escort_Diesel'][i]),0)
    Tot_Passengers = iferror(lambda: float(GHG_Escort_Boats['Long_Escort_Tot_Passengers	'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Escort_Boats['Long_Escort_Tot_Distance'][i]),0)
    Long_Escort_CO2e = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Long_Escort_CO2e'] = Long_Escort_CO2e
    GHG_Logistics_Monthly.loc[i, 'L_Escort_Per_Passenger'] = iferror(lambda: Long_Escort_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'L_Escort_Per_Distance'] = iferror(lambda: Long_Escort_CO2e/Tot_Distance,0)
    
    # Calculating emissions for Passenger_Escort_CO2e and storing to dataframe for all months
    Gasoline_Density = iferror(lambda: float(df_Factors['Factor_Value']['Gasoline_Density']),0)
    Petrol_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Petrol_CO2']),0)
    Petrol = iferror(lambda: float(GHG_Escort_Boats['Passenger_Escort_Petrol'][i]),0)
    Tot_Passengers = iferror(lambda: float(GHG_Escort_Boats['Passenger_Escort_Tot_Passengers'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Escort_Boats['Passenger_Escort_Tot_Distance'][i]),0)
    Passenger_Escort_CO2e = iferror(lambda: Petrol/1000 * Gasoline_Density/1000 * Petrol_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Passenger_Escort_CO2e'] = Passenger_Escort_CO2e
    GHG_Logistics_Monthly.loc[i, 'P_Escort_Per_Passenger'] = iferror(lambda: Passenger_Escort_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'P_Escort_Per_Distance'] = iferror(lambda: Passenger_Escort_CO2e/Tot_Distance,0)
    
    GHG_Logistics_Monthly.loc[i, 'Escort_CO2e'] = Long_Escort_CO2e + Passenger_Escort_CO2e


# In[18]:


# Calculating emissions for Bny_Fleet_CO2e and storing to dataframe for all months
for i, row in GHG_Bonny_Fleet.iterrows():
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Bonny_Fleet['Diesel'][i]),0)
    Bny_Fleet_Diesel_CO2e = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Bny_Fleet_Diesel_CO2e'] = Bny_Fleet_Diesel_CO2e
    
    # Calculating emissions for Bny_Fleet_Petrol_CO2e and storing to dataframe for all months
    Gasoline_Density = iferror(lambda: float(df_Factors['Factor_Value']['Gasoline_Density']),0)
    Petrol_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Petrol_CO2']),0)
    Petrol = iferror(lambda: float(GHG_Bonny_Fleet['Petrol'][i]),0)
    Bny_Fleet_Petrol_CO2e = iferror(lambda: Petrol/1000 * Gasoline_Density/1000 * Petrol_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Bny_Fleet_Petrol_CO2e'] = Bny_Fleet_Petrol_CO2e
    
    Bny_Fleet_CO2e = Bny_Fleet_Diesel_CO2e + Bny_Fleet_Petrol_CO2e    
    GHG_Logistics_Monthly.loc[i, 'Bny_Fleet_CO2e'] = Bny_Fleet_CO2e
    
    Tot_Passengers = iferror(lambda: float(GHG_Bonny_Fleet['Tot_Passengers'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Bonny_Fleet['Tot_Distance'][i]),0)    
    GHG_Logistics_Monthly.loc[i, 'Bny_Fleet_Per_Passenger'] = iferror(lambda: Bny_Fleet_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'Bny_Fleet_Per_Distance'] = iferror(lambda: Bny_Fleet_CO2e/Tot_Distance,0)


# In[19]:


# Calculating emissions for Non_Bny_Fleet_CO2e and storing to dataframe for all months
for i, row in GHG_Bonny_Fleet.iterrows():
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Non_Bonny_Fleet['Diesel'][i]),0)
    Non_Bny_Fleet_Diesel_CO2e = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Non_Bny_Fleet_Diesel_CO2e'] = Non_Bny_Fleet_Diesel_CO2e
    
    # Calculating emissions for Non_Bny_Fleet_Petrol_CO2e and storing to dataframe for all months
    Gasoline_Density = iferror(lambda: float(df_Factors['Factor_Value']['Gasoline_Density']),0)
    Petrol_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Petrol_CO2']),0)
    Petrol = iferror(lambda: float(GHG_Non_Bonny_Fleet['Petrol'][i]),0)
    Non_Bny_Fleet_Petrol_CO2e = iferror(lambda: Petrol/1000 * Gasoline_Density/1000 * Petrol_CO2,0)
    GHG_Logistics_Monthly.loc[i, 'Non_Bny_Fleet_Petrol_CO2e'] = Non_Bny_Fleet_Petrol_CO2e
    
    Non_Bny_Fleet_CO2e = Non_Bny_Fleet_Diesel_CO2e + Non_Bny_Fleet_Petrol_CO2e
    GHG_Logistics_Monthly.loc[i, 'Non_Bny_Fleet_CO2e'] = Non_Bny_Fleet_CO2e
    
    Tot_Passengers = iferror(lambda: float(GHG_Non_Bonny_Fleet['Tot_Passengers'][i]),0)
    Tot_Distance = iferror(lambda: float(GHG_Non_Bonny_Fleet['Tot_Distance'][i]),0)    
    GHG_Logistics_Monthly.loc[i, 'Non_Bny_Fleet_Per_Passenger'] = iferror(lambda: Non_Bny_Fleet_CO2e/Tot_Passengers,0)
    GHG_Logistics_Monthly.loc[i, 'Non_Bny_Fleet_Per_Distance'] = iferror(lambda: Non_Bny_Fleet_CO2e/Tot_Distance,0)


# In[20]:


GHG_Logistics_Monthly


# In[21]:


df_GHG_Logistics_Monthly.shape[0]


# In[22]:


# Posting all GHG entries to database
col_list = GHG_Logistics_Monthly.columns
for i, row in GHG_Logistics_Monthly.iterrows():
    record_date = GHG_Logistics_Monthly.at[i, 'RecordDate']
    if df_GHG_Logistics_Monthly.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in df_GHG_Logistics_Monthly.iterrows():
            new_date = df_GHG_Logistics_Monthly.at[j, 'RecordDate'] 
            if record_date.month==new_date.month and record_date.year==new_date.year:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Logistics_Monthly.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        row_id = str(df_GHG_Logistics_Monthly.at[j, 'id'])
        update_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Logistics_Monthly",cols_vals=cols_vals,row_id = row_id)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Logistics_Monthly.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Logistics_Monthly",cols=cols,vals=vals)


# In[ ]:




