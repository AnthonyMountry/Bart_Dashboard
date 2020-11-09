from os.path import (
    join as path_join,
    exists as path_exists,
)
import re
import csv
from datetime import datetime, MINYEAR
import multiprocessing as mp

import pyexcel as pe
from pyexcel.sheet import Sheet
from pyexcel.book import Book
from pyexcel.internal.generators import BookStream

BASE_DIR = 'UC Merced 2020 SE Project'
if path_exists('./db'):
    BASE_DIR = path_join('db', BASE_DIR)

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
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sheet.get_csv())

def is_sql_sheet(s: Sheet) -> bool:
    return s.name.lower() == 'sql' or len(s) <= 2

def is_meter_data(sheet: Sheet) -> bool:
    return (
        sheet.row[0] == meter_schema_upper or
        sheet.row[0] == meter_schema
    )

def max_column_len(sheet: Sheet, name: str) -> int:
    mx = 0
    col = sheet.named_column_at(name)
    if isinstance(col[5], (int, float)):
        raise TypeError('cannot get max length of a number colunm')
    for r in col:
        if len(r) > mx:
            mx = len(r)
    return mx


# ----- Extract The Weird MPU Data -----

def extract_base(book):
    base: Sheet = book.sheet_by_index(0)
    base.delete_columns([0, 1])
    base.delete_rows(list(range(24)))
    write_sheet(base, path_join(BASE_DIR, 'Monthly Project Update - MPU/exceptions_template.csv'))
    return base


def extract_mpu(book, csv_file: str):
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
    for i, c in enumerate(mpu.column['rr_funded']):
        mpu[i, 'rr_funded'] = 1 if c == 'Y' else 0
    for name in ['district_location', 'accomplishments']:
        for i, c in enumerate(mpu.column[name]):
            if c == '--' or c == '-':
                mpu[i, name] = ''
    for i, c in enumerate(mpu.column['remaining_budget']):
        if c == 'Full Scope':
            raise ValueError('expected a number but got a string')
    # mpu.delete_rows([0]) # delete the column names
    write_sheet(mpu, csv_file)
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


def parse_date(d):
    return datetime.strptime(d, '%d-%b-%y') if d else MINYEAR


def _process_sheet(sheet: Sheet) -> Sheet:
    # Skip this sheet if it doesn't
    # have the right column length
    # or its an SQL sheet.
    if (
        len(sheet.row[0]) != len(meter_schema) or
        is_sql_sheet(sheet)
    ):
        return None
    # Delete the first row if it is
    # empty or if it has column names
    if (
        is_meter_data(sheet) or
        all([c == '' for c in sheet.row[0]])
    ):
        sheet.delete_rows([0])
    print(f'sheet: {sheet.name}, length: {len(sheet)}')
    # append the sheet to the csv file
    for i in range(sheet.number_of_rows()):
        sheet[i, 8] = parse_date(sheet[i, 8])
        sheet[i, 9] = parse_date(sheet[i, 9])
    return sheet


# This class reads a bunch of meterdata files and
# combines then into one csv file
#
# This solution takes A LOT of memory
# https://stackoverflow.com/questions/13446445/python-multiprocessing-safely-writing-to-a-file
class MeterDataWriter:

    def __init__(self, filename: str, datafiles: list):
        self.filename = filename
        self.datafiles = datafiles
        with open(self.filename, 'w'): pass

    @staticmethod
    def _worker(bookname, q):
        filename = path_join(BASE_DIR, bookname)
        book = pe.get_book(file_name=filename)
        for sheet in book:
            s = _process_sheet(sheet)
            if s is None:
                continue
            else:
                q.put(s.get_csv())

    def _listener(self, q):
        with open(self.filename, 'w') as f:
            while True:
                data = q.get()
                if data == 'done':
                    print('got done signal')
                    break
                print('writing', len(data), 'bytes')
                f.write(data)
                f.flush()

    def run(self):
        manager = mp.Manager()
        q = manager.Queue()
        pool = mp.Pool(
            # we want to reuse processes because memory
            # is not infinate
            processes=int(mp.cpu_count() / 2),
            # even if we still only use one process
            # we still want to apply it to all files
            maxtasksperchild=len(self.datafiles)
        )
        jobs = []
        watcher = pool.apply_async(self._listener, (q,))
        for f in self.datafiles:
            job = pool.apply_async(self._worker, (f, q))
            jobs.append(job)
        for job in jobs:
            job.get()
        q.put('done') # listener will return
        pool.close()
        pool.join()


def combine_all_meterdata(csv_file: str):
    if not path_exists(csv_file):
        raise Exception('csv file does not exist')
    for f in METER_READING_FILES:
        filename = path_join(BASE_DIR, f)
        book = pe.get_book(file_name=filename)
        for sheet in book:
            s = _process_sheet(sheet)
            if s is None:
                continue
            else:
                with open(csv_file, 'a') as f:
                    data = s.get_csv()
                    f.write(data)
                    if data[-1] != '\n':
                        f.write('\n')

def extract_asset_aliases(csv_file: str):
    filename = path_join(BASE_DIR, 'TC Switch Machines/Switch Machine WO By Quarter Analysis 2020May.xlsx')
    bk: Book = pe.get_book(file_name=filename)
    sheet: Sheet = bk.sheet_by_name('All Asset Summary')
    n = sheet.number_of_columns()
    sheet.delete_columns(list(range(4, n)))
    sheet.name_columns_by_row(0)
    mx = 0
    for a in sheet.column[1]:
        if len(a) > mx:
            mx = len(a)
    print('max alias len:', mx)
    print('max alias len:', max_column_len(sheet, 'Alias'))
    print('max status len:', max_column_len(sheet, 'Status'))
    print('max location len:', max_column_len(sheet, 'Location'))
    if sheet.row[-1][0] == 'Total':
        sheet.delete_rows([-1])
    with open(csv_file, 'w') as f:
        f.write(sheet.get_csv())


def meter_reading_lengths():
    filename = path_join(BASE_DIR, 'Fares NonRevVehicles/all_meterdata.csv')
    max_dept = max_desc = max_status = max_metername = max_source = 0
    with open(filename, 'r') as f:
        r = csv.reader(f)
        for row in r:
            max_dept = max(len(row[0]), max_dept)
            max_desc = max(len(row[2]), max_desc)
            max_status = max(len(row[3]), max_status)
            max_metername = max(len(row[4]), max_metername)
            max_source = max(len(row[5]), max_source)
    print('max bartdept:', max_dept)
    print('max desc:', max_desc)
    print('max status:', max_status)
    print('max metername:', max_metername)
    print('max readingsource:', max_source)


def extract_work_orders(csv_file: str):
    pass


def main():
    # asset_alias_csv = path_join(BASE_DIR, 'tmp_asset_aliases.csv')
    # extract_asset_aliases(asset_alias_csv)

    # filename = path_join(BASE_DIR, 'Fares NonRevVehicles/all_meterdata.csv')
    # writer = MeterDataWriter(filename, METER_READING_FILES)
    # writer.run()

    book_filename = path_join(BASE_DIR, 'Monthly Project Update - MPU/MPU_July 20_20200820.xlsm')
    book = pe.get_book(file_name=book_filename)
    # extract_mpu(book, 'Monthly Project Update - MPU/mpu.csv')
    extract_mpu(book, 'cleaned/mpu.csv')


if __name__ == '__main__':
    main()
