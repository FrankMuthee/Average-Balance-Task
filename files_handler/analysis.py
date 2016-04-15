# -*- coding: utf-8 -*-                                                                                                                            
#                                                                                                                                                  
# author: frank muthee | mutheefrank@gmail.com                                                                                                     
# 
import datetime
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
from datetime import datetime
from plotly.tools import FigureFactory as FF

from methods import get_clients_df, get_date, birthdays
from methods import FILE_DIR



"""
Few analytics rendered with plotply
"""

def get_sexes_list():
    """
    return a list of gender count
    from clients file
    """
    df = pd.read_csv(FILE_DIR+'clients.csv',usecols=['gender'])    
    return  dict(df['gender'].value_counts())

def get_dateofbirth_df():
    """
    returns a list the dobs from the 
    clients file
    """
    dob_dict = dict(pd.read_csv(FILE_DIR+'clients.csv', usecols=['dob']))
    return dob_dict

def get_piegraph_gender():
    """
    Rendering sex distribution pie chart from 
    the clients.csv file using plotly
    """
    gender = get_sexes_list()
    fig = {
        'data': [{'labels': ['Male', 'Female', 'Not Specified'],
                  'values': [gender['M'],gender['F'],gender['N']],
                  'type': 'pie'}],
        'layout': {'title': 'Gender Distribution From Clients File'}
       }

    url = py.plot(fig, filename='Gender Pie Chart', auto_open=False)
    return tls.get_embed(url)


def get_bargraph_gender():
    """
    Rendering sex distribution bar graph from 
    the clients.csv file using plotly
    """
    values = get_sexes_list()
    data = [
        go.Bar(
            x=['Male','Female','Not Specified'],
            y=[values['M'],values['F'],values['N']]
        )
    ]
    plot_url = py.plot(data, filename='Gender Bar Char',auto_open=False)
    
    return tls.get_embed(plot_url)

    
def get_clients_table():
    """
    return all columns of 
    client table on plotply
    """
    df = get_clients_df()
    df_sample = df[50:60]

    table = FF.create_table(df_sample)
    plot_url = py.iplot(table, filename ='Clients Details')
    
    return get_clients_table()

