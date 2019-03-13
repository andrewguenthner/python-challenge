#PyBank README

Quick user info:
This script expects a CSV input data file named budget_data.csv 
inside a folder named "Resources" within the same directory as
the script.  The input file should include a header row and
two columns, the first with a month entry (reproduced as a 
string in the summary) and the second with a purely numeric
profit and loss entry (interpreted as $).

It will output a simple summary to the terminal as well as to
a text file named PyBank_Results.txt.  

Design doc:

Objective:  Automatically summarize profit and loss information
from the file budget_data.csv, with results displayed in both
the terminal and an output file (PyBank_resultx.txt).

Rationale:  This straigtforward task is being automated to save
time (so we're going to keep it simple).

Expected input:  CSV data file with arbitrary number of rows.
The program will expect a header row, and at least two columns
of data.  The header row format will be ignored.  Column 1 
will be a label corresponding to a month.  Although this data
is typically provided in mmm-YYYY format, the script will simply
pass the label as a string.  The months will normally be sorted
but the script will sort the data to ensure the sequential changes
have been calculated correctly.  If there are duplicate months,
the second and subsequent occurrences will be ignored.  If there
are missing months, the script will still compute and compare
sequential changes.  In both duplicate and missing month cases,
the script will just inform the user of the number of duplicates
and missing months it noticed.  

Column 2 will contain a number listing profit (positive) or loss 
(negative) for the indicated month.  Typically, this entry will
be an unformatted integer representing a dollar amount, but
the script will accept any number.  

Expected output:
Both terminal and file output will be identical.  The output will
consist of a simple table with header, in the following example
format:

  Financial Analysis
  ----------------------------
  Total Months: 86
  Total: $38382578
  Average  Change: $-2315.12
  Greatest Increase in Profits: Feb-2012 ($1926159)
  Greatest Decrease in Profits: Sep-2013 ($-2196167)
  [NOTES]

Total Months will give the total number of months reported.
Total will show in $, the total net profit or loss for all 
periods reported.  The "change" funtions will simply take the
difference from whatever the previous month in the data was, 
ingoring skipped months.  The greatest increase or decrease
will show the corresponding month and amount. If the script finds
a tie for the greatest increase or decrease, it will take
the earlier date as the "winner" and note the others.  If it
finds no months with an increase or decrease, this will also
be noted.  

The optional [NOTES] will simply let the user know that the 
program found that some months were skipped or duplicated
or that some lines other than the header could not be 
interpreted.  To keep it simple, just the total number of
each type of error will be noted.  

  Procedural Outline
R) Use csvreader to input file.  Discard header.
P) Process data by P1) sorting by date, P2) line-by-line Analysis
W) finish by writing the output table to terminal and file

  Detailed Procedures

  0 -- import dependencies and define constants (months dictionary)

Main program:
Reader part:
  R.1 -- set paths
  R.2 -- input-success = False
  R.3 -- try:  (rest of R, except OSError: write error message)
  R.4 -- with open(file), create reader object (reader)
  R.5 -- use next to skip header
  R.6 -- initialize month-num[], month-label[], profit-value[]
  R.7 -- for row in reader:
  R.7.1     month-label.append(row[0])
  R.7.2     profit-value.append(float(row[1]))
Process part (P):  if input-success == True:
  P1 (pre-process)
  P1.1 -- initialize -- bad-rows = 0, extras = 0, gaps = 0
  P1.1 -- call F1 (month-label, entry-dict) to generate the index
  P1.2 -- call F2 (month-index, month-label, profit-value) to sort 
  P1.3 -- call F3 (month-index, month-label, profit-value) to clean up
          The call returns variables extras and gaps as counts
  At this point, we have month-index as a sorted integer array with
  no duplicates, month-label and profit-value as corresponing item lists

  P2 (process)  if len(mont-num) > 0:  (else: write error message, no data)
  P2.1 -- initialize, pl-total = 0, pl-average-delta = 0, max-delta = 0,
          min-delta = 0, pl-delta = 0, max-delta-label = "None found..",
          min-delta-label = "None found...", max-ties = "", min-ties = ""
  These are set up so if there is only one row of data, they default
  to the way that they should be reported 
  P2.2 -- pl_total = sum(profit-value) -- we could have done this at 
  initialization but it just makes the code simpler to follow to 
  have it in the "compute" section
  P2.3 -- if len(profit-value) > 1: 
  P2.3.1      pl-average-delta = (profit-value[-1] - profit-value[0]) /
              (len(proft-value) - 1) -- a handy calculus shortcut
  P2.4 -- if len(month-num) > 1:  ("change" requires 2 or more entries)
  P2.4.1      for i, label in enumerate(month-num):
  P2.4.1.1        if i > 0:  skip the first month  
  P2.4.1.1.1          pl-delta = profit-value[i] - profit-value[i-1]
  P2.4.1.1.2          if pl-delta > max-delta:
  P2.4.1.1.2.1            max-delta = pl-delta
  P2.4.1.1.2.2            max-delta-label = label
  P2.4.1.1.2.3            max-ties = "" (kill the list of ties)
  P2.4.1.1.3           elif pl-delta == max-delta:
  P2.4.1.1.3.1            max-ties += label + " " (append the month label)
  P2.4.1.1.4          if pl-delta < min-delta:
  P2.4.1.1.4.1            min-delta = pl-delta
  P2.4.1.1.4.2            min-delta-label = label
  P2.4.1.1.4.3            min-ties = "" (kill the list of ties)
  P2.4.1.1.5           elif pl-delta == min-delta:
  P2.4.1.1.5.1            min-ties += label + " " (append the month label)

Write output -- this is still inside the if branches for input-success 
and len(month-num) > 0 
  W.1 -- write to terminal and file, header line
  W.2 -- write table with count, total, average
  W.3 -- if len(max-ties) > 0:
  W.3.1     write max-ties message
  W.4 -- if len(min-ties) > 0:
  W.4.1     write min-ties message
  W.5 -- if bad-rows > 0:
  W.5.1      write number of bad rows found in message
  W.6 -- if extras > 0:
  W.6.1      write number of duplicated rows in message
  W.7 -- if gaps > 0:
  W.7.1      write number of gaps in message 


  Detailed procedures for functions:

  F1.  Date interpreter function (date-list =[], entry-dict)
  """ Takes a list of month entries & entry-dict and returns two objects,
      a list of integers that allows for sorting, and a 
      count of entries it fails to interpret."""
  F1.1  iniitalize num-list [], readerrors = 0
  F1.3  for item in date-list:
  F1.3.1    use get to return the corresponding month # from dictionary,
            or 0 if no matching entry found, ignore case, use 
	    str(date-list[0:3]).lower() as input to get funciton
  F1.3.2    try:   year = int(date-list[item][-3:-1])
  F1.3.3    except valueerror:  year = -1
  F1.3.4    if month > 0 and year >= 0:
  F1.3.4.1      num-list.append(year  *12 + month)
  F1.3.5    else:  
  F1.3.5.1      readerrors += 1
  F1.3.5.2      num-list.append(0)
  F1.4  return num-list, readerrors 

  F2.  Insertion-type sort function (key[], label[], val[]) -- we'll do this type 
       of sort because we expect the list to be already sorted, we just
       want to check, and this will be quick andd simple in that case. 
       The lists are <1000 items, so in the unlikely event they aren't 
       sorted the time penalty will not be signifiant.  Because other
       lists are along for the ride, the python sort method was not used.  
        
 F2.1 -- for i in range(len(key)):
 F2.1.1     cursor = key[i]
 F2.1.2     tagalong1 = label[i]
 F2.1.3     tagalong2 = val[i]
 F2.1.4     pos = i
 F2.1.5     while pos > 0 and key[pos - 1] > cursor:
 F2.1.5.1       key[pos] = key[pos - 1]
 F2.1.5.2       label[pos] = label[pos - 1]
 F2.1.5.3       val[pos] = val[pos - 1]
 F2.1.5.4       pos = pos - 1
 F2.1.6     key[pos] = cursor -- second half of swap
 F2.1.7     label[pos] = tagalong1
 F2.1.8     val[pos] = tagalong2
 F2.2 -- return key, labels, val 

 F3.  "Clean up" function (key[], label[], val[]) 
      """This function requires a sorted numerical key array.
	 It deletes any rows with a key of 0 or duplicate keys.
         It also returns counts of duplicates and gaps in the key index.
 F3.1 -- initialize: i = 0, cut_count = 0, gap-count = 0
 F3.2 -- while i < len(key) - 1:
 F3.2.1      if key[i] == 0:
 F3.2.1.1         del key[i]
 F3.2.1.2         del label[i]
 F3.2.1.3         del val[i]
 F3.2.2      elif key[i+1] == key[i]:
 F3.2.2.1         del(key[i+1])
 F3.2.2.2         del(label[i+1])
 F3.2.2.3         del(val[i+1])
 F3.2.2.4         cut_count += 1
 F3.2.2      else: i += 1
 F3.3 -- if len(key) > 0:   (do the gap count if there's data left)
 F3.3.1      gap-count = key[-1] - key[0] - len(key) + 1 
             This works because at this point we have a list with
             sorted integers and no duplicates.  
 F3.4 -- return key, label, val, cut-count, gap-count 
