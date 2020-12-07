-- Data Loading script for postgresql
--  \i 'db/postgres/init/views.sql'

\copy work_order FROM 'db/cleaned/work_order.csv' DELIMITER ',' CSV;

-- Loading Meter data
DROP TABLE IF EXISTS meter_reading_tmp;
CREATE TABLE meter_reading_tmp (
    bartdept      varchar(8),
    assetnum      INT,
    description   TEXT,
    status        varchar(16),
    metername     varchar(16),
    readingsource varchar(32),
    reading       FLOAT,
    delta         FLOAT,
    readingdate   date,
    enterdate     date
);
-- load the data into a temp table

\copy meter_reading_tmp FROM 'db/cleaned/all_meterdata.csv' DELIMITER ',' CSV;

UPDATE meter_reading_tmp SET delta   = 0 WHERE delta   IS NULL;
UPDATE meter_reading_tmp SET reading = 0 WHERE reading IS NULL;

INSERT INTO
    asset
SELECT DISTINCT
    assetnum as num,
    bartdept,
    description,
    status
FROM meter_reading_tmp;

INSERT INTO
    meter_reading
SELECT DISTINCT
    assetnum,
    metername,
    readingsource,
    reading,
    delta,
    readingdate,
    enterdate
FROM meter_reading_tmp;

DROP TABLE meter_reading_tmp;

VACUUM; -- clean up the temp data

-- DROP TABLE IF EXISTS asset_aliases;
-- CREATE TABLE asset_aliases (
--     asset INT,
--     alias varchar(32),
--     status varchar(32),
--     location varchar(16)
-- );
--  \COPY asset_aliases FROM 'db/cleaned/tmp_asset_aliases.csv' DELIMITER ',' CSV;

-- Loading MPUs
\copy mpu FROM 'db/cleaned/mpu.csv' DELIMITER ',' CSV;

CREATE VIEW
table_counts(name, counts) AS
    SELECT 'asset', COUNT(*) FROM asset
    UNION ALL
    SELECT 'meter_reading', COUNT(*) FROM meter_reading
    UNION ALL
    SELECT 'work_order', COUNT(*) FROM work_order
    UNION ALL
    SELECT 'mpu', COUNT(*) FROM mpu;
