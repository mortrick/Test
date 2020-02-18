#!/usr/bin/env python
import datetime as dt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import mysqlactions as mysql
import platform
from logs import dynamic_log as dl


import twlsms as twl

### Authorized columns



def jsonfname ():
    now = dt.datetime.now()
    dtstring = now.strftime("%d_%m_%Y_%H_%M_%S")
    filname = "notflattendata" + dtstring +".json"
    fullpath = "./unflatten_data/" + filname
    return fullpath

def returnurl():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    return url

def prms(cur):
    if cur == 1:
        parameters = {
          'start': '1',
          'limit': '5000',
          'convert': 'USD'
        }
        return parameters
    else:
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'BTC'
        }
        return parameters

def headers():
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '492b9d81-0f94-4449-90b1-3fe1ff9b29ff',
    }
    return headers





def callcms(cur, run_id, debugmode):
    session = Session()
    session.headers.update(headers())
    try:
      response = session.get(returnurl(), params=prms(cur))
      data = json.loads(response.text)
      # with open(jsonfname(), "w") as temp_data:
      #   temp_data.write(str(data))
      dl.writelog(dl.logpath(run_id), "successfuly finished to retrieve data to the server, moving on to insert it to DB" + '\n', debugmode)
      return (data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        dl.writelog(dl.logpath(run_id), "Somthing went wrong with cmc API." + '\n', debugmode)
        print(e)


# def dimscolumns():
#     authcolumns = ["id", "name", "symbol", "tags", "max_supply", "circulating_supply", "total_supply", "cmc_rank"]
#     return authcolumns
#
#
# def quotecolumns():
#     cols =["price", "volume_24h", "percent_change_1h", "percent_change_24h", "market_cap", "last_updated"]
#     return cols

def setobj(obj, conversiontype):
    if conversiontype == 1:
        rnd = 3
    else:
        rnd = 10
    if not obj:
        return str('null')
    if obj == 'None':
        return str('null')
    if obj is None:
        return str('null')
    elif type(obj) == int:
        return str(obj)
    elif type(obj) == float:
        newobj = round(obj, rnd)
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


def getsql(arr, conversion_type, debugmode, run_id):
    if platform.system() == 'Windows':
        sql = "INSERT INTO mrr_test.fact_30_min_raw_data VALUES\n"
    else:
        sql = "INSERT INTO mrr.fact_30_min_raw_data VALUES\n"
    if conversion_type == 1:
        contype = "USD"
    else:
        contype = "BTC"
    islast_row = 0
    for dict in arr:
        islast_row += 1
        insertrow = '('
        insertvlues = [str(setobj(dict["id"], conversion_type)),
                       str(conversion_type),
                       str(setobj(dict["name"], conversion_type)),
                       str(setobj(dict["symbol"], conversion_type)),
                       str(setobj(dict["tags"], conversion_type)),
                       str(setobj(dict["max_supply"], conversion_type)),
                       str(setobj(dict["circulating_supply"], conversion_type)),
                       str(setobj(dict["total_supply"], conversion_type)),
                       str(setobj(dict["cmc_rank"], conversion_type)),
                       str(setobj(dict["quote"][contype]["price"], conversion_type)),
                       str(setobj(dict["quote"][contype]["volume_24h"], conversion_type)),
                       str(setobj(dict["quote"][contype]["percent_change_1h"], conversion_type)),
                       str(setobj(dict["quote"][contype]["percent_change_24h"], conversion_type)),
                       str(setobj(dict["quote"][contype]["market_cap"], conversion_type)),
                       str(setobj(dict["quote"][contype]["last_updated"], conversion_type))
                     ]
        fixedfieldlist =[]
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
    dl.writelog(dl.logpath(run_id), "The sql prepared for insertion is :" + '\n' + sql +'\n', debugmode)
    return sql



# def execmngsql(query_id, is_return=0):
#     sql = "select query_str from mng.environment_queries where query_id = " + str(query_id)
#     execsql = cn.connect(sql, 1)[0]
#     print("I Execute the query", execsql)
#     if is_return == 0:
#         cn.connect(execsql, is_return)
#         return(execsql)
#     else:
#         isdata = cn.connect(sql, is_return)[0]
#         data = cn.connect(isdata, is_return)[0]
#         if not data:
#             print("The query return no data")
#             return 0
#         else:
#             print("Here are the results for the query")
#             return data

def load_cmc_data(cur, debugmode = 0,run_id = 0):
    # Download new data
    if cur == "USD":
        curid = 1
    else:
        curid = 2
    dl.writelog(dl.logpath(run_id), "\n Start fetching currencies " + cur + '\n', debugmode)
    # Call cmc func take currency id and return data
    fulldata = callcms(curid, run_id=run_id, debugmode=debugmode)
    dl.writelog(dl.logpath(run_id), "\n Data fetched finished, prepareing the SQL" + '\n', debugmode)
    # Isolate only the relevant data
    crpdata = fulldata["data"]
    # Prepare the insert sql statement
    sql = getsql(arr=crpdata, conversion_type= curid, run_id= run_id, debugmode=debugmode)
    dl.writelog(dl.logpath(run_id), "\n Data fetched finished, prepareing the SQL" + '\n', debugmode)
    # Execute the sql
    mysql.qryexec(numb=sql, retval=0, run_id=run_id, debugmode=debugmode)
    dl.writelog(dl.logpath(run_id), "\n Data successfully inserted to aurora"  , debugmode)


# Return only the sql to execute



# twl.sendsms()
# execmngsql(2, 0)
# execmngsql(1, 0)

# test = execmngsql(3, 1)
# print(test)
# txt = "2020-02-18T01:07:08.000Z"
#
# print(setobj(txt, 1))


def getrunid_str():
    date = dt.datetime.now()
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hr = str(date.hour)
    mn = str(date.minute)
    timestamp = year + month + day + hr + mn
    return timestamp