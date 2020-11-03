-- Assets
-- Files: Fares NonRevVehicles/* and Power/POWER Meter Data (all).xlsx
CREATE TABLE asset (
    num         int,
    bartdept    varchar(16),
    description varchar(128),
    status      varchar(28)
);

-- Files: Fares NonRevVehicles/* and Power/POWER Meter Data (all).xlsx
CREATE TABLE meter_reading (
    assetnum      int,
    metername     varchar(28),
    readingsource varchar(28),
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
    end_date          date
);
