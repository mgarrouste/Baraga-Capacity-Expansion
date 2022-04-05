from email import header
import pandas as pd 
import matplotlib.pyplot as plt
#import geopandas as gpd 
#from shapely.geometry import Point
import os 
import seaborn as sns
import numpy as np
import csv

def createLocData(box=(46.420557,46.967298,-88.990959,-88.678627), folder='baraga_county_wind_data'):
    files  = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    dicttodf = { 'id':[], 'latitude':[], 'longitude':[]}
    for f in files: 
        templist = f.split('_')
        # Check latitude and laongitude are in baraga county limits
        lat = float(templist[1])
        long = float(templist[2])
        if lat>box[0] and lat<box[1] and long>box[2] and long>box[3]:
            dicttodf['id'].append(int(templist[0]))
            dicttodf['latitude'].append(lat)
            dicttodf['longitude'].append(long)
            checkLat = True
    df = pd.DataFrame(dicttodf)
    return df 

def createMap(df, map_image):
    BBox = (df.longitude.min(), df.longitude.max(),df.latitude.min(),df.latitude.max())
    print(BBox)
    map = plt.imread(map_image)
    fig, ax = plt.subplots(figsize=(8,7))
    ax.scatter(df.longitude, df.latitude, zorder=1, alpha=0.2, c='b', s=10)
    ax.set_title('Wind Stations Locations Baraga County')
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.imshow(map, zorder=0, extent=BBox, aspect='equal')
    plt.savefig('./map_baraga_wind_loc.png')
    plt.close()

def plotWindDistribution(folder):
    files  = [os.path.join(folder,f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    windSpeeds =[]
    for f in files:
        df = pd.read_csv(f, skiprows=1)
        windSpeeds+=list(df['wind speed at 100m (m/s)'])
    nbBins = 25
    fig, ax  = plt.subplots(figsize=(8,7))
    winddf = pd.DataFrame(data=windSpeeds, columns=['Wind Speed at 100m (m/s)'])
    p = sns.histplot(data=winddf, x ='Wind Speed at 100m (m/s)', stat='probability', ax=ax)
    plt.savefig('./wind_speeds_distribution.png')
    plt.close()
    
def windspeedToCF(windSpeed, powerCurve):
    df = pd.read_csv(powerCurve)
    windSRefs = np.array(df.iloc[:,0])
    power = list(df.iloc[:,1])
    maxPower = max(power)
    CF =[]
    for ws in windSpeed:
        # Cutout speed
        if ws >25:
            ws=25
        index = np.argmin(np.abs(windSRefs-ws))
        CF.append(power[index]/maxPower)
    return CF
    

def createCFData(folder):
    files  = [os.path.join(folder,f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    times = ['t'+str(k+1) for k in range(8760)]
    header = ['']+['w'+str(k) for k in range(1,9)]
    dico = {}
    count = 1
    for f in files: 
        df = pd.read_csv(f, skiprows=1)
        ws =list(df['wind speed at 100m (m/s)'])
        keyWind = 'w'+str(count)
        dico[keyWind] = windspeedToCF(ws,'NREL_2000kW_power_curve.csv')
        count +=1
    with open('windCF.csv', mode='w', newline='') as CFfile:
        writer = csv.writer(CFfile, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        for k in range(8760):
            row = [times[k]]+[dico['w'+str(loc)][k] for loc in range(1,9)]
            writer.writerow(row)



if __name__ == "__main__":
    # Get to script directory
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(scriptPath)
    folder = 'baraga_county_wind_data_subset'
    df = createLocData(folder=folder)
    #createMap(df, './map_baraga.png') : initial png wrong
    plotWindDistribution(folder)
    createCFData(folder)