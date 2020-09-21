#!/usr/bin/env python

# Drives the creation of a web page
# to visualise the results

import sqlite3
import sys
from flask import Flask
from flask import render_template

# global variables
dbname='/home/pi/rpi_temp_logger/colchester.db'
app = Flask(__name__)

# return a list of records from the database
def get_data(interval):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    if interval == None:
        curs.execute("SELECT * FROM temps")
    else:
        curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-%s hours')" % interval)
    rows=curs.fetchall()
    conn.close()
    return rows


# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""
    for row in rows[:-1]:
        rowstr="['{0}', {1}],\n".format(str(row[0]),str(row[1]))
        chart_table+=rowstr
    row=rows[-1]
    rowstr="['{0}', {1}]\n".format(str(row[0]),str(row[1]))
    chart_table+=rowstr
    return chart_table

# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):
    global rowmax, rowmin, rowavg
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    if option is None:
        option = str(24)

    curs.execute("SELECT timestamp,max(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmax[0]),str(rowmax[1]))

    curs.execute("SELECT timestamp,min(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    rowmin=curs.fetchone()
    rowstrmin="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(temp) FROM temps WHERE timestamp>datetime('now','-%s hour') AND timestamp<=datetime('now')" % option)
    rowavg=curs.fetchone()

    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('new','-1 hour') AND timestamp<=datetime('new')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C</td></tr>".format(str(row[0]),str(row[1]))
        print rowstr
    
    conn.close()

# main function
@app.route('/')
def main():

    # Default to 24 hours    
    option = str(24)
    # get data from the database
    records=get_data(option)
    # If no records returned, exit
    if len(records) != 0:
        # convert the data into a table
        table=create_table(records)
    else:
        print "No data found"
        return
    # Gen min, max and avg
    show_stats(option)
    times = []
    temps = []
    for val in records:
        times.append(str(val[0]))
        temps.append(val[1])
    
    print rowmax[0]
    print type(rowmax)
    return render_template("temp.html", time_data=times, temp_data=temps, date_min=rowmin[0], date_max=rowmax[0], min=rowmin[1], max=rowmax[1], avg=rowavg[0])
   
if __name__=="__main__":
    app.run(host='0.0.0.0')




