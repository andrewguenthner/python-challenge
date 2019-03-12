# -*- coding: utf-8 -*-
"""
PyBank: Automatically summarize profit and loss information
from the file budget_data.csv, with results displayed in both
the terminal and an output file, PyBank_Results.csv

The design doc and detailed information is avaialbe in the README
file included with this script.  Input files should be in a folder
named "Resources" in the same directory as this script.  Output will
be in the same folder as the script.  

Important design note:  this file is meant for monthly data, so
it does not expect extremely large data sets.

Written by:  Andrew Guenthner, UC Berkeley Extension
Version:  1.0   10-Mar-2019
Github:  https://github.com/andrewguenthner/python-challenge
"""
import os
import csv

# This is the "base year" for data,
# a value of "50" indicates that data in mmm-yy
# format extend from 1950 to 2049, not XX = 00
# means data are from 2000-2099  
XX = 50    # Must be a positive integer from 0 - 99 
# For parsing monthly data in mmm format
MONTH_DICT = {"jan":1,"feb":2,"mar":3,"apr":4,
              "may":5,"jun":6,"jul":7,"aug":8,
              "sep":9,"oct":10,"nov":11,"dec":12}
# {"1":"January","2":"February","3":"March",
 #             "4":"april,","5":"May","6":"June",
  #            "7":"July","8":"August","9":"September",
   #           "10":"October","11":"November",
    #          "12":"December"}

def add_month_index(labels, month_key, base_year):
      """ Takes a list of [M|m]mm[*]-yy month labels, a dictionary of
      month keys, and a base_year, and returns two objects,
      a list of integers that allows for sorting, and a 
      count of entries it fails to interpret.  The 
      integer created corresponds to the number of months 
      after the start of base_year, so if base_year = 50
      and the label is Jan-50, the integer will be 1, if the
      label is Dec-51, the integer will be 24, but if the
      label is Jan-40, the integer will be 90 * 12 + 1 = 1081"""
    # Initialize
    month_index = []
    readerrors = 0
    # Get month and year values from string, month_id = 0 if not found, year_id = -1 if error
    for i, item in enumerate(labels):
        month_id = month_key.getkey(item[0:2].lower(),0)
        try:
            year_id = int(item[-3:-1])
        except ValueError:
            year_id = -1
        # Either convert a valid month_id and year_id to the desired integer, or generate 0
        if month_id > 0:
            if year_id > base_year:
                month_index.append(year_id - base_year) * 12 + month_id
            elif year_id >= 0:
                month_index.append(year_id + 100 - base_year) * 12 + month_id
            else:
                readerrors += 1
                month_index.append(0)
        else:
            readerrors += 1
            month_index.append(0)
    return month_index, readerrors

def sort_by_month (key, label, val):
"""Implimments an insertion sort using "key" as the sort key
   and taking label and val along for the ride.  See design
   doc for rationale"""
    for i in range(len(key)):
        cursor = key[i]
        tagalong1 = label[i]
        tagalong2 = val[i]
        pos = i
        while pos > 0 and key[pos - 1] > cursor:  # first half of swap
            key[pos] = key[pos - 1]
            label[pos] = label[po - 1]
            val[pos] = val[pos - 1]
            pos = pos - 1
            key[pos] = cursor # second half of swap
            label[pos] = tagalong1
            val[pos] = tagalong2
    return key, label, val 

def clean_data(key, label, val):
"""This function expects three coupled lists sorted by key.  
   Anything with a key value of zero is assumed bad and removed.
   The second or more occurrene of anything with the same key is removed.
   If there is a gap between consecutive keys, the "missing values" are 
   counted but no rows are added."""
    # Initialize 
    i = 0
    cut_count = 0
    gap_count = 0
    while i < len(key):
        if key[i] == 0:   # Cut out anything marked as invalid
            del key[i]
            del label[i]
            del val[i]
        elif key[i+1] == key[i]:   #Remove duplicates and track how many were cut
            del(key[i+1])
            del(label[i+1])
            del(val[i+1])
            cut_count += 1
        else:
            i += 1
    # With every row being a sorted non-zero key and no duplicates, gap-counting is easy
    gap_count = key[-1] - key[0] - len(key) + 1   
    return key, label, val, cut_count, gap_count 

in_file = os.path.join("..","Resources","budget_data.csv")
out_file = os.path.join("PyBank_results.csv")
# Handle 'file not found' errors 
input_success = False
try:
    # Read in the CSV file and skip the header row
    with open(in_file, 'r') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        header = next(csvreader)
        # Initialize the lists that will store data
        month_index = []
        month_label = []
        profit_value = [] 
        # Assign data to these lists from the file 
        # 1st column is a month label in mmm-yy format
        # 2nd column is a profit or loss value for the month
        for row in csvreader:
            month_label.append(row[0])
            profit_value.append(row[1])
    input_success = True
except FileNotFoundError as e:
    with open(out_file, 'w') as results_file:
        print("An error occured while reading the input file.")
        print("Please check the file and try again.")
        results_file.write("An Error occured while reading the input file.\n")
        results_file.write("Please check the file and try again.")
# Pre-process the data
# Initialize some counters
bad_rows = 0  # Will count & flag bad rows
extras = 0 # Will flag & count duplicated monthly data
gaps = 0 # Will flag & count missing months 
# First, decode and assign an index to each month label (returns 0 for bad data)
month_index, bad_rows = add_month_index(month_label, MONTH_DICT, XX)
# Now, use the index to ensure months are sorted
month_index, month_label, profit_value = sort_by_month(month_index, month_label, profit_value)
# Finish the clean-up by removing duplicates and noting gaps
month_index, month_label, profit_value, extras, gaps = clean_data(month_index, month_label, profit_value)
# Begin analysis - initialize variables
pl_total = 0.0     # Total profit - set to zero for readability
pl_average_delta = 0.0   # default value 
max_delta = 0.0    # will hold larget increase in profit, if any
min_delta = 0.0    # will hold largest drop in profit if any 
max_delta_label = "No sequentil increae in net profit found" # location of max_delta
min_delta_index = "No sequential decrease in net profit found" # location of min_delta
pl_delta = 0.0      # temporary holder for change in profit
max_ties = ""
       # will hold any info on ties for max_delta
min_ties = ""
       # will hold any info on ties for min_delta
# First compute some simple stats
pl_total = profit_value.sum()
# The "average change" in monthly profits is just (last - first) / # of months
# it's not just mathematical, but also a nice result from calculus
if len(profit_value) > 0:   # Just make sure there's something to average
    pl_average_delta = (profit_value[-1] - profit_value[0]) / len(profit_value)
# Run thrugh all months to gather max and min info
# Note that we are looking for max increase and max decrease, so the max must be >0
# and the min <0, this is provided by the initial values
for i, label in enumerate(month_label):
    if (i > 0):  # don't look for changes for the first month
        pl_delta = profit_value[i] - profit_value[i-1]
        if pl_delta > max_delta:    # Record max
            max_delta = pl_delta
            max_delta_label = label
            max_ties = ""
                # Overwrite the list of ties if a new max is found
        elif pl_delta == max_delta:  # Keep track of ties
            max_ties += label +  " "
        elif pl_delta < min_delta:   #Same logic for min as for max
            min_delta = pl_delta
            min_delta_label = label
            min_ties = ""
        elif pl_delta == min_delta:  # Keep track of ties
            min_ties += label +  " "
# Now report the results 
# First, fix the date formats to be consistent with report template (Mmm-yyyy)
try:   #Add '19' or '20' to year labels for max and min delta
    if int(max_delta_label[-2]) < XX:
        max_delta_label = max_delta_label[0:-2] + "20" + max_delta_label[-2]
    else:
        max_delta_label = max_delta_label[0:-2] + "19" + max_delta_label[-2]
except ValueError as e:
    pass    # Don't bother if no max was found
try:   #Fix min label just like we did for max above 
    if int(min_delta_label[-2]) < XX:
        min_delta_label = min_delta_label[0:-2] + "20" + min_delta_label[-2]
    else:
        min_delta_label = min_delta_label[0:-2] + "19" + min_delta_label[-2]
except ValueError as e:
    pass    
# Now write the results 
with open(out_file, 'w') as results_file:
    print ("Financial Analysis")
    results_file.write("Financial Analysis\n")
    print ("----------------------------")
    results_file.write ("----------------------------\n")
    print ("Total Months: {}".format(len(profit_value)))
    results_file.write ("Total Months: {}\n".format(len(profit_value)))
    print ("Total: ${}".format(pl_total))
    results_file.write ("Total: ${}\n".format(pl_total))
    print ("Average Change: ${:f2}".format(pl_average_delta))
    results_file.write ("Average Change: ${:f2}\n".format(pl_average_delta))
    print ("Greatest Increase in Profits: {} (${})".format(max_delta_label,max_delta))
    results_file.write ("Greatest Increase in Profits: {} (${})\n".format(max_delta_label,max_delta))
    print ("Greatest Decrease in Profits: {} (${})".format(min_delta_label,min_delta))
    results_file.write ("Greatest Decrease in Profits: {} (${})\n".format(min_delta_label,min_delta))
    if len(max_ties) > 0:  #Note ties:
        print ("Months in which the greatest increase was tied with that reporte were: " + Max_Ties)
        results_file.write ("Months in which the greatest  increase was tied with that reporte were: " + Max_Ties + "\n")
        print ("Months in which the greatest  decrease was tied with that reporte were: " + Min_Ties)
        results_file.write ("Months in which the greatest decrease was tied with that reporte were: " + Min_Ties + "\n")
   # Note other data issues.
    if bad_rows > 0:   
        print ("{} bad rows of data were excluded from analysis.".format(bad-rows))
        results_file.write ("{} bad rows of data were excluded from analysis.\n".format(bad-rows))
    if extras > 0:
        print ("{} rows with duplicated months were excluded from analysis (only the first instance found was kept).".format(extras))
        results_file.write ("{} rows with duplicated months were excluded from analysis (only the first instance found was kept).\n".format(extras))
    if gaps > 0:
        print ("{} months were missing from analysis.".format(gaps))
        results_file.write ("{} months were missing from analysis.\n".format(gaps))
