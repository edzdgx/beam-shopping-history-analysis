python -m template --input movie_dataset.csv --output movie_numbers.csv --runner Direct --copies_sold
python -m template --input movie_dataset.csv --output movie_revenue.csv --runner Direct --dollars_sold
python -m template --input movie_dataset.csv --output director_numbers.csv --runner Direct --director_copies_sold
python -m template --input movie_dataset.csv --output director_revenue.csv --runner Direct --director_dollars_sold
python -m template --input movie_dataset.csv --output Action_numbers.csv --runner Direct --copies_sold --genre Action
python -m template --input movie_dataset.csv --output Action_revenue.csv --runner Direct --dollars_sold --genre Action
python -m template --input movie_dataset.csv --output Action_director_numbers.csv --runner Direct --director_copies_sold --genre Action
python -m template --input movie_dataset.csv --output Action_director_revenue.csv --runner Direct --director_dollars_sold --genre Action
python -m template --input movie_dataset.csv --output most_purchased_rented_together.csv --runner Direct --purchased_together

0:MovieID, 1:Title, 2:Year, 3:Duration, 4:Genre, 5:DirectorID, 6:Director, 7:Actor1, 8:Actor2, 9:BuyPrice, 10:RentPrice, 11: Count, 12:TransactionType, 13:UserID, 14:DateTime

Main Idea
In this assignment, you will use Google Cloud Dataflow pipelines to analyze purchasing and rental data generated from a movie store that is similar to the one you developed in Assignment 2. The data is stored in a csv file with one purchased or rented movie per line. The file can be downloaded from the link provided in the "Resources" section of this assignment below.

A line in the file includes information about the movie, quantity bought or rented (always 1), type of transaction ("rent" or "buy"), user ID of individual who made the transaction, and transaction date and time. The movie information includes a unique ID for the movie, title, year of release, duration, genre, a unique ID for the director, director's name, main actor 1 (possibly blank), main actor 2 (possibly blank), buy price, and rent price. On this data set, you will carry out a variety of analyses, which are described below.

Part 1
Write Dataflow piplines to implement the following analyses and run them in Google Cloud:

1. Count and output the total number of purchased copies and total number of rentals for each movie that appears in the data set. Each movie has a unique ID, which can be matched to identify that two different transactions involve the same movie. Make sure to calculate and output 0 in the appropriate field if a movie was rented but never sold or vice versa.
2. Calculate and output the total revenue for each movie. Again, use the movie ID to match movies to generate this data.
3. Count and output the total number of purchased copies and total number of rentals for each director that appears in the data set.
4. Calculate and output the total revenue for each director. Match directors' names as discussed in Item 3.
5. Repeat Items 1-4 for one of the following genres: 
  Action
  Comedy
  Documentary
  Horror
  Musical
  Sci-Fi

Each analysis result should be in a single csv file (i.e. 8 csv files total should be turned in) labeled in the manner of the template's arguments with the following formats. csv format should be \t separated (tab separated). There should be no headers in any of the files (e.g. NO "Movie Index \t Copies Sold \t Copies Rented" on the first line):
movie_numbers.csv: <movie_index>  \t  <copies_sold>  \t  <copies_rented>
movie_revenue.csv: <movie_index>  \t  <movie_total_dollars>
director_numbers.csv: <director_ID>  \t  <copies_sold >  \t  <copies_rented>
director_revenue.csv: <director_ID>  \t  <director_total_dollars>
<genre>_numbers.csv: <movie_index>  \t  <copies_sold>  \t  <copies_rented>
<genre>_revenue.csv: <movie_index>  \t  <movie_total_dollars>
<genre>_director_numbers.csv: <director_ID>  \t  <copies_sold >  \t  <copies_rented>
<genre>_director_revenue.csv: <director_ID>  \t  <director_total_dollars>

Part 2
For each movie that was purchased or rented at least once, find the other movie that was most often purchased or rented at the same time and count how many times the two movies were part of the same transaction. Note that one transaction involving multiple movies is entered as multiple lines in the data set. Movies purchased or rented in the same transaction have matching dates, times, and user IDs.

Notes:

The standard format of a line in the output file is: <movie_index_1>   \t   <movie_index_2>   \t   <times_purchased_rented_together>
Each movie purchased or rented at least once should appear exactly once as <movie_index_1> in the csv file
As in Part 1, there should be no headers in the csv file
If a movie was never purchased or rented with another movie, the output should show <movie_index_1> followed by "\t  None  \t  0"
If a movie was purchased or rented together the same number of times with multiple other movies and all are the largest number, the output should show: <movie_index_1>   \t   <movie_index_2>   \t   <movie_index_3>  \t  ...  \t   <times_purchased_rented_together>. The list of movies following <movie_index_1> must be in sorted ascending numerical order in this case. Essentially, concatenate the movies in ascending numerical order that share the max number of times purchased or rented together with <movie_index_1> 

Example: If A is purchased together 10 times each with B and C and 10 is the largest "purchased-rented-together" value, then the output for A would look like: "A   \t   B   \t   C   \t   10", where B and C are in sorted order by movie ID
