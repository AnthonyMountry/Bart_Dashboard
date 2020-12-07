.mode "csv"
.separator ","

-- Loading MPUs
.import "db/cleaned/mpu.csv" "mpu"
SELECT "mpu loaded";
.import "db/cleaned/work_order.csv" "work_order"
SELECT "work_order loaded";

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
	project            VARCHAR(3),
	department         VARCHAR(20),
	meter_location     VARCHAR(8),
	metername          VARCHAR(10),
	meter_description  VARCHAR(128),
	meter_reading      INTEGER,
	reading_date       DATE,
	meter_units_sql    VARCHAR(4),
	meter_units_from_project VARCHAR(22),
	meter_units        VARCHAR(22),
	goal               INTEGER,
	completion_percent VARCHAR(8),
	goal_group         VARCHAR(32),
	workorder_num      INTEGER NOT NULL,
	description        VARCHAR(128),
	current_status     VARCHAR(20),
	reported_date      DATE,
	type               TEXT,
	tpid               INTEGER NOT NULL,
	ps_project              TEXT,
	ps_project_description  TEXT,
	ps_activity             TEXT,
	ps_activity_description TEXT,
);

.import "db/cleaned/project_meter.csv" "_tmp_project_meter"

SELECT 'project_meter loaded';

