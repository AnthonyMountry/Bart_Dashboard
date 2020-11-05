-- Assets
-- Files: Fares NonRevVehicles/* and Power/POWER Meter Data (all).xlsx
CREATE TABLE asset (
    num         int,
    bartdept    varchar(8),
    description varchar(100),
    status      varchar(16)
);

-- Files: Fares NonRevVehicles/* and Power/POWER Meter Data (all).xlsx
CREATE TABLE meter_reading (
    assetnum      int,
    metername     varchar(16),
    readingsource varchar(32),
    reading       int,
    delta         int,
    readingdate   date,
    enterdate     date
);

CREATE TABLE mpu (
    id                varchar(14),
    name              varchar(128),
    short_name        varchar(128),
    ranking           int,
    description       varchar(128),
    location          varchar(32),
    sub_location      varchar(32),
    district_location varchar(64),
    mpu_phase         varchar(32),
    budget_amount     float,
    expended_amount   float,
    monthly_burn_rate float,
    remaining_budget  float,
    funding_level     varchar(16),
    rr_funded         boolean,
    project_group     varchar(64),
    project_manager   varchar(32),
    accomplishments   varchar(128),
    program           varchar(32),
    review_format     varchar(32),
    end_date          date,
    CHECK (rr_funded IN (0, 1))
);

-- Work orders
-- File: Power/POWER WOs 9-22-2018 to 9-21-2020.xlsx
CREATE TABLE power_work_order (
    wonum                 INT NOT NULL, -- work order number
    description           VARCHAR(128),
    detail_description    VARCHAR(128),
    -- TODO most of the "alias" column has INTs but some look like "64-14-19150-2704"
    alias                 VARCHAR(32),
    location              VARCHAR(64),
    loc_desc              VARCHAR(128),
    worktype              VARCHAR(8),
    asset_type            VARCHAR(16),
    bartdept              VARCHAR(8),
    status                VARCHAR(28),
    reportdate            DATE,
    actstart              DATE,
    actfinish             DATE,
    actual_labor_hours    FLOAT,
    material_cost         FLOAT,
    problem_code_desc     VARCHAR(64),
    reason_to_repair_desc VARCHAR(64),
    component_desc        VARCHAR(64),
    part_failure_desc     VARCHAR(28),
    work_accomp_desc      VARCHAR(28),
    wl_date               DATE,
    wl_summary            VARCHAR(256),
    wl_summary_detail     VARCHAR(256)
);