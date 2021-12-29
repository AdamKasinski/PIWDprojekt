import os
import pandas as pd
from pandasql import sqldf
import pandasql
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import numpy as np



fils = os.listdir('dataWIZD')
files = {fils[i][:-4]:pd.read_csv(f'dataWIZD\\{fils[i]}') for i in range(len(fils))}



economy_sec = files['economy'][['Variable','UNIT','COU','Country','Year','Value','Measure']]
economy_sec['Country'].replace({'Korea': 'South Korea',"China (People's Republic of)":'China'}, inplace = True)
continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}
countries = economy_sec['Country']
conts = [continents[country_alpha2_to_continent_code(country_name_to_country_alpha2(country))] for country in countries]
economy_sec['Continent'] = conts


years = economy_sec['Year'].unique()
continent_vals = []
for i in economy_sec['Year'].unique():
    #second_one = []
    for j in (economy_sec['Continent'].unique()):
        continent_vals.append([np.mean(economy_sec[(economy_sec['Measure'] == '/capita, US$ exchange rate') & (economy_sec['Continent'] == j) & (economy_sec['Year'] == i)]['Value']),i,j])
    #continent_vals.append(second_one)
dfa = pd.DataFrame(continent_vals)
dfa.columns = ['val','year','cont']


lifeExpectancy_sec = files['lifeExpectancy'][['Variable','Measure','COU','Country','Year','Value','UNIT']]
lifeExpectancy_sec = lifeExpectancy_sec[lifeExpectancy_sec['Measure'] == 'Years']

females = lifeExpectancy_sec.loc[lifeExpectancy_sec['Variable'].str[:3].isin(['Fem']) & (lifeExpectancy_sec['Measure'] == 'Years')]
males = lifeExpectancy_sec.loc[lifeExpectancy_sec['Variable'].str[:3].isin(['Mal']) & (lifeExpectancy_sec['Measure'] == 'Years')]


revenue = files['revenue'][['GOV','TAX','Tax revenue', 'VAR', 'Indicator', 'COU','Country','Year','Unit Code', 'Unit','Value']]


ttrEuro = revenue[(revenue['GOV'] == 'SUPRA') & (revenue['TAX'] == 'TOTALTAX') & (revenue['Unit'] == 'Euro')]
ttrEuro = ttrEuro.sort_values(by=['Year'])

ttrNotEuro = revenue[(revenue['GOV'] == 'SUPRA') & (revenue['TAX'] == 'TOTALTAX') & (revenue['Unit'] != 'Euro')]
ttrNotEuro = ttrNotEuro.sort_values(by=['Year'])

ttrAll = revenue[(revenue['GOV'] == 'SUPRA') & (revenue['TAX'] == 'TOTALTAX')]
ttrAll = ttrAll.sort_values(by=['Year'])



z = lifeExpectancy_sec.loc[(lifeExpectancy_sec['Variable']=='Females at birth') & (lifeExpectancy_sec['Year']>=2010) & (lifeExpectancy_sec['Year']<=2019)][['COU','Country','Year','Value']]
d = economy_sec.loc[economy_sec['Variable']=='Purchasing Power Parities for GDP, US$'][['COU','Country','Year','Value']]

mysql = lambda q: sqldf(q, globals())


a = mysql('SELECT E.Country, E.Variable EconomyVar,E.COU ,E.Unit, E.Year, E.Value Val_Economy, L.Variable, L.Value LifeExpentancy FROM economy_sec E JOIN lifeExpectancy_sec L ON (E.Country = L.Country AND E.Year = L.Year)') 
a = a[(a['EconomyVar'] == 'Purchasing Power Parities for GDP, US$') & (a['UNIT'] == 'TXNUPPTX') & (a['LifeExpentancy'] > 20)]
k = 'Females at birth'
#d = a[['Country','Val_Economy','Variable','LifeExpentancy','Year','COU']]
d = a[a['Variable'] == k][['Country','Val_Economy','Variable','LifeExpentancy','Year','COU']]

kLe = 'birth'
ttLe = lifeExpectancy_sec[(lifeExpectancy_sec['Measure'] == 'Years') & ((lifeExpectancy_sec['Variable'] == f'Females at {kLe}') | (lifeExpectancy_sec['Variable'] == f'Males at {kLe}'))]


ttLe2 = lifeExpectancy_sec
years = ttLe2['Year'].unique()
le_vals = []
for i in ttLe2['Year'].unique():
    for j in (ttLe2['Variable'].unique()):
        le_vals.append([np.mean(ttLe2[(ttLe2['Variable'] == j) & (ttLe2['Year'] == i)]['Value']),i,j])
df = pd.DataFrame(le_vals)
df.columns = ['val','year','var']

kle2 = 'birth'
dfe = df[(df['var'] == f'Females at {kle2}') | (df['var'] == f'Males at {kle2}')]

revenueLE = mysql('SELECT R.GOV,R.TAX,R."Tax Revenue",R.INDICATOR,R.COU,R.COUNTRY,R.YEAR,R.Unit,R.Value rev_unit, L.Variable, L.Measure, L.Value le_value FROM revenue R JOIN lifeExpectancy_sec L ON (R.Year = L.Year and R.Country = L.Country)')
revenueLE = revenueLE[revenueLE['Measure'] == 'Years']
revenueLE['Country'].replace({'Korea': 'South Korea',"China (People's Republic of)":'China'}, inplace = True)
continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}
countr = revenueLE['Country']
conts = [continents[country_alpha2_to_continent_code(country_name_to_country_alpha2(country))] for country in countr]
revenueLE['Continent'] = conts
revenueLE2 = revenueLE[(revenueLE['Variable'] == 'Total population at birth') & (revenueLE['Continent'] != 'Australia') & (revenueLE['Tax revenue'] == 'Total tax revenue')]
