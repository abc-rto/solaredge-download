import solaredge as solaredge
import pandas as pd
import json as json
import datetime
import dateutil.relativedelta
import os


# Set granularity required (multiple selections are allowed)
data30min = False
data1hour = True
dataDaily = True
dataMonthly = False

# Define SolarEdge devices to be queried
devices = [
    # {'id': 2384458, 'apikey': 'FZHDW756GBLH5CCTG2TS5UUZS9QUVFMK', 'house': 10},
    # {'id': 2274372, 'apikey': '5ZOGJGOZ4ZXMFP9QHD3UYRM4T8H64VH1', 'house': 14},
    {'id': 2055689, 'apikey': '4ATE07E0ZGRPGKPKLUBOUJFXZMHPQXK9', 'house': 17},
    {'id': 1816420, 'apikey': 'AD3375GQD9ZZMURNQAY42TUZ2C03CMR3', 'house': 19},
    #{'id': 2384874, 'apikey': 'LA804POO6SL8G8EKB2EC3IYI5RMFNBXE', 'house': 22},
    # {'id': 2243196, 'apikey': '2RVNDJ2MA5STRHJSXPKQ4OXQMFFNY6RM', 'house': 23},
    # {'id': 2401661, 'apikey': 'ZWW4AYR5T2HI7K4FKAQX3FZ1EE62O5N4', 'house': 24}
]

# 15min API returns max one month of data. This utility function converts start and end dates
# into a list of consecutive months that can be queried individually to obtain an entire 15min dataset


def getDateList(startDate, endDate):
    newStart = datetime.datetime.strptime(
        startDate, "%Y-%m-%d") - dateutil.relativedelta.relativedelta(months=1)
    newEnd = datetime.datetime.strptime(
        endDate, "%Y-%m-%d") + dateutil.relativedelta.relativedelta(months=1)
    dateArray = pd.date_range(newStart, endDate, freq='m')
    return dateArray

# Function to download, wrangle, and print energy data to csv


def downloadEnergyData(id, apikey):
    # Make a directory for the data
    if not os.path.exists(str(id)):
        os.makedirs(str(id))

    # Initizalise API object with site to analyze
    s = solaredge.Solaredge(apikey)

    # Overview
    details = json.dumps(s.get_details(id))
    inventory = json.dumps(s.get_inventory(id))
    overview = json.dumps(s.get_overview(id))

    summary = json.loads(
        '[' + details + ',' + inventory + ',' + overview + ']')

    with open(str(id) + '/' + str(id) + '-details.json', 'w') as f:
        json.dump(summary, f)

    # Request all available readings for each energy meter present from the API
    dataPeriod = s.get_data_period(id).get('dataPeriod')

    # Get date list here
    dateArray = getDateList(dataPeriod.get(
        'startDate'), dataPeriod.get('endDate'))

    # # Loop goes here
    for i, date in enumerate(dateArray):
        if i != len(dateArray) - 1:
           # print(str(dateArray[i]) + ' : ' + str(dateArray[i+1]))

           # Request from API
            energyDetails = s.get_energy_details(id, dateArray[i],
                                                 dateArray[i+1], time_unit='QUARTER_OF_AN_HOUR').get('energyDetails').get('meters')

            # Convert JSON payload into csv containing readings from each available meter
            dfTotal = pd.DataFrame()
            dfDate = pd.DataFrame()
            for meter in energyDetails:
                meterName = meter.get('type')
                meterValues = json.dumps(meter.get('values'))
                df = pd.read_json(meterValues)
                df.columns = ['date', 'values-' + meterName]
                dfTotal['date'] = df['date']
                dfTotal['values-' + meterName] = df['values-' + meterName]

            if not os.path.isfile(str(id) + '/' + str(id) + '-15min.csv'):
                dfTotal.to_csv(str(id) + '/' + str(id) +
                               '-15min.csv', header='column_names')
            else:  # else it exists so append without writing the header
                dfTotal.to_csv(str(id) + '/' + str(id) +
                               '-15min.csv', mode='a', header=False)

            if data30min == True:
                df30min = dfTotal.groupby(pd.Grouper(
                    key='date', freq='30min')).sum().reset_index()
                if not os.path.isfile(str(id) + '/' + str(id) + '-30min.csv'):
                    df30min.to_csv(str(id) + '/' + str(id) +
                                   '-30min.csv', header='column_names')
                else:  # else it exists so append without writing the header
                    df30min.to_csv(str(id) + '/' + str(id) +
                                   '-30min.csv', mode='a', header=False)

            if data1hour == True:
                dfhour = dfTotal.groupby(pd.Grouper(
                    key='date', freq='H')).sum().reset_index()
                if not os.path.isfile(str(id) + '/' + str(id) + '-houly.csv'):
                    dfhour.to_csv(str(id) + '/' + str(id) +
                                  '-hourly.csv', header='column_names')
                else:  # else it exists so append without writing the header
                    dfhour.to_csv(str(id) + '/' + str(id) +
                                  '-hourly.csv', mode='a', header=False)

            if dataDaily == True:
                dfDay = dfTotal.groupby(pd.Grouper(
                    key='date', freq='D')).sum().reset_index()
                if not os.path.isfile(str(id) + '/' + str(id) + '-daily.csv'):
                    dfDay.to_csv(str(id) + '/' + str(id) +
                                 '-daily.csv', header='column_names')
                else:  # else it exists so append without writing the header
                    dfDay.to_csv(str(id) + '/' + str(id) +
                                 '-daily.csv', mode='a', header=False)

            if dataMonthly == True:
                dfMonth = dfTotal.groupby(pd.Grouper(
                    key='date', freq='M')).sum().reset_index()
                if not os.path.isfile(str(id) + '/' + str(id) + '-monthly.csv'):
                    dfMonth.to_csv(str(id) + '/' + str(id) +
                                   '-monthly.csv', header='column_names')
                else:  # else it exists so append without writing the header
                    dfMonth.to_csv(str(id) + '/' + str(id) +
                                   '-monthly.csv', mode='a', header=False)


for device in devices:
    downloadEnergyData(device.get('id'), device.get('apikey'))
