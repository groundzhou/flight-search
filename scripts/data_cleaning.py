import os
import pandas as pd

DATA_PATH = '../data'
BASIC_DATA_PATH = os.path.join(DATA_PATH, 'basic')


# 处理基础数据
def main():
    # 全国机场数据
    airports_header = ['airport_id', 'name', 'city', 'country', 'iata', 'icao',
                       'latitude', 'longitude', 'altitude',
                       'timezone', 'dst', 'tz', 'type', 'source']
    df_airports = pd.read_csv(os.path.join(BASIC_DATA_PATH, 'airports.csv'), names=airports_header)
    df_airports_china = df_airports[(df_airports['country'] == 'China') |
                                    (df_airports['country'] == 'Hong Kong') |
                                    (df_airports['country'] == 'Taiwan') |
                                    (df_airports['country'] == 'Macau')]
    df_airports_china.to_csv(os.path.join(DATA_PATH, 'airports_china.csv'), header=airports_header, index=False)

    # 全国航空公司数据
    airlines_header = ['airline_id', 'name', 'alias', 'iata', 'icao', 'callsign', 'country', 'active']
    df_airlines = pd.read_csv(os.path.join(BASIC_DATA_PATH, 'airlines.csv'), names=airlines_header)
    df_airlines_china = df_airlines[(df_airlines['country'] == 'China') |
                                    (df_airlines['country'] == 'Hong Kong') |
                                    (df_airlines['country'] == 'Taiwan') |
                                    (df_airlines['country'] == 'Macau')]
    df_airlines_china.to_csv(os.path.join(DATA_PATH, 'airlines_china.csv'), header=airlines_header, index=False)

    airports_list = df_airports_china['airport_id'].astype('str').to_list()
    # 航班数据
    routes_header = ['airline', 'airline_id',
                     'source_airport', 'source_airport_id',
                     'destination_airport', 'destination_airport_id',
                     'codeshare', 'stops', 'equipment']
    df_routes = pd.read_csv(os.path.join(BASIC_DATA_PATH, 'routes.csv'), names=routes_header)
    df_routes_china = df_routes[df_routes['source_airport_id'].isin(airports_list) &
                                df_routes['destination_airport_id'].isin(airports_list)]

    df_routes_china.to_csv(os.path.join(DATA_PATH, 'routes_china.csv'), header=routes_header, index=False)


if __name__ == '__main__':
    main()
