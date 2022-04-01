import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#print(os.getcwd())

def cleanUpData(path='./MISO.csv'):
    # Convert time stamps to date
    MISOdata = pd.read_csv(path)
    MISOdata['date_time'] =  pd.to_datetime(MISOdata['date_time'])
    # Create dataset with only dates and cleaned demand
    cleanMISOdata = MISOdata[['date_time','Cleaned Demand (MW)']].copy()
    # Scale down to 1000MW max
    cleanMISOdata['Cleaned Demand (MW)'] = 1000*cleanMISOdata['Cleaned Demand (MW)']/max(cleanMISOdata['Cleaned Demand (MW)'])
    cleanMISOdata.rename(columns={'Cleaned Demand (MW)':'demand'}, inplace=True)
    # Select only 2018 data
    print(cleanMISOdata.head())
    mask = (cleanMISOdata['date_time']>'2018-01-01') & (cleanMISOdata['date_time']<'2018-12-31')
    cleanMISOdata = cleanMISOdata.loc[mask]
    print(cleanMISOdata.head())
    return cleanMISOdata['date_time'], cleanMISOdata['demand']

def plotDemand(time, demand): 
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.plot(time, demand, alpha=0.7)
    ax.set_xlabel('Date')
    ax.set_ylabel('Demand (MW)')
    ax.set_title('MISO scaled down data')
    ax.grid()
    fig.autofmt_xdate()
    plt.savefig('2018_MISO_demand_scaled_1000MW')
    plt.close()

#cleanMISOdata.plot(kind='scatter',  x='date_time', y='demand', s=0.05, title='MISO scaled down data', ylabel='Demand (MW)',  xlabel='Date')


if __name__ =="__main__":
    # Get to script directory
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(scriptPath)
    time,demand = cleanUpData()
    plotDemand(time,demand)
