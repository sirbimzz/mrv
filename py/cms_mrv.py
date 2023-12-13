#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from calendar import monthrange
from operator import sub
from xlsxwriter import Workbook
import openpyxl
import glob
import os
import sys
import requests
import io

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

def del_SQL(server,db,user,pwd,tbl,condition):
    conn = pyodbc.connect(Driver="{SQL Server}", Server=server, Database=db, Trusted_Connection="NO", User=user, Password=pwd)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM """ + tbl + """ WHERE """ + condition + """;""")
    conn.commit()
    
def iferror(success, failure, *exceptions):
    try:
        return success()
    except Exception as e:
        return failure
def conv_mth(x):
    if len(str(x)) == 1:
        return '0' + str(x)
    else:
        return x

#############-----------Uploading shipping.EmissionsData------------#############
txt = 'uploading GHG_Shipping'


# In[4]:


txt = 'Uploading shipping.EmissionsData - Step 1'
df_ghg_cms, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Nlng.Tia",
        pwd = "Digital@1234",
        sql_string = """SELECT * FROM GHG_Shipping"""
        )
#df_EmissionsData.drop(['Id'], axis=1, inplace=True)

# In[5]:


username = 'Abimbola.Salami@nlng.com'
password = 'Nlng@30709'

mth_list = ['January','-_February','March','April','May','June','July','August','September','October','November','December']
mth_no = datetime.today().month

for i in range(mth_no-1):
    try:
        mth = mth_list[i]
        url = 'https://ecm.nlng.com/ECM-MD/HSE/Documents/HSE-4%20HSE,%20Commercial%20%26%20Shipping-Marine/006.%20Implementation,%20Monitoring%20and%20Reporting/Monthly%20HSSE%20Performance/2023/NLNG_Shipping_Fleet_HSSE_Statistics_' + mth + '%202023.xls'

        response = requests.get(url,verify=False, auth=(username, password))

        with io.BytesIO(response.content) as fh:
            df = pd.io.excel.read_excel(fh, sheet_name='CMS HSSE') #sheetname becomes sheet_name
        curr_yr = int(df.iloc[0,0][0:4])


        # In[6]:


        curr_yr


        # In[7]:


        df_Env = df


        # In[8]:


        for i, row in df_Env.iterrows():
            if df_Env.iloc[i, 0] == 'VESSELS':
                curr_mth = df_Env.iloc[i-2, 0].split(' - ')[1]
                row_start = i-1
        for i in range(row_start,df_Env.shape[0]):
            if df_Env.iloc[i, 0] == 'NLNG Total ' or df_Env.iloc[i, 0] == 'NLNG Total':
                row_end = i - 1
                break
        new_df = df_Env[row_start:row_end]
        for i in range(new_df.shape[1]):
            if new_df.iloc[0,i] == 'Carbon Intensity Indicator (CII)':
                col_end = i+1
        df_Env = df_Env.iloc[row_start+2:row_end,0:col_end]


        # In[9]:


        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        for i in range(len(months)):
            if curr_mth == months[i]:
                curr_month = i+1


        # In[10]:


        curr_month


        # In[11]:


        df_Env.columns = ['Vessels', 'FO', 'DO', 'LNG', 'YTD_Distance', 'YTD_Cargo_Loaded', 'Energy_Use', 'Waste_at_Sea',
            'Waste_Incarnated_Onboard', 'Waste_Shore_Recep', 'Discharged_at_Bonny',
            'Exchanged_at_Sea', 'Venting', 'Refit_Preparations', 'Due_to_Daily',
            'Vol_Vented_for_Tank_Pressure_Ctrl', 'Total_CH4', 'NOx', 'CO2', 'Comb_Boilers', 'HCFCS_Freon', 'Laden', 'Overall',
            'Voyage_Rolling_Laden', 'Voyage_Rolling_Overall', 'Vessel_Dead_Weight', 'CII']


        # In[12]:


        post_df = pd.DataFrame(columns = df_ghg_cms.columns[1:])
        for i, row in df_Env.iterrows():
            j = post_df.shape[0]
            RecordDate = datetime.strptime((str(curr_yr) + '-' + str(conv_mth(curr_month)) + '-01'), '%Y-%m-%d')
            post_df.loc[j, 'RecordDate'] = RecordDate 
            post_df.loc[j, 'UpdatedDate'] = datetime.today().strftime('%Y-%m-%d')
            post_df.loc[j, 'UpdatedBy'] = 'Admin'
            post_df.loc[j, 'Vessel_Name'] = df_Env.loc[i, 'Vessels']
            post_df.loc[j, 'DWT'] = df_Env.loc[i, 'Vessel_Dead_Weight']
            post_df.loc[j, 'Tot_Distance'] = df_Env.loc[i, 'YTD_Distance']
            post_df.loc[j, 'Tot_MGO'] = df_Env.loc[i, 'FO']
            post_df.loc[j, 'Tot_HFO'] = df_Env.loc[i, 'DO']
            post_df.loc[j, 'Tot_LFO'] = 0
            post_df.loc[j, 'Tot_LNG'] = df_Env.loc[i, 'LNG']

        post_df = post_df.fillna(0)


        # In[13]:


        post_df


        # In[14]:


        for i, row in post_df.iterrows():
            row_found = ''
            for j, row in df_ghg_cms.iterrows():
                if post_df.loc[i, 'RecordDate'].month == df_ghg_cms.loc[j, 'RecordDate'].month and post_df.loc[i, 'RecordDate'].year == df_ghg_cms.loc[j, 'RecordDate'].year and post_df.loc[i, 'Vessel_Name'] == df_ghg_cms.loc[j, 'Vessel_Name']:
                    row_found = 'YES'
                    row_id = str(df_ghg_cms.loc[j, 'id'])
                    break
                    
            if row_found == 'YES':
                for col in post_df.columns[1:]:
                    cols_vals = col + "=" + "'" + str(post_df.at[i, col]) + "'"
                    update_SQL(
                        server = "BNY-S-560",
                        db = "dataEntryDB",
                        user = "Nlng.Tia",
                        pwd = "Digital@1234",
                        tbl = "GHG_Shipping",
                        cols_vals = cols_vals,
                        row_id = row_id
                    )
            else:
                vals = ''
                cols = ''
                for col in post_df.columns:
                    cols = cols + col + ","
                    vals = vals + "'" + str(post_df.at[i, col]) + "',"
                vals=vals[:-1]
                cols=cols[:-1]
                insert_SQL(
                    server = "BNY-S-560",
                    db = "dataEntryDB",
                    user = "Nlng.Tia",
                    pwd = "Digital@1234",
                    tbl = "GHG_Shipping",
                    cols = cols,
                    vals = vals
                )
    except:
        pass



