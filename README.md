# cis-benchmark-to-csv
Converts dumped text from CIS Benchmark PDFs into usable CSV files.

## Requirements
- Python 3

## Program Usage
```
usage: cisConv.py [-h] inputFile

positional arguments:
  inputFile       CIS text dump to parse.

optional arguments:
  -h, --help  show this help message and exit
```

## Output
Below are some sample outputs of the script.

```
Parsing CIS Apple macOS 10.13 Benchmark v1.0.0.txt
Writing to CIS Apple macOS 10.13 Benchmark v1.0.0.txt.csv
Total lines: 2424
Written Rows: 111

Parsing CIS Microsoft Windows 10 Enterprise (Release 1809) Benchmark v1.6.0.txt
Writing to CIS Microsoft Windows 10 Enterprise (Release 1809) Benchmark v1.6.0.txt.csv
Total lines: 15367
Written Rows: 507

Parsing CIS Microsoft Windows Server 2019 RTM (Release 1809) Benchmark v1.0.0.txt
Writing to CIS Microsoft Windows Server 2019 RTM (Release 1809) Benchmark v1.0.0.txt.csv
Total lines: 12190
Written Rows: 382

Parsing CIS Microsoft Windows Server 2016 RTM (Release 1607) Benchmark v1.1.0.txt
Writing to CIS Microsoft Windows Server 2016 RTM (Release 1607) Benchmark v1.1.0.txt.csv
Total lines: 11704
Written Rows: 371

Parsing CIS Red Hat Enterprise Linux 7 Benchmark v2.2.0.txt
Writing to CIS Red Hat Enterprise Linux 7 Benchmark v2.2.0.txt.csv
Total lines: 4361
Written Rows: 225

Parsing CIS Red Hat Enterprise Linux 6 Benchmark v2.1.0.txt
Writing to CIS Red Hat Enterprise Linux 6 Benchmark v2.1.0.txt.csv
Total lines: 4339
Written Rows: 225

Parsing CIS Apple iOS 12 Benchmark v1.0.0.txt
Writing to CIS Apple iOS 12 Benchmark v1.0.0.txt.csv
Total lines: 2254
Written Rows: 67

Parsing CIS Google Android Benchmark v1.2.0.txt
Writing to CIS Google Android Benchmark v1.2.0.txt.csv
Total lines: 1644
Written Rows: 43
```
