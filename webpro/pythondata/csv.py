import csv

fn = 'csvReport.csv'
with open(fn)  as csvFile:
    csvReader =csv.reader(csvFile)
    listReport =list(csvReader)
print(listReport)