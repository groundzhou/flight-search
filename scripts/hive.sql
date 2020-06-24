USE flight;

-- 所有航班数据
DROP TABLE IF EXISTS dws_flight;
CREATE EXTERNAL TABLE dws_flight
(
    dairport_code STRING,
    dairport      STRING,
    dterminal     STRING,
    dcity_code    STRING,
    dcity         STRING,
    aairport_code STRING,
    aairport      STRING,
    aterminal     STRING,
    acity_code    STRING,
    acity         STRING,
    airline_code  STRING,
    airline       STRING,
    flight_num    STRING,
    plane_code    STRING,
    plane_kind    STRING,
    plane         STRING,
    dtime         STRING,
    atime         STRING,
    price         INT,
    discount      DOUBLE,
    class         STRING,
    punctuality   INT,
    stop          INT
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/warehouse/flight/dws_flight/';

-- 每天最低价格
DROP TABLE IF EXISTS ads_min_price;
CREATE EXTERNAL TABLE ads_min_price
(
    dcity_code STRING,
    acity_code STRING,
    ddate STRING,
    min_price  INT
) LOCATION '/warehouse/flight/ads_min_price/';

INSERT OVERWRITE TABLE ads_min_price
SELECT dcity_code,
       acity_code,
       date(dtime),
       min(price)
from dws_flight
GROUP BY dcity_code,
         acity_code,
         date(dtime);
