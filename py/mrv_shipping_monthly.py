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
    
def update_SQL2(server,db,user,pwd,tbl,cols_vals,Vessel_Name,record_date):
    conn = pyodbc.connect(Driver="{SQL Server}", Server=server, Database=db, Trusted_Connection="NO", User=user, Password=pwd)
    cursor = conn.cursor()
    cursor.execute("""UPDATE """ + tbl + """ SET """ + cols_vals + """ WHERE Vessel_Name = """ + Vessel_Name + """ AND RecordDate = """ + record_date + """;""")
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
Shipping_Fleet_Mgr, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.Shipping_Fleet_Mgr"""
        )
Shipping_Fleet_Mgr = Shipping_Fleet_Mgr.set_index('Vessel_Name')


# In[5]:


Shipping_Fleet_Mgr


# In[6]:


# Getting GHG_Projects_Monthly data from Datatbase
GHG_Shipping_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Shipping_Monthly"""
        )


# In[7]:


# Getting Projects data from Datatbase
GHG_Shipping, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM dbo.GHG_Shipping"""
        )


# In[8]:


GHG_Shipping


# In[9]:


this_year = str(datetime.today().year)
GHG_Shipping = GHG_Shipping[GHG_Shipping['RecordDate'].astype(str).str.contains(this_year)]
GHG_Shipping = GHG_Shipping.reset_index()
GHG_Shipping.drop(['index'], axis=1, inplace=True)


# In[10]:


this_year = str(datetime.today().year)
GHG_Shipping[GHG_Shipping['RecordDate'].astype(str).str.contains(this_year)]


# In[11]:


for i, row in GHG_Shipping.iterrows():
    GHG_Shipping.at[i, 'Month'] = GHG_Shipping.at[i, 'RecordDate'].month
    GHG_Shipping.at[i, 'Year'] = GHG_Shipping.at[i, 'RecordDate'].year


# In[12]:


Vessels = GHG_Shipping['Vessel_Name'].unique()
Years = GHG_Shipping['Year'].unique()
for year in Years:
    for vessel in Vessels:
        curr_df = GHG_Shipping.loc[(GHG_Shipping['Vessel_Name'] == vessel) & (GHG_Shipping['Year'] == year)]
        curr_df = curr_df.sort_values(by=['RecordDate'], ascending=False)
        curr_df = curr_df.reset_index()
        curr_df.drop(['index'], axis=1, inplace=True)
        val_cols = ['Tot_Distance', 'Tot_MGO', 'Tot_HFO', 'Tot_LFO', 'Tot_LNG']
        for k, row in curr_df.iterrows():
            if curr_df.at[k, 'Month'] != 1:
                for col in val_cols:
                    curr_data = iferror(lambda: float(curr_df.at[k, col]) - float(curr_df.at[k+1, col]),float(curr_df.at[k, col]))
                    for j, row in GHG_Shipping.iterrows():
                        if curr_df.at[k, 'id'] == GHG_Shipping.at[j, 'id']:
                            GHG_Shipping.at[j, col] = curr_data


# In[13]:


GHG_Shipping.drop(['Month','Year'], axis=1, inplace=True)


# In[14]:


# Calculating emissions and storing to dataframe for all months
for i, row in GHG_Shipping.iterrows():
    Vessel_Name = GHG_Shipping.at[i, 'Vessel_Name']
    GHG_Shipping.at[i, 'Fleet_Mgr'] = iferror(lambda: Shipping_Fleet_Mgr['Fleet_Mgr'][Vessel_Name],'Others')
    DWT = Vessel_Name = iferror(lambda: float(GHG_Shipping.at[i, 'DWT']),0)
    Tot_Distance = Vessel_Name = iferror(lambda: float(GHG_Shipping.at[i, 'Tot_Distance']),0)
    Tot_MGO = Vessel_Name = iferror(lambda: float(GHG_Shipping.at[i, 'Tot_MGO']),0)
    Tot_HFO = Vessel_Name = iferror(lambda: float(GHG_Shipping.at[i, 'Tot_HFO']),0)
    Tot_LFO = Vessel_Name = iferror(lambda: float(GHG_Shipping.at[i, 'Tot_LFO']),0)
    Tot_LNG = Vessel_Name = iferror(lambda: float(GHG_Shipping.at[i, 'Tot_LNG']),0)
    
    MGO_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['MGO_CO2']),0)
    HFO_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['HFO_CO2']),0)
    LNG_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['LNG_CO2']),0)
    LFO_CO2 = iferror(lambda: float(df_Factors['Factor_Value']['LFO_CO2']),0)
    MDO_Aux_Eng_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['MDO_Aux_Eng_CH4']),0)
    HFO_Boiler_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['HFO_Boiler_CH4']),0)
    LNG_Boiler_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['LNG_Boiler_CH4']),0)
    MDO_Aux_Eng_N2O = iferror(lambda: float(df_Factors['Factor_Value']['MDO_Aux_Eng_N2O']),0)
    HFO_Boiler_N2O = iferror(lambda: float(df_Factors['Factor_Value']['HFO_Boiler_N2O']),0)
    LNG_Boiler_N2O = iferror(lambda: float(df_Factors['Factor_Value']['LNG_Boiler_N2O']),0)
    GWP100_N2O = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_N2O']),0)
    GWP100_CH4 = iferror(lambda: float(df_Factors['Factor_Value']['GWP100_CH4']),0)
    
    CO2 = iferror(lambda: float((Tot_MGO*MGO_CO2)+(Tot_HFO*HFO_CO2)+(Tot_LFO*LFO_CO2)+(Tot_LNG*LNG_CO2)),0)
    N2O = iferror(lambda: float((Tot_MGO*MDO_Aux_Eng_N2O)+(Tot_HFO*HFO_Boiler_N2O)+(Tot_LFO*HFO_Boiler_N2O)+(Tot_LNG*LNG_Boiler_N2O)),0)
    CH4 = iferror(lambda: float((Tot_MGO*MDO_Aux_Eng_CH4)+(Tot_HFO*HFO_Boiler_CH4)+(Tot_LFO*HFO_Boiler_CH4)+(Tot_LNG*LNG_Boiler_CH4)),0)
    CII = iferror(lambda: float((CO2/DWT)/Tot_Distance*1000000),0)
    CO2e = CO2+N2O*GWP100_N2O+CH4*GWP100_CH4
    
    GHG_Shipping.at[i, 'CO2'] = CO2
    GHG_Shipping.at[i, 'N2O'] = N2O
    GHG_Shipping.at[i, 'CH4'] = CH4
    GHG_Shipping.at[i, 'CII'] = CII
    GHG_Shipping.at[i, 'CO2e'] = CO2e


# In[16]:


GHG_Shipping


# In[17]:


GHG_Shipping.columns


# In[18]:


GHG_Shipping.drop(['id','DWT',
       'Tot_Distance', 'Tot_MGO', 'Tot_HFO', 'Tot_LFO', 'Tot_LNG'], axis=1, inplace=True)


# In[19]:


GHG_Shipping


# In[20]:


# Posting all GHG entries to database
col_list = GHG_Shipping.columns
for i, row in GHG_Shipping.iterrows():
    record_date = GHG_Shipping.at[i, 'RecordDate']
    Vessel_Name = GHG_Shipping.at[i, 'Vessel_Name']
    if GHG_Shipping_Monthly.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in GHG_Shipping_Monthly.iterrows():
            new_date = GHG_Shipping_Monthly.at[j, 'RecordDate']
            new_vessel = GHG_Shipping_Monthly.at[j, 'Vessel_Name']
            if record_date.month==new_date.month and record_date.year==new_date.year and Vessel_Name == new_vessel:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Shipping.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        Vessel_Name = "'" + Vessel_Name + "'"
        record_date = "'" + str(record_date) + "'"
        update_SQL2(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Shipping_Monthly",cols_vals=cols_vals,Vessel_Name=Vessel_Name,record_date=record_date)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Shipping.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Nlng.Tia",pwd="Digital@1234",tbl="GHG_Shipping_Monthly",cols=cols,vals=vals)


# In[ ]:





# In[ ]:





# In[ ]:




