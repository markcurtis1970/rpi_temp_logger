#!/usr/bin/env python

# For checking the SQLlite DB

import sqlite3
import os
import time
import glob
import datetime

# global variables
dbname='./colchester.db'


# display the contents of the database
def display_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()


# main function
# This is where the program starts 
def main():

        # display the contents of the database
        display_data()


if __name__=="__main__":
    main()




