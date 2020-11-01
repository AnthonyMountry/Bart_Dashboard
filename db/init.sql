-- Assets
-- Files: Fares NonRevVehicles/* and Power/POWER Meter Data (all).xlsx
CREATE TABLE meter_reading (
    bartdept      varchar(8),
    assetnum      INT NOT NULL PRIMARY KEY,
    description   VARCHAR(128),
    status        VARCHAR(28),
    metername     VARCHAR(28),
    readingsource VARCHAR(28),
    reading       INT,
    delta         INT,
    readingdate   DATE,
    enterdate     DATE
);

-- Work orders
-- File: Power/POWER WOs 9-22-2018 to 9-21-2020.xlsx
CREATE TABLE power_work_order (
    wonum                 INT NOT NULL PRIMARY KEY, -- work order number
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

-- MPU Sheet
-- Omitting lots of fields from the excel spreadsheet
-- File: Monthy Project Updates - MPU/MPU_July 20_20200820.xlsm
CREATE TABLE mpu (
    id                           VARCHAR(14) NOT NULL, -- primary key
    name                         VARCHAR(128),
    short_name                   VARCHAR(128),
    criteria_ranking             INT,
    location                     VARCHAR(128),
    sub_location                 VARCHAR(128),
    district_location            VARCHAR(64),
    bart_performing_design       BOOLEAN,
    bart_performing_construction BOOLEAN,
    project_plan                 VARCHAR(255),
    asset_risk_register_id       VARCHAR(20),
    budget_amount                INT,
    expended_amount              INT,
    funding_level                VARCHAR(32),
    end_date                     DATE,
    monthly_burn_rate            INT
);

-- Selection Criteria sheet
-- File: Monthy Project Updates - MPU/MPU_July 20_20200820.xlsm
CREATE TABLE mpu_selection_criteria (
    id              VARCHAR(14) NOT NULL,
    name            VARCHAR(128),
    MPL_status      VARCHAR(8),
    peoplesoft_pm   VARCHAR(128), -- Peoplesoft project manager
    rr_funded       BOOLEAN,
    fta_funded      BOOLEAN,
    program_manager VARCHAR(128),
    -- I hate this, if someone
    -- thinks of something better
    -- please tell me
    crit1       INT,
    crit2       INT,
    crit3       INT,
    crit4       INT,
    crit5       INT,
    crit6       INT,
    crit7       INT,
    crit8       INT,
    crit9       INT,
    crit10      INT,
    crit11      INT,
    crit12      INT,
    total_score INT
);

-- See file 'Monthly Project Update - MPU/MPU_July 20_20200820.xlsx'
-- This is a subtable that is part of 'mpu_selection_criteria'
-- File: Monthy Project Updates - MPU/MPU_July 20_20200820.xlsm
CREATE TABLE mpu_score_criteria (
    number INT, -- Criteria #4, Criteria #5, ect.
    weight INT
);

-- EXPFUNDS sheet
-- no columns skipped
-- File: Monthy Project Updates - MPU/MPU_July 20_20200820.xlsm
CREATE TABLE mpu_expiring_funds (
    id                  VARCHAR(14) NOT NULL,
    activity            VARCHAR(128),
    seq                 INT,
    rate                INT,
    gl_unit             VARCHAR(32),
    fund                VARCHAR(8),
    descr               VARCHAR(32),
    tgt_activity_id     VARCHAR(10),
    category            VARCHAR(14),
    threshold_amount    INT,
    distribution_amount INT,
    remaining_amount    INT,
    fund_dst_status     VARCHAR(2),
    seq2                INT,
    adjust              VARCHAR(2),
    seq_trans_id        INT,
    end_date            DATE,
    project_manager     VARCHAR(32),
    department          VARCHAR(64)
);

-- MILESTONES sheet
-- no columns skipped
-- File: Monthy Project Updates - MPU/MPU_July 20_20200820.xlsm
CREATE TABLE mpu_milestones (
    id            VARCHAR(14) NOT NULL,
    name          VARCHAR(128),
    phase         VARCHAR(32),
    task          VARCHAR(32),
    schedule_code VARCHAR(20),
    activity_name VARCHAR(64),
    currentdate   DATE,
    baseline_date DATE,
    days_ahead    INT
);
