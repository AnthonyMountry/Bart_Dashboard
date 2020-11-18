from os.path import (
    join as path_join,
    exists as path_exists,
)
import re
import csv
from datetime import datetime, MINYEAR
import multiprocessing as mp

import pyexcel as pe
from pyexcel.internal.sheets.matrix import transpose
from pyexcel.sheet import Sheet
from pyexcel.book import Book
from pyexcel.internal.generators import BookStream

from typing import Generator, List

BASE_DIR = 'UC Merced 2020 SE Project'
DB_DIR = './'
if path_exists('./db'):
    BASE_DIR = path_join('db', BASE_DIR)
    DB_DIR = './db'

CLEANED = path_join(DB_DIR, 'cleaned')

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

workorder_schema_mappings = {
    'WONUM': 'num',
    'REPORTDATE': 'report_date',
    'ALIAS': 'alias',
    'LOCATION': 'location',
    'WORKTYPE': 'work_type',
    'DESCRIPTION': 'description',
    'ASSET_TYPE': 'asset_type',
    'BARTDEPT': 'bartdept',
    'STATUS': 'status',
    'ACTSTART': 'start',
    'ACTFINISH': 'finish',
    'ACTUAL_LABOR_HOURS': 'labor_hours',
    'MATERIAL_COST': 'material_cost',
}

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
    "Monthly Burn Rate \n(average 3 months of actual costs May 20, Jun 20, July 20)": 'monthly_burn_rate',
    "End Date\n(from Milestones, or from MPL if no Milestone)": 'end_date',
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
    col = sheet.named_column_at(name)
    if all(map(lambda x: isinstance(x, (int, float)), col)):
        raise TypeError('cannot get max length of a number colunm')
    return max(map(len, col))


# ----- Extract The Weird MPU Data -----

def extract_base(book):
    base: Sheet = book.sheet_by_index(0)
    base.delete_columns([0, 1])
    base.delete_rows(list(range(24)))
    write_sheet(base, path_join(BASE_DIR, 'Monthly Project Update - MPU/exceptions_template.csv'))
    return base


def extract_mpu(book, csv_file: str):
    col_re = re.compile('Column([0-9]+)')
    mpu: Sheet = book.sheet_by_name('MPU')
    mpu.delete_rows(list(range(14))) # remove garbage at the top
    mpu.delete_columns([0])          # delete empty column
    mpu.name_columns_by_row(0)       # set column names
    # Find empty columns (named "Column3" or
    # "Column9", ect.) and remove them
    mpu.delete_columns([i for i,c in enumerate(mpu.colnames) if col_re.match(c)])
    # Delete the columns that we don't want
    desired_columns = set(mpu_schema_mappings.keys())
    names = set(mpu.colnames)
    for col in names.difference(desired_columns):
        mpu.delete_named_column_at(col)
    # Rename the columns based on the schema mapping
    mpu.colnames = [mpu_schema_mappings[n] for n in mpu.colnames]
    mpu.column['rr_funded'] = list(map(lambda c: 1 if c == 'Y' else 0,
                                   mpu.column['rr_funded']))
    for name in ['district_location', 'accomplishments']:
        for i, c in enumerate(mpu.column[name]):
            if c == '--' or c == '-':
                mpu[i, name] = ''
    if any(map(lambda c: c=='Full Scope', mpu.column['remaining_budget'])):
        raise ValueError('expected a number but got a string')
    mpu.colnames = []
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
    return datetime.strptime(d, '%d-%b-%y') if d else datetime(MINYEAR, 1, 1)


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
        book = pe.get_book(file_name=bookname)
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


def combine_all_meterdata(data_dir: str, csv_file: str):
    if not path_exists(csv_file):
        raise Exception('csv file does not exist')
    for f in METER_READING_FILES:
        filename = path_join(data_dir, f)
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


def extract_asset_aliases(data_dir: str, csv_file: str, silent=True):
    filename = path_join(data_dir, 'TC Switch Machines/Switch Machine WO By Quarter Analysis 2020May.xlsx')
    bk: Book = pe.get_book(file_name=filename)
    sheet: Sheet = bk.sheet_by_name('All Asset Summary')
    n = sheet.number_of_columns()
    sheet.delete_columns(list(range(4, n)))
    sheet.name_columns_by_row(0)
    if not silent:
        mx = max(map(len, sheet.column[1]))
        print('max alias len:', mx)
        print('max alias len:', max_column_len(sheet, 'Alias'))
        print('max status len:', max_column_len(sheet, 'Status'))
        print('max location len:', max_column_len(sheet, 'Location'))
    if sheet.row[-1][0] == 'Total':
        sheet.delete_rows([-1])
    with open(csv_file, 'w') as f:
        f.write(sheet.get_csv())


def meter_reading_lengths(filename):
    # filename = path_join(BASE_DIR, 'Fares NonRevVehicles/all_meterdata.csv')
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


def parse_quarterly_workorder(base_sheets: list):
    sheets = []
    for sheet in base_sheets:
        r = sheet.number_of_rows()
        n = sheet.number_of_columns() - 4
        if n / 4 != int(n/4):
            raise ValueError("bad number of columns")
        for i in range(4, n, 4):
            inner = sheet.column[0:4]
            inner.append([sheet.column[i][0]] * r)
            inner.extend(sheet.column[i:i+4])
            st = Sheet(inner, transpose_after=True)
            st.delete_rows([0, 1, 2])
            if st.row[-1][0].lower() == 'total':
                st.delete_rows([r-1])
            sheets.append(st)
    all_rows = [['asset', 'alias', 'status', 'location', 'quarter',
                'num_cms', 'cm_hours', 'pms', 'pm_hours']]
    for st in sheets:
        all_rows.extend(st.row)
    return Sheet(all_rows)

def extract_work_orders(filename):
    book: Book = pe.get_book(file_name=filename)
    sheet: Sheet = book.sheet_by_index(0)
    sheet.row[0] = [n.lower() for n in sheet.row[0]]
    sheet.name_columns_by_row(0)
    mapping = {k.lower(): v for k, v in workorder_schema_mappings.items()}
    names = sheet.colnames[:]
    newnames = []
    for name in names:
        if name not in mapping:
            sheet.delete_named_column_at(name)
        else:
            newnames.append(mapping[name])
    sheet.colnames = newnames

    repeats = []
    visited = {}
    for i, num in enumerate(sheet.named_column_at('num')):
        if num in visited:
            repeats.append(i)
            a, b = sheet.row[visited[num]], sheet.row[i]
            if a != b:
                print(a)
                print(b)
                raise Exception("should be the same data")
        else:
            visited[num] = i
    sheet.delete_rows(repeats)
    return Sheet([
        sheet.named_column_at('num'),
        list(map(parse_date, sheet.named_column_at('report_date'))),
        sheet.named_column_at('alias'),
        sheet.named_column_at('location'),
        sheet.named_column_at('work_type'),
        sheet.named_column_at('description'),
        sheet.named_column_at('asset_type'),
        sheet.named_column_at('bartdept'),
        sheet.named_column_at('status'),
        list(map(parse_date, sheet.named_column_at('start'))),
        list(map(parse_date, sheet.named_column_at('finish'))),
        sheet.named_column_at('labor_hours'),
        sheet.named_column_at('material_cost'),
    ], transpose_after=True)


def extract_throw_counts(files: List[str]):
    sheet_pat = re.compile('\d+-\d+(-\d+)?.Data')
    books: List[Book] = (pe.get_book(file_name=f) for f in files)
    sheets: Generator[Sheet] = (b.sheet_by_name(s) for b in books for s in b.sheet_names() if sheet_pat.match(s))
    visited = {}
    names = ['assetnum', 'alias', 'location', 'TOTAL COUNT SINCE 02042020', 'last pm date', 'next pm date', 'last cm date']
    for sh in sheets:
        sh.delete_rows([0, 1, 2])
        sh.name_columns_by_row(0)
        # print(sh.colnames[0:8])
        print(sh.colnames[8:14])
        # print(sh.name, sh.row[0][0:4])


def clean(base_dir, output_dir):
    filename = path_join(base_dir, "Power", "POWER WOs 9-22-2018 to 9-21-2020.xlsx")
    with open(path_join(output_dir, 'work_order.csv'), 'w') as f:
        f.write(extract_work_orders(filename).get_csv())

    files = [
        path_join(base_dir, 'TC Switch Machines', 'Switch Machine WO By Quarter Analysis 2020May.xlsx'),
        path_join(base_dir, 'TC Switch Machines', 'Switch Machine WO By Quarter 8-5-2020 v2.xlsx'),
    ]
    wo_books = [pe.get_book(file_name=f) for f in files]
    res = parse_quarterly_workorder(b.sheet_by_name("All Asset Summary") for b in wo_books)
    with open(path_join(output_dir, 'quarterly_wo_analysis.csv'), 'w') as f:
        f.write(res.get_csv())

    extract_asset_aliases(base_dir, path_join(output_dir, 'tmp_asset_aliases.csv'))

    book_filename = path_join(base_dir, 'Monthly Project Update - MPU/MPU_July 20_20200820.xlsm')
    book = pe.get_book(file_name=book_filename)
    extract_mpu(book, path_join(output_dir, 'mpu.csv'))

    # This takes a very long time.
    # # filename = path_join(BASE_DIR, 'Fares NonRevVehicles/all_meterdata.csv')
    # filename = path_join(CLEANED, 'all_meterdata.csv')
    # writer = MeterDataWriter(filename, METER_READING_FILES)
    # writer.run()

# Really just for testing
def main(base_dir, output_dir):
    # extract_throw_counts([
    #     path_join(BASE_DIR, 'TC Switch Machines', 'Switch Machine Count Report 8-24-20 r2.xlsx'),
    #     path_join(BASE_DIR, 'TC Switch Machines', 'Quarterly Throw Count Labor Evaluation - 2020-05-19.xlsx'),
    # ])
    files = [
        path_join(
            base_dir, 'TC Switch Machines',
            'Oct 9, 2019 thru Apr 8, 2020 PM, CM, PMREP data.xlsx',
        ),
    ]
    # extract_work_orders(filename)
    # with open(path_join(CLEANED, 'work_order.csv'), 'w') as f:
    #     f.write(extract_work_orders(filename).get_csv())
    # extract_work_orders(filename)
    filename = path_join(base_dir, "Power", "POWER WOs 9-22-2018 to 9-21-2020.xlsx")
    with open(path_join(output_dir, 'work_order.csv'), 'w') as f:
        f.write(extract_work_orders(filename).get_csv())
    # return

    files = [
        path_join(base_dir, 'TC Switch Machines', 'Switch Machine WO By Quarter Analysis 2020May.xlsx'),
        path_join(base_dir, 'TC Switch Machines', 'Switch Machine WO By Quarter 8-5-2020 v2.xlsx'),
    ]
    wo_books = [pe.get_book(file_name=f) for f in files]
    res = parse_quarterly_workorder(b.sheet_by_name("All Asset Summary") for b in wo_books)
    with open(path_join(output_dir, 'quarterly_wo_analysis.csv'), 'w') as f:
        f.write(res.get_csv())
    # extract_asset_aliases(path_join(CLEANED, 'tmp_asset_aliases.csv'))


if __name__ == '__main__':
    main(BASE_DIR, CLEANED)
