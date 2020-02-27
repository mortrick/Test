#!/usr/bin/env python3

import datetime as dt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import mysqlactions as mysql
from logs import dynamic_log as dl
from keys import conf


def jsonfname ():
    now = dt.datetime.now()
    dtstring = now.strftime("%d_%m_%Y_%H_%M_%S")
    filname = "notflattendata" + dtstring +".json"
    fullpath = "./unflatten_data/" + filname
    return fullpath

def returnurl():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    return url

def prms():
    parameters = {
      'start': '1',
      'limit': '130',
      'convert': 'USD,BTC'
    }
    return parameters


def callcms( run_id, debugmode, savejson=0):
    session = Session()
    session.headers.update(conf.headers())
    try:
       response = session.get(returnurl(), params=prms())
       data = json.loads(response.text)
       if savejson == 1:
          with open(jsonfname(), "w") as temp_data:
               temp_data.write(str(data))
               dl.writelog(dl.logpath(run_id),
                           'successfuly finished !  Json available in unfflatten folder \n',
                           debugmode)
               return data
       else:
            dl.writelog(dl.logpath(run_id), "successfuly finished to retriev data to the server,moving on to insert it to DB \n" , debugmode)
            return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
            dl.writelog(dl.logpath(run_id), "Somthing went wrong with cmc API." + '\n', debugmode)
            print(e)

def setobj(obj):
    if not obj:
        return str('null')
    if obj == 'None':
        return str('null')
    if obj is None:
        return str('null')
    elif type(obj) == int:
        return str(obj)
    elif type(obj) == float:
        newobj = round(obj, 9)
        return newobj
    elif type(obj) == str:
        if len(obj) >= 22:
            if obj[10]=="T" and obj[13] == ":":
                newobj = obj.replace("T", " ")
                newobjstr = str(newobj)[:19]
                return str("'" + newobjstr.replace("'", "") + "'")
            else:
                return str("'" + obj.replace("'", "") + "'")
        else:
            return str("'" + obj.replace("'", "") + "'")
    elif type(obj) == list:
        if obj == []:
            return str('null')
        newobj = obj[0]
        return str("'" + newobj +"'")
    else:
        return str("'" + obj.replace("'", "") + "'")


def getsql(arr, debugmode, run_id=0, env='test'):
    if env == 'test':
        sql = "INSERT INTO mrr_test.fact_20_min_raw_data VALUES\n"
    else:
        sql = "INSERT INTO mrr.fact_20_min_raw_data VALUES\n"
    islast_row = 0
    for dict in arr :
        islast_row += 1
        insertrow = '('
        insertvlues = [str(run_id),
                       str(setobj(dict["last_updated"])),
                       str(setobj(dict["id"])),
                       str(setobj(dict["name"])),
                       str(setobj(dict["symbol"])),
                       str(setobj(dict["tags"])),
                       str(setobj(dict["max_supply"])),
                       str(setobj(dict["circulating_supply"])),
                       str(setobj(dict["total_supply"])),
                       str(setobj(dict["cmc_rank"])),
                       str(setobj(dict["quote"]["USD"]["price"])),
                       str(setobj(dict["quote"]["BTC"]["price"])),
                       str(setobj(dict["quote"]["USD"]["volume_24h"])),
                       str(setobj(dict["quote"]["BTC"]["volume_24h"])),
                       str(setobj(dict["quote"]["USD"]["percent_change_1h"])),
                       str(setobj(dict["quote"]["BTC"]["percent_change_1h"])),
                       str(setobj(dict["quote"]["USD"]["percent_change_24h"])),
                       str(setobj(dict["quote"]["BTC"]["percent_change_24h"])),
                       str(setobj(dict["quote"]["USD"]["percent_change_7d"])),
                       str(setobj(dict["quote"]["BTC"]["percent_change_7d"])),
                       str(setobj(dict["quote"]["USD"]["market_cap"])),
                       str(setobj(dict["quote"]["BTC"]["market_cap"]))
                       ]
        fixedfieldlist = []
        for i in insertvlues:
            if i != None:
                fixedfieldlist.append(i)
            else:
                fixedfieldlist.append('null')
        txtvals = ",".join(fixedfieldlist)
        rtoadd = insertrow + txtvals + ")"
        if len(arr) != islast_row:
            rtoadd += ',\n'
        sql += rtoadd
    dl.writelog(dl.logpath(run_id), "The sql prepared for insertion is :" + '\n' + sql[:1500] +'\n', debugmode)
    print(str(islast_row) +" Rows retrieved from this response")
    return sql


def load_cmc_data( debugmode=0, run_id=0, env='test'):
    # Download new data
    dl.writelog(dl.logpath(run_id), '\n Start fetching currencies \n', debugmode)
    # Call cmc func take currency id and return data
    fulldata = callcms(run_id=run_id, debugmode=debugmode)
    dl.writelog(dl.logpath(run_id), "\n Data fetched finished, prepareing the SQL" + '\n', debugmode)
    # Isolate only the relevant data
    crpdata = fulldata["data"]
    # Prepare the insert sql statement
    sql = getsql(arr=crpdata, run_id= run_id, debugmode=debugmode, env=env)
    dl.writelog(dl.logpath(run_id), "\n Data fetched finished, prepareing the SQL" + '\n', debugmode)
    # Execute the sql
    mysql.qryexec(numb=sql, retval=0, run_id=run_id, debugmode=debugmode, env=env)
    dl.writelog(dl.logpath(run_id), "\n Data successfully inserted to aurora", debugmode)


# Return only the sql to execute

def getrunid_str():
    date = dt.datetime.now()
    year = str(date.year)
    month = str(date.month)
    if len(month) == 1:
        month = '0' + str(month)
    day = str(date.day)
    if len(day) ==1:
        day = '0' + str(day)
    hr = str(date.hour)
    if len(hr) ==1:
        hr = '0'+str(hr)
    mn = str(date.minute)
    if len(mn) == 1 :
        mn = '0' +mn
    timestamp = year + month + day + hr + mn
    return timestamp
