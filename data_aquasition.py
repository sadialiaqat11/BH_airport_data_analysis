from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import time


def collect_flight_data(day,flight_direction):
    '''
    this function collects the data from bahrain airport and return it as a table
    arg:
    day(str): it will be today(td) or tomorrow (tm).
    flight_direction (str): it will return arrival or departure
    returns:
    oandas dataframe that has 7b columns
    '''
    url=f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    time_lst=[]
    destination=[]
    airways_lst=[]
    gate_lst=[]
    status_lst=[]
    flight_lst=[]
    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"})
    for flight in flights:
    # print(i)
        try:
            airways_lst.append(flight.find('img')['alt'])
        except:
            airways_lst.append(pd.NA)
        flight_lst.append(flight.find('div',class_="col col-flight-no").text.strip())
        status_lst.append(flight.find('div',class_="col col-flight-status").text.strip())
        gate_lst.append(flight.find('div',class_="col col-gate").text.strip())
        # airways_lst.append(flight.find('img'))
        time_lst.append(flight.find('div',class_="col col-flight-time").text.strip())
        destination.append(flight.find('div',class_="col col-flight-origin").text.strip())
    flights_data={'origin': destination,
                  'flight Nm':flight_lst,
                  'airline':airways_lst,
                  'gate':gate_lst,
                  'status':status_lst,
                  'time':time_lst}
    df=pd.DataFrame(flights_data)
    TODAY_DATE= datetime.date.today()
    TOMORROW_DATE= TODAY_DATE+datetime.timedelta(days=1)
    if day=='TD':
        date=TODAY_DATE
    elif day=='TM':
        date=TOMORROW_DATE
    df['date']=date
    df['direction']=flight_direction
    return df

def collect_arrivals_dep():
    tables=[]
    directions= ['arrivals','departures']
    days =['TD','TM']
    for direction in directions:
        for day in days:
            df = collect_flight_data(day, direction)
            tables.append(collect_flight_data(day, direction))
            time.sleep(10)
    df = pd.concat(tables)
    return df
df=collect_arrivals_dep()
df

def save_data(df):
    today= datetime.date.today()
    path = f'all_flights_data_{today}.csv'.replace('-','_')
    df.to_csv(path)

df = collect_arrival_dep()
save_data(df)