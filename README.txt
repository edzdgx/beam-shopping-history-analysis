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