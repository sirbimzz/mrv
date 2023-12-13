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


# Getting Projects data from Datatbase
GHG_Plant, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Plant"""
        )


# In[4]:


# Getting GHG_Projects_Monthly data from Datatbase
df_GHG_Plant_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Plant_Monthly"""
        )


# In[5]:


df_GHG_Plant_Monthly.columns


# In[6]:


# Creating a new dataframe to store GHG output
GHG_Plant_Monthly = pd.DataFrame(columns = ['RecordDate', 'UpdatedDate', 'UpdatedBy', 'Waste_CO2',
       'Waste_N2O', 'Waste_CH4', 'Waste_CO2e', 'Mobile_CO2', 'Mobile_N2O',
       'Mobile_CH4', 'Mobile_CO2e', 'Fugitives_CH4', 'Fugitives_CO2e'])


# In[7]:


# Calculating emissions for Waste_CO2 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Fired_Heaters_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Fired_Heaters_CO2']),0)
    Fuel_Gas = iferror(lambda: float(GHG_Plant['Fuel_Gas'][i]),0)
    Waste_CO2 = iferror(lambda: Fuel_Gas * Fired_Heaters_CO2,0)
    GHG_Plant_Monthly.loc[i, 'Waste_CO2'] = Waste_CO2
    GHG_Plant_Monthly.loc[i, "RecordDate"] = GHG_Plant['RecordDate'][i]
    GHG_Plant_Monthly.loc[i, "UpdatedDate"] = datetime.today().strftime('%Y-%m-%d')
    GHG_Plant_Monthly.loc[i, "UpdatedBy"] = 'Admin'


# In[8]:


# Calculating emissions for Waste_N2O and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Fired_Heaters_N2O = iferror(lambda: float(df_Factors['Factor_Value']['Fired_Heaters_N2O']),0)
    Fuel_Gas = iferror(lambda: float(GHG_Plant['Fuel_Gas'][i]),0)
    Waste_N2O = iferror(lambda: Fuel_Gas * Fired_Heaters_N2O,0)
    GHG_Plant_Monthly.loc[i, 'Waste_N2O'] = Waste_N2O


# In[9]:


# Calculating emissions for Waste_CH4 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Fired_Heaters_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['Fired_Heaters_CH4']),0)
    Fuel_Gas = iferror(lambda: float(GHG_Plant['Fuel_Gas'][i]),0)
    Waste_CH4 = iferror(lambda: Fuel_Gas * Fired_Heaters_CH4,0)
    GHG_Plant_Monthly.loc[i, 'Waste_CH4'] = Waste_CH4


# In[10]:


# Calculating emissions for Waste_CO2e and storing to dataframe for all months
for i in range(GHG_Plant_Monthly.shape[0]):
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)    
    Waste_CO2 = iferror(lambda: float(GHG_Plant_Monthly['Waste_CO2'][i]),0)
    Waste_N2O = iferror(lambda: float(GHG_Plant_Monthly['Waste_N2O'][i]),0)
    Waste_CH4 = iferror(lambda: float(GHG_Plant_Monthly['Waste_CH4'][i]),0)
    
    Waste_CO2e = iferror(lambda: Waste_CO2+(Waste_N2O*GWP100_N2O)+(Waste_CH4*GWP100_CH4),0)
    GHG_Plant_Monthly.loc[i, 'Waste_CO2e'] = Waste_CO2e


# In[11]:


# Calculating emissions for Mobile_CO2 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CO2']),0)
    Diesel = iferror(lambda: float(GHG_Plant['Diesel'][i]),0)
    Mobile_CO2 = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CO2,0)
    GHG_Plant_Monthly.loc[i, 'Mobile_CO2'] = Mobile_CO2


# In[12]:


# Calculating emissions for Mobile_N2O and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_N2O = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_N2O']),0)
    Diesel = iferror(lambda: float(GHG_Plant['Diesel'][i]),0)
    Mobile_N2O = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_N2O,0)
    GHG_Plant_Monthly.loc[i, 'Mobile_N2O'] = Mobile_N2O


# In[13]:


# Calculating emissions for Mobile_CH4 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Diesel_Density = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_Density']),0)
    Diesel_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['Diesel_CH4']),0)
    Diesel = iferror(lambda: float(GHG_Plant['Diesel'][i]),0)
    Mobile_CH4 = iferror(lambda: Diesel/1000 * Diesel_Density/1000 * Diesel_CH4,0)
    GHG_Plant_Monthly.loc[i, 'Mobile_CH4'] = Mobile_CH4


# In[14]:


# Calculating emissions for Mobile_CO2e and storing to dataframe for all months
for i in range(GHG_Plant_Monthly.shape[0]):
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)    
    Mobile_CO2 = iferror(lambda: float(GHG_Plant_Monthly['Mobile_CO2'][i]),0)
    Mobile_N2O = iferror(lambda: float(GHG_Plant_Monthly['Mobile_N2O'][i]),0)
    Mobile_CH4 = iferror(lambda: float(GHG_Plant_Monthly['Mobile_CH4'][i]),0)
    
    Mobile_CO2e = iferror(lambda: Mobile_CO2+(Mobile_N2O*GWP100_N2O)+(Mobile_CH4*GWP100_CH4),0)
    GHG_Plant_Monthly.loc[i, 'Mobile_CO2e'] = Mobile_CO2e


# In[15]:


# Calculating emissions for Fugitives_CH4 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    Fugitives_CH4 = iferror(lambda: float(GHG_Plant['Fugitives_CH4'][i]),0)
    GHG_Plant_Monthly.loc[i, 'Fugitives_CH4'] = Fugitives_CH4


# In[16]:


# Calculating emissions for Fugitives_CO2e and storing to dataframe for all months
for i in range(GHG_Plant_Monthly.shape[0]):
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)
    Fugitives_CH4 = iferror(lambda: float(GHG_Plant_Monthly['Fugitives_CH4'][i]),0)
    Fugitives_CO2e = Fugitives_CH4 * GWP100_CH4
    GHG_Plant_Monthly.loc[i, 'Fugitives_CO2e'] = Fugitives_CO2e


# In[17]:


# Calculating emissions for Flare_CO2 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    F_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['Flare_CO2']),0)
    Gas_Flared = iferror(lambda: float(GHG_Plant['Gas_Flared'][i]),0)
    Flare_CO2 = iferror(lambda: Gas_Flared * F_CO2,0)
    GHG_Plant_Monthly.loc[i, 'Flare_CO2'] = Flare_CO2
    GHG_Plant_Monthly.loc[i, "RecordDate"] = GHG_Plant['RecordDate'][i]
    GHG_Plant_Monthly.loc[i, "UpdatedDate"] = datetime.today().strftime('%Y-%m-%d')
    GHG_Plant_Monthly.loc[i, "UpdatedBy"] = 'Admin'


# In[18]:


# Calculating emissions for Flare_N2O and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    F_N2O = iferror(lambda: float(df_Factors['Factor_Value']['Flare_N2O']),0)
    Gas_Flared = iferror(lambda: float(GHG_Plant['Gas_Flared'][i]),0)
    Flare_N2O = iferror(lambda: Gas_Flared * F_N2O,0)
    GHG_Plant_Monthly.loc[i, 'Flare_N2O'] = Flare_N2O


# In[19]:


# Calculating emissions for Flare_CH4 and storing to dataframe for all months
for i in range(GHG_Plant.shape[0]):
    F_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['Flare_CH4']),0)
    Gas_Flared = iferror(lambda: float(GHG_Plant['Gas_Flared'][i]),0)
    Flare_CH4 = iferror(lambda: Gas_Flared * F_CH4,0)
    GHG_Plant_Monthly.loc[i, 'Flare_CH4'] = Flare_CH4


# In[20]:


# Calculating emissions for Flare_CO2e and storing to dataframe for all months
for i in range(GHG_Plant_Monthly.shape[0]):
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)    
    Flare_CO2 = iferror(lambda: float(GHG_Plant_Monthly['Flare_CO2'][i]),0)
    Flare_N2O = iferror(lambda: float(GHG_Plant_Monthly['Flare_N2O'][i]),0)
    Flare_CH4 = iferror(lambda: float(GHG_Plant_Monthly['Flare_CH4'][i]),0)
    
    Flare_CO2e = iferror(lambda: Flare_CO2+(Flare_N2O*GWP100_N2O)+(Flare_CH4*GWP100_CH4),0)
    GHG_Plant_Monthly.loc[i, 'Flare_CO2e'] = Flare_CO2e


# In[21]:


# Posting all GHG entries to database
col_list = GHG_Plant_Monthly.columns
for i, row in GHG_Plant_Monthly.iterrows():
    record_date = GHG_Plant_Monthly.at[i, 'RecordDate']
    if df_GHG_Plant_Monthly.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in df_GHG_Plant_Monthly.iterrows():
            new_date = df_GHG_Plant_Monthly.at[j, 'RecordDate'] 
            if record_date.month==new_date.month and record_date.year==new_date.year:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Plant_Monthly.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        row_id = str(df_GHG_Plant_Monthly.at[j, 'id'])
        update_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Plant_Monthly",cols_vals=cols_vals,row_id = row_id)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Plant_Monthly.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Plant_Monthly",cols=cols,vals=vals)


# In[ ]:




