#!/usr/bin/env python3

import argparse
import re
import os
import logging


# TODO - Probably use contexts in the future
# TODO - Arguments for file type output


class CISConverter:
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', dest='logLevel', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level')
    parser.add_argument('inputFilePath', type=str, help='CIS text dump to parse.')

    def __init__(self):
        self.args = CISConverter.parser.parse_args()

        if self.args.logLevel:
            logging.basicConfig(level=getattr(logging, self.args.logLevel))

        self.metrics_total = 0
        self.metrics_good = 0

    searcher = re.compile(f'^(?P<cisnum>[\.\d]+)(?:\s+\((?P<level>[\w\d]+)\))?(?:\s+(?P<policy>.+))(?:\s\((?P<scored>Not\ Scored|Scored|Manual|Automated)\)\s?)$')

    garbage_list = [
        '| P a g e'
    ]
    
    appendix_list = [
        'Appendix: Summary Table',
        'Appendix: Recommendation Summary Table'
    ]

    modes = [
        'Profile Applicability',
        'Description',
        'Rationale',
        'Audit',
        'Remediation',
        'Impact',
        'Default Value',
        'References',
        'CIS Controls'
    ]

    @staticmethod
    def build_blank():
        return {
            'Benchmark': None,
            'CIS #': '',
            'Scored': '',
            'Type': '',
            'Policy': '',
            'Profile Applicability': [],
            'Description': '',
            'Rationale': '',
            'Audit': '',
            'Remediation': '',
            'Impact': '',
            'Default Value': '',
            'References': '',
            'CIS Controls': ''
        }

    def write_row(self, row):
        logging.debug(row)

    def parse_text(self):
        with open(self.args.inputFilePath, mode='rt', encoding='utf8') as inFile:
            logging.info(f'Parsing {self.args.inputFilePath}')

            row = None
            cur_mode = None
            force_write = False

            self.write_header()

            for line in inFile:
                # line = line.replace('\n', '')
                logging.debug(f'Line: "{line}"')
                self.metrics_total += 1
                # line = line.strip()
                # Skip garbage lines here
                if any(ele in line for ele in CISConverter.garbage_list):
                    continue

                match = CISConverter.searcher.match(line)
                if match or force_write:
                    # Check if row is created, skips initial blanks
                    if row:
                        if row['Type'] == None:
                            if len(row['Profile Applicability']) == 1:
                                row['Type'] = row['Profile Applicability'][0]
                            else:
                                row['Type'] = 'See Profile Applicability'
                        for key in row.keys():
                            if isinstance(row[key], list):
                                row[key] = '\n'.join(row[key])
                        self.write_row(row)

                        self.metrics_good += 1
                        if force_write:
                            break
                    row = self.build_blank()
                    row['Benchmark'] = os.path.basename(self.args.inputFilePath)[:-4]
                    row['CIS #'] = match.group('cisnum')
                    row['Type'] = match.group('level')
                    row['Policy'] = match.group('policy')
                    row['Scored'] = match.group('scored')
                    cur_mode = None
                    continue

                else:
                    mode_set = False
                    for mode in CISConverter.modes:
                        if line.startswith(f'{mode}:'):
                            cur_mode = mode
                            mode_set = True

                    # Only do something on the line(s) after a mode set
                    if not mode_set and cur_mode:
                        # # Perform sanitization here.
                        if cur_mode == 'Profile Applicability':
                            line = line.replace('\uf0b7 ', '', 1)
                        line = line.replace(' ', '', 1)
                        # check if we have transitioned to Appendix
                        if any(ele in line for ele in CISConverter.appendix_list):
                            cur_mode = None
                            force_write = True
                            continue

                        if isinstance(row[cur_mode], str):
                            row[cur_mode] += line
                        elif isinstance(row[cur_mode], list):
                            row[cur_mode].append(line.strip())
                        else:
                            logging.critical('ERROR: Bad type. This should never happen.')
                            exit(-1)

        logging.info(f'Total lines: {self.metrics_total}')
        logging.info(f'Written Rows: {self.metrics_good}')


class CISConverterCSV(CISConverter):
    pass

    def __init__(self):
        # TODO - arg for csv quoting
        # TODO - arg for csv encoding
        super(__class__, self).__init__()
        import csv
        import codecs

        self.outputFilePath = f'{self.args.inputFilePath[:-4]}.csv'

        with open(self.outputFilePath, 'wt', encoding='utf-8') as outFile:
            logging.info(f'Writing to {self.outputFilePath}')
            outFile.write(str(codecs.BOM_UTF8))
            self.cw = csv.DictWriter(outFile, fieldnames=list(self.build_blank()), quoting=csv.QUOTE_ALL)
            self.parse_text()

    def write_header(self):
        self.cw.writeheader()

    def write_row(self, row):
        self.cw.writerow(row)


class CISConverterExcel(CISConverter):

    def __init__(self):
        CISConverter.parser.add_argument('--sheetName', dest='sheetName', type=str, required=False, help='Set the sheet name in Excel.')

        super(__class__, self).__init__()
        import xlsxwriter

        self.outputFilePath = f'{self.args.inputFilePath[:-4]}.xlsx'

        if not self.args.sheetName:
            self.args.sheetName = os.path.basename(self.args.inputFilePath)[:-4]
        self.args.sheetName = self.args.sheetName[:31]

        logging.info(f'Writing to "{self.outputFilePath}"')
        self.xrow = 0
        self.xcol = 0

        with xlsxwriter.Workbook(self.outputFilePath) as workbook:
            self.worksheet = workbook.add_worksheet(self.args.sheetName)
            self.format_text = workbook.add_format({'num_format': '@'})
            self.parse_text()

    def write_header(self):
        # Cheat and zip together the keys since write row expects a dictionary
        self.write_row(dict(zip(self.build_blank().keys(), self.build_blank().keys())))

    def write_row(self, row):
        for key, value in row.items():
            self.worksheet.write_string(self.xrow, self.xcol, value.strip(), self.format_text)
            self.xcol += 1
        self.xcol = 0
        self.xrow += 1
