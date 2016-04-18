# -*- coding: utf-8 -*-
# 
# author: frank muthee | mutheefrank@gmail.com
#

import datetime
import numpy as np
import pandas as pd
from pprint import pprint
from dateutil.relativedelta import relativedelta
from django.conf import settings

"""
dir where files are loaded from
"""
FILE_DIR = settings.MEDIA_ROOT
FILE_URL = settings.MEDIA_URL



def get_filenames():
    """
    Return filenames for the files that need
    to be processed
    """
    files_list = ['accts.csv','tx.csv','bal.csv','clients.csv']
    return files_list

def get_balances_df():
    """
    Read balances data into working df
    """
    return pd.read_csv(FILE_DIR+'bal.csv')


def get_accounts_df():
    """
    Read accounts data into working df
    """
    return pd.read_csv(FILE_DIR+"accts.csv")


def get_clients_df():
    """
    Read clients data into working df
    """
    return pd.read_csv(FILE_DIR+"clients.csv")


def get_transactions_df():
    """
    Read transactions data into working df
    """
    return pd.read_csv(FILE_DIR+"tx.csv")


def get_date(date):
    """
    Python date from input format
    """
    return datetime.datetime.strptime("{}".format(date), "%Y%m%d").date()


def get_opening_balances(accounts_df):
    """
    Create initial transaction for each account
    """
    default_date = (datetime.datetime.now()-relativedelta(years=50)).date()

    accounts = {}
    for index, row in accounts_df.iterrows():
        str_date = row["opening_date"]
        try:
            str_date = str(int(str_date))
            date = get_date(str_date)
        except ValueError:
            date = default_date

        acc_id = row["acct_id"]
        key = "{},{},{}".format(acc_id, date.year, date.month)
        
        tx_row = (date, row["open_bal"], "opening_balance", row["open_bal"])
        
        accounts[key] = [tx_row]

    return accounts


def create_summary_df(opening_balances, transactions_df):
    """
    Dataframe of the form
    acc_id, YY_MM, [(date, amount, type, balance)]
    """
    result = {}
    for index, row in transactions_df.iterrows():
        date = get_date(row["tx_date"])
        acc_id = row["acct_id"]
        key = "{},{}_{}".format(acc_id, date.year, date.month)
        if not key in result:
            try:
                result[key] = [opening_balances[acc_id]]
            except KeyError:
                """
                No opening balance
                """
                result[key] = []
        try:
            previous_transaction = result[key][len(result[key])-1]
        except IndexError:
            """
            No previous transaction
            """
            previous_transaction = (0,0,0,0)
        tx_row = (date, row["amount"], row["type"], row["amount"]+previous_transaction[1])
        result[key].append(tx_row)
    
    return result


def get_average_balances(summary_df):
    """
    Return list as required by assignment
    acc_id, yyuumm, avg_balance
    """
    avg_balances = []
    for key in summary_df.keys():
        summary = {
            "acct_id": key.split(",")[0],
            "yyyymm": key.split(",")[1],
            "avg_balance": np.mean([x[3] for x in summary_df.get(key)])
        }
        avg_balances.append(summary)

    return sorted(avg_balances, key=lambda x: x["yyyymm"])


def overall_analysis():
    """
    Process everything, return list as required by assignment
    """
    transactions_df = get_transactions_df()

    accounts_df = get_accounts_df()

    opening_balances = get_opening_balances(accounts_df)  
  
    summary_df = create_summary_df(opening_balances, transactions_df)

    return get_average_balances(summary_df)


def birthdays():
    """                                                                                                                                             
    Processes a dict of the count 
    of cllents born for each 
    respective month
    """
    clients_df = get_clients_df()

    result = {}
    for index, row in clients_df.iterrows():
        try:
            date = get_date(str(int(row["dob"])))
        except ValueError, ex:
            """                                                                                                                                                 Date is not present                                                                                                                    
            """
            pass
        key = "{}".format( date.month)
        if not key in result:
            result[key] = 1
        else:
            result[key] += 1

    return result


"""
call the function that processes average 
balances and assign it as a parameter
"""

param = overall_analysis()

def process_csv(param):
    """
    export processed output to csv
    """
    f_columns = ['acct_id','yyyymm','avg_balance']

    df = pd.DataFrame(param, columns = f_columns)

    file_name = FILE_DIR+'processed_output.csv'

    df.to_csv(file_name,index=False, columns = f_columns, sep='\t', encoding='utf-8')
    
    return FILE_URL+'processed_output.csv'

def process_excel(param):
    """
    export processed output to excel
    """
    f_columns = ['acct_id','yyyymm','avg_balance']

    df = pd.DataFrame(param, columns = f_columns)

    writer = pd.ExcelWriter(FILE_DIR+'processed_output.xlsx')

    df.to_excel(writer, 'Average Balances')

    writer.save()

    return FILE_URL+'processed_output.xlsx'

def csv_download():
    """
    call function that returns csv download url
    """
    return process_csv(param)

def excel_download():
    """
    call function that returns excel download url
    """
    return process_excel(param)



