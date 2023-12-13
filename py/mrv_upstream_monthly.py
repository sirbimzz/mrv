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


# Getting SPDC data from Datatbase
GHG_SPDC, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_SPDC"""
        )


# In[5]:


# Getting TEPNG data from Datatbase
GHG_TEPNG, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_TEPNG"""
        )


# In[6]:


# Getting NAOC data from Datatbase
GHG_NAOC, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_NAOC"""
        )


# In[7]:


# Getting GHG_Upstream data from Datatbase
df_GHG_Upstream, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Upstream"""
        )


# In[8]:


# Calculating emissions for SPDC_CO2 and storing to dataframe for all months
GHG_Upstream = pd.DataFrame()
for i in range(GHG_SPDC.shape[0]):
    Combustion_CO2 = iferror(lambda: float(GHG_SPDC['Combustion_CO2'][i]),0)
    Flaring_CO2 = iferror(lambda: float(GHG_SPDC['Flaring_CO2'][i]),0)
    Fugitives_CO2 = iferror(lambda: float(GHG_SPDC['Fugitives_CO2'][i]),0)
    Venting_CO2 = iferror(lambda: float(GHG_SPDC['Venting_CO2'][i]),0)
    Indirect_CO2 = iferror(lambda: float(GHG_SPDC['Indirect_CO2'][i]),0)
    GHG_Upstream.loc[i, "RecordDate"] = GHG_SPDC['RecordDate'][i]
    GHG_Upstream.loc[i, "UpdatedDate"] = datetime.today().strftime('%Y-%m-%d')
    GHG_Upstream.loc[i, "UpdatedBy"] = 'Admin'
    GHG_Upstream.loc[i, 'SPDC_CO2'] = Combustion_CO2+Flaring_CO2+Fugitives_CO2+Indirect_CO2


# In[9]:


# Calculating emissions for SPDC_N2O and storing to dataframe for all months
for i in range(GHG_SPDC.shape[0]):
    Combustion_N2O = iferror(lambda: float(GHG_SPDC['Combustion_N2O'][i]),0)
    Flaring_N2O = iferror(lambda: float(GHG_SPDC['Flaring_N2O'][i]),0)
    GHG_Upstream.loc[i, 'SPDC_N2O'] = Combustion_N2O+Flaring_N2O


# In[10]:


# Calculating emissions for SPDC_CH4 and storing to dataframe for all months
for i in range(GHG_SPDC.shape[0]):
    Fugitives_CH4 = iferror(lambda: float(GHG_SPDC['Fugitives_CH4'][i]),0)
    Venting_CH4 = iferror(lambda: float(GHG_SPDC['Venting_CH4'][i]),0)
    GHG_Upstream.loc[i, 'SPDC_CH4'] = Fugitives_CH4+Venting_CH4


# In[11]:


# Creating a new dataframe to store GHG output
# GHG_Upstream = pd.DataFrame(columns = ['RecordDate', 'UpdatedDate', 'UpdatedBy', 'SPDC_CO2', 'SPDC_N2O',
#        'SPDC_CH4', 'SPDC_GTS_CH4', 'SPDC_CO2e', 'TEPNG_CO2', 'TEPNG_N2O',
#        'TEPNG_CH4', 'TEPNG_GTS_CH4', 'TEPNG_CO2e', 'NAOC_CO2', 'NAOC_N2O',
#        'NAOC_CH4', 'NAOC_GTS_CH4', 'NAOC_CO2e', 'SPDC_GTS_CO2e',
#        'TEPNG_GTS_CO2e', 'NAOC_GTS_CO2e'])


# In[12]:


# Calculating emissions for SPDC_GTS_CH4 and storing to dataframe for all months
for i in range(GHG_SPDC.shape[0]):
    GTS_Fugitives_CH4 = iferror(lambda: float(GHG_SPDC['GTS_Fugitives_CH4'][i]),0)
    GTS_Venting_CH4 = iferror(lambda: float(GHG_SPDC['GTS_Venting_CH4'][i]),0)
    GHG_Upstream.loc[i, 'SPDC_GTS_CH4'] = GTS_Fugitives_CH4+GTS_Venting_CH4


# In[13]:


# Calculating emissions for SPDC_CO2e, SPDC_GTS_CO2e and storing to dataframe for all months
for i in range(GHG_Upstream.shape[0]):
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)
    SPDC_CO2 = iferror(lambda: float(GHG_Upstream['SPDC_CO2'][i]),0)
    SPDC_N2O = iferror(lambda: float(GHG_Upstream['SPDC_N2O'][i]),0)
    SPDC_CH4 = iferror(lambda: float(GHG_Upstream['SPDC_CH4'][i]),0)
    SPDC_GTS_CH4 = iferror(lambda: float(GHG_Upstream['SPDC_GTS_CH4'][i]),0)
    
    GHG_Upstream.loc[i, 'SPDC_CO2e'] = SPDC_CO2+SPDC_N2O*GWP100_N2O+SPDC_CH4*GWP100_CH4+SPDC_GTS_CH4*GWP100_CH4
    GHG_Upstream.loc[i, 'SPDC_GTS_CO2e'] = SPDC_GTS_CH4*GWP100_CH4


# In[14]:


# Calculating emissions for TEPNG_CO2 and storing to dataframe for all months
for i in range(GHG_TEPNG.shape[0]):
    Combustion_CO2 = iferror(lambda: float(GHG_TEPNG['Combustion_CO2'][i]),0)
    Flaring_CO2 = iferror(lambda: float(GHG_TEPNG['Flaring_CO2'][i]),0)
    Fugitives_CO2 = iferror(lambda: float(GHG_TEPNG['Fugitives_CO2'][i]),0)
    Venting_CO2 = iferror(lambda: float(GHG_TEPNG['Venting_CO2'][i]),0)
    Indirect_CO2 = iferror(lambda: float(GHG_TEPNG['Indirect_CO2'][i]),0)
    GHG_Upstream.loc[i, 'TEPNG_CO2'] = Combustion_CO2+Flaring_CO2+Fugitives_CO2+Indirect_CO2


# In[15]:


# Calculating emissions for TEPNG_N2O and storing to dataframe for all months
for i in range(GHG_TEPNG.shape[0]):
    Combustion_N2O = iferror(lambda: float(GHG_TEPNG['Combustion_N2O'][i]),0)
    Flaring_N2O = iferror(lambda: float(GHG_TEPNG['Flaring_N2O'][i]),0)
    GHG_Upstream.loc[i, 'TEPNG_N2O'] = Combustion_N2O+Flaring_N2O


# In[16]:


# Calculating emissions for TEPNG_CH4 and storing to dataframe for all months
for i in range(GHG_TEPNG.shape[0]):
    Fugitives_CH4 = iferror(lambda: float(GHG_TEPNG['Fugitives_CH4'][i]),0)
    Venting_CH4 = iferror(lambda: float(GHG_TEPNG['Venting_CH4'][i]),0)
    GHG_Upstream.loc[i, 'TEPNG_CH4'] = Fugitives_CH4+Venting_CH4


# In[17]:


# Calculating emissions for TEPNG_GTS_CH4 and storing to dataframe for all months
for i in range(GHG_TEPNG.shape[0]):
    GTS_Fugitives_CH4 = iferror(lambda: float(GHG_TEPNG['GTS_Fugitives_CH4'][i]),0)
    GTS_Venting_CH4 = iferror(lambda: float(GHG_TEPNG['GTS_Venting_CH4'][i]),0)
    GHG_Upstream.loc[i, 'TEPNG_GTS_CH4'] = GTS_Fugitives_CH4+GTS_Venting_CH4


# In[18]:


# Calculating emissions for TEPNG_CO2e, TEPNG_GTS_CO2e and storing to dataframe for all months
for i in range(GHG_Upstream.shape[0]):
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)
    TEPNG_CO2 = iferror(lambda: float(GHG_Upstream['TEPNG_CO2'][i]),0)
    TEPNG_N2O = iferror(lambda: float(GHG_Upstream['TEPNG_N2O'][i]),0)
    TEPNG_CH4 = iferror(lambda: float(GHG_Upstream['TEPNG_CH4'][i]),0)
    TEPNG_GTS_CH4 = iferror(lambda: float(GHG_Upstream['TEPNG_GTS_CH4'][i]),0)
    
    GHG_Upstream.loc[i, 'TEPNG_CO2e'] = TEPNG_CO2+TEPNG_N2O*GWP100_N2O+TEPNG_CH4*GWP100_CH4+TEPNG_GTS_CH4*GWP100_CH4
    GHG_Upstream.loc[i, 'TEPNG_GTS_CO2e'] = TEPNG_GTS_CH4*GWP100_CH4


# In[19]:


# Calculating emissions for NAOC_CO2 and storing to dataframe for all months
for i in range(GHG_NAOC.shape[0]):
    Combustion_CO2 = iferror(lambda: float(GHG_NAOC['Combustion_CO2'][i]),0)
    Flaring_CO2 = iferror(lambda: float(GHG_NAOC['Flaring_CO2'][i]),0)
    Fugitives_CO2 = iferror(lambda: float(GHG_NAOC['Fugitives_CO2'][i]),0)
    Venting_CO2 = iferror(lambda: float(GHG_NAOC['Venting_CO2'][i]),0)
    Indirect_CO2 = iferror(lambda: float(GHG_NAOC['Indirect_CO2'][i]),0)
    GHG_Upstream.loc[i, 'NAOC_CO2'] = Combustion_CO2+Flaring_CO2+Fugitives_CO2+Indirect_CO2


# In[20]:


# Calculating emissions for NAOC_N2O and storing to dataframe for all months
for i in range(GHG_NAOC.shape[0]):
    Combustion_N2O = iferror(lambda: float(GHG_NAOC['Combustion_N2O'][i]),0)
    Flaring_N2O = iferror(lambda: float(GHG_NAOC['Flaring_N2O'][i]),0)
    GHG_Upstream.loc[i, 'NAOC_N2O'] = Combustion_N2O+Flaring_N2O


# In[21]:


# Calculating emissions for NAOC_CH4 and storing to dataframe for all months
for i in range(GHG_NAOC.shape[0]):
    Fugitives_CH4 = iferror(lambda: float(GHG_NAOC['Fugitives_CH4'][i]),0)
    Venting_CH4 = iferror(lambda: float(GHG_NAOC['Venting_CH4'][i]),0)
    GHG_Upstream.loc[i, 'NAOC_CH4'] = Fugitives_CH4+Venting_CH4


# In[22]:


# Calculating emissions for NAOC_GTS_CH4 and storing to dataframe for all months
for i in range(GHG_NAOC.shape[0]):
    GTS_Fugitives_CH4 = iferror(lambda: float(GHG_NAOC['GTS_Fugitives_CH4'][i]),0)
    GTS_Venting_CH4 = iferror(lambda: float(GHG_NAOC['GTS_Venting_CH4'][i]),0)
    GHG_Upstream.loc[i, 'NAOC_GTS_CH4'] = GTS_Fugitives_CH4+GTS_Venting_CH4


# In[23]:


# Calculating emissions for NAOC_CO2e, TEPNG_GTS_CO2e and storing to dataframe for all months
for i in range(GHG_Upstream.shape[0]):
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)
    NAOC_CO2 = iferror(lambda: float(GHG_Upstream['NAOC_CO2'][i]),0)
    NAOC_N2O = iferror(lambda: float(GHG_Upstream['NAOC_N2O'][i]),0)
    NAOC_CH4 = iferror(lambda: float(GHG_Upstream['NAOC_CH4'][i]),0)
    NAOC_GTS_CH4 = iferror(lambda: float(GHG_Upstream['NAOC_GTS_CH4'][i]),0)
    
    GHG_Upstream.loc[i, 'NAOC_CO2e'] = NAOC_CO2+NAOC_N2O*GWP100_N2O+NAOC_CH4*GWP100_CH4+NAOC_GTS_CH4*GWP100_CH4
    GHG_Upstream.loc[i, 'NAOC_GTS_CO2e'] = NAOC_GTS_CH4*GWP100_CH4


# In[25]:


# Posting all GHG entries to database
col_list = GHG_Upstream.columns
for i, row in GHG_Upstream.iterrows():
    record_date = GHG_Upstream.at[i, 'RecordDate']
    if df_GHG_Upstream.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in df_GHG_Upstream.iterrows():
            new_date = df_GHG_Upstream.at[j, 'RecordDate'] 
            if record_date.month==new_date.month and record_date.year==new_date.year:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Upstream.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        row_id = str(df_GHG_Upstream.at[j, 'id'])
        update_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Upstream",cols_vals=cols_vals,row_id = row_id)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Upstream.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Upstream",cols=cols,vals=vals)


# In[ ]:




