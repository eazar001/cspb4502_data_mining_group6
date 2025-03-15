import pandas as pd
import re
import csv


def preprocess_csv(enabled, input_file, output_file):
    if not enabled:
        return

    hash_tag_pattern = re.compile(r"(.+) #.*")

    with open(input_file, 'r', encoding='utf8', newline='') as original_csv:
        with open(output_file, 'w', encoding='utf8', newline='') as new_csv:
            writer = csv.writer(new_csv)
            header = next(csv.reader(original_csv))
            writer.writerow(header)
            header_idx = dict(zip(header, range(len(header))))

            writer.writerows(map(lambda x: preprocess_csv_row(hash_tag_pattern, x, header_idx), csv.reader(original_csv)))

def preprocess_csv_row(hash_tag_pattern, row, header_idx):
    agency_idx = header_idx['Agency Name']
    borough_idx = header_idx['Work Location Borough']
    hash_tag_match = re.match(hash_tag_pattern, row[agency_idx])

    if hash_tag_match:
        row[agency_idx] = hash_tag_match.group(1)

    row[borough_idx] = row[borough_idx].upper()

    return row


def add_normalized_pay(f, df):
    df['Calculated Hourly Rate'] = df['Regular Gross Paid'] / df['Regular Hours']
    f.write(f"{df['Calculated Hourly Rate']}")

def budgets_by_year(f, df):
    f.write(f"{df.groupby(['Fiscal Year'])['Regular Gross Paid'].sum()}\n\n")

def budgets_by_dept(f, df):
    f.write(f"{df.groupby(['Agency Name'])['Regular Gross Paid'].sum()}\n\n")

def budgets_by_borough(f, df):
    f.write(f"{df.groupby(['Work Location Borough'])['Regular Gross Paid'].sum()}\n\n")

def normalized_pay(f, df):
    f.write(f"{df.groupby(['Title Description'])['Calculated Hourly Rate'].sum()}\n\n")

def main():
    preprocess_csv(False, 'payroll_original.csv', 'payroll.csv')
    df = pd.read_csv('payroll.csv')
    pd.options.display.float_format = '{:.2f}'.format
    pd.set_option('display.max_rows', None)

    with open('out.txt', 'w') as out_file:
        budgets_by_year(out_file, df)
        budgets_by_dept(out_file, df)
        budgets_by_borough(out_file, df)
        add_normalized_pay(out_file, df)


if __name__ == '__main__':
    main()
