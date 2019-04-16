#!/usr/bin/env python2.7
###################################################################################################################################################
# Template written by David Cabinian and edited by Ang Deng
# dhcabinian@gatech.edu
# adeng3@gatech.edu
# Written for python 2.7
# Run python template.py --help for information.
###################################################################################################################################################
# DO NOT MODIFY THESE IMPORTS / DO NOT ADD IMPORTS IN THIS NAMESPACE
# Importing a filesystem library such as ['sys', 'os', 'shutil'] will result in loss of all homework points.
###################################################################################################################################################
import argparse
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
###################################################################################################################################################


'''
0:MovieID, 1:Title, 2:Year, 3:Duration, 4:Genre, 5:DirectorID, 6:Director, 7:Actor1, 8:Actor2,
9:BuyPrice, 10:RentPrice, 11: Count, 12:TransactionType, 13:UserID, 14:DateTime
'''
def run(args, pipeline_args):
    def Split(line):
        # split to extract each field in the .csv file
        return line.replace(', ', ' ').split(',')

    # 1
    def PairWithCopy(line):
        if(line[12]=='buy'):
            BuyCount = 1
            RentCount = 0
        else:
            BuyCount = 0
            RentCount = 1
        # MovieID, (BuyCount, RentCount)
        return (line[0], (BuyCount, RentCount))

    def Sum_Format(element):
        BuyCount = 0
        RentCount = 0
        for item in element[1]:
            BuyCount = BuyCount + int(item[0])
            RentCount = RentCount + int(item[1])
        return "{}\t{}\t{}".format(element[0], BuyCount, RentCount)

    # 2
    def PairWithRevenue(line):
        # MovieID, BuyPrice or RentPrice
        if(line[12]=='buy'):
            return (line[0], int(line[9]))
        return (line[0], int(line[10]))

    def FormatRevenue(element):
        return "{}\t{}".format(element[0], element[1])

    # 3
    def PairWithDirectorCopy(line):
        if(line[12]=='buy'):
            BuyCount = 1
            RentCount = 0
        else:
            BuyCount = 0
            RentCount = 1
        # directorID, (BuyCount, RentCount)
        return (line[5], (BuyCount, RentCount))

    # 4
    def PairWithDirectorRevenue(line):
        # DirectorID, BuyPrice or RentPrice
        if(line[12]=='buy'):
            return (line[5], int(line[9]))
        return (line[5], int(line[10]))

    # 5
    def FilterByGenre(line):
        if(line[4]==args.genre):
            return line

    infile = args.input
    outfile = args.output

    # P2
    def PairWithSamePurchase(line):
        # ((timestamp,userID), movieID)
        # (timestamp, userID) is unique for the same purchase, thus the KEY
        return ((line[13], line[14]), line[0])

    def CreateTogetherList(purchase):
        movies = purchase[1]
        movie_list = []
        for movie in movies:
            if len(movies) <= 1:
                movie_list.append(((movie, None), 0))
            else:
                for movie2 in movies:
                    if (movie2!=movie):
                        movie_list.append(((movie, movie2), 1))

        return movie_list

    def Swap(tup):
        return (tup[0][0], (tup[0][1], tup[1]))

    def AscendingSort(key_movielist):

        sorted_tuples = sorted(key_movielist[1], key=lambda x:(-x[1],x[0]))
        most_purchased_list = []
        if sorted_tuples[0][1] != 0:
            for i in range(0, len(sorted_tuples)):
                if (sorted_tuples[i][1]==sorted_tuples[0][1]):
                    most_purchased_list.append(sorted_tuples[i])
        else:
            most_purchased_list.append(('None', 0))

        # return (key_movielist[0], most_purchased_list)

        formatted = [key_movielist[0]]
        for movie in most_purchased_list:
            formatted.append(movie[0])
        formatted.append(str(most_purchased_list[0][1])) # count
        return '\t'.join(formatted)


    with beam.Pipeline(options=PipelineOptions()) as p:
        if args.genre:
            rows = (
                p |
                "Read from csv" >> beam.io.ReadFromText(args.input) |
                "Split csv" >> beam.Map(Split)|
                'Filter' >> beam.Filter(lambda line: line[4] == args.genre)
            )
        else:
            rows = (
                p |
                "Read from csv" >> beam.io.ReadFromText(args.input) |
                "Split csv" >> beam.Map(Split)
            )

        # Count and output the total number of purchased copies and total number of rentals for each movie that appears in the data set.
        if args.copies_sold:
            movie_numbers = (
                rows |
                "Pair with copy" >> beam.Map(PairWithCopy) |
                "Grouping buys" >> beam.GroupByKey() |
                "Sum and format" >> beam.Map(Sum_Format) |
                "WriteToCSV" >> WriteToText(outfile)
            )

        if args.dollars_sold:
            movie_revenue = (
                rows |
                "Pair with revenue" >> beam.Map(PairWithRevenue) |
                "Sum" >>  beam.CombinePerKey(sum) |
                "Format" >> beam.Map(FormatRevenue) |
                "WriteToCSV" >> WriteToText(outfile)
            )

        if args.director_copies_sold:
            director_numbers = (
                rows |
                "Pair with director copy" >> beam.Map(PairWithDirectorCopy) |
                "Grouping buys" >> beam.GroupByKey() |
                "Sum and format" >> beam.Map(Sum_Format) |
                "WriteToCSV" >> WriteToText(outfile)
            )

        if args.director_dollars_sold:
            director_revenue = (
                rows |
                "Pair with revenue" >> beam.Map(PairWithDirectorRevenue) |
                "Sum" >>  beam.CombinePerKey(sum) |
                "Format" >> beam.Map(FormatRevenue) |
                "WriteToCSV" >> WriteToText(outfile)
            )
        if args.purchased_together:
            movies_purchased_together = (
                rows |
                "Pair with Same Purchase" >> beam.Map(PairWithSamePurchase) |
                "Group By unique (timestamp, userID)" >> beam.GroupByKey() | # group with unique ((datetime, userID), [movie1, movie2, ...])
                "Create List of Movies Purchased Together" >> beam.FlatMap(CreateTogetherList) |
                "Count purchased together times" >> beam.CombinePerKey(sum) |
                "Swap Key" >> beam.Map(Swap) | # (movie, (other, 1))
                "Group By movies" >> beam.GroupByKey() | # (movie, [(other1, count1), (other2, count2), ...])
                "Sort" >> beam.Map(AscendingSort) |
                "WriteToCSV" >> WriteToText(outfile)
            )
    pass




###################################################################################################################################################
# DO NOT MODIFY BELOW THIS LINE
###################################################################################################################################################
if __name__ == '__main__':
    # This function will parse the required arguments for you.
    # Try template.py --help for more information
    # View https://docs.python.org/3/library/argparse.html for more information on how it works
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="ECE 6102 Assignment 3", epilog="Example Usages:\npython test.py --input small_dataset.csv --output out.csv --runner Direct --copies_sold\npython test.py --input $BUCKET/input_files/small_dataset.csv --output $BUCKET/out.csv --runner DataflowRunner --project $PROJECT --temp_location $BUCKET/tmp/ --copies_sold")
    parser.add_argument('--input', help="Input file to process.", required=True)
    parser.add_argument('--output', help="Output file to write results to.", required=True)
    parser.add_argument('--project', help="Your Google Cloud Project ID.")
    parser.add_argument('--runner', help="The runner you would like to use for the map reduce.", choices=['Direct', 'DataflowRunner'], required=True)
    parser.add_argument('--temp_location', help="Location where temporary files should be stored.")
    parser.add_argument('--num_workers', help="Set the number of workers for Google Cloud Dataflow to allocate (instead of autoallocation). Default value = 0 uses autoallocation.", default="0")
    pipelines = parser.add_mutually_exclusive_group(required=True)
    pipelines.add_argument('--copies_sold', help="Count the total number of movie purchases and rentals for each movie that has been purchased at least once and order the final result from largest to smallest count.", action='store_true')
    pipelines.add_argument('--dollars_sold', help="Calculate the total dollar amount of sales for each movie and order the final result from largest to smallest amount.", action='store_true')
    pipelines.add_argument('--director_copies_sold', help="Count the total number of number of movie purchases and rentals for each director that has had at least one movie purchased and order the final result from largest to smallest count.", action='store_true')
    pipelines.add_argument('--director_dollars_sold', help="Calculate the total dollar amount of sales for each director and order the final result from largest to smallest amount.", action='store_true')
    pipelines.add_argument('--purchased_together', help="For each movie that was purchased at least once, find the other movie that was purchased most often at the same time and count how many times the two wines were purchased together.", action='store_true')
    parser.add_argument('--genre', help="Use the genre whose first letter is the closest to the first letter of your last name. ", choices=["Action", "Animation", "Comedy", "Documentary", "Drama", "Horror", "Musical", "Sci-Fi"])
    args = parser.parse_args()

    # Separating Pipeline options from IO options
    # HINT: pipeline args go nicely into: options=PipelineOptions(pipeline_args)
    if args.runner  == "DataflowRunner":
        if None in [args.project, args.temp_location]:
            raise Exception("Missing some pipeline options.")
        pipeline_args = []
        pipeline_args.append("--runner")
        pipeline_args.append(args.runner)
        pipeline_args.append("--project")
        pipeline_args.append(args.project)
        pipeline_args.append("--temp_location")
        pipeline_args.append(args.temp_location)
        if args.num_workers != "0":
            # This disables the autoscaling if you have specified a number of workers
            pipeline_args.append("--num_workers")
            pipeline_args.append(args.num_workers)
            pipeline_args.append("--autoscaling_algorithm")
            pipeline_args.append("NONE")
    else:
        pipeline_args = []


    run(args, pipeline_args)