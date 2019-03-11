#PyBank README

Quick user info:
This script expects a CSV input data file named election_data.csv 
inside a folder named "Resources" within the same directory as
the script.  The input file should include a header row and
3 columns, the first with a voter ID, the second with a county name,
and the third with an election candidate name.

It will output a simple vote summary to the terminal as well as to
a CSV file named PyPoll_Results.csv.  

Design doc:

Objective:  Automatically summarize vote data from the file
election_data.csv, with results displayed in both
the terminal and an output file.

Rationale:  This straigtforward task is being automated to modernize
the vote counting process.  Data integrity, process transparency,
and voter privacy are important issues.  

Expected input:  CSV data file with arbitrary number of rows.
The program will expect a header row, and exactly three columns
of data.  The header row content will be checked, as will 
the presence of at least one row of vote data.  Column 1 will
be an ID number. Column 2 will be a county name.  Column 3 will
be a candidate name.  For this script, we will be very strict 
about errors.  If the script encounters an error in the form of:
1) a non-numeric voter ID, 2) no county entered, or 3) no candidate
name listed, it will output an error message asking the user to
check the file for problems.  It wil not output any "provisional"
data, and in fact it will not execute any algorithm that could
generate any kind of vote count data unless the input data is 
formatted perfectly.  (The script's job is to count valid votes,
not geneate "what-if" scenarios.)


Expected output:
The output will be strictly controlled, in both terminal and
PyPoll_Results.csv files.  If no errors are found, it will look
like the following
example:  

  Election Results
  -------------------------
  Total Votes: 3521001
  -------------------------
  Khan: 63.000% (2218231)
  Correy: 20.000% (704200)
  Li: 14.000% (492940)
  O'Tooley: 3.000% (105630)
  -------------------------
  Winner: Khan
  -------------------------
If there is a tie, it will look like the following

  Election Results
  -------------------------
  Total Votes: 100000
  -------------------------
  Khan: 44.000%  (44000)
  Correy: 44.000% (44000)
  Li: 12.000% (12000)
  -------------------------
  A tie among candidates with the most votes was found.  
  -------------------------

If an error is found, it will look like the following:

One or more errors were encountered in the input data file.  
As a result, the vote-counting portion of the script was skipped.
Please check the input file before attempting to re-run the script.

If data processing is interrupted or in some way an improper behavior
is detected, then the output will look like the following:

An error was encountered during processing of the data.  
The program has terminated without saving or displaying
results.  Please cotact your supervisor. 

"Total Votes" will provide the sum of all votes in the table.
The next section will provide the name, percentage, and vote total
for all candidates with votes.

The final row will either state the candidate name with the most
votes if no tie is encountered.

  Procedural Outline
R) Use csvreader to input file.  
C) Check file for valid date, proceed only if all data is valid
P) Process data by reading file line by line and building a results list.
Check that every line of the file was analyzed.  
W) finish by writing the output table to terminal and file

  Detailed Procedures
  R.1 -- import libs
  R.2 -- set path
  R.3 -- use a try: to enlcoe rest of R; with error send bad-file message
  R.4 -- create reader object (reader) -- use with for R and C, the 
  file will be closed and re-opened for processing -- this will check
  that we can open, read everything, and close without a problem before
  we actually do any counting
  C.1 -- Initialize valid-flag, row-OK [], row-count to 0
  C.2 -- for row in reader:
  C.2.1      if row-count == 0:
  C.2.1.1       if (row[0] == "Voter ID") and (row[1] == "County") and (row[2] = "Canddiate"):
  C.2.1.1.1         row-OK.append(True)
  C.2.2.2       else:  row-OK.append(False)
  C.2.2      else:
  C.2.2.1       row-check = False
  C.2.2.2       try: 
  C.2.2.2.1         voter-ID = int(row[0]) 
  C.2.2.2.2         if len(row[1]) > 0 and len(row[2] > 0):
  C.2.2.2.2.1           row-check = True
  C.2.2.3        except ValueErorr: continue
  C.2.2.4        row-OK.append(row-check)
  C.2.3     row-count += 1
  C.3 -- if len(Row-OK.filter(True)) == len(Row-OK) == row-count:
  C.3.1     valid-flag = True -- only if every row was checked and marked True
For processing, the data structure is kept simple to keep the code 
easy to understand.  Less-known or complex Python functions are avoided. 
The elements of the data structure are kept to a minimum also.
  P.1 -- if valid-flag = True:
  P.1.1     try:  
  P.1.1.1       reader2 = csvreader(file) -- re-open file, it will close 
                at end of C
  P.1.1.2       Initialize: rows-counted = 0, total-votes = 0,
                candiate_list [], candidate_votes []
  P.1.1.3       next reader2
  P.1.1.4       for row in reader2:
  P.1.1.4.1         candidate = row[2]
  P.1.1.4.2         entry-found = False
  P.1.1.4.3         for i,entry in enumerate(candidate_list):
  P.1.1.4.3.1          if candidate == entry:
  P.1.1.4.3.1.1            candidate_votes[i] += 1
  P.1.1.4.3.1.2            entry-found = True
  P.1.1.4.3.2       if entry-found == False:
  P.1.1.4.3.2.1            candidate_list.append(candidate)
  P.1.1.4.3.2.2            candidate_votes.append(0)
  P.1.1.4.4         rows-counted += 1
  P.1.1.5       total-votes = candidate_votes.sum()
  P.1.2     except:  process-error message
  P.2 -- else:
  P.2.1     output file-error message
  for simplicity we will decouple P and W, we could do it in one big 
  loop, but that would make the script hard to follow 

  W.1 --  if valid-flag == True and rows-counted == total-votes:  (sort list and write)
          we will use a selection sort to make the method simple and
          transparent
  W.1.1       for i in range(len(candidate_list)): 
  W.1.1.1        max_index = i 
  W.1.1.2        for j in range(i+1, len(candidate_list)): 
  W.1.1.2.1         if candidate_list[j] > candidate_list[max_index]: 
  W.1.1.2.1.1            max_index = j 
  W.1.1.3        candidate_list[i], candidate_list[max_index] =
                 candidate_list[max_index] , candidate_list[i]
  W.1.1.4        candidate_votes[i], candidate_votes[max_index] =
                 candidate_votes[max_index] , candidate_votes[i]
  W.1.2       open output file for writing, use with 
  W.1.3       write header rows to terminal and file
  W.1.4       write total votes line to terminal and file, use total-votes
  W.1.5       write separator row to terminal and file
  W.1.6       for line in range(len(canidate_list)):
  W.1.6.1         write candidate name, vote total, and formatted percentage
                  (use an on the fly division)
  W.1.7       write separator row to terminal and file
  W.1.8       if candidate_votes[0] == candidate_votes[1]:
  W.1.8.1         write tie message to terminal and file
  W.1.9       else:
  W.1.9.1         write Winner + candidate_list[0] to terminal and file
  W.2 -- else:  (somehow results were not valid)
  W.2.1      output processing-error message 