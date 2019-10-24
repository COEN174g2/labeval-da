'''
This file contains code for the data analytics module
'''

from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import statistics
import nltk
import csv 
import sys

#def histogram():
#    np.histogram([1, 2, 1], bins=[0, 1, 2, 3])

def create_histogram(answer_list):
    new_histogram = np.histogram(answer_list, bins = list(range(1, num_choices)))
    plt.hist(new_histogram, bins = num_choices)
    plt.ylabel("Number of students")
    plt.xlabel("Answer choice")
    plt.show()

def calc_mean(answer_list):
    summation = 0
    for choice, num_responses in enumerate(answer_list):
        summation+=(choice+1)*num_responses
    return summation/len(answer_list)

def calc_standard_deviation(answer_list):
    list_of_responses = []
    for choice, num_responses in enumerate(answer_list):
        for i in range(num_responses):
            list_of_responses.append(choice+1)

    return round(statistics.stdev(list_of_responses),1)

def calc_median(answer_list):
    list_of_responses = []
    for choice, num_responses in enumerate(answer_list):
        for i in range(num_responses):
            list_of_responses.append(choice+1)
    return statistics.median(list_of_responses)

def calc_mode(answer_list):
    list_of_responses = []
    for choice, num_responses in enumerate(answer_list):
        for i in range(num_responses):
            list_of_responses.append(choice+1)

    most = max(list(map(list_of_responses.count, list_of_responses)))
    return list(set(filter(lambda val: list_of_responses.count(val) == most, list_of_responses)))

def numerical_metrics(): 

    for key, answer_list in question_dict.items():
        num_students_most_popular_choice = max(answer_list)
        most_popular_choice = answer_list.index(num_students_most_popular_choice) + 1 # the first answer choice starts at 1
        print("For question {}:".format(key))
        print("- Number of students choosing each numeric choice: {}".format(answer_list))
        print("- Most chosen numeric choice is {}".format(most_popular_choice))
        print("- Mean value of numeric response is {}".format(calc_mean(answer_list)))
        print("- Mode value(s) of numeric response is/are {}".format(calc_mode(answer_list)))
        print("- Median value of numeric response is {}".format(calc_median(answer_list)))
        print("- Standard deviation of numeric response is {}".format(calc_standard_deviation(answer_list)))
        print("------------------------------")
        create_histogram(answer_list)

def sentiment_analysis():

    num_positive = 0
    num_negative = 0
    num_objective = 0
    num_subjective = 0

    for key, response_list in student_dict.items():
        print("Performing sentiment analysis on textual responses from student {}".format(key))
        for index, response in enumerate(response_list):
            if not response.isnumeric(): # only perform sentiment analysis on non-numeric responses
                obj = TextBlob(response)
                polarity = obj.sentiment.polarity # a value within the range [-1.0,1.0]
                subjectivity = obj.sentiment.subjectivity # a value between [0.0,1.0]
                status = []

                if polarity == 0:
                    status.append("Neutral")
                elif polarity > 0:
                    status.append('Positive')
                    num_positive+=1
                else:
                    status.append('Negative')
                    num_negative+=1

                if subjectivity < 0.5:
                    status.append("objective")
                    num_objective+=1
                elif subjectivity > 0.5:
                    status.append("subjective")
                    num_subjective+=1

                if len(status) == 0:
                    print("Question {}: {} and {} response".format(index+1, status[0], status[1]))
                else:
                    print("Question {}: {} response".format(index+1, status[0]))                

        print("------------------------------")
    print("Total number of positive responses for all textual questions: {}".format(num_positive))
    print("Total number of negative responses for all textual questions: {}".format(num_negative))
    print("Total number of objective responses for all textual questions: {}".format(num_objective))
    print("Total number of subjective responses for all textual questions: {}".format(num_subjective))
            


def parse():
    global student_count
    with open(answers_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',', quotechar ='"', quoting = csv.QUOTE_ALL)
        next(csv_reader) # skip a row
        next(csv_reader) # skip a row
        line_count = 0

        for row in csv_reader:
            
            if line_count % num_questions == 0:
                student_count+=1
                student_dict[student_count] = [] # create an empty list to hold the student's responses
            if row[1] != '':
                student_dict[student_count].append(row[1])
                question_dict[int(row[0])] = [0]*num_choices
            else:
                student_dict[student_count].append(row[2])
            line_count+=1

        for key, response_list in student_dict.items(): # tally the responses for each numeric question
            for index, response in enumerate(response_list):
                if response.isnumeric():
                    question_dict[index+1][int(response)-1]+=1

def main():
    parse()
    print("Student dict content is: \n {}".format(student_dict))
    print("------------------------------")
    print("Student count is {}".format(student_count))
    print("------------------------------")
    print("Number of answer choices possible is {}".format(num_choices))
    print("------------------------------")
    numerical_metrics()
    sentiment_analysis()

question_dict = {}
student_dict = {} # dictionary containing lists of student responses
num_questions = 9
num_choices = 5
student_count = 0
questions_file = sys.argv[1]
answers_file = sys.argv[2]

if __name__ == '__main__':
    main()