import pandas as pd
import re
import csv


def main():
    preprocess_csv(False)
    df = pd.read_csv('payroll.csv')
    pd.options.display.float_format = '{:.2f}'.format
    pd.set_option('display.max_rows', None)

    add_normalized_pay(df)

    with open('out.txt', 'w') as out_file:
        budgets_by_year(out_file, df)
        budgets_by_dept(out_file, df)
        budgets_by_borough(out_file, df)

def preprocess_csv(preprocess):
    if not preprocess:
        return

    r = re.compile(r"(.+) #.*")

    with open('payroll_original.csv', 'r', encoding='utf8', newline='') as original_csv:
        with open('payroll.csv', 'w', encoding='utf8', newline='') as new_csv:
            writer = csv.writer(new_csv)
            header = next(csv.reader(original_csv))
            writer.writerow(header)
            header_idx = dict(zip(header, range(len(header))))
            agency_idx = header_idx['Agency Name']
            borough_idx = header_idx['Work Location Borough']

            for row in csv.reader(original_csv):
                m = re.match(r, row[agency_idx])

                if m:
                    row[agency_idx] = m.group(1)

                row[borough_idx] = row[borough_idx].upper()
                writer.writerow(row)

def add_normalized_pay(df):
    df['Calculated Hourly Rate'] = df['Regular Gross Paid'] / df['Regular Hours']

def budgets_by_year(f, df):
    f.write(f"{df.groupby(['Fiscal Year'])['Regular Gross Paid'].sum()}\n\n")

def budgets_by_dept(f, df):
    f.write(f"{df.groupby(['Agency Name'])['Regular Gross Paid'].sum()}\n\n")

def budgets_by_borough(f, df):
    f.write(f"{df.groupby(['Work Location Borough'])['Regular Gross Paid'].sum()}\n\n")

def normalized_pay(f, df):
    f.write(f"{df.groupby(['Title Description'])['Calculated Hourly Rate'].sum()}\n\n")


if __name__ == '__main__':
    main()
