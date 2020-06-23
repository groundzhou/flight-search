USE flight;

DROP TABLE IF EXISTS airport;
CREATE TABLE airport
(
    `airport_id` INT,
    `name`       VARCHAR(250),
    `city`       VARCHAR(250),
    `country`    VARCHAR(250),
    `iata`       CHAR(3),
    `icao`       CHAR(4),
    `latitude`   DOUBLE,
    `longitude`  DOUBLE,
    `altitude`   DOUBLE,
    `timezone`   INT,
    `dst`        CHAR(1),
    `tz`         VARCHAR(60),
    `type`       VARCHAR(20),
    `source`     VARCHAR(20),
    PRIMARY KEY (`airport_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS airline;
CREATE TABLE airline
(
    `airline_id` INT,
    `name`       VARCHAR(250),
    `alias`      VARCHAR(60),
    `iata`       CHAR(2),
    `icao`       CHAR(3),
    `callsign`   VARCHAR(250),
    `country`    VARCHAR(250),
    `active`     CHAR(1),
    PRIMARY KEY (`airline_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS route;
CREATE TABLE route
(
    `airline`                CHAR(2),
    `airline_id`             INT,
    `source_airport`         CHAR(3),
    `source_airport_id`      INT,
    `destination_airport`    CHAR(3),
    `destination_airport_id` INT,
    `codeshare`              CHAR(1),
    `stops`                  INT,
    `equipment`              VARCHAR(100)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS plane;
CREATE TABLE plane
(
    `name` VARCHAR(250) NOT NULL,
    `iata` CHAR(3),
    `icao` CHAR(4)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS flight;
CREATE TABLE flight
(
    dairport_code CHAR(3),
    dairport      VARCHAR(100),
    dterminal     VARCHAR(10),
    dcity_code    CHAR(3),
    dcity         VARCHAR(100),
    aairport_code CHAR(3),
    aairport      VARCHAR(100),
    aterminal     VARCHAR(10),
    acity_code    CHAR(3),
    acity         VARCHAR(100),
    airline_code  CHAR(2),
    airline       VARCHAR(100),
    flight_num    CHAR(6),
    plane_code    CHAR(3),
    plane_kind    VARCHAR(20),
    plane         VARCHAR(100),
    dtime         DATETIME,
    atime         DATETIME,
    price         INT,
    discount      DOUBLE,
    class         VARCHAR(100),
    punctuality   INT,
    stop          INT
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

LOAD DATA LOCAL INFILE '/home/suncaper/flight-search/data/airports_china.csv' INTO TABLE airport
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE '/home/suncaper/flight-search/data/airlines_china.csv' INTO TABLE airline
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE '/home/suncaper/flight-search/data/routes_china.csv' INTO TABLE route
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE '/home/suncaper/flight-search/data/basic/planes.csv' INTO TABLE plane
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' escaped by '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE '/home/suncaper/flight-search/data/flights.csv' INTO TABLE flight
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
