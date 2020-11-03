from os.path import (
    join as path_join,
    exists as path_exists,
)
import re
import sqlite3
from sqlite3 import Connection

import pyexcel as pe
from pyexcel.sheet import Sheet
from pyexcel.book import Book
from pyexcel.internal.generators import BookStream

BASE_DIR = 'UC Merced 2020 SE Project'

meter_schema_upper = [
    'BARTDEPT', 'ASSETNUM', 'DESCRIPTION', 'STATUS', 'METERNAME',
    'READINGSOURCE', 'READING', 'DELTA', 'READINGDATE', 'ENTERDATE',
]

meter_schema = [s.lower() for s in meter_schema_upper]

METER_READING_FILES = [
    "Fares NonRevVehicles/NRVE, AFC Meter Data 1.xlsx",
    "Fares NonRevVehicles/NRVE, AFC Meter Data 2.xlsx",
    "Fares NonRevVehicles/NRVE, AFC Meter Data 3.xlsx",
    "Fares NonRevVehicles/NRVE, AFC Meter Data 4.xlsx",
    "Fares NonRevVehicles/NRVE, AFC Meter Data 5.xlsx",
    "Fares NonRevVehicles/NRVE, AFC Meter Data 6.xlsx",
    "Fares NonRevVehicles/NRVE, AFC Meter Data 7.xlsx",
    "Power/POWER Meter Data (all).xlsx",
]

work_order_schema = [
    'wonum', 'description', 'detail_description', 'alias',
    'location', 'loc_desc', 'worktype', 'asset_type',
    'bartdept', 'status', 'reportdate', 'actstart',
    'actfinish', 'actual_labor_hours', 'material_cost',
    'problem_code_desc', 'reason_to_repair_desc', 'component_desc',
    'part_failure_desc', 'work_accomp_desc', 'wl_date',
    'wl_summary', 'wl_summary_detail',
]

mpu_schema_mappings = {
    "Project ID":         'id',
    "Project Name":       'name',
    "Project Short Name": 'short_name',
    "Ranking from Selection Criteria": 'ranking',
    "Scope Description": 'description',
    "Location":          'location',
    "Sub-location":      'sub_location',
    "District Location": 'district_location',
    "MPU Phase":         'mpu_phase',
    "Budget Amount":     'budget_amount',
    "Expended Amount":   'expended_amount',
    "Funding Level":     'funding_level',
    "RR Funded":         'rr_funded',
    "Group":             'project_group',
    "Project Manager":   'project_manager',
    "Accomplishments":   'accomplishments',
    "Program":           'program',
    "Review format":     'review_format',
    "Remaining Unencumbered Budget": 'remaining_budget',
    "End Date\n(from Milestones, or from MPL if no Milestone)": 'end_date',
    "Monthly Burn Rate \n(average 3 months of actual costs May 20, Jun 20, July 20)": 'monthly_burn_rate',
}

# only get the sheets that look like "8-11 Data"
throw_count_sheet_re = re.compile('[0-9]{1,2}-[0-9]{1,2} Data')
throw_count_files = [
    'TC Switch Machines/Switch Machine Count Report 8-24-20 r2.xlsx',
    'TC Switch Machines/Switch Machine Count Report 9-8-20.xlsx',
    'TC Switch Machines/Quarterly Throw Count Labor Evaluation - 2020-05-19.xlsx',
]

switch_machine_workorder_files = [
    'TC Switch Machines/Switch Machine WO By Quarter 8-5-2020 v2.xlsx'
]


# ----- Utilities ------

def write_sheet(sheet: Sheet, filename: str):
    with open(path_join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(sheet.get_csv())

def is_sql_sheet(s: Sheet) -> bool:
    return s.name.lower() == 'sql' or len(s) <= 2

def is_meter_data(sheet: Sheet) -> bool:
    return (
        sheet.row[0] == meter_schema_upper or
        sheet.row[0] == meter_schema
    )

# ----- Extract The Weird MPU Data -----

def extract_base(book):
    base: Sheet = book.sheet_by_index(0)
    base.delete_columns([0, 1])
    base.delete_rows(list(range(24)))
    write_sheet(base, 'Monthly Project Update - MPU/exceptions_template.csv')
    return base


def extract_mpu(book):
    column_re = re.compile('Column([0-9]+)')
    mpu: Sheet = book.sheet_by_name('MPU')
    mpu.delete_rows(list(range(14))) # remove garbage at the top
    mpu.delete_columns([0])          # delete empty column
    mpu.name_columns_by_row(0)       # set column names
    # Find empty columns (named "Column3" or
    # "Column9", ect.) and remove them
    bad_cols = []
    for i, col in enumerate(mpu.colnames):
        if column_re.match(col) is not None:
            bad_cols.append(i)
    mpu.delete_columns(bad_cols)
    # Delete the columns that we don't want
    desired_columns = set(mpu_schema_mappings.keys())
    names = set(mpu.colnames)
    for col in names.difference(desired_columns):
        mpu.delete_named_column_at(col)
    # Rename the columns based on the schema mapping
    for i, name in enumerate(mpu.colnames):
        mpu.colnames[i] = mpu_schema_mappings[name]
    write_sheet(mpu, 'Monthly Project Update - MPU/mpu.csv')
    return mpu


def extract_criteria(book):
    sheet: Sheet = book.sheet_by_name('Selection Criteria')
    sheet.delete_rows(list(range(9)))
    write_sheet(sheet, 'Monthly Project Update - MPU/criteria.csv')
    return sheet

def extract_expfunds(book):
    expfunds: Sheet = book.sheet_by_name('EXPFUNDS')
    expfunds.delete_rows([0, 1])
    write_sheet(expfunds, 'Monthly Project Update - MPU/expfunds.csv')
    return expfunds

def extract_milestones(book):
    milestones = book.sheet_by_name('MILESTONES')
    milestones.delete_rows([0, 1])
    write_sheet(milestones, 'Monthly Project Update - MPU/milestones.csv')
    return milestones

def combine_all_meterdata(csv_file):
    if not path_exists(csv_file):
        raise Exception('csv file does not exist')
    for f in METER_READING_FILES:
        filename = path_join(BASE_DIR, f)
        book = pe.get_book(file_name=filename)
        for sheet in book:
            # Skip this sheet if it doesn't
            # have the right column length
            # or its an SQL sheet.
            if (
                len(sheet.row[0]) != len(meter_schema) or
                is_sql_sheet(sheet)
            ):
                continue
            # Delete the first row if it is
            # empty or if it has column names
            if (
                is_meter_data(sheet) or
                all([c == '' for c in sheet.row[0]])
            ):
                sheet.delete_rows([0])
            print(f'file: {filename}, length: {len(sheet)}')
            # append the sheet to the csv file
            with open(csv_file, 'a') as f:
                data = sheet.get_csv()
                f.write(data)
                if data[-1] != '\n':
                    f.write('\n')


def main():
    filename = path_join(BASE_DIR, 'Fares NonRevVehicles/all_meterdata.csv')
    if not path_exists(filename):
        with open(filename, 'w'): pass
        combine_all_meterdata(filename)

    book_filename = path_join(BASE_DIR, 'Monthly Project Update - MPU/MPU_July 20_20200820.xlsm')
    book = pe.get_book(file_name=book_filename)
    extract_mpu(book)

if __name__ == '__main__':
    main()
