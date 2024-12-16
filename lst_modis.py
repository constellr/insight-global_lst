import ee
import pandas as pd

ee.Authenticate()
ee.Initialize()

def get_modis_time_series(csv, startdate, enddate):

    citylist = pd.read_csv(csv)

    lst = ee.ImageCollection('MODIS/061/MOD11A1')

    LST_day = lst.select('LST_Day_1km', 'QC_Day').filterDate(startdate, enddate)
    LST_night = lst.select('LST_Night_1km', 'QC_Night').filterDate(startdate, enddate)

    selection = citylist[
        ((citylist['population'] > 250000) & (citylist['country'] != "China") & (citylist['country'] != "India")) |
         ((citylist['population'] > 5000000) & (citylist['country'] == "China") & (citylist['country'] == "India"))
    ]

    collection = pd.DataFrame()
    for i, row in selection.iterrows():

        lon = row["lng"]
        lat = row["lat"]
        name = row["city"]
        country = row["country"]
        pop = row["population"]

        point = ee.Geometry.Point(lon, lat)

        scale = 1000

        lst_daily = LST_day.getRegion(point, scale).getInfo()
        lst_night = LST_night.getRegion(point, scale).getInfo()

        df = pd.DataFrame(lst_daily)
        gf = pd.DataFrame(lst_night)

        headers_1 = df.iloc[0]
        headers_2 = gf.iloc[0]

        df = pd.DataFrame(df.values[1:], columns=headers_1)
        df = df[['longitude', 'latitude', 'time', 'LST_Day_1km']].dropna()

        gf = pd.DataFrame(gf.values[1:], columns=headers_2)
        gf = gf[['longitude', 'latitude', 'time', 'LST_Night_1km']].dropna()

        df['LST_Day_1km'] = pd.to_numeric(df['LST_Day_1km'], errors='coerce')
        df['datetime'] = pd.to_datetime(df['time'], unit='ms')
        df = df[['time', 'datetime', 'LST_Day_1km']]
        df['city'] = name
        df['country'] = country
        df['lat'] = lat
        df['lon'] = lon
        df['pop'] = pop

        gf['LST_Night_1km'] = pd.to_numeric(gf['LST_Night_1km'], errors='coerce')
        gf['datetime'] = pd.to_datetime(gf['time'], unit='ms')
        gf = gf[['time', 'datetime', 'LST_Night_1km']]
        gf['city'] = name
        gf['country'] = country
        gf['lat'] = lat
        gf['lon'] = lon
        gf['pop'] = pop

        def kelvin_to_celcius(t_kelvin):
            t_celsius = t_kelvin * 0.02 - 273.15
            return t_celsius

        df['LST_Day_1km'] = df['LST_Day_1km'].apply(kelvin_to_celcius)
        df['LST_Night_1km'] = gf['LST_Night_1km'].apply(kelvin_to_celcius)

        collection = pd.concat([collection,df])

    collection['year'] = collection['datetime'].dt.year
    collection['month'] = collection['datetime'].dt.month

    return collection




