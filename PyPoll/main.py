# -*- coding: utf-8 -*-
"""
PyPoll:  Automatically counts votes from a specific file,
Resources/election_data.csv, and puts the tally in a file
called PyPoll_results.txt (same folder as script)

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
out_file = os.path.join("PyPoll_results.txt")
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
        print("There was an error opening the input file.  No results computed.")
        results_file.write("There was an error opening the input file.  No results computed\n")       
# File checking portion
if (OK_to_proceed) == True:
    # Initialize
    valid_flag = False
    row_OK = []
    row_count = 0 
    # Check every row for conformity to expected file format.
    # If any anomaly is found, the script will notify the user and avoid tallying votes.
    with open(in_file, 'r') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            if (row_count == 0):  # for the header row only
                if (row[0] == "Voter ID") and (row[1] == "County") and (row[2] == "Candidate"):
                    row_OK.append(True)
                else:
                    row_OK.append(False)
            else:                   # for all the other rows
                row_check = False
                try:
                    if (int(row[0]) >= 0) (len(row[1]) > 0) and (len(row[2]) > 0):
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
    rows_counted = 0
    candidate_list = []  # For simplicity and transparency, the
    candidate_votes = [] # use of Python counter object was avoided
    with open(in_file, 'r') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            if rows_counted == 0:  # First two cases
                if header_scanned == False:  # For header, just flag it as counted
                    header_scanned = True
                else:
                    candidate = row[2]   # count the first vote
                    candidate_list.append(candidate)
                    candidate_votes.append(1)
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
                if entry_found == False:    # if this name is new, add it to the list
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
if (OK_to_proceed) == True:
    #First, sort the data via a selection-sort.  Slow but easy-to-explain to non-experts.
    for i in range(len(candidate_list)): 
        max_index = i 
        for j in range(i+1, len(candidate_list)): 
            if candidate_votes[j] > candidate_votes[max_index]: 
                max_index = j 
            candidate_list[i], candidate_list[max_index] =\
            candidate_list[max_index] , candidate_list[i]
            candidate_votes[i], candidate_votes[max_index] =\
            candidate_votes[max_index] , candidate_votes[i]
        # Now report the results 
    with open(out_file, 'w') as results_file:
        print ("Election Results")
        results_file.write("Election results\n")
        print ("-------------------------")
        results_file.write ("--------------------------\n")
        print (f"Total Votes: {total_votes}")
        results_file.write (f"Total Votes: {total_votes}\n")
        print ("-------------------------")
        results_file.write ("--------------------------\n")
        for i, candidate_name in enumerate(candidate_list):
            print (f"{candidate_name}: {(candidate_votes[i]/total_votes*100):.3f}% ({candidate_votes[i]})")
            results_file.write (f"{candidate_name}: {(candidate_votes[i]/total_votes*100):.3f}% ({candidate_votes[i]})\n")
        print ("-------------------------")
        results_file.write ("--------------------------\n")           
        if candidate_votes[0] == candidate_votes[1]:   # If there's a tie for first, don't declare a winner
            print ("A tie among candidates with the most votes was found.")
            results_file.write ("A tie among candidates with the most votes was found.\n")
        else:
            print (f"Winner:  {candidate_list[0]}")
            results_file.write(f"Winner:  {candidate_list[0]}\n")
        print ("-------------------------")
        results_file.write ("--------------------------\n")    
else:   #if OK_to_proceed was false 
    print("An anomaly in data processing occurred.  Results have not been reported.")
    with open(out_file, 'w') as results_file:
        results_file.write("An anomaly in data processing occurred.  Results have not been reported.\n")