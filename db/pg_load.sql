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


CREATE TABLE _tmp_project_meter (
	project                  VARCHAR(30),
	department               VARCHAR(20),
	meter_location           VARCHAR(8),
	metername                VARCHAR(10),
	meter_description        VARCHAR(128),
	meter_reading            FLOAT,
	reading_date             DATE,
	meter_units_sql          VARCHAR(4), -- basically useless
	meter_units_from_project VARCHAR(22), -- same as meter_units
	meter_units              VARCHAR(22),
	goal                     INTEGER,
	completion_percent       VARCHAR(8),
	goal_group               VARCHAR(32),
	workorder_num            INTEGER NOT NULL,
	description              VARCHAR(128),
	current_status           VARCHAR(20),
	reported_date            DATE,
	type                     TEXT,
	tpid                     INTEGER NOT NULL,
	ps_project               VARCHAR(20),
	ps_project_description   TEXT,
	ps_activity              VARCHAR(20),
	ps_activity_description  TEXT
);

-- TODO This still has type errors
-- \copy _tmp_project_meter FROM 'db/cleaned/project_meter.csv' DELIMITER ',' CSV;

--  UPDATE _tmp_project_meter SET tpid = -1            WHERE tpid = 'NO LISTED PROJECT WO';
--  UPDATE _tmp_project_meter SET workorder_num = -1   WHERE workorder_num = 'NO LISTED PROJECT';
--  UPDATE _tmp_project_meter SET goal = -1            WHERE goal = 'NO KNOWN GOAL';
--  UPDATE _tmp_project_meter SET meter_reading = 0    WHERE meter_reading = '';
--  UPDATE _tmp_project_meter SET reported_date = null WHERE reported_date = 'NO LISTED PROJECT WO';
