CREATE TABLE meter_reading_tmp (
    bartdept      varchar(8),
    assetnum      INT,
    description   VARCHAR(128),
    status        VARCHAR(28),
    metername     VARCHAR(28),
    readingsource VARCHAR(28),
    reading       INT,
    delta         INT,
    readingdate   date,
    enterdate     date
);

.mode "csv"
.separator ","
.import "bart_data/Fares NonRevVehicles/all_meterdata.csv" "meter_reading_tmp"

INSERT INTO asset
    SELECT assetnum as num, bartdept, description, status
    FROM meter_reading_tmp
    GROUP BY num;

INSERT INTO meter_reading
    SELECT assetnum, metername, readingsource, reading, delta, readingdate, enterdate
    FROM meter_reading_tmp;

DROP TABLE meter_reading_tmp;