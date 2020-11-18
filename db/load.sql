.mode "csv"
.separator ","

-- Loading MPUs
--.import "UC Merced 2020 SE Project/Monthly Project Update - MPU/mpu.csv" "mpu"
.import "cleaned/mpu.csv" "mpu"
.import "cleaned/work_order.csv" "work_order"

-- Loading Meter data
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
--.import "UC Merced 2020 SE Project/Fares NonRevVehicles/all_meterdata.csv" "meter_reading_tmp"
.import "cleaned/all_meterdata.csv" "meter_reading_tmp"

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

CREATE TABLE asset_aliases (
    asset integer,
    alias varchar(32),
    status varchar(32),
    location varchar(16)
);

--.import "UC Merced 2020 SE Project/tmp_asset_aliases.csv" "asset_aliases"
.import "cleaned/tmp_asset_aliases.csv" "asset_aliases"
