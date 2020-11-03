#!/usr/bin/env python3

import argparse
import csv
import re
import pprint
import code
import codecs

searcher = re.compile(r'^((?P<cisnum>(\d+\.)+\d+)\s)(\((?P<level>.+?)\)\s)?((?P<policy>.+))(\s\((?P<scored>Scored|Not\ Scored)\))$')

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


def parse_text(inFileName):
    with open(inFileName, 'rt') as inFile:
        print(f'Parsing {inFileName}')
        outFileName = f'{inFileName}.csv'
        with open(outFileName, 'wt', encoding='utf-8') as outFile:
            print(f'Writing to {outFileName}')
            outFile.write(str(codecs.BOM_UTF8))
            cw = csv.DictWriter(outFile, fieldnames=list(build_blank().keys()), quoting=csv.QUOTE_ALL)
            cw.writeheader()
            metrics_total = 0
            metrics_good = 0

            row = None
            cur_mode = None
            force_write = False

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
                        cw.writerow(row)
                        # pprint.pprint(row)
                        metrics_good += 1
                        if force_write:
                            break
                    row = build_blank()
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
    parse_text(args.inputFile)
