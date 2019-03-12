#PyBank README

Quick user info:
This script expects a CSV input data file named budget_data.csv 
inside a folder named "Resources" within the same directory as
the script.  The input file should include a header row and
two columns, the first with a month entry (reproduced as a 
string in the summary) and the second with a purely numeric
profit and loss entry (interpreted as $).

It will output a simple summary to the terminal as well as to
a CSV file named PyBank_Results.csv.  

Design doc:

Objective:  Automatically summarize profit and loss information
from the file budget_data.csv, with results displayed in both
the terminal and an output file (PyBank_Results.csv).

Rationale:  This straigtforward task is being automated to save
time (so we're going to keep it simple).

Expected input:  CSV data file with arbitrary number of rows.
The program will expect a header row, and at least two columns
of data.  The header row format will be ignored.  Column 1 
will be a label corresponding to a month.  Although this data
is typically provided in mmm-YY format, the script will simply
pass the label as a string.  The months will normally be sorted
but the script will handle unsorted data, as well as missing
months.  For these purposes, the first three letters (not case
sensitive) and last two digits in this entry will be interpreted.
Years > XX will be interpreted as 20th century, years <= XX
as 21st century, where XX is set to 50 in the script as a parameter.
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
periods reported.  The "average change" will simply take the
difference from whatever period is previously reported, 
ingoring skipped months.  The greatest increase or decrease
will show the corresponding month and amount, using whatever
the previous reporting period was as the reference, ingoring
skipped months.  If the program finds duplicated months, it
will keep only the first entry it finds.  If the script finds
a tie for the greatest increase or decrease, it will take
the earlier date as the "winner" and note the others.  If it
finds no months with an increase or decrease, this will also
be noted.  

The optional [NOTES] will simply let the user know that the 
program found that some months were skipped or duplicated
or that some lines other than the header could not be 
interpreted.  To keep it simple, more detail won't be provided. 
 The most likely cause of an error is naming the wrong file as
budget_data.csv, in which case Total Months will print 0,
total will print 0, and the remaining values will print n/a.
[NOTES] will also let the user know if there were ties in
the greatest or least values, with the corresponding months.

  Procedural Outline
R) Use csvreader to input file.  Discard header.
P) Process data by P1) sorting by date, P2) line-by-line Analysis
W) finish by writing the output table to terminal and file

  Detailed Procedures
  R.0 -- define entry-dict, set XX (year-base 19XX)
  R.1 -- import libs
  R.2 -- set path
  R.3 -- use a try: to enclose rest of R4-R5 with a EOFError except w/
         message to terminal and line in output file 
  R.4 -- create reader object (reader)
  R.5-- use next to skip header
  R.6 -- initialize month-num[], month-label[], profit-value[]
  R.7 -- for row in reader:
  R.7.1     month-label.append(row[0])
  R.7.2     profit-value.append(row[1])
  P1.1 -- call a date-interpreter function date -> number
          will make a new column that retains the month labels
          as-entered 
  P1.2 -- call a sort function on the result from P1.1
  P1.3 -- call a cut-n-fill function to regularize the list 
  P2.1 -- initialize line-by-line vars (total, avg delta, max
           delta, min delta, max delta-label, min delta-label, 
           missing-count, count), + internal (delta,sumdelta,prev-profit),
           and two strings for holing ties (max-ties and min-ties)
           max and min labels initialize to "no increase/decrease 
           found" to make the table note this situation properly.
  P2.2 -- for each row, month-label, profit-value in enumerate(regularized-list)
  P2.2.1      if profit-value is not missing then:
  P2.2.1.1          count += 1
  P2.2.1.2          total += profit-value
  P2.2.1.3          delta = profit-value - prev-profit
  P2.2.1.4          sumdelta += delta
  P2.2.1.5          if delta > max-delta then:
  P2.2.1.5.1            max-delta = delta
  P2.2.1.5.2            max-delta-label = month-label at row
  P2.2.2.5.3            max-ties = ""
  P2.2.2.6          elif  delta = max-delta then
  P2.2.2.6.1            max-ties.append(message w/ month)
  P2.2.1.7          elif delta < min-delta then:
  P2.2.1.7.1            min-delta = delta
  P2.2.1.7.2            min-delta-label = month-label at row
  P2.2.2.7.3            min-ties = ""
  P2.2.1.8          elif delta = min-delta then:
  P2.2.1.8.1            min-ties.append(message w/ month)
  P2.2.1.9          prev-profit = profit-value
  P2.2.2        else: (this happens with profit-value is missing)
  P2.2.2.1          missing-count += 1
  P2.3 -- compute average = sumdelta / count 
  W.1 -- write to terminal and file, header line
  W.2 -- write table with count, total, average
  W.3 -- if len(max-ties) > 0:
  W.3.1     write max-ties message
  W.4 -- if len(min-ties) > 0:
  W.4.1     write min-ties message
  W.5 -- if missing-count > 0:
  W.5.1     write missing-count "months with missing data found"
  W.6. -- if cut-n-fill returned an invalid-row > 0:
  W.6.1     write invalid-row "rows of unreadable data found"

  Detailed procedures for functions:

  F1.  Date interpreter function (date-list =[], entry-dict, year-base)
  """ Takes a list of month entries & entry-dict and returns two objects,
      a list of integers that allows for sorting, and a 
      count of entries it fails to interpret."""
  F1.1  iniitalize num-list [], readerrors = 0
  F1.2  base = 1900 + year-base
  F1.3  for item in date-list:
  F1.3.2    try:  month-id = entry-dict[date-list[item][0:2].lower()] 
  F1.3.3    except value/dict error:  month-id = 0
  F1.3.4    try:   year = int(date-list[item][-3:-1])
  F1.3.5    except valueerror:  year = -1
  F1.3.6    if year > year-base and month-id > 0:
  F1.3.6.1      num-list.append((year + 1900 - base)*12 + month-id)
  F1.3.7    elif year >= 0 and month-id > 0
  F1.3.7.1      num-list.append((year + 2000 - base)*12 + month-id)
  F1.3.8    else:  
  F1.3.8.1      readerrors += 1
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
 F2.1.5.2       label[pos] = label[po - 1]
 F2.1.5.3       val[pos] = val[pos - 1]
 F2.1.5.4       pos = pos - 1
 F2.1.6     arr[pos] = cursor -- second half of swap
 F2.1.7     label[pos] = tagalong1
 F2.1.8     val[pos] = tagalong2
 F2.2 -- return key, labels, val 

 F3.  "Cut-n-fill" function (key[], label[], val[]) -- cut repeats & fill gaps
      """This function requires a sorted numerical key array
         and it also returns counts of rows cut and rows gap-filled 
 F3.1 -- initialize: i = 0, cut_count = 0  -- cut part
 F3.2 -- while i < len(key):
 F3.2.1      if key[i+1] == key[i]:
 F3.2.1.1         del(key[i+1])
 F3.2.1.2         del(label[i+1])
 F3.2.1.3         del(val[i+1])
 F3.2.1.4         cut_count += 1
 F3.2.2      else: increment i
 F3.3 -- initialize i = 0, gap_count = 0, keymax = key[-1] -- gap fill, expects no dups
 F3.3 --  while key[i] < keymax: 
 F3.3.1       gap = key[i+1] - key[i] - 1
 F3.3.2       if gap > 0:
 F3.3.2.1         for count in range(0,gap,-1):
 F3.3.2.1.1           key.insert(i + 1,key[i] + gap)
 F3.3.2.2.2           label.insert(i + 1,"n/a")
 F3.3.2.2.3           val.insert(i + 1,NaN)
 F3.3.2.2.4           gap_count += 1
 F3.3.2.2.5           i += gap 
 F3.3.2       i += 1
