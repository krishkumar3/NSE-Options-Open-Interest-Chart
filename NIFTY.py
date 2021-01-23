import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from matplotlib.pyplot import figure
from nsetools import Nse
from datetime import date
from datetime import timedelta
import datetime


nse = Nse()
cmp = nse.get_index_quote('NIFTY 50')
cmp = cmp['lastPrice']
cmp = int(round(cmp/50.0)*50.0)


new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(new_url,headers=headers)
dajs = page.json()


def plot_openInterest(c,p):

    ax = c.plot(figsize=(15,6),x='strikePrice',y='openInterest',title=cmp,kind='bar',color='red',xlabel='Strike Price',ylabel='Price'
            ,yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.85)
    p.plot(figsize=(15,6),ax=ax,x='strikePrice',y='openInterest',kind='bar',color='green',yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.65)
   
    c.plot(figsize=(15,6),ax=ax,x='strikePrice',y='changeinOpenInterest',title=cmp,kind='bar',color='yellow',xlabel='Strike Price',ylabel='Price'
            ,yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.35)
    p.plot(figsize=(15,6),ax=ax,x='strikePrice',y='changeinOpenInterest',kind='bar',color='black',yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.45)
    ax.legend(["Open Interest CE", "Open Interest PE","Change in Open Interest CE","Change in Open Interest PE"])

def plot_prices(ce_dt,pe_dt):
    ce = ce_dt[['lastPrice','strikePrice','openInterest']]
    pe = pe_dt[['lastPrice','strikePrice','openInterest']]
    r = ce_dt['strikePrice']

    for i in range(len(ce_dt['strikePrice'])):
        if r[i]==cmp-500:
            ce =ce[i:i+21]
            break

    r = pe_dt['strikePrice']
    for i in range(len(pe_dt['strikePrice'])):
        if r[i]==cmp-500:
            pe =pe[i:i+21]
            break
 
    ax = ce.plot(figsize=(15,6),x='strikePrice',y='lastPrice',kind='bar',color='red',xlabel='Strike Price',ylabel='Price'
            ,yticks=list(range(0,int(max(ce['lastPrice']+pe['lastPrice'])),50)),position=1,width=0.25)
    pe.plot(figsize=(15,6),ax=ax,position=0,x='strikePrice',y='lastPrice',kind='bar',color='green',yticks=list(range(0,int(max(ce['lastPrice']+pe['lastPrice'])),50)),width=0.25)
    

    
def fetch_oi(expiry_dt):
    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    
    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])

    pd.set_option('display.max_rows', None)
    ce = ce_dt[['lastPrice','strikePrice','openInterest','changeinOpenInterest']]
    pe = pe_dt[['lastPrice','strikePrice','openInterest','changeinOpenInterest']]
    c=ce[50:]
    p=pe[50:]

    plot_openInterest(c,p)
    #plot_prices(ce_dt,pe_dt)
    plt.subplots_adjust(bottom=0.13,left=0.065,right=0.97, top=0.96)
    plt.show()

  
def main():
    today = date.today()
    offset = (today.weekday()) 
    if offset<4:
        thursday = today + timedelta(days=3-offset) 
    else:
        thursday = today + timedelta(days=10-offset)
    expiry_dt = str(thursday.strftime('%d-%b-%Y'))
    fetch_oi(expiry_dt)
if __name__ == '__main__':
    main()