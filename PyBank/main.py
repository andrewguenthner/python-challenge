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
Version:  1.0   12-Mar-2019
Github:  https://github.com/andrewguenthner/python-challenge
"""
import os
import csv

# For parsing monthly data in mmm format
MONTH_DICT = {"jan":1,"feb":2,"mar":3,"apr":4,
              "may":5,"jun":6,"jul":7,"aug":8,
              "sep":9,"oct":10,"nov":11,"dec":12}


def add_month_index(labels, month_key):
    """ Takes a list of [M|m]mm[*]-yyyy month labels, and 
    a dictionary of month keys, and returns two objects,
    a list of integers that allows for sorting, and a 
    count of entries it fails to interpret.  The 
    integer created corresponds to the number of months 
    after the start of 0 A.D. (four digit years required)
    """
    # Initialize
    month_index = []
    readerrors = 0
    # Get month and year values from string, month_id = 0 if not found, year_id = -1 if error
    for item in labels:
        month_id = int(month_key.get(str(item[0:3]).lower(),0))
        try:
            year_id = int(item[-4:])
        except ValueError:
            year_id = -1
        # Either convert a valid month_id and year_id to the desired integer, or generate 0
        if (month_id > 0) and (year_id >= 0):
            month_index.append(year_id * 12 + month_id)
        else:
            readerrors += 1
            month_index.append(0)
    return month_index, readerrors

def sort_by_month (key, label, val):
    """Implimments an insertion sort using "key" as the sort key
    and taking label and val along for the ride.  See design
    doc for rationale
    """
    for i in range(len(key)):
        cursor = key[i]
        tagalong1 = label[i]
        tagalong2 = val[i]
        pos = i
        while pos > 0 and key[pos - 1] > cursor:  # first half of swap
            key[pos] = key[pos - 1]
            label[pos] = label[pos - 1]
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
    counted but no rows are added.
    """
    # Initialize 
    i = 0
    cut_count = 0
    gap_count = 0
    while i < len(key) - 1:
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
    if len(key) > 0:   #Make sure there's at least one good row left before...
        gap_count = key[-1] - key[0] - len(key) + 1   
    return key, label, val, cut_count, gap_count 

in_file = os.path.join("Resources","budget_data.csv")
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
            profit_value.append(float(row[1]))
    input_success = True
except FileNotFoundError as e:
    with open(out_file, 'w') as results_file:
        print("An error occured while reading the input file.")
        print("Please check the file and try again.")
        results_file.write("An Error occured while reading the input file.\n")
        results_file.write("Please check the file and try again.")
if input_success == True:
    # Pre-process the data
    # Initialize some counters
    bad_rows = 0  # Will count & flag bad rows
    extras = 0 # Will flag & count duplicated monthly data
    gaps = 0 # Will flag & count missing months 
    # First, decode and assign an index to each month label (returns 0 for bad data)
    month_index, bad_rows = add_month_index(month_label, MONTH_DICT)
    # Now, use the index to ensure months are sorted
    month_index, month_label, profit_value = sort_by_month(month_index, month_label, profit_value)
    # Finish the clean-up by removing duplicates and noting gaps
    month_index, month_label, profit_value, extras, gaps = clean_data(month_index, month_label, profit_value)
    # Begin analysis - initialize variables
    if len(month_index) > 0:   #Make sure there's at least one good row left to work on
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
        pl_total = sum(profit_value)
        # The "average change" in monthly profits is just (last - first) / (# months - 1)
        # a nice bit of math
        if len(profit_value) > 1:   # Needs at leat two values to be valid
            pl_average_delta = (profit_value[-1] - profit_value[0]) / (len(profit_value) - 1)
        # Run thrugh all months to gather max and min info
        # Note that we are looking for max increase and max decrease, so the max must be >0
        # and the min <0, this is provided by the initial values
        if len(month_index) > 1:  #Search only if more than one row of data exists
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
        with open(out_file, 'w') as results_file:
            print ("Financial Analysis")
            results_file.write("Financial Analysis\n")
            print ("----------------------------")
            results_file.write ("----------------------------\n")
            print (f"Total Months: {len(profit_value)}")
            results_file.write (f"Total Months: {len(profit_value)}\n")
            print (f"Total: ${pl_total:.0f}")
            results_file.write (f"Total: ${pl_total:.0f}")
            print (f"Average Change: ${pl_average_delta:.2f}")
            results_file.write (f"Average Change: ${pl_average_delta:.2f}\n")
            print (f"Greatest Increase in Profits: {max_delta_label} (${max_delta:.0f})")
            results_file.write (f"Greatest Increase in Profits: {max_delta_label} (${max_delta:.0f})\n")
            print (f"Greatest Decrease in Profits: {min_delta_label} (${min_delta:.0f})")
            results_file.write (f"Greatest Decrease in Profits: {min_delta_label} (${min_delta:.0f})\n")
            if len(max_ties) > 0:  #Note ties:
                print ("Months in which the greatest increase was tied with that reporte were: " + max_ties)
                results_file.write ("Months in which the greatest  increase was tied with that reporte were: " + max_ties + "\n")
                print ("Months in which the greatest  decrease was tied with that reporte were: " +min_ties)
                results_file.write ("Months in which the greatest decrease was tied with that reporte were: " + min_ties + "\n")
        # Note other data issues.
            if bad_rows > 0:   
                print (f"{bad_rows} bad rows of data were excluded from analysis.")
                results_file.write (f"{bad_rows} bad rows of data were excluded from analysis.\n")
            if extras > 0:
                print (f"{extras} rows with duplicated months were excluded from analysis (only the first instance found was kept).")
                results_file.write (f"{extras} rows with duplicated months were excluded from analysis (only the first instance found was kept).\n")
            if gaps > 0:
                print (f"{gaps} months were missing from analysis.")
                results_file.write (f"{gaps} months were missing from analysis.\n")
    else:   #Happens when no valid rows are present
        print("No data was found in the file.")
        with open(out_file, 'w') as results_file:
            results_file.write("No data was found in the input file.\n")