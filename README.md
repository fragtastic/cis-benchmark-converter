# cis-benchmark-to-csv
Converts **dumped text** from CIS Benchmark PDFs into usable CSV & Excel files.

For expected numbers see the [reference results](reference_results.md) of the conversions.

## Requirements
- Python 3
- For Excel output install the `xlsxwriter` Python package

## Dumping Text
**Warning:** Adobe Acrobat DC on Windows will produce broken txt files. Use Adobe Acrobat DC on MacOS only.
```
In Adobe Acrobat DC:
- File -> Export To -> Text (Plain)
- Ensure export is set to Settings -> UTF-8
- Uncheck "View Result"
```

## Program Usage
```
usage: cis2csv.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] inputFilePath

positional arguments:
  inputFilePath         CIS text dump to parse.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
```

```
usage: cis2excel.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [--sheetName SHEETNAME]
                    inputFilePath

positional arguments:
  inputFilePath         CIS text dump to parse.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
  --sheetName SHEETNAME
                        Set the sheet name in Excel.
```
