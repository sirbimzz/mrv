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
import sys

def conn_oracle(dbq, dns, uid, pwd, sql_string):
    """
    Establish connection to Oracle database and return data as DataFrame
    Parameters
    ----------
    driver : string
        database driver name.
    dbq : string
        DESCRIPTION.
    dns : string
        DESCRIPTION.
    uid : string
        database user connection user id.
    pwd : string
        database user connection password.
    sql_string : string
        SQL query.

    Returns
    -------
    df : DataFrame
        DESCRIPTION.

    """
    df = pd.DataFrame()
    try:
        conn = pyodbc.connect(Driver="{Oracle in OraClient11g_home1}", DBQ=dbq, DNS=dns, Trusted_Connection="NO", UID=uid, PWD=pwd)
        print("connection with {} successful".format(dns))
        df = pd.read_sql_query(sql_string, conn)
        conn.close()
        success = True
    except Exception as e:
        print("connection with database failed: ->{}".format(str(e)))
        success = False
    return df, success

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


# Getting GHG_Summary_Monthly data from Datatbase
df_GHG_Summary_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Summary_Monthly"""
        )


# In[3]:


# Getting GHG_Daily_Data data from Datatbase
GHG_Daily_Data, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Daily_Data"""
        )


# In[4]:


# Getting GHG_Flaring_Weekly data from Datatbase
GHG_Flaring_Weekly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Flaring_Weekly"""
        )


# In[5]:


# Getting GHG_Plant_Monthly data from Datatbase
GHG_Plant_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Plant_Monthly"""
        )


# In[6]:


# Getting GHG_Upstream data from Datatbase
GHG_Upstream, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Upstream"""
        )


# In[7]:


# Getting GHG_Upstream data from Datatbase
GHG_Shipping_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Shipping_Monthly"""
        )


# In[8]:


# Getting GHG_Upstream data from Datatbase
GHG_Logistics_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Logistics_Monthly"""
        )


# In[9]:


# Getting GHG_Upstream data from Datatbase
GHG_Offices_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Offices_Monthly"""
        )


# In[10]:


# Getting GHG_Upstream data from Datatbase
GHG_Projects_Monthly, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.GHG_Projects_Monthly"""
        )


# In[11]:


# Getting Daily_Production data from Datatbase
Daily_Production, success = conn_sql_server(
        server = "BNY-S-560",
        db = "dataEntryDB",
        user = "Abimbola.Salami",
        pwd = "NLNG@3070",
        sql_string = """SELECT * FROM dbo.Daily_Production"""
        )


# In[12]:


df_cargoes, success = conn_oracle(
        dbq = "energy",
        dns = "energy",
        uid = "BIM_MRV",
        pwd = "UserMrv1",
        sql_string = """SELECT * FROM eckernel_nlng.zv_rep_cargoes_mrv"""
        )


# In[13]:


# Creating a new dataframe to store GHG output
GHG_Summary_Monthly = pd.DataFrame(columns = ['RecordDate', 'UpdatedDate', 'UpdatedBy', 'SPDC_CO2e','TEPNG_CO2e',
       'NAOC_CO2e', 'Upstream_CO2e'])


# In[14]:


Upstream = pd.DataFrame(columns = ['RecordDate','SPDC_CO2e','TEPNG_CO2e','NAOC_CO2e','Upstream_CO2e'])


# In[15]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in GHG_Upstream.iterrows():
    SPDC_CO2e = iferror(lambda: float(GHG_Upstream['SPDC_CO2e'][i]),0)
    TEPNG_CO2e = iferror(lambda: float(GHG_Upstream['TEPNG_CO2e'][i]),0)
    NAOC_CO2e = iferror(lambda: float(GHG_Upstream['NAOC_CO2e'][i]),0)
    RecordDate = GHG_Upstream['RecordDate'][i]
    Upstream.loc[i, 'RecordDate'] = RecordDate
    Upstream.loc[i, 'SPDC_CO2e'] = SPDC_CO2e
    Upstream.loc[i, 'TEPNG_CO2e'] = TEPNG_CO2e
    Upstream.loc[i, 'NAOC_CO2e'] = NAOC_CO2e
    Upstream.loc[i, 'Upstream_CO2e'] = SPDC_CO2e + TEPNG_CO2e + NAOC_CO2e


# In[16]:


for i, row in df_cargoes.iterrows():
    Month = (df_cargoes['LOADING_DATE'][i]).month
    Year = (df_cargoes['LOADING_DATE'][i]).year
    df_cargoes.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)


# In[17]:


for i, row in df_cargoes.iterrows():
    if 'LNG' in df_cargoes.loc[i, 'BUYER']:
        df_cargoes.loc[i, 'LNG_Tons'] = df_cargoes.loc[i, 'QUANTITY_DISCHARGED_TONS']
        df_cargoes.loc[i, 'LNG_MMBTU'] = df_cargoes.loc[i, 'QUANTITY_DISCHARGED_TONS'] * 52.4
    elif 'LPG' in df_cargoes.loc[i, 'BUYER']:
        df_cargoes.loc[i, 'LPG_Tons'] = df_cargoes.loc[i, 'QUANTITY_DISCHARGED_TONS']
        df_cargoes.loc[i, 'LPG_MMBTU'] = df_cargoes.loc[i, 'QUANTITY_DISCHARGED_TONS'] * 52.4
    elif 'COND' in df_cargoes.loc[i, 'BUYER']:
        df_cargoes.loc[i, 'COND_Tons'] = df_cargoes.loc[i, 'QUANTITY_DISCHARGED_TONS']
        df_cargoes.loc[i, 'COND_MMBTU'] = df_cargoes.loc[i, 'QUANTITY_DISCHARGED_TONS'] * 52.4


# In[18]:


Daily_Production = df_cargoes.groupby(['Month_Year']).sum()


# In[19]:


Daily_Production.reset_index(inplace=True)


# In[20]:


Production = pd.DataFrame()


# In[21]:


# Calculating monthly emissions for Production and storing to dataframe for all months
for i, row in Daily_Production.iterrows():
    x = Daily_Production['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    Production.loc[i, 'RecordDate'] = RecordDate
    Production.loc[i, 'LNG_Tons'] = Daily_Production['LNG_Tons'][i]
    Production.loc[i, 'LNG_MMBTU'] = Daily_Production['LNG_MMBTU'][i]
    Production.loc[i, 'LPG_Tons'] = Daily_Production['LPG_Tons'][i]
    Production.loc[i, 'LPG_MMBTU'] = Daily_Production['LPG_MMBTU'][i]
    Production.loc[i, 'COND_Tons'] = Daily_Production['COND_Tons'][i]
    Production.loc[i, 'COND_MMBTU'] = Daily_Production['COND_MMBTU'][i]


# In[22]:


for i, row in Upstream.iterrows():
    Month = (Upstream['RecordDate'][i]).month
    Year = (Upstream['RecordDate'][i]).year
    Upstream.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)
    x = Upstream['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    Upstream.loc[i, 'RecordDate'] = RecordDate
Upstream.drop(['Month_Year'], axis=1, inplace=True)


# In[23]:


Plant = pd.DataFrame(columns = ['RecordDate','Acid_Gas_CO2e','Trains_CO2e','LHU_CO2e','GTG_CO2e'])


# In[24]:


for i, row in GHG_Daily_Data.iterrows():
    Month = (GHG_Daily_Data['RecordDate'][i]).month
    Year = (GHG_Daily_Data['RecordDate'][i]).year
    GHG_Daily_Data.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)


# In[25]:


cols = ['Acid_Gas_T1_CO2',
       'Acid_Gas_T2_CO2', 'Acid_Gas_T3_CO2', 'Acid_Gas_T4_CO2',
       'Acid_Gas_T5_CO2', 'Acid_Gas_T6_CO2', 'Acid_Gas_CO2', 'T1_CO2',
       'T2_CO2', 'T3_CO2', 'T4_CO2', 'T5_CO2', 'T6_CO2', 'Trains_CO2',
       'T1_N2O', 'T2_N2O', 'T3_N2O', 'T4_N2O', 'T5_N2O', 'T6_N2O',
       'Trains_N2O', 'T1_CH4', 'T2_CH4', 'T3_CH4', 'T4_CH4', 'T5_CH4',
       'T6_CH4', 'Trains_CH4', 'T1_CO2e', 'T2_CO2e', 'T3_CO2e', 'T4_CO2e',
       'T5_CO2e', 'T6_CO2e', 'Trains_CO2e', 'LHU_CO2', 'LHU_N2O', 'LHU_CH4',
       'LHU_CO2e', 'GTG_CO2', 'GTG_N2O', 'GTG_CH4', 'GTG_CO2e']

for col in cols:
    GHG_Daily_Data[col] = GHG_Daily_Data[col].astype(float)


# In[26]:


GHG_Daily_Data = GHG_Daily_Data.groupby(['Month_Year']).sum()


# In[27]:


GHG_Daily_Data = GHG_Daily_Data.reset_index()


# In[28]:


# Calculating monthly emissions for Plant and storing to dataframe for all months
for i, row in GHG_Daily_Data.iterrows():
    x = GHG_Daily_Data['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    Plant.loc[i, 'RecordDate'] = RecordDate
    Plant.loc[i, 'Acid_Gas_CO2e'] = GHG_Daily_Data['Acid_Gas_CO2'][i]
    Plant.loc[i, 'Trains_CO2e'] = GHG_Daily_Data['Trains_CO2e'][i]
    Plant.loc[i, 'LHU_CO2e'] = GHG_Daily_Data['LHU_CO2e'][i]
    Plant.loc[i, 'GTG_CO2e'] = GHG_Daily_Data['GTG_CO2e'][i]


# In[29]:


Plant = Plant.sort_values(by=['RecordDate']).reset_index()
Plant.drop(['index'], axis=1, inplace=True)


# In[30]:


for i, row in GHG_Plant_Monthly.iterrows():
    Month = (GHG_Plant_Monthly['RecordDate'][i]).month
    Year = (GHG_Plant_Monthly['RecordDate'][i]).year
    GHG_Plant_Monthly.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)


# In[31]:


cols = ['Waste_CO2',
       'Waste_N2O', 'Waste_CH4', 'Waste_CO2e', 'Mobile_CO2', 'Mobile_N2O',
       'Mobile_CH4', 'Mobile_CO2e', 'Fugitives_CH4', 'Fugitives_CO2e','Flare_CO2',
       'Flare_N2O', 'Flare_CH4', 'Flare_CO2e']

for col in cols:
    GHG_Plant_Monthly[col] = GHG_Plant_Monthly[col].apply(pd.to_numeric)


# In[32]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in GHG_Plant_Monthly.iterrows():
    Waste_CO2e = iferror(lambda: float(GHG_Plant_Monthly['Waste_CO2e'][i]),0)
    Mobile_CO2e = iferror(lambda: float(GHG_Plant_Monthly['Mobile_CO2e'][i]),0)
    Fugitives_CO2e = iferror(lambda: float(GHG_Plant_Monthly['Fugitives_CO2e'][i]),0)
    Flare_CO2e = iferror(lambda: float(GHG_Plant_Monthly['Flare_CO2e'][i]),0)
    x = GHG_Plant_Monthly['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    GHG_Plant_Monthly.loc[i, 'RecordDate'] = RecordDate


# In[33]:


GHG_Plant_Monthly = GHG_Plant_Monthly.sort_values(by=['RecordDate'])


# In[34]:


for i, row in Plant.iterrows():
    RecordDate = Plant['RecordDate'][i]
    for j, row in GHG_Plant_Monthly.iterrows():
        if type(GHG_Plant_Monthly['RecordDate'][j]) != str:
            RecordDate2 = GHG_Plant_Monthly['RecordDate'][j].strftime('%Y-%m-%d')
        else:
            RecordDate2 = GHG_Plant_Monthly['RecordDate'][j]
            
        if RecordDate == RecordDate2: 
            Plant.loc[i, 'Waste_CO2e'] = GHG_Plant_Monthly['Waste_CO2e'][j]
            Plant.loc[i, 'Mobile_CO2e'] = GHG_Plant_Monthly['Mobile_CO2e'][j]
            Plant.loc[i, 'Fugitives_CO2e'] = GHG_Plant_Monthly['Fugitives_CO2e'][j]
            Plant.loc[i, 'Flare_CO2e'] = GHG_Plant_Monthly['Flare_CO2e'][j]


# In[35]:


for i, row in Plant.iterrows():
    Acid_Gas_CO2e = iferror(lambda: float(Plant['Acid_Gas_CO2e'][i]),'')
    Trains_CO2e = iferror(lambda: float(Plant['Trains_CO2e'][i]),'')
    LHU_CO2e = iferror(lambda: float(Plant['LHU_CO2e'][i]),'')
    GTG_CO2e = iferror(lambda: float(Plant['GTG_CO2e'][i]),'')
    Waste_CO2e = iferror(lambda: float(Plant['Waste_CO2e'][i]),'')
    Mobile_CO2e = iferror(lambda: float(Plant['Mobile_CO2e'][i]),'')
    Fugitives_CO2e = iferror(lambda: float(Plant['Fugitives_CO2e'][i]),'')
    Flare_CO2e = iferror(lambda: float(Plant['Flare_CO2e'][i]),'')
    Plant.loc[i, 'Plant_CO2e'] = Acid_Gas_CO2e+Trains_CO2e+LHU_CO2e+GTG_CO2e+Waste_CO2e+Mobile_CO2e+Fugitives_CO2e+Flare_CO2e


# In[36]:


cols = ['CO2', 'N2O', 'CH4', 'CII', 'CO2e']

for col in cols:
    GHG_Shipping_Monthly[col] = GHG_Shipping_Monthly[col].astype(float)


# In[37]:


GHG_Shipping_Monthly = GHG_Shipping_Monthly.groupby(['RecordDate']).sum()


# In[38]:


GHG_Shipping_Monthly = GHG_Shipping_Monthly.sort_values(by=['RecordDate']).reset_index()


# In[39]:


for i, row in GHG_Shipping_Monthly.iterrows():
    Month = (GHG_Shipping_Monthly['RecordDate'][i]).month
    Year = (GHG_Shipping_Monthly['RecordDate'][i]).year
    GHG_Shipping_Monthly.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)
    x = GHG_Shipping_Monthly['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    GHG_Shipping_Monthly.loc[i, 'RecordDate'] = RecordDate
GHG_Shipping_Monthly.drop(['Month_Year'], axis=1, inplace=True)


# In[40]:


Shipping = pd.DataFrame(columns = ['RecordDate', 'Shipping_CO2e'])


# In[41]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in GHG_Shipping_Monthly.iterrows():
    Shipping.loc[i, 'RecordDate'] = GHG_Shipping_Monthly['RecordDate'][i] 
    Shipping.loc[i, 'Shipping_CO2e'] = GHG_Shipping_Monthly['CO2e'][i] 


# In[42]:


Mobile = pd.DataFrame(columns = ['RecordDate', 'Logistics_CO2e'])


# In[43]:


cols = ['Aviation_CO2e',
       'Av_Per_Passenger', 'Av_Per_Distance', 'Passenger_Boats_CO2e',
       'P_Boats_Per_Passenger', 'P_Boats_Per_Distance', 'Tug_Boats_CO2e',
       'T_Boats_Per_Passenger', 'T_Boats_Per_Distance', 'Long_Escort_CO2e',
       'L_Escort_Per_Passenger', 'L_Escort_Per_Distance',
       'Passenger_Escort_CO2e', 'P_Escort_Per_Passenger',
       'P_Escort_Per_Distance', 'Escort_CO2e', 'Bny_Fleet_Diesel_CO2e',
       'Bny_Fleet_Petrol_CO2e', 'Bny_Fleet_CO2e', 'Bny_Fleet_Per_Passenger',
       'Bny_Fleet_Per_Distance', 'Non_Bny_Fleet_Diesel_CO2e',
       'Non_Bny_Fleet_Petrol_CO2e', 'Non_Bny_Fleet_CO2e',
       'Non_Bny_Fleet_Per_Passenger', 'Non_Bny_Fleet_Per_Distance']

for col in cols:
    GHG_Logistics_Monthly[col] = GHG_Logistics_Monthly[col].astype(float)


# In[44]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in GHG_Logistics_Monthly.iterrows():
    Aviation_CO2e = GHG_Logistics_Monthly['Aviation_CO2e'][i] 
    Passenger_Boats_CO2e = GHG_Logistics_Monthly['Passenger_Boats_CO2e'][i] 
    Tug_Boats_CO2e = GHG_Logistics_Monthly['Tug_Boats_CO2e'][i] 
    Long_Escort_CO2e = GHG_Logistics_Monthly['Long_Escort_CO2e'][i] 
    Passenger_Escort_CO2e = GHG_Logistics_Monthly['Passenger_Escort_CO2e'][i] 
    Bny_Fleet_CO2e = GHG_Logistics_Monthly['Bny_Fleet_CO2e'][i]
    Non_Bny_Fleet_CO2e = GHG_Logistics_Monthly['Non_Bny_Fleet_CO2e'][i]
    Mobile.loc[i, 'Logistics_CO2e'] = Aviation_CO2e+Passenger_Boats_CO2e+Tug_Boats_CO2e+Long_Escort_CO2e+Passenger_Escort_CO2e+Bny_Fleet_CO2e+Non_Bny_Fleet_CO2e
    Mobile.loc[i, 'RecordDate'] = GHG_Logistics_Monthly['RecordDate'][i]


# In[45]:


for i, row in Mobile.iterrows():
    Month = (Mobile['RecordDate'][i]).month
    Year = (Mobile['RecordDate'][i]).year
    Mobile.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)


# In[46]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in Mobile.iterrows():
    x = Mobile['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    Mobile.loc[i, 'RecordDate'] = RecordDate


# In[47]:


Mobile.drop(['Month_Year'], axis=1, inplace=True)


# In[48]:


Offices = pd.DataFrame(columns = ['RecordDate', 'Office_CO2e'])


# In[49]:


for i, row in GHG_Offices_Monthly.iterrows():
    PHC_CO2e = iferror(lambda: float(GHG_Offices_Monthly['PHC_CO2e'][i]),'')
    ABJ_CO2e = iferror(lambda: float(GHG_Offices_Monthly['ABJ_CO2e'][i]),'')
    LTO_CO2e = iferror(lambda: float(GHG_Offices_Monthly['LTO_CO2e'][i]),'')
    LON_NG_CO2e = iferror(lambda: float(GHG_Offices_Monthly['LON_NG_CO2e'][i]),'')
    Offices.loc[i, 'Office_CO2e'] = PHC_CO2e + ABJ_CO2e + LTO_CO2e + LON_NG_CO2e
    Offices.loc[i, 'RecordDate'] = GHG_Offices_Monthly['RecordDate'][i]


# In[50]:


for i, row in Offices.iterrows():
    Month = (Offices['RecordDate'][i]).month
    Year = (Offices['RecordDate'][i]).year
    Offices.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)


# In[51]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in Offices.iterrows():
    x = Offices['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    Offices.loc[i, 'RecordDate'] = RecordDate


# In[52]:


Offices.drop(['Month_Year'], axis=1, inplace=True)


# In[53]:


Projects = pd.DataFrame(columns = ['RecordDate', 'Project_CO2e'])


# In[54]:


for i, row in GHG_Projects_Monthly.iterrows():
    Projects.loc[i, 'Project_CO2e'] = GHG_Projects_Monthly['Projects_CO2e'][i]
    Projects.loc[i, 'RecordDate'] = GHG_Projects_Monthly['RecordDate'][i]


# In[55]:


for i, row in Projects.iterrows():
    Month = (Projects['RecordDate'][i]).month
    Year = (Projects['RecordDate'][i]).year
    Projects.loc[i, 'Month_Year'] = str(Year) + '-' + str(Month)


# In[56]:


# Calculating monthly emissions for Upstream_CO2e and storing to dataframe for all months
for i, row in Projects.iterrows():
    x = Projects['Month_Year'][i] + '-1'
    RecordDate = (datetime.strptime(x, '%Y-%m-%d')).strftime('%Y-%m-%d')
    Projects.loc[i, 'RecordDate'] = RecordDate


# In[57]:


Projects.drop(['Month_Year'], axis=1, inplace=True)


# In[58]:


start_date = datetime.strptime('2016-01-01', '%Y-%m-%d')
#end_date = datetime.strptime('2022-01-01', '%Y-%m-%d')
end_date = datetime.today()
diff_months = (relativedelta(end_date, start_date)).months + (relativedelta(end_date, start_date)).years*12


# In[59]:


table_list = [Upstream,Plant,Shipping,Mobile,Offices,Projects,Production]
for table in table_list:
    for i in range(diff_months):
        this_date = start_date + relativedelta(months=i)
        #date_list.append(this_date.strftime('%Y-%m-%d'))
        GHG_Summary_Monthly.loc[i, 'RecordDate'] = this_date.strftime('%Y-%m-%d')
        GHG_Summary_Monthly.loc[i, 'UpdatedDate'] = datetime.today().strftime('%Y-%m-%d')
        GHG_Summary_Monthly.loc[i, 'UpdatedBy'] = 'Admin'
        for col in table.columns:
            if col != 'RecordDate':
                for j, row in table.iterrows():
                    if type(table.loc[j, 'RecordDate']) != str:
                        RecordDate = table.loc[j, 'RecordDate'].strftime('%Y-%m-%d')
                    else:
                        RecordDate = table.loc[j, 'RecordDate']                    
                    if this_date.strftime('%Y-%m-%d') == RecordDate:
                        GHG_Summary_Monthly.loc[i, col] = table.loc[j, col]


# In[60]:


GHG_Summary_Monthly['RecordDate2'] = pd.to_datetime(GHG_Summary_Monthly['RecordDate'])


# In[61]:


GHG_Summary_Monthly = GHG_Summary_Monthly.sort_values(by='RecordDate2',ascending=False)


# In[62]:


for col in GHG_Summary_Monthly.columns:
    if col != 'RecordDate' and col != 'UpdatedDate' and col != 'UpdatedBy' and col != 'RecordDate2':
        GHG_Summary_Monthly[col] = pd.to_numeric(GHG_Summary_Monthly[col])


# In[63]:


GHG_Summary_Monthly.reset_index(inplace=True)
GHG_Summary_Monthly.drop(['index'], axis=1, inplace=True)


# In[64]:


GHG_Summary_Monthly2 = GHG_Summary_Monthly.copy()


# In[65]:


sel_cols = ['Upstream_CO2e','Plant_CO2e','Shipping_CO2e','Logistics_CO2e','Office_CO2e','Project_CO2e']
for col in sel_cols:
    for i in range(GHG_Summary_Monthly2.shape[0]-11):
        x = float(GHG_Summary_Monthly2[col][i])
        if math.isnan(x) == False:
            Tot_CO2e = 0
            for j in range(12):
                Tot_CO2e = Tot_CO2e + GHG_Summary_Monthly2[col][i+j]
            GHG_Summary_Monthly2.loc[i,'Tot_' + col] = Tot_CO2e


# In[66]:


sel_cols = ['Upstream_CO2e','Plant_CO2e','Shipping_CO2e','Logistics_CO2e','Office_CO2e','Project_CO2e']
for col in sel_cols:
    for i in range(GHG_Summary_Monthly2.shape[0]-1):
        x = float(GHG_Summary_Monthly2['Tot_' + col][i])
        if math.isnan(x) == True:
            y = 0
            for j in range(i,GHG_Summary_Monthly2.shape[0]):
                y = float(GHG_Summary_Monthly2['Tot_' + col][j])
                if math.isnan(y) == False:
                    GHG_Summary_Monthly2.loc[i,'Lag_Tot_' + col] = y
                    break
        else:
            GHG_Summary_Monthly2.loc[i,'Lag_Tot_' + col] = x


# In[67]:


#GHG_Summary_Monthly2['Tot_CO2e'] = GHG_Summary_Monthly2['Tot_Upstream_CO2e']+GHG_Summary_Monthly2['Tot_Plant_CO2e']+GHG_Summary_Monthly2['Tot_Shipping_CO2e']+GHG_Summary_Monthly2['Tot_Logistics_CO2e']+GHG_Summary_Monthly2['Tot_Office_CO2e']+GHG_Summary_Monthly2['Tot_Project_CO2e']
#GHG_Summary_Monthly2['Lag_Tot_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Upstream_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Plant_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Shipping_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Logistics_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Office_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Project_CO2e']
GHG_Summary_Monthly2['Tot_CO2e'] = GHG_Summary_Monthly2['Tot_Plant_CO2e']+GHG_Summary_Monthly2['Tot_Shipping_CO2e']+GHG_Summary_Monthly2['Tot_Logistics_CO2e']+GHG_Summary_Monthly2['Tot_Office_CO2e']+GHG_Summary_Monthly2['Tot_Project_CO2e']
GHG_Summary_Monthly2['Lag_Tot_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Plant_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Shipping_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Logistics_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Office_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Project_CO2e']
GHG_Summary_Monthly2['Total_Prod'] = GHG_Summary_Monthly2['LNG_Tons']+GHG_Summary_Monthly2['LPG_Tons']+GHG_Summary_Monthly2['COND_Tons']
GHG_Summary_Monthly2['Tot_Prod_MMBTU'] = GHG_Summary_Monthly2['LNG_MMBTU']+GHG_Summary_Monthly2['LPG_MMBTU']+GHG_Summary_Monthly2['COND_MMBTU']


# In[68]:


sel_cols = ['LNG_Tons','Total_Prod', 'Tot_Prod_MMBTU', 'LNG_MMBTU', 'LPG_MMBTU', 'COND_MMBTU']
for col in sel_cols:
    for i in range(GHG_Summary_Monthly2.shape[0]-11):
        x = float(GHG_Summary_Monthly2[col][i])
        if math.isnan(x) == False:
            Tot = 0
            for j in range(12):
                Tot = Tot + GHG_Summary_Monthly2[col][i+j]
            GHG_Summary_Monthly2.loc[i,'Cumm_' + col] = Tot


# In[69]:


GHG_Summary_Monthly.columns


# In[70]:


GHG_Summary_Monthly2['CO2e_Per_LNG'] = GHG_Summary_Monthly2['Tot_CO2e']/GHG_Summary_Monthly2['Cumm_LNG_Tons']
GHG_Summary_Monthly2['CO2e_Per_Prod'] = GHG_Summary_Monthly2['Tot_CO2e']/GHG_Summary_Monthly2['Cumm_Total_Prod']
GHG_Summary_Monthly2['CO2e_Per_LNG_Lag'] = GHG_Summary_Monthly2['Lag_Tot_CO2e']/GHG_Summary_Monthly2['Cumm_LNG_Tons']
GHG_Summary_Monthly2['CO2e_Per_Prod_Lag'] = GHG_Summary_Monthly2['Lag_Tot_CO2e']/GHG_Summary_Monthly2['Cumm_Total_Prod']
GHG_Summary_Monthly2['CO2e_Per_Prod_MMBTU'] = GHG_Summary_Monthly2['Lag_Tot_CO2e']/GHG_Summary_Monthly2['Tot_Prod_MMBTU']
GHG_Summary_Monthly2['CO2e_Per_LNG_MMBTU'] = GHG_Summary_Monthly2['Lag_Tot_CO2e']/GHG_Summary_Monthly2['Cumm_LNG_MMBTU']
GHG_Summary_Monthly2['CO2e_Per_LPG_MMBTU'] = GHG_Summary_Monthly2['Lag_Tot_CO2e']/GHG_Summary_Monthly2['Cumm_LPG_MMBTU']
GHG_Summary_Monthly2['CO2e_Per_COND_MMBTU'] = GHG_Summary_Monthly2['Lag_Tot_CO2e']/GHG_Summary_Monthly2['Cumm_COND_MMBTU']
GHG_Summary_Monthly2['Upstream_Per_LNG'] = GHG_Summary_Monthly2['Lag_Tot_Upstream_CO2e']/GHG_Summary_Monthly2['Cumm_LNG_Tons']
GHG_Summary_Monthly2['Plant_Per_LNG'] = (GHG_Summary_Monthly2['Lag_Tot_Plant_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Logistics_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Office_CO2e']+GHG_Summary_Monthly2['Lag_Tot_Project_CO2e'])/GHG_Summary_Monthly2['Cumm_LNG_Tons']
GHG_Summary_Monthly2['Ship_Per_LNG'] = GHG_Summary_Monthly2['Lag_Tot_Shipping_CO2e']/GHG_Summary_Monthly2['Cumm_LNG_Tons']


# In[71]:


GHG_Summary_Monthly.drop(['RecordDate2'], axis=1, inplace=True)


# In[72]:


GHG_Summary_Monthly['CO2e_Per_LNG'] = GHG_Summary_Monthly2['CO2e_Per_LNG']
GHG_Summary_Monthly['CO2e_Per_Prod'] = GHG_Summary_Monthly2['CO2e_Per_Prod']
GHG_Summary_Monthly['CO2e_Per_LNG_Lag'] = GHG_Summary_Monthly2['CO2e_Per_LNG_Lag']
GHG_Summary_Monthly['CO2e_Per_Prod_Lag'] = GHG_Summary_Monthly2['CO2e_Per_Prod_Lag']
GHG_Summary_Monthly['CO2e_Per_Prod_MMBTU'] = GHG_Summary_Monthly2['CO2e_Per_Prod_MMBTU']
GHG_Summary_Monthly['CO2e_Per_LNG_MMBTU'] = GHG_Summary_Monthly2['CO2e_Per_LNG_MMBTU']
GHG_Summary_Monthly['CO2e_Per_LPG_MMBTU'] = GHG_Summary_Monthly2['CO2e_Per_LPG_MMBTU']
GHG_Summary_Monthly['CO2e_Per_COND_MMBTU'] = GHG_Summary_Monthly2['CO2e_Per_COND_MMBTU']
GHG_Summary_Monthly['Upstream_Per_LNG'] = GHG_Summary_Monthly2['Upstream_Per_LNG']
GHG_Summary_Monthly['Plant_Per_LNG'] = GHG_Summary_Monthly2['Plant_Per_LNG']
GHG_Summary_Monthly['Ship_Per_LNG'] = GHG_Summary_Monthly2['Ship_Per_LNG']
GHG_Summary_Monthly['Lag_Tot_Plant_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Plant_CO2e']
GHG_Summary_Monthly['Lag_Tot_Logistics_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Logistics_CO2e']
GHG_Summary_Monthly['Lag_Tot_Office_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Office_CO2e']
GHG_Summary_Monthly['Lag_Tot_Project_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Project_CO2e']
GHG_Summary_Monthly['Lag_Tot_Shipping_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Shipping_CO2e']
GHG_Summary_Monthly['Lag_Tot_Upstream_CO2e'] = GHG_Summary_Monthly2['Lag_Tot_Upstream_CO2e']


# In[73]:


#GHG_Summary_Monthly.to_csv('Output.csv')


# In[74]:


GHG_Summary_Monthly.drop(['LNG_Tons'], axis=1, inplace=True)
GHG_Summary_Monthly.drop(['LNG_MMBTU'], axis=1, inplace=True)
GHG_Summary_Monthly.drop(['LPG_Tons'], axis=1, inplace=True)
GHG_Summary_Monthly.drop(['LPG_MMBTU'], axis=1, inplace=True)
GHG_Summary_Monthly.drop(['COND_Tons'], axis=1, inplace=True)
GHG_Summary_Monthly.drop(['COND_MMBTU'], axis=1, inplace=True)


# In[75]:


GHG_Summary_Monthly


# In[76]:


# Posting all GHG entries to database
col_list = GHG_Summary_Monthly.columns
for i, row in GHG_Summary_Monthly.iterrows():
    record_date = datetime.strptime(GHG_Summary_Monthly.at[i, 'RecordDate'], '%Y-%m-%d')
    if df_GHG_Summary_Monthly.shape[0] == 0:
        record_found = "NO"
    else:
        for j, row in df_GHG_Summary_Monthly.iterrows():
            new_date = df_GHG_Summary_Monthly.at[j, 'RecordDate']
            if record_date.month==new_date.month and record_date.year==new_date.year:
                record_found = "YES"
                break
            else:
                record_found = "NO"
    if record_found == "YES":
        cols_vals = ''
        cols_vals = ''
        for col in col_list:
            cols_vals = cols_vals + col + "=" + "'" + str(GHG_Summary_Monthly.at[i, col]) + "',"
        cols_vals=cols_vals[:-1]
        row_id = str(df_GHG_Summary_Monthly.at[j, 'id'])
        update_SQL(server="BNY-S-560",db="dataEntryDB",user="Abimbola.Salami",pwd="NLNG@3070",tbl="GHG_Summary_Monthly",cols_vals=cols_vals,row_id = row_id)
    else:
        vals = ''
        cols = ''
        for col in col_list:
            cols = cols + col + ","
            vals = vals + "'" + str(GHG_Summary_Monthly.at[i, col]) + "',"
        vals=vals[:-1]
        cols=cols[:-1]
        insert_SQL(server="BNY-S-560",db="dataEntryDB",user="Abimbola.Salami",pwd="NLNG@3070",tbl="GHG_Summary_Monthly",cols=cols,vals=vals)


# In[77]:


root_folder = r"\\BNY-S-560\mrv_data"
df_cargoes['LOADING_DATE'] = df_cargoes['LOADING_DATE'].astype(str)
df_cargoes['UNLOAD_DATE'] = df_cargoes['UNLOAD_DATE'].astype(str)
df_cargoes['QUANTITY_DISCHARGED_TONS'] = df_cargoes['QUANTITY_DISCHARGED_TONS'].fillna(0)
df_cargoes['QUANTITY_DISCHARGED_MMBTU'] = df_cargoes['QUANTITY_DISCHARGED_MMBTU'].fillna(0)
df_cargoes.to_json(root_folder + '/cargoes.json', orient='records', lines=False)


# In[ ]:




