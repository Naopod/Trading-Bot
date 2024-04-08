import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def fetch_news_calendar():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    u = 'https://www.forexfactory.com/calendar?day=today'

    session = requests.Session()
    r = session.get(u, timeout=30, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    events_cal = []

    for events in soup.select('.calendar__row'):
        time_elem = events.select_one('.calendar__cell.calendar__time')
        currency_elem = events.select_one('.calendar__cell.calendar__currency')
        title_elem = events.select_one('.calendar__cell.calendar__event')
        actual_elem = events.select_one('.calendar__cell.calendar__actual')
        forecast_elem = events.select_one('.calendar__cell.calendar__forecast')
        previous_elem = events.select_one('.calendar__cell.calendar__previous')
        
        impact_elem = events.select_one('.calendar__cell.calendar__impact')
        impact_class = impact_elem.find('span').get('class') if impact_elem and impact_elem.find('span') else ''
        if impact_class == ['icon', 'icon--ff-impact-red']:
            impact = 'high'
        else:
            impact = ''

        time = time_elem.text if time_elem else ''
        currency = currency_elem.text if currency_elem else ''
        title = title_elem.text if title_elem else ''
        actual = actual_elem.text if actual_elem else ''
        forecast = forecast_elem.text if forecast_elem else ''
        previous = previous_elem.text if previous_elem else ''

        events_cal.append({'Time': time,
                           'Title': title,
                           'Currency': currency,
                           'Impact': impact,
                           'Actual': actual,
                           'Previous': previous,
                           'Forecast': forecast})

    df = pd.DataFrame(events_cal)
    df = df[df['Impact']=='high']
    
    return df

########################GUI###########################

sg.theme('DarkBlue')

# Define a look and feel theme for the GUI
sg.LOOK_AND_FEEL_TABLE['DarkBlue'] = {
    'BACKGROUND': '#2C2F33',
    'TEXT': '#C7C7C7',
    'INPUT': '#2D3E50',
    'TEXT_INPUT': '#C7C7C7',
    'SCROLL': '#C7C7C7',
    'BUTTON': ('white', '#7289DA'),
    'PROGRESS': ('#01826B', '#D0D0D0'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}


df = fetch_news_calendar()

# Initial setup
headings = list(df.columns)
values = df.values.tolist()

layout = [[sg.Table(values=values,
                    headings=headings,
                    auto_size_columns=False,
                    col_widths=list(map(lambda x: len(x) + 8, headings)),
                    key='-TABLE-')]]

window = sg.Window('Calendar - Important News today', layout)

# This counter is to track the time elapsed and fetch new data every 300 seconds (5 minutes)
counter = 0

while True:
    event, values = window.read(timeout=100)  # Read with a timeout of 100 ms
    
    # Break the loop if the window is closed
    if event == sg.WINDOW_CLOSED:
        break
    
    # Increment counter by 0.1 second (100 ms)
    counter += 0.1

    # Check if 5 minutes have passed; 5 minutes = 300 seconds
    if counter >= 300:
        # Fetch new data
        df = fetch_news_calendar()
        
        # Update the Table Element
        headings = list(df.columns)
        values = df.values.tolist()
        window['-TABLE-'].update(values=values, col_widths=list(map(lambda x: len(x) + 8, headings)))

        # Reset counter
        counter = 0

window.close()