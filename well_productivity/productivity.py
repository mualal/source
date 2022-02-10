import xlwings as xw
import pandas as pd

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    data_range = sheet['A1:C25']
    df = data_range.options(pd.DataFrame, index=False, header=True).value
    print(df)
    sheet['E1'].value = df.describe()

if __name__ == "__main__":
    xw.Book('productivity.xlsm').set_mock_caller()
    main()
