DROP TABLE IF EXISTS airport;
CREATE TABLE airport (
    `airport_id` INT,
    `name` VARCHAR(250),
    `city` VARCHAR(250),
    `country`VARCHAR(250),
    `iata` CHAR(3),
    `icao` CHAR(4),
    `latitude` DOUBLE,
    `longitude` DOUBLE,
    `altitude` DOUBLE ,
    `timezone` INT,
    `dst` CHAR(1),
    `tz` VARCHAR(60),
    `type` VARCHAR(20),
    `source` VARCHAR(20),
    PRIMARY KEY (`airport_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS airline;
CREATE TABLE airline (
    `airline_id` INT,
    `name` VARCHAR(250),
    `alias` VARCHAR(60),
    `iata` CHAR(2),
    `icao` CHAR(3),
    `callsign` VARCHAR(250),
     `country` VARCHAR(250),
     `active` CHAR(1),
    PRIMARY KEY (`airline_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS route;
CREATE TABLE route (
    `airline` CHAR(2),
    `airline_id` INT,
    `source_airport` CHAR(3),
    `source_airport_id` INT,
    `destination_airport`CHAR(3),
    `destination_airport_id` INT,
    `codeshare` CHAR(1),
    `stops` INT,
    `equipment` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS plane;
CREATE TABLE plane (
    `name` VARCHAR(250) NOT NULL,
    `iata` CHAR(3),
    `icao` CHAR(4)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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