import os
import camelot
import csv

list_of_pdf_files = os.listdir("pdf_files")


for pdf_file in list_of_pdf_files:
    tables = camelot.read_pdf(f'pdf_files/{pdf_file}', pages='all', flavor='stream')
    tables.export(f'csv_files/{pdf_file}.csv', f='csv', compress=False)

list_of_csv_files = os.listdir("csv_files")

for csv_file in list_of_csv_files:
    print(f'working on csv file: {csv_file}')
    table_start_text = 'DATE'
    file_end_text = 'continued'
    start_deposit_text = 'Deposits, credits'
    end_deposit_text = 'Total deposits, credits and interest'

    with open(f'csv_files/{csv_file}', 'r') as csvfile, open(f'final_csv_files/final-csv.csv', 'a+') as outFile:
        print('starting write of final csv file: final_csv_files/{csv_file}')
        datareader = csv.reader(csvfile)
        datawriter = csv.writer(outFile, delimiter=',')
        deposits = False
        for row in datareader:
            # Row is: ['Deposits, credits and interest', '+ 21,954.67', '', '', '', '']
            if start_deposit_text in row[0]:
                if '+' not in row[1]:
                    deposits = True
                    print("*************Deposits started, adding in different column*************")
                    print(f"Row is: {row}")

            if end_deposit_text in row[0]:
                print("*********Deposits Stopped, adding in normal column**********")
                deposits = False
                print(f"Row is: {row}")

            if '/' in row[0]:
                if len(row[0]) < 6:
                    if row[2] == '':
                        if deposits:
                            print(f'Adding row {row} to Deposit column')
                            csvrow = [row[0], row[1], '', row[5]]
                            datawriter.writerow(csvrow)
                        else:
                            print(f'Adding row {row} to Normal column')
                            csvrow = [row[0], row[1], row[5]]
                            datawriter.writerow(csvrow)
                    else:
                        if '.' not in row[2]:
                            continue
                        if deposits:
                            print(f'Adding row {row} to Deposit column')
                            csvrow = [row[0], row[1], '', row[2]]
                            datawriter.writerow(csvrow)
                        else:
                            print(f'Adding row {row} to Normal column')
                            csvrow = [row[0], row[1], row[2]]
                            datawriter.writerow(csvrow)
