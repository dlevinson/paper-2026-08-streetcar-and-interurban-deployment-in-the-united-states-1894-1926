import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import us
from re import search
import string
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv

def read_file(year):
    out = None
    with open(
        f'{year} TXT.txt', #text file name
        encoding="utf8"
    ) as f:
        out = pd.DataFrame(f)
        out['Info'] = out[0].apply(lambda x: x.strip())
        out['Year'] = year
        out = out.drop(columns=[0])
    return out

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))   

def capratio(bits):
    bits = ''.join((x for x in bits if not x.isdigit()))
    start = 0
    ratio = 0
    translator = bits.maketrans('', '', string.punctuation)
    ring = bits.translate(translator)
    ringing = ring.replace(' ', '')
    
    for i in range(len(bits)):
        if bits[i].isupper() is True:
            start = start + 1
    if len(ringing) > 0:
        ratio = start/len(ringing)
    
    return ratio
    
def get_state(x):
    if x in states and hasNumbers(x) is False:
        return x
    else:
        return np.nan
    
def get_city(x):
    if capratio(x) > 0.7 and len(x) > 5 and hasNumbers(x) is True and 'STA.' not in x and 'EQUIP' not in x:
        x.replace('8', 'S')
        x.replace('5', 'S')
        if 'ST.' not in x and 'FT.' and 'MT.' not in x:
            try:
                return x.split('.')[0]
            except:
                return np.nan
        else:
            splits = x.split('.')
            try:
                if hasNumbers(splits[1]) is False:
                    return splits[0] + splits[1]
                else:
                    return splits[0]
            except:
                return np.nan
    else:
        return np.nan

def get_company(x):
    if '---' in x and hasNumbers(x[0:2]) is True:
        if 'Co.' in x:  #one for split at emdash and Co.
            try:
                compstring = x.split('---')[1]
                if len(compstring) > 2:
                    company = compstring.split('Co.')[0] + 'Co.'
                    return company
                else:
                    compstring = x.split('---')[0]
                    company = ''.join((x for x in compstring if not x.isdigit()))
                    return company
            except:
                return np.nan
        elif len(x.split('---')) > 2:
            return x.split('---')[1]
        else:
            try:
                return x.split('---')[1]
            except:
                return np.nan
    else:
        return np.nan
        
def get_mile(x):
    x = x.lower()
    if len(x) > 20:
        if 'miles owned' in x: #simplest
            splitter = 'miles owned'
            try:
                str_to_check = x.split(splitter)[0]
                num_list = re.findall(r"[+-]?\d+\.+\d+|[+-]?\d+\,+\d+|\d+ \d+|\d+", str_to_check)
                mile = num_list[len(num_list)-1]
                return mile
            except:
                return 'No'
        elif '4-8' in x:
            splits = x.split('4-8')
            checkpoint = ''.join('' if x is splits[len(splits)-1] else x for x in splits)
            longs = len(checkpoint) - 1
            if longs > 180:
                shorts = longs - 180
            else:
                shorts = 0
            alist = checkpoint[shorts:longs].split(' ')
            alist = [x for x in alist if len(x) > 4]
            if fuzz.partial_ratio('miles', x[shorts:longs]) > 75: #miles is in the string
                try:
                    splitter = process.extractOne('miles', alist, scorer=fuzz.partial_ratio)[0]
                    try:
                        str_to_check = x[shorts:longs].split(splitter)[0]
                        num_list = re.findall(r"[+-]?\d+\.+\d+|[+-]?\d+\,+\d+|\d+ \d+|\d+", str_to_check)
                        mile = num_list[len(num_list)-1]
                        return mile
                    except:
                        return 'No'
                except:
                    pass
            else:
                return 'No'
        elif '5-2' in x and '5-2000' not in x:
            splits = x.split('5-2')
            checkpoint = ''.join('' if x is splits[len(splits)-1] else x for x in splits)
            longs = len(checkpoint) - 1
            if longs > 180:
                shorts = longs - 180
            else:
                shorts = 0
            alist = checkpoint[shorts:longs].split(' ')
            alist = [x for x in alist if len(x) > 4 and x is not None]
            if fuzz.partial_ratio('miles', x[shorts:longs]) > 75: #miles is in the string
                splitter = process.extractOne('miles', alist, scorer=fuzz.partial_ratio)[0]
                try:
                    str_to_check = x[shorts:longs].split(splitter)[0]
                    num_list = re.findall(r"[+-]?\d+\.+\d+|[+-]?\d+\,+\d+|\d+ \d+|\d+", str_to_check)
                    mile = num_list[len(num_list)-1]
                    return mile
                except:
                    return 'No'
            else:
                return 'No'
        else:
            longs = len(x) - 1
            if longs > 180:
                shorts = longs - 180
            else:
                shorts = 0
            if 'miles' in x[shorts:longs]:
                str_to_check = x[shorts:longs].split('miles')[0]
                try:
                    num_list = re.findall(r"[+-]?\d+\.+\d+|[+-]?\d+\,+\d+|\d+ \d+|\d+", str_to_check)
                    mile = num_list[len(num_list)-1]
                    return mile
                except:
                    return 'No'
            else:
                return 'No'            
    else:
        return 'No'
        
states1 = [str(i).upper() for i in us.states.STATES]
states2 = [str(i).upper() + '.' for i in us.states.STATES]
states = states1 + states2

years = list(range(1917, 1927))

for year in years:
    df = read_file(year)
    
    value = len(df)
    start = 0
    end = 0
    
    for i in range(value):
            if 'START OF RECORDS' in df['Info'][i]:
                start = i
            elif 'END OF RECORDS' in df['Info'][i]:
                end = i+1

    df = df.drop(df.index[end:value])
    df = df.drop(df.index[0:start])
    df = df.reset_index(drop=True)
    
    df['Info'] = df['Info'].str.replace('. 0.', '. O.')
    df['Info'] = df['Info'].str.replace(', 0.', ', O.')
    df['Info'] = df['Info'].str.replace('\t', ' ')
    df = df[df["Info"].str.contains("UNIVERSITY")==False]
    df = df.reset_index(drop=True)
    
    df['State'] = df['Info'].apply(get_state)
    df['State'] = df['State'].ffill()
    
    df['City'] = df['Info'].apply(get_city)
    df['City'] = df['City'].str.replace('8', 'S')
    df['City'] = df['City'].ffill()

    df['Miles'] = df['Info'].apply(get_mile)
    df['Company'] = df['Info'].apply(get_company)
    df['Company'] = df['Company'].ffill()
    
    extract = []
    
    for x in range(len(df)):
            if df['Miles'][x] != 'No':
                extract.append(x)
    results = df.take(extract)
    results = results.drop(columns=['Info'])
    display(results)
