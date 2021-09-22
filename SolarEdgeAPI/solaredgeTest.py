import solaredge
import pandas

def getDateList(startDate, endDate):
    dateArray = pandas.date_range(startDate, endDate, freq='m')
    for i, date in enumerate(dateArray):
        if i != len(dateArray) - 1:
           print(str(dateArray[i]) + ' : ' + str(dateArray[i+1]))



    #dateList
    #return dateList

devices = [
    {'id': 2384458, 'apikey': 'FZHDW756GBLH5CCTG2TS5UUZS9QUVFMK', 'house': 10},
    {'id': 2274372, 'apikey': '5ZOGJGOZ4ZXMFP9QHD3UYRM4T8H64VH1', 'house': 14},
    {'id': 2055689, 'apikey': '4ATE07E0ZGRPGKPKLUBOUJFXZMHPQXK9', 'house': 17},
    {'id': 1816420, 'apikey': 'AD3375GQD9ZZMURNQAY42TUZ2C03CMR3', 'house': 19},
    {'id': 2384874, 'apikey': 'LA804POO6SL8G8EKB2EC3IYI5RMFNBXE', 'house': 22},
    {'id': 2243196, 'apikey': '2RVNDJ2MA5STRHJSXPKQ4OXQMFFNY6RM', 'house': 23},
    {'id': 2401661, 'apikey': 'ZWW4AYR5T2HI7K4FKAQX3FZ1EE62O5N4', 'house': 24}
]

for device in devices:
    # Inititalise api request object for each device
    s = solaredge.Solaredge(device.get('apikey'))
    print('Home ' + str(device.get('house')) + ':')
    #print(s.get_data_period(device.get('id')))
    dataPeriod = s.get_data_period(device.get('id')).get('dataPeriod')
    print(dataPeriod)
    #energyData = s.get_energy(device.get('id'), dataPeriod.get('startDate'), dataPeriod.get('endDate'), time_unit='QUARTER_OF_AN_HOUR')
    #imeFrameEnergyData = s.get_time_frame_energy(device.get('id'), '2021-08-30', '2021-08-31', time_unit='DAY')
    #print(energyData)
    #getDateList('2021-01-30', '2021-08-31')
    #print(timeFrameEnergyData)

    # details = s.get_inventory(device.get('id'))
    # meters = details.get('Inventory').get('meters')
    # meter_names = ''
    # for meter in meters:
    #     meter_names = meter_names + ', ' + meter.get('name')
    #print(meter_names)

def downloadEnergyData(id, apikey):
    s = solaredge.Solaredge(device.get(apikey))
    dataPeriod = s.get_data_period(device.get('id')).get('dataPeriod')
    energyData = s.get_energy(id, dataPeriod.get('startDate'), dataPeriod.get('endDate'), time_unit='DAY')



#print(s.get_list())

#print(s.get_details('2384458'))

#print(s.get_data_period('2384458'))

#print(s.get_inventory('2384458'))




