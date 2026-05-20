import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
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
    
def getcities(Info):
if capratio(Info) > 0.7 and len(Info) < 30:
    return Info
elif len(Info) in range(7,25) and process.extractOne(Info.lower(), cities.str.lower(), scorer=fuzz.ratio)[1] > 80 and hasNumbers(Info) is False:
    if abs(len(process.extractOne(Info.lower(), cities.str.lower(), scorer=fuzz.ratio)[0]) - len(Info.lower())) < 4:
        return Info
else:
    return 999
    
def city2(CityInfo): 
    if CityInfo != 999 and CityInfo is not None:
        section = CityInfo
        if process.extractOne(section.lower(), cities, scorer=fuzz.ratio)[1] > 80:
            return process.extractOne(section.lower(), cities, scorer=fuzz.ratio)[0]
        elif process.extractOne(section.lower(), cities, scorer=fuzz.partial_ratio)[1] > 98 and process.extractOne(section.lower(), cities, scorer=fuzz.ratio)[1] > 50:
            return process.extractOne(section.lower(), cities, scorer=fuzz.partial_ratio)[0]
        else:
            return np.nan
    else:
        return np.nan

def getcompanies(Info, CleanCity, CompIndex, Truth):
    try:
        if len(Info) > 5:
            if len(re.findall('Funded|leased|Leased|See|Deficit|Interest', Info[0:40])) == 0 and '....' not in Info:
                if len(re.findall('Charter|Incorp|Succe|consolidation|Connects|This|connect|Organize|organize|Owns|succe|Annual|Formed|nchise', Info)) > 0 or Truth:
                    for x in CompIndex:
                        if fuzz.ratio(x[1], CleanCity) > 90:
                            if x[0] in Info[0:70]:
                                return x[0]
                            elif fuzz.partial_ratio(x[0].lower(), Info[0:70].lower()) > 90 and len(Info) > 11:
                                return x[0]
                            elif 'Population' in Info:
                                if fuzz.partial_ratio(x[0].lower(), Info[0:140].lower()) > 90:
                                    return x[0]
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
            else:
                pass
        else:
            pass
    except:
        pass
    
def getcompanies2(Info, CleanCity, CurrentList, CompIndex, Truth):
    try:
        if len(Info) > 5:
            if CurrentList is None:
                if len(re.findall('Funded|leased|Leased|See|Deficit|Interest', Info[0:40])) == 0 and '....' not in Info:
                    if len(re.findall('Charter|Incorp|Succe|consolidation|Connects|This|connect|Organize|organize|Owns|succe|Annual|Formed|nchise', Info)) > 0:
                        for x in CompIndex:
                            if fuzz.ratio(x[1], CleanCity) > 80:
                                if fuzz.partial_ratio(x[0].lower(), Info[0:70].lower()) > 80 and len(Info) > 11: 
                                    return x[0]
                                elif 'Population' in Info:
                                    if fuzz.partial_ratio(x[0].lower(), Info[0:140].lower()) > 80:
                                        return x[0]
                                else:
                                    pass
                            else:
                                pass
                        
                    else:
                        pass
                else:
                    pass
            else:
                return CurrentList
        else:
            pass
    except:
        pass
        
def getmiles(Info): 
    if 'Contemplated' not in Info and 'Proposed' not in Info and 'under construction' not in Info[0:40] and 'power plant' not in Info[0:40]:
        if fuzz.partial_ratio(Info, 'Plant and Equipment') > 80 and len(Info) > 20 and 'total' in Info:
            try:
                split_string = Info.split('total')[1]
                mile = (re.findall("[+-]?\d+\.+\d+|\d+", split_string))[0]
                return mile
            except:
                return 'No'
        elif fuzz.partial_ratio(Info, 'Plant and Equipment') > 80 and len(Info) > 20:
            try:
                split_string = Info.split('ment')[1]        
                mile = (re.findall("[+-]?\d+\.+\d+|\d+", split_string))[0]
                return mile
            except:
                return 'No'
        elif 'Miles of track' in Info[0:60] and 'total' in Info:
            split_string = Info.split('total')[1]
            mile = (re.findall("[+-]?\d+\.+\d+|\d+", split_string))[0]
            return mile
        elif 'Miles of track' in Info[0:60]:
            split_string = Info.split('of track')[1]
            try:
                mile = (re.findall("[+-]?\d+\.+\d+|\d+", split_string))[0]
                return mile
            except:
                return 'No'
        elif 'Miles of Track' in Info[0:60]:
            split_string = Info.split('of track')[1]
            try:
                mile = (re.findall("[+-]?\d+\.+\d+|\d+", split_string))[0]
                return mile
            except:
                return 'No'
        else:
            return 'No'
    else:
        return 'No'
        
def getstate(Companies, RealCities, CompIndex):
    for x in CompIndex:
        if Companies == x[0] and RealCities == x[1]:
            return x[2]
            
years = [1894] + list(range(1898, 1915))
for year in years:
    try:
        comps = pd.read_csv(f'{year}.csv')
        comps = comps.drop(['Unnamed: 0'], axis = 1)

        companies = comps['Company']
        places = comps['Place']
        cities = comps['Place'].str.split(',').str[0]
        states = comps['Place'].str.split(',').str[-1]

        index = list(zip(companies, cities, states))

        df = read_file(year)

        value = len(df)
        start = 0
        end = 0

        for i in range(value):
            if 'START OF RECORDS' in df.iloc[i,0]:
                start = i
            elif 'END OF RECORDS' in df.iloc[i,0]:
                end = i+1

        df = df.drop(df.index[end:value])
        df = df.drop(df.index[0:start])
        df = df.reset_index(drop=True)

        df['Info'] = df['Info'].str.replace('\t', ' ')
        df['Info'] = df['Info'].str.replace('. 0.', '. O.')
        df['Info'] = df['Info'].str.replace(', 0.', ', O.')
        df = df[df['Info'].map(len) > 4]

        df['Info'].replace('', np.nan, inplace=True)
        df.dropna(subset=['Info'], inplace=True)
        df = df.reset_index(drop=True)

        unwanted = []

        for x in df['Info']:
            if 'MANUAL' in x or 'McGRAW' in x or 'AMERICAN STREET' in x or 'INVESTMENTS' in x or 'UNIVERSITY' in x:
                unwanted.append(x)

        unwanted = list(set(unwanted))

        df['Unwanted'] = df['Info'].isin(unwanted)

        listA= df[df['Unwanted'] == True].index.tolist()

        listB= []

        for x in listA:
            try:
                if capratio(df['Info'][x+1]) < 0.7 and len(df['Info'][x+1]) < 20:
                   listB.append(x+1)
                if capratio(df['Info'][x-1]) < 0.7 and len(df['Info'][x-1]) < 20:
                   listB.append(x-1)
                if capratio(df['Info'][x+2]) < 0.7 and len(df['Info'][x+2]) < 20:
                   listB.append(x+2)
                if capratio(df['Info'][x-2]) < 0.7 and len(df['Info'][x-2]) < 20:
                   listB.append(x-2)
                if capratio(df['Info'][x+3]) < 0.7 and len(df['Info'][x+3]) < 20:
                   listB.append(x+3)
                if capratio(df['Info'][x-3]) < 0.7 and len(df['Info'][x-3]) < 20:
                   listB.append(x-3)
                if capratio(df['Info'][x+4]) < 0.7 and len(df['Info'][x+4]) < 20:
                   listB.append(x+4)
                if capratio(df['Info'][x-4]) < 0.7 and len(df['Info'][x-4]) < 20:
                   listB.append(x-4)
            except:
                pass

        listC = listA+listB
        indexes_to_keep = list(set(list(range(len(df)))) - set(listC))
        df = df.take(indexes_to_keep)   
        df = df.reset_index(drop=True)
        
        df['Truth'] = df['Info'].str.contains('Capital Stock|Funded Debt')
        for x in range(len(df['Truth'])):
            if df['Truth'][x]:
                df['Truth'][x-1] = True
                df['Truth'][x-2] = True
    
        df['Cities'] = df['Info'].apply(getcities)
        df['RealCities'] = df['Cities'].apply(city2)
        df['RealCities'] = df['RealCities'].ffill()

        df['Miles'] = df['Info'].apply(getmiles)

        df['Company'] = df[1:len(df)].apply(lambda x: getcompanies(x.Info, x.RealCities, index, x.Truth), axis=1)
        df['Company'] = df[1:len(df)].apply(lambda x: getcompanies2(x.Info, x.RealCities, x.Company, index, x.Truth), axis=1)

        for i in range(len(df)):
            try:
                if df['Company'][i] is not None and df['Company'][i+1] is None and df['RealCities'][i] == df['RealCities'][i+1]:
                    df['Company'][i+1] = df['Company'][i]
            except:
                pass

        df['State'] = df.apply(lambda x: getstate(x.Company, x.RealCities, index), axis=1)

        extract = []

        for x in range(len(df)):
            if df['Miles'][x] != 'No':
                extract.append(x)
        results = df.take(extract)
        results = results.drop(columns=['Info', 'Cities', 'Unwanted'])
        display(results)
    except:
        pass
