from os.path import join as path_join
import re
import sqlite3
from sqlite3 import Connection

import pyexcel as pe
from pyexcel.sheet import Sheet
from pyexcel.book import Book

BASE_DIR = 'bart_data'

csvfiles = [
    'exceptions_template.csv',
    'mpu.csv',
    'criteria.csv',
    'expfunds.csv',
    'milestones.csv',
]

meter_schema_upper = [
    'BARTDEPT',
    'ASSETNUM',
    'DESCRIPTION',
    'STATUS',
    'METERNAME',
    'READINGSOURCE',
    'READING',
    'DELTA',
    'READINGDATE',
    'ENTERDATE',
]

meter_schema = [s.lower() for s in meter_schema_upper]

work_order_schema = [
    'wonum', 'description', 'detail_description', 'alias',
    'location', 'loc_desc', 'worktype', 'asset_type',
    'bartdept', 'status', 'reportdate', 'actstart',
    'actfinish', 'actual_labor_hours', 'material_cost',
    'problem_code_desc', 'reason_to_repair_desc', 'component_desc',
    'part_failure_desc', 'work_accomp_desc', 'wl_date',
    'wl_summary', 'wl_summary_detail',
]

mpu_schema = [
    'id', 'name', 'short_name', 'criteria_ranking', 'location',
    'sub_location', 'district_location', 'bart_performing_design',
    'bart_performing_construction', 'project_plan', 'asset_risk_register_id',
    'budget_amount', 'expended_amount', 'funding_level', 'end_date', 'monthly_burn_rate',
]

# ----- Utilities ------

def write_sheet(sheet: Sheet, filename: str):
    with open(path_join(BASE_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(sheet.get_csv())

def remove_sql_sheet(b: Book):
    for name in b.sheet_names():
        sheet = b.sheet_by_name(name)
        if name.lower() == 'sql' or len(sheet) <= 2:
            b.remove_sheet(name)

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
    mpu.delete_rows(list(range(14)))
    mpu.delete_columns([0])
    bad_cols = []
    for i, col in enumerate(mpu.column):
        if column_re.match(col[0]) is not None:
            bad_cols.append(i)
    mpu.delete_columns(bad_cols)
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

def populate_meter_readings(db: Connection, filename):
    book: Book = pe.get_book(file_name=filename)
    remove_sql_sheet(book)
    query = 'INSERT INTO meter_reading VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    for sheet in book:
        if len(sheet.row[0]) != len(meter_schema):
            continue
        if is_meter_data(sheet) or all([c == '' for c in sheet.row[0]]):
            sheet.delete_rows([0])
        for row in sheet:
            db.execute(query, tuple(row))

def combine_all_meterdata():
    files = [
        "Fares NonRevVehicles/NRVE, AFC Meter Data 1.xlsx",
        "Fares NonRevVehicles/NRVE, AFC Meter Data 2.xlsx",
        "Fares NonRevVehicles/NRVE, AFC Meter Data 3.xlsx",
        "Fares NonRevVehicles/NRVE, AFC Meter Data 4.xlsx",
        "Fares NonRevVehicles/NRVE, AFC Meter Data 5.xlsx",
        "Fares NonRevVehicles/NRVE, AFC Meter Data 6.xlsx",
        "Fares NonRevVehicles/NRVE, AFC Meter Data 7.xlsx",
        "Power/POWER Meter Data (all).xlsx",
    ]
    merged = None
    for f in files:
        filename = path_join('bart_data', f)
        book: Book = pe.get_book(file_name=filename)
        remove_sql_sheet(book)
        for sheet in book:
            print(filename, len(sheet))
            if len(sheet.row[0]) != len(meter_schema):
                continue
            if is_meter_data(sheet) or all([c == '' for c in sheet.row[0]]):
                sheet.delete_rows([0])
            if merged is None:
                merged = sheet
            else:
                merged += sheet
    return merged

throw_count_sheet_re = re.compile('[0-9]{1,2}-[0-9]{1,2} Data')
throw_count_files = [
    'TC Switch Machines/Switch Machine Count Report 8-24-20 r2.xlsx',
    'TC Switch Machines/Switch Machine Count Report 9-8-20.xlsx',
    'TC Switch Machines/Quarterly Throw Count Labor Evaluation - 2020-05-19.xlsx',
]

switch_machine_workorder_files = [
    'TC Switch Machines/Switch Machine WO By Quarter 8-5-2020 v2.xlsx'
]


def main():
    # run sqlite3 dashboard.db ".read init.sql"

    # db = sqlite3.connect('./dashboard.db')
    # db.commit()
    # db.close()

    book_filename = path_join(BASE_DIR, 'MPU_July 20_20200820.xlsm')
    book = pe.get_book(file_name=book_filename)
    extract_mpu(book)
    extract_criteria(book)
    extract_expfunds(book)
    extract_base(book)
    extract_milestones(book)

if __name__ == '__main__':
    main()
