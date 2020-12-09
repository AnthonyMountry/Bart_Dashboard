.mode "csv"
.separator ","

-- Loading MPUs
.import "db/cleaned/mpu.csv" "mpu"
SELECT 'mpu loaded';
.import "db/cleaned/work_order.csv" "work_order"
SELECT 'work_order loaded';

-- Loading Meter data
CREATE TABLE meter_reading_tmp (
    bartdept      varchar(8),
    assetnum      int,
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

.import "db/cleaned/all_meterdata.csv" "meter_reading_tmp"

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

SELECT "meter_reading loaded";

CREATE TABLE asset_aliases (
    asset integer,
    alias varchar(32),
    status varchar(32),
    location varchar(16)
);

--.import "UC Merced 2020 SE Project/tmp_asset_aliases.csv" "asset_aliases"
.import "db/cleaned/tmp_asset_aliases.csv" "asset_aliases"
SELECT 'tmp_asset_aliases loaded';

CREATE TABLE _tmp_project_meter (
	project                  VARCHAR(3),
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

.import "db/cleaned/project_meter.csv" "_tmp_project_meter"

UPDATE _tmp_project_meter SET tpid = -1            WHERE tpid = 'NO LISTED PROJECT WO';
UPDATE _tmp_project_meter SET workorder_num = -1   WHERE workorder_num = 'NO LISTED PROJECT';
UPDATE _tmp_project_meter SET goal = -1            WHERE goal = 'NO KNOWN GOAL';
UPDATE _tmp_project_meter SET meter_reading = 0    WHERE meter_reading = '';
UPDATE _tmp_project_meter SET reported_date = null WHERE reported_date = 'NO LISTED PROJECT WO';

delete from project_meter;

INSERT INTO project_meter
SELECT *
FROM _tmp_project_meter
GROUP BY
	metername,
	reading_date,
	workorder_num,
	tpid
HAVING COUNT(*) = 1;

select * from project_meter where tpid != -1;

-- CREATE TABLE project_meter (
-- 	project varchar(3),
-- 	name varchar(10),
-- 	location varchar(8),
-- 	description TEXT,
-- 	units varchar(24),
-- 	status varchar(20),
-- 	tpid INTEGER NOT NULL
-- );

-- insert into project_meter
-- select distinct
--    	        metername as name,
--    	        meter_location as location,
--    	        meter_description as description,
--    	        meter_units as units,
--    	        current_status as status,
-- from _tmp_project_meter;

-- insert into project_meter
--      select
-- 			project as project,
--    	        metername as name,
--    	        meter_location as location,
--    	        meter_description as description
--    	        meter_units as units,
--    	        current_status as status,
--    	        tpid
--        from _tmp_project_meter
--    group by metername;

SELECT 'project_meter loaded';

