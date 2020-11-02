#!/usr/bin/env python3

import argparse
import xlsxwriter
import re
import pprint
import code
import codecs
import os

# https://www.debuggex.com/
# So far this works on every file tested.
searcher = re.compile(r'^((?P<cisnum>(\d+\.)+\d+)\s)(\((?P<level>.+?)\)\s)?((?P<policy>.+))(\s\((?P<scored>Scored|Not\ Scored|Automated|Manual)\))$')

garbage_list = [
    '| P a g e'
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

xrow = 0
xcol = 0

def buildBlank():
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

def write_row(worksheet, format_text, values):
    global xcol, xrow
    for val in values:
        worksheet.write_string(xrow, xcol, val, format_text)
        xcol += 1
    xcol = 0
    xrow += 1


def parseText(inFileName):
    with open(inFileName, 'rt') as inFile:
        print(f'Parsing {inFileName}')
        with xlsxwriter.Workbook(f'{inFileName[:-4]}.xlsx') as workbook:
            worksheet = workbook.add_worksheet(os.path.basename(inFileName)[:31])
            format_text = workbook.add_format({'num_format': '@'})

            metrics_total = 0
            metrics_good = 0

            row = None
            cur_mode = None
            force_write = False

            write_row(worksheet, format_text, list(buildBlank().keys()))

            for line in inFile:
                line = line.replace('\n', '')
                metrics_total += 1
                # line = line.strip()
                # Skip garbage lines here
                if any(ele in line for ele in garbage_list):
                    continue

                match = searcher.match(line)
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
                        write_row(worksheet, format_text, list(row.values()))
                        # pprint.pprint(row)
                        metrics_good += 1
                        if force_write:
                            break
                    row = buildBlank()
                    # code.interact(local=locals())
                    row['Benchmark'] = inFileName[:-4]
                    row['CIS #'] = match.group('cisnum')
                    row['Type'] = match.group('level')
                    row['Policy'] = match.group('policy')
                    row['Scored'] = match.group('scored')
                    cur_mode = None
                    continue

                else:
                    mode_set = False
                    for mode in modes:
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
                        if line.startswith('Appendix: Summary Table'):
                            cur_mode = None
                            force_write = True
                            continue

                        if isinstance(row[cur_mode], str):
                            row[cur_mode] += line
                        elif isinstance(row[cur_mode], list):
                            row[cur_mode].append(line.strip())
                        else:
                            print('ERROR: Bad type. This should never happen.')
                            exit(-1)


    print(f'Total lines: {metrics_total}')
    print(f'Written Rows: {metrics_good}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile', type=str, help='CIS text dump to parse.')
    args = parser.parse_args()
    parseText(args.inputFile)
