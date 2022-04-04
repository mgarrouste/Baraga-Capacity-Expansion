from email import header
import pandas as pd 
import matplotlib.pyplot as plt
#import geopandas as gpd 
#from shapely.geometry import Point
import os 
import seaborn as sns

def createLocData(box=(46.420557,46.967298,-88.990959,-88.678627), folder='baraga_county_wind_data'):
    files  = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    #print(files)
    dicttodf = { 'id':[], 'latitude':[], 'longitude':[]}
    print(box)
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
    #print(windSpeeds)
    nbBins = 25
    fig, ax  = plt.subplots(figsize=(8,7))
    winddf = pd.DataFrame(data=windSpeeds, columns=['Wind Speed at 100m (m/s)'])
    p = sns.histplot(data=winddf, x ='Wind Speed at 100m (m/s)', stat='probability', ax=ax)
    plt.savefig('./wind_speeds_distribution.png')
    plt.close()

def createCFData(folder):
    files  = [os.path.join(folder,f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    times = ['t'+str(k+1) for k in range(8761)]
    header = ['']+['w'+str(k) for k in range(1,9)]
    print(times)
    print(header)
    for f in files: 
        df = pd.read_csv(f, skiprows=1)
        windSpeeds =list(df['wind speed at 100m (m/s)'])
    



if __name__ == "__main__":
    # Get to script directory
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(scriptPath)
    df = createLocData(folder='baraga_county_wind_data_subset')
    #createMap(df, './map_baraga.png') : initial png wrong
    plotWindDistribution('baraga_county_wind_data_subset')