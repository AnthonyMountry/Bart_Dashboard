import os.path
from os.path import join as path_join
import re
import sqlite3

import pyexcel as pe
from pyexcel.sheet import Sheet
from pyexcel.book import Book

BASE_DIR = 'bart_data/Monthly Project Update - MPU'

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
    write_sheet(base, 'exceptions_template.csv')
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
    write_sheet(mpu, 'mpu.csv')
    return mpu

def extract_criteria(book):
    sheet: Sheet = book.sheet_by_name('Selection Criteria')
    sheet.delete_rows(list(range(9)))
    write_sheet(sheet, 'criteria.csv')
    return sheet

def extract_expfunds(book):
    expfunds: Sheet = book.sheet_by_name('EXPFUNDS')
    expfunds.delete_rows([0, 1])
    write_sheet(expfunds, 'expfunds.csv')
    return expfunds

def extract_milestones(book):
    milestones = book.sheet_by_name('MILESTONES')
    milestones.delete_rows([0, 1])
    write_sheet(milestones, 'milestones.csv')
    return milestones

def populate_meter_readings(db, filename):
    book = pe.get_book(file_name=filename)
    remove_sql_sheet(book)
    for sheet in book:
        print(len(sheet))
        if len(sheet.row[0]) != len(meter_schema):
            continue
        if is_meter_data(sheet):
            sheet.delete_rows([0])

# run sqlite3 dashboard.db ".read init.sql"

def main():
    raise Exception("this script is not finished yet")
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
    # db = sqlite3.connect('./dashboard.db')
    for f in files:
        # populate_meter_readings(None, path_join('bart_data', f))
        bk = pe.get_book(file_name=path_join('bart_data', f))

    # populate_asset_readings(db, 'bart_data/Fares NonRevVehicles/')
    # book_filename = os.path.join(BASE_DIR, 'MPU_July 20_20200820.xlsm')
    # book = pe.get_book(file_name=book_filename)
    # extract_mpu(book)
    # extract_criteria(book)
    # extract_expfunds(book)
    # extract_base(book)
    # extract_milestones(book)


if __name__ == '__main__':
    main()