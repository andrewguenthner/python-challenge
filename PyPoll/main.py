# -*- coding: utf-8 -*-
    """
    PyPoll:  Automatically counts votes from a specific file,
    Resources/election_data.csv, and puts the tally in a file
    called PyPoll_Results.csv (same folder as script)

    The design doc and detailed information is avaialbe in the README
    file included with this script.  

    Important design note:  this file is meant only for the exact 
    data format (including headers) as shown in election_data.csv.  
    If any deviations are detected, the script will not execute the 
    tally.  

    Written by:  Andrew Guenthner, UC Berkeley Extension
    Version:  1.0   12-Mar-2019
    Github:  https://github.com/andrewguenthner/python-challenge
    """
import os
import csv
# File reading portion
in_file = os.path.join("Resources","election_data.csv")
out_file = os.path.join("PyPoll_results.csv")
# Handle 'file not found' error
OK_to_proceed = False
try:
    # Read in the CSV file.  Set input_success flag if successful.
    with open(in_file, 'r') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        OK_to_proceed = True
except OSError as e:
    # If no file is present, notify user
    with open(out_file, 'w') as results_file:
        print("The input file was not found.  No results computed.")
        results_file.write("The input file was not found.  No results computed\n")       
# File checking portion
if (OK_to_proceed) == True:
    # Initialize
    valid_flag = False
    row_OK = []
    row_count = 0 
    # Check every row for conformity to expected file format.
    # If any anomaly is found, the script will notify the user and avoid tallying votes.
    for row in csvreader:
        if (row_count == 0):  # for the header row only
            if (row[0] == "Voter ID") and (row[1] == "County") and (row[2] == "Candiate"):
                row_OK.append(True)
            else:
                row_OK.append(False)
        else:                   # for all the other rows
            row_check = False
            try:
                _ = int(row[0]) # Try to force integer conversion
                if (len(row[1]) > 0) and (len(row[2]) > 0):
                    row_check = True
            except ValueError as e:
                pass
            except IndexError as e:
                pass
            row_OK.append(row_check)
        row_count += 1    # "Reality check" to count loop executions
    if row_OK.count(True) == len(row_OK) == row_count:
        # Only if each and every pass through the loop appended True
        # to row_OK will it be OK to start tallying the votes
        # row-count will be used later on to check the tally also
        valid_flag = True
    OK_to_proceed = valid_flag
else:  #This should only happen if soan unforeseen error stopped the csvreader from working
     with open(out_file, 'w') as results_file:
        print("An unexpected event stopped the file check from running.  No results computed ")
        results_file.write("An unexpected event stopped the file check from running.  No results computed.\n")     

# Tally portion 
if (OK_to_proceed) == True:
    # Initialize
    header_scanned = False
    votes_counted = 0
    total_votes = 0
    candidate_list = []  # For simplicity and transparency, the
    candidate_votes = [] # use of Python counter object was avoided
    for row in csvreader:
        if rows_counted == 0:  #First two cases
            if header_scanned == False:  # For header, just flag it as counted
                header_scanned = True
            else:
                candidate = row[2]   # count the first vote
                candidate_list.append(candidate)
                candidate_votes[0] = 1
                total_votes += 1   # for an independent check of the code
                rows_counted += 1
        else:  # for all but the first vote
            candidate = row[2]
            rows_counted += 1
            entry_found = False
            for i, entry in enumerate(candidate_list):  #Check for previous votes
                if candidate == entry:      # add to vote total if found
                    candidate_votes[i] += 1
                    total_votes += 1        # for "reality check"
                    entry_found = True
            if entry_found = False:    # if this name is new, add it to the list
                    candidate_list.append(candidate)
                    candidate_votes.append(1)  
                    total_votes += 1    # for "reality check"
    # Now check the integrity of the process
    if rows_counted == total_votes == sum(candidate_votes) == row_count - 1:
        OK_to_proceed = True    
        # only if each row (except header) in the file corresponds to a pass
        # through the counting loop, and an execution of an increment to candidate_votes
        # and the sum that's actually in candidate votes reflects the code execution,
        # only then are the results printed and saved 
    else:
        OK_to_proceed = False
else:   # if the file check failed and the tallying portion did not run
    with open(out_file, 'w') as results_file:
            print("The file check encountered an anomaly.  No results computed ")
            results_file.write("The file check encountered an anomaly.  No results computed.\n")     
# Reporting portion 
if (OK_to_proceed) = True:

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