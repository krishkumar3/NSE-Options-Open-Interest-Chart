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
import time
from json import JSONDecodeError



def basic():
    nse = Nse()
    cmp = nse.get_index_quote('NIFTY BANK')
    cmp = cmp['lastPrice']
    cmp = int(round(cmp/100.0)*100.0)
    l=[]


    new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
    headers = {'User-Agent': 'Mozilla/5.0'}
   
    page = requests.get(new_url,headers=headers)    
    while len(page.content)==272:
        page = requests.get(new_url,headers=headers)
        print("Fetching data... Please wait")
    dajs = page.json()
    l.append(dajs)
    l.append(cmp)
    return l


def plot_openInterest(c,p,cmp):

    ax = c.plot(figsize=(15,6),x='strikePrice',y='openInterest',title=cmp,kind='bar',color='red',xlabel='Strike Price',ylabel='Price'
            ,yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.85)
    p.plot(figsize=(15,6),ax=ax,x='strikePrice',y='openInterest',kind='bar',color='green',yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.65)
   
    c.plot(figsize=(15,6),ax=ax,x='strikePrice',y='changeinOpenInterest',title=cmp,kind='bar',color='yellow',xlabel='Strike Price',ylabel='Price'
            ,yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.35)
    p.plot(figsize=(15,6),ax=ax,x='strikePrice',y='changeinOpenInterest',kind='bar',color='black',yticks=list(range(0,max(c['openInterest']+p['openInterest']),12000)),width=0.35)
    ax.legend(["Open Interest CE", "Open Interest PE","Change in Open Interest CE","Change in Open Interest PE"])
    ax.set_facecolor([0.78,0.78,0.88])

def plot_prices(ce_dt,pe_dt,cmp):
    ce = ce_dt[['lastPrice','strikePrice','openInterest']]
    pe = pe_dt[['lastPrice','strikePrice','openInterest']]
    r = ce_dt['strikePrice']

    for i in range(len(ce_dt['strikePrice'])):
        if r[i]==cmp-2000:
            ce =ce[i:]
            ce = ce[:-20]
            break

    r = pe_dt['strikePrice']
    for i in range(len(pe_dt['strikePrice'])):
        if r[i]==cmp-2000:
            pe =pe[i:]
            pe = pe[:-20]
            break
 
    ax = ce.plot(figsize=(15,6),x='strikePrice',y='lastPrice',kind='bar',color='red',xlabel='Strike Price',ylabel='Price'
            ,yticks=list(range(0,int(max(ce['lastPrice']+pe['lastPrice'])),50)),position=1,width=0.25)
    pe.plot(figsize=(15,6),ax=ax,position=0,x='strikePrice',y='lastPrice',kind='bar',color='green',yticks=list(range(0,int(max(ce['lastPrice']+pe['lastPrice'])),50)),width=0.25)
    ax.set_facecolor([0.78,0.78,0.88])


    
def fetch_oi(expiry_dt,dajs,cmp):
    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    
    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])

    pd.set_option('display.max_rows', None)
    ce = ce_dt[['lastPrice','strikePrice','openInterest','changeinOpenInterest']]
    pe = pe_dt[['lastPrice','strikePrice','openInterest','changeinOpenInterest']]
    c=ce[65:]
    p=pe[65:]

    plot_openInterest(c,p,cmp)
    plot_prices(ce_dt,pe_dt,cmp)
    plt.subplots_adjust(bottom=0.13,left=0.065,right=0.97, top=0.96)
    plt.show(block=False)
    plt.pause(100)
    plt.close()

def main():
    today = date.today()
    offset = (today.weekday()) 
    if offset<4:
        thursday = today + timedelta(days=3-offset) 
    else:
        thursday = today + timedelta(days=10-offset)
    expiry_dt = str(thursday.strftime('%d-%b-%Y'))
    t=time.time()
    while time.time() < t+900:
        print("Calling again:",time.time())
        dajs = basic()
        cmp = dajs[1]
        dajs = dajs[0]
        fetch_oi(expiry_dt,dajs,cmp)
if __name__ == '__main__':
    main()
