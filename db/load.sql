.mode "csv"
.separator ","

-- Loading MPUs
.import "UC Merced 2020 SE Project/Monthly Project Update - MPU/mpu.csv" "mpu"

-- Loading Meter data
CREATE TABLE meter_reading_tmp (
    bartdept      varchar(8),
    assetnum      int,
    description   varchar(128),
    status        varchar(28),
    metername     varchar(28),
    readingsource varchar(28),
    reading       int,
    delta         int,
    readingdate   date,
    enterdate     date
);
-- load the data into a temp table
.import "UC Merced 2020 SE Project/Fares NonRevVehicles/all_meterdata.csv" "meter_reading_tmp"

INSERT INTO asset
    SELECT assetnum as num, bartdept, description, status
    FROM meter_reading_tmp
    GROUP BY num;
INSERT INTO meter_reading
    SELECT DISTINCT assetnum, metername, readingsource, reading, delta, readingdate, enterdate
    FROM meter_reading_tmp;
DROP TABLE meter_reading_tmp;

VACUUM; -- clean up the temp data
