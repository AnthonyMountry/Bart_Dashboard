-- Data Loading script for postgresql

--.mode "csv"
--.separator ","

-- Loading MPUs
--.import "UC Merced 2020 SE Project/Monthly Project Update - MPU/mpu.csv" "mpu"

COPY mpu
FROM '/home/harry/school/cse120/bart-dashboard/db/UC Merced 2020 SE Project/Monthly Project Update - MPU/mpu.csv'
DELIMITER ','
CSV;

-- Loading Meter data
DROP TABLE IF EXISTS meter_reading_tmp;
CREATE TABLE meter_reading_tmp (
    bartdept      varchar(8),
    assetnum      int,
    description   varchar(100),
    status        varchar(16),
    metername     varchar(16),
    readingsource varchar(32),
    reading       int,
    delta         int,
    readingdate   date,
    enterdate     date
);
-- load the data into a temp table
/**/
-- .import "UC Merced 2020 SE Project/Fares NonRevVehicles/all_meterdata.csv" "meter_reading_tmp"
COPY meter_reading_tmp
FROM '/home/harry/school/cse120/bart-dashboard/db/UC Merced 2020 SE Project/Fares NonRevVehicles/all_meterdata.csv'
DELIMITER ','
CSV;

INSERT INTO asset
    SELECT assetnum as num, bartdept, description, status
    FROM meter_reading_tmp
    GROUP BY num;
INSERT INTO meter_reading
    SELECT DISTINCT assetnum, metername, readingsource, reading, delta, readingdate, enterdate
    FROM meter_reading_tmp;
/**/
-- DROP TABLE meter_reading_tmp;

VACUUM; -- clean up the temp data

DROP TABLE IF EXISTS asset_aliases;
CREATE TABLE asset_aliases (
    asset INT,
    alias varchar(32),
    status varchar(32),
    location varchar(16)
);
COPY asset_aliases
FROM '/home/harry/school/cse120/bart-dashboard/db/UC Merced 2020 SE Project/tmp_asset_aliases.csv'
DELIMITER ','
CSV;

-- .import "UC Merced 2020 SE Project/tmp_asset_aliases.csv" "asset_aliases"