#PyBank README

Quick user info:
This script expects a CSV input data file named election_data.csv 
inside a folder named "Resources" within the same directory as
the script.  The input file should include a header row and
3 columns, the first with a voter ID, the second with a county name,
and the third with an election candidate name.

It will output a simple vote summary to the terminal as well as to
a CSV file named PyPoll_results.csv.  

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
be an ID number (just digits, no minus signs or decimals).
Column 2 will be a county name and Column 3 will be a candidate name
(any non-empty value is OK). For this script, we will be very strict 
about errors.  If the script encounters an error in the form of:
1) a non-numeric voter ID, 2) no county entered, or 3) no candidate
name listed, it will output an error message, rather than "provisional"
data, and in fact it will not execute any algorithm that could
generate any kind of vote count data unless the input data is 
formatted perfectly.  (It is important that this script avoid
even the appearance of trying to "interpret" votes.)  


Expected output:
The output will be strictly controlled, in both terminal and
PyPoll_results.txt files.  If no errors are found, it will look
like the following example:  

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

If an error is found, it will generate one of the follwing
general messages.

There was an error opening the input file.  No results computed.

An unexpected event stopped the file check from running.  No results computed.

The file check encountered an anomaly.  No results computed.

An anomaly in data processing occurred.  Results have not been reported.


"Total Votes" will provide the sum of all votes in the table.
The next section will provide the name, percentage, and vote total
for all candidates with votes.

The final row will either state the candidate name with the most
votes if no tie is encountered, or state that a tie occurred.


  Procedural Outline
R) Use csvreader to test opening the file and creating the
reader object.  The use of open files will be kept to the minimum
required.  
C) Check file for valid data, proceed only if all data is valid
(even the data we don't use directly).  Due to the sensitive 
and public nature of the analysis, the underlying assumption
is that if anything at all is amiss or unexpected, it is better
not to proceed than to make an assumption about what is "OK to ignore".
P) Process data by reading file line by line and building a results list.
Check that every line of the file was analyzed.  Use simple data forms
and methods to make the code easy to understand.  Thoroughly check
that the process behaved exactly as intended before proceeding  
W) finish by writing the output table to terminal and file

  Detailed Procedures
  R.1 -- import libs
  R.2 -- set input and output paths 
  R.3 -- initialize:  ok-to-proceed = false
  R.3 -- try: open file and set reader
  R.3.1    ok-to-proceed = true 
  R.4 -- except OSError: write error message to terminal & file
  C -- If ok-to-proceed == true:  (else: write error message)
  C.1 -- Initialize valid-flag = false, row-ok = [], row-count = 0
  C.2 -- open file, make reader, for row in reader:
  C.2.1      if row-count == 0:  (check for correct header)
  C.2.1.1       if (row[0] == "Voter ID") and (row[1] == "County") and (row[2] = "Canddiate")::
  C.2.1.1.1         row-OK.append(True)
  C.2.2.2       else:  row-OK.append(False)
  C.2.2      else:
  C.2.2.1       row-check = False
  C.2.2.2       try: 
  C.2.2.2.1         if int(row[0]) >= 0 and len(row[1]) > 0 and len(row[2]) > 0:
  C.2.2.2.1.1           row-check = True
  C.2.2.3        except ValueErorr or IndexError: pass
  C.2.2.4        row-OK.append(row-check)
  C.2.3     row-count += 1 (count every row actually read, don't just infer)
  C.3 -- if len(Row-OK.count(True)) == len(Row-OK) == row-count:
  C.3.1     valid-flag = True -- only if each and every row was checked and marked True
  C.4 -- ok-to-proceed = valid-flag 
The tallying process will sacrifice efficiency for checking and 
re-checking everything (in classic bureaucratic fashion) 
  P. -- if ok-to-proceed == True:    (else:  write error message)
  P.1 -- initialize header-scanned = False, votes-counted, total-votes, rows-counted = 0
         candidate-list, candidate-votes = []
  P.2    open file and generate reader object 
  P.3    for row in reader2:
  P.3.1	      if rows-counted == 0:  (this will be for the header and first valid vote) 
  P.3.1.1        if header-scanned == False: (do this only once, the first time through)
  P.3.1.1.1           header-scanned = True  (confirm that a header was scanned) 
  P.3.1.2        else:   
  P.3.1.2.1           candidate = row[2]  
  P.3.1.2.2           candidate-list.append(candidate) (this will be the first one)
  P.3.1.2.3           candidate-votes.append(1)
  P.3.1.2.4           total-votes += 1 (always do this when we add a vote)
  P.3.1.2.5           rows-counted += 1 (always do this when we go through a row)
  P.3.2       else: (for the third and continuing rows)  
  P.3.2.1         candidate = row[2]
  P.3.2.2         rows-counted += 1
  P.3.2.3         entry-found = False
  P.3.2.4         for i,entry in enumerate(candidate-list): (check list)
  P.3.2.4.1           if candidate == entry: (then add to list)
  P.3.2.4.1.1              candidate-votes[i] += 1
  P.3.2.4.1.2              total-votes += 1
  P.3.2.4.1.3              entry-found = True
  P.3.2.4.2           if entry-found == False:
  P.3.2.4.2.1              candidate-list.append(candidate)
  P.3.2.4.2.2              candidate-votes.append(1)
  P.3.2.4.2.3              total-votes += 1
  P.4 -- if rows-counted == total-votes == sum(candidate-votes) == row-count - 1:
  P.4.1         ok-to-proceed = True
  P.5 -- else:       ok-to-procee = False
   (this is a stringent test, total-votes counts how many times a vote was added in
    code, sum(candidate-votes) checks that it really adds up to the total (i.e. the
    code works as it should), rows-counted double-checks that every time we intended to
    count a vote, we did (again, code works as it should), row-count enables us to 
    compare this to the expected characteristics of the file)

  W.  -- if ok-to-proceed = True -- else: write error message
  W.1 -- selection-sort -- this was chosen because although not efficient
for long lists, if someone asks, "how exactly is the winner of the election determined?"
we want to be able to explain every detail with ease.  
        for i in range(len(candidate-list)): 
  W.1.1     max-index = i 
  W.1.2     for j in range(i+1, len(candidate_list)): 
  W.1.2.1        if candidate-votes[j] > candidate-votes[max-index] 
  W.1.2.1.1            max-index = j 
  W.1.2.2        candidate-list[i], candidate-list[max_index] =
                 candidate-list[max_index] , candidate-list[i]
  W.1.2.3        candidate-votes[i], candidate-votes[max_index] =
                 candidate-votes[max_index] , candidate-votes[i]
  W.2 -- open output file for writing -- all writes will be terminal & fiile
  W.3 -- write header rows 
  W.4 -- write total votes line 
  W.5 -- write separator row 
  W.6 -- for i, candidate-name in enumerate(candidate-list):
  W.6.1        write candidate-name, percentage, and votes
                  (use an on the fly computation)
  W.7 -- write separator row 
  W.8 -- if candidate_votes[0] == candidate_votes[1]: (there's a tie)
  W.8.1      write tie message to terminal and file
  W.9 -- else:
  W.9.1      write Winner + candidate_list[0]  
