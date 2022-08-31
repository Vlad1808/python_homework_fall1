import pprint 
import requests
import pandas as pd 
from datetime import date, datetime, timezone


loc = ['Bengaluru, India', 'Glasgow, Scotland', 'Gumi, South Korea', 'Lagos, Nigeria', 'Nanaimo, Canada', 
      'Niskayuna, New York', 'Nizhny Novgorod, Russia', 'Olongapo, Phillipines', 'Peshawar, Pakistan', 
       'Peterhead, Scotland', 'Quito, Ecuador', 'Simmern, Germany', 'Tainan, Taiwan', 'Tbilisi, Georgia', 
        'Vinh Long, Vietnam', "Xi'an, China"]


# wtiting a function to get the data so that it could iterate over a list of cities 
def weather_forecast_for_cities(city_name):
    api_key = '*****'
    URL = 'http://api.openweathermap.org/data/2.5/forecast?'
    URL = URL + 'q=' + city_name + '&appid=' + api_key + '&units=metric'

    response = requests.get( URL )
    if response.status_code == 200:      # Success
        data = response.json()
        return data
        printer = pprint.PrettyPrinter( width=80, compact=True )
        printer.pprint( data[ 'list' ] )
    else:                                # Failure
        print( 'Error:', response.status_code )
        
        
# iterating over the list of the cities and storing data in the list of lists 
weather_list=[]
for i in loc:
    weather_list.append(weather_forecast_for_cities(i))
    
# extracting the necessary data from the weather_list 
min_temp = []
max_temp = []
city = []
country = []
time = []
for i in range(0,len(weather_list)):
    for j in range(0, 40):
        city.append(weather_list[i]['city']['name'])
        country.append(weather_list[i]['city']['country'])
        min_temp.append(weather_list[i]['list'][j]['main']['temp_min'])
        max_temp.append(weather_list[i]['list'][j]['main']['temp_max'])
        time.append(weather_list[i]['list'][j]['dt_txt'])   

# storing individual lists into a data frame 
df = pd.DataFrame()
df['Min '] = min_temp
df['Max '] = max_temp
df['time'] = time
df['country'] = country
df['City'] = city   


# creating dates and the delta of days 
df['today'] = datetime.now(timezone.utc).date()
df['time'] = pd.to_datetime(df['time']).dt.normalize()
df['today'] = pd.to_datetime(df['today']).dt.normalize()
df['delta'] = (df['time'] - df['today']).dt.days
# filtering the dataset by data 
df = df.loc[(df['delta'] <= 4) & (df['delta'] != 0)]

# aggregating data 
df_pivot = pd.pivot_table(df, values = ['Min ', 'Max '], index = 'City', columns='delta', 
                   aggfunc={'Min ':'min', 'Max ':'max'}) \
.reset_index()


# getting rid of two levels of the column names
df_pivot.columns =[lev1 + str(lev2) for (lev1,lev2) in df_pivot.columns.tolist()]

# going back to the original city names 
df_pivot['City'] = loc

df_pivot = df_pivot[['City', 'Min 1', 'Max 1', 'Min 2', 'Max 2', 'Min 3', 'Max 3', 'Min 4', 'Max 4']]
df_pivot['Min Avg'] = round((df_pivot['Min 1'] + df_pivot['Min 2'] + df_pivot['Min 3'] + df_pivot['Min 4']) / 4, 2)
df_pivot['Max Avg'] = round((df_pivot['Max 1'] + df_pivot['Max 2'] + df_pivot['Max 3'] + df_pivot['Max 4']) / 4, 2)


df_pivot.to_csv('/Users/vladislavlukonin/temp.csv', index=False, float_format='%.2f')
