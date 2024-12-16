import os
import numpy as np
import pandas as pd

from lst_modis import get_modis_time_series
from map_app import make_3d_map

if __name__ == '__main__':

    csv = "data/worldcities.csv"
    csv_daily = "data/worldcities_all_LST.csv"
    csv_month = "data/worldcities_all_LST_monthly.csv"

    startdate = '2014-01-01'
    enddate = '2024-11-01'

    if os.path.exists(csv_daily) == False:
        lst_daily = get_modis_time_series(csv, startdate, enddate)
        print (True)
    else:
        lst_daily = pd.read_csv(csv_daily)

    lst_daily['LST_Day'] = np.round(lst_daily['LST_Day_1km'], 1)
    lst_daily['LST_Night'] = np.round(lst_daily['LST_Night_1km'], 1)
    lst_daily.to_csv(csv_daily)

    lst_monthly = lst_daily.groupby(['city', 'country', 'month', 'year', 'lat', 'lon', 'pop'])[['LST_Day', 'LST_Night']].max().reset_index()
    lst_monthly.to_csv(csv_month)

    make_3d_map(lst_monthly)
