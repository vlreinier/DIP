import datetime
import pandas as pd
import numpy as np

format_str = '%Y-%m-%d'

def holidays():
    sinterklaas = [datetime.datetime.strptime("2019-12-05", format_str).date()]
    pasen = pd.date_range(datetime.datetime.strptime("2019-04-12", format_str), periods=2).date
    nieuwjaarsdag = [datetime.datetime.strptime("2019-01-01", format_str).date()]
    koningsdag = [datetime.datetime.strptime("2019-04-27", format_str).date()]
    pinksteren = pd.date_range(datetime.datetime.strptime("2019-05-31", format_str), periods=2).date
    bevrijdingsdag = [datetime.datetime.strptime("2019-05-5", format_str).date()]
    hemelvaartsdag = [datetime.datetime.strptime("2019-05-21", format_str).date()]
    goede_vrijdag = [datetime.datetime.strptime("2019-04-10", format_str).date()]
    return {1:sinterklaas,2:pasen,3:nieuwjaarsdag,4:koningsdag,5:pinksteren,6:bevrijdingsdag,7:hemelvaartsdag,8:goede_vrijdag}

def vacations():
    mei_vakantie = pd.date_range(datetime.datetime.strptime("2019-02-15", format_str), periods=9).date
    zomer_vakantie = pd.date_range(datetime.datetime.strptime("2019-07-04", format_str), periods=44).date
    herfst_vakantie = pd.date_range(datetime.datetime.strptime("2019-10-10", format_str), periods=9).date
    voorjaars_vakantie = pd.date_range(datetime.datetime.strptime("2019-02-15", format_str), periods=9).date
    kerst_vakantie = np.concatenate((pd.date_range(datetime.datetime.strptime("2019-12-22", format_str), periods=10).date, pd.date_range(datetime.datetime.strptime("2019-01-01", format_str), periods=6).date))
    return {1:mei_vakantie,2:zomer_vakantie,3:herfst_vakantie,4:voorjaars_vakantie,5:kerst_vakantie}
    
