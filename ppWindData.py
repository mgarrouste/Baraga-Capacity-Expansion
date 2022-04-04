import pandas as pd 
import matplotlib.pyplot as plt
#import geopandas as gpd 
#from shapely.geometry import Point
import os 

def createLocData(folder='baraga_county_wind_data'):
    files  = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    #print(files)
    dicttodf = { 'id':[], 'latitude':[], 'longitude':[]}
    for f in files: 
        templist = f.split('_')
        dicttodf['id'].append(int(templist[0]))
        dicttodf['latitude'].append(float(templist[1]))
        dicttodf['longitude'].append(float(templist[2]))
    df = pd.DataFrame(dicttodf)
    print(df.head())


if __name__ == "__main__":
    # Get to script directory
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(scriptPath)
    createLocData(folder='baraga_county_wind_data')