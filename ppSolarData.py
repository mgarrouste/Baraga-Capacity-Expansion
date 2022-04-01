import pandas as pd
import matplotlib.pyplot as plt 
import os 
import matplotlib.dates as mdates 
from dateutil import parser


def cleanUpData(path='./baraga_solar3.csv'):
    solarData = pd.read_csv(path, skiprows=13)
    solarData.dropna(how='all',axis='columns',inplace=True)
    solarData['Time stamp']=solarData['Time stamp'].map(lambda x: parser.parse(x))
    time = pd.to_datetime(solarData['Time stamp'])
    cf = solarData.iloc[:,-1].str.rstrip('%').astype(float)/100.0
    return time, cf

def plotSolarCF(time, cf): 
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    cf = cf*100
    ax.plot(time, cf, alpha=0.7, color='r')
    ax.set_xlabel('Date')
    ax.set_ylabel('Capacity factor (%)')
    ax.set_title('Baraga county solar capacity factor')
    ax.grid()
    fig.autofmt_xdate()
    plt.savefig('solarCF')
    plt.close()

if __name__ =="__main__":
    # Get to script directory
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(scriptPath)
    time, cf  = cleanUpData()
    plotSolarCF(time, cf)