'''
This file contains code for the data analytics module. To run: python data_analytics.py [questions.csv] [answers.csv] [output_path - optional]
'''

from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import statistics
import csv 
import sys
import math

def create_histogram(question_num, distribution_list):

    answer_list = []
    for index, val in enumerate(distribution_list):
        for i in range(val):
            answer_list.append(index+1)

    num_bins = num_choices
    lower_bound, upper_bound = 1, num_choices+1 

    y = np.asarray(answer_list)
    hist, bin_edges = np.histogram(y, num_bins, range=(lower_bound, upper_bound))
    width = bin_edges[1] - bin_edges[0]
    fig = plt.figure()
    plt.bar(bin_edges[:-1], hist, align='center', width=width*0.6, edgecolor='k', facecolor='blue', alpha=0.5)
    plt.xticks(range(num_bins+1))
    plt.yticks(range(max(distribution_list)+1))
    plt.xlim([lower_bound-width/2, upper_bound-width/2])
    plt.title("Question {}".format(question_num))
    plt.xlabel("Choice")
    plt.ylabel("Number of Students Choosing")
    plt.savefig(output_path + "histogram_question_{}".format(question_num)) # saves the figure as a file
    
def calc_mean(distribution_list):

    summation = 0
    for choice, num_responses in enumerate(distribution_list):
        summation+=(choice+1)*num_responses
    return summation/len(distribution_list)

def calc_standard_deviation(distribution_list):

    list_of_responses = []
    for choice, num_responses in enumerate(distribution_list):
        for i in range(num_responses):
            list_of_responses.append(choice+1)

    return round(statistics.stdev(list_of_responses),1)

def calc_median(distribution_list):

    list_of_responses = []
    for choice, num_responses in enumerate(distribution_list):
        for i in range(num_responses):
            list_of_responses.append(choice+1)
    return statistics.median(list_of_responses)

def calc_mode(distribution_list):

    list_of_responses = []
    for choice, num_responses in enumerate(distribution_list):
        for i in range(num_responses):
            list_of_responses.append(choice+1)

    most = max(list(map(list_of_responses.count, list_of_responses)))
    return list(set(filter(lambda val: list_of_responses.count(val) == most, list_of_responses)))

def write_csv():

    with open("analytics.csv", mode = "w", newline = '') as out_file:
        file_writer = csv.writer(out_file, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        file_writer.writerow(["MULTIPLE_CHOICE QUESTION:"])
        file_writer.writerow(["is_multiple_choice","question_number","most_popular_choice","mean","mode","median","standard_deviation"])
        file_writer.writerow(["OPEN_ENDED QUESTION:"])
        file_writer.writerow(["is_open_ended","question_number","percentage_positive_all_students", "percentage_negative_all_students", "percentage_subjective_all_students", "percentage_objective_all_students"])
        for row_number, row_content in analytics_dict.items():
            file_writer.writerow(row_content)

def numerical_metrics(): 

    for key, distribution_list in numeric_question_dict.items():
        num_students_most_popular_choice = max(distribution_list)
        most_popular_choice = distribution_list.index(num_students_most_popular_choice) + 1 # the first answer choice starts at 1
        print("For question {}:".format(key)) # included in csv file
        print("- Number of students choosing each numeric choice: {}".format(distribution_list)) 
        print("- Most chosen numeric choice is {}".format(most_popular_choice)) # included in csv file
        print("- Mean value of numeric response is {}".format(calc_mean(distribution_list))) # included in csv file
        print("- Mode value(s) of numeric response is/are {}".format(calc_mode(distribution_list))) # included in csv file
        print("- Median value of numeric response is {}".format(calc_median(distribution_list))) # included in csv file
        print("- Standard deviation of numeric response is {}".format(calc_standard_deviation(distribution_list))) # included in csv file
        print("------------------------------")
        create_histogram(key, distribution_list)

        analytics_dict[key] = []
        new_row = ["multiple_choice",key, most_popular_choice, calc_mean(distribution_list), calc_mode(distribution_list), calc_median(distribution_list), calc_standard_deviation(distribution_list)]
        analytics_dict[key].extend(new_row)

def sentiment_analysis():

    num_positive = 0
    num_negative = 0
    num_objective = 0
    num_subjective = 0
    num_neutral = 0

    num_aggregate_responses = 0

    for key, response_list in student_dict.items():
        print("Performing sentiment analysis on textual responses from student {}".format(key))
        for index, response in enumerate(response_list):
            if not response.isnumeric(): # only perform sentiment analysis on non-numeric responses

                analytics_dict[index+1] = []
                obj = TextBlob(response)
                polarity = round(obj.sentiment.polarity,1) # a value within the range [-1.0,1.0]
                subjectivity = round(obj.sentiment.subjectivity,1) # a value between [0.0,1.0]
                status = []
                num_aggregate_responses+=1

                if polarity == 0 or subjectivity == 0.5:
                    status.append("Neutral")
                    overall_sentiment = "Neutral"
                    num_neutral+=1
                    print("Question {}: {} response".format(index+1, overall_sentiment))
                    textual_question_dict[index+1].append([status[0]])     
                else:

                    if polarity > 0:
                        status.append('Positive')
                        num_positive+=1
                    elif polarity < 0:
                        status.append('Negative')
                        num_negative+=1

                    if subjectivity < 0.5:
                        status.append("Objective")
                        num_objective+=1
                    elif subjectivity > 0.5:
                        status.append("Subjective")
                        num_subjective+=1

                    overall_sentiment = "{} and {}".format(status[0], status[1])
                    print("Question {}: {} response".format(index+1, overall_sentiment))   
                    textual_question_dict[index+1].append([status[0],status[1]])      

        print("------------------------------")

    for question_id, response_sentiment_list in textual_question_dict.items():
        analytics_dict[question_id] = []
        flattened_list = [item for sublist in response_sentiment_list for item in sublist]
        percentage_positive = (flattened_list.count("Positive")/len(response_sentiment_list))*100
        percentage_negative = (flattened_list.count("Negative")/len(response_sentiment_list))*100
        percentage_objective = (flattened_list.count("Objective")/len(response_sentiment_list))*100
        percentage_subjective = (flattened_list.count("Subjective")/len(response_sentiment_list))*100
        percentage_neutral = (flattened_list.count("Neutral")/len(response_sentiment_list))*100
        new_row = ["open_ended",question_id, percentage_positive, percentage_negative, percentage_subjective, percentage_objective, percentage_neutral]
        analytics_dict[question_id].extend(new_row)
        
        # pie charts
        labels = 'Subjective', 'Objective'
        sizes = [(flattened_list.count("Subjective")/len(response_sentiment_list))*360, (flattened_list.count("Objective")/len(response_sentiment_list))*360]
        colors = ['gold', 'yellowgreen']
        explode = (0, 0.1)
        subjectivity_chart_per_question = plt.figure()
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title("Question {}: Subjectivity Chart for Student Responses".format(question_id))
        plt.savefig(output_path + "subjectivity_chart_question_{}".format(question_id)) # saves the figure as a file

        labels = 'Positive', 'Negative'
        sizes = [(flattened_list.count("Positive")/len(response_sentiment_list))*360, (flattened_list.count("Negative")/len(response_sentiment_list))*360]
        colors = ['gold', 'yellowgreen']
        explode = (0, 0.1)
        polarity_chart_per_question = plt.figure()
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title("Question {}: Polarity Chart for Student Responses".format(question_id))
        plt.axis('equal')
        plt.savefig(output_path + "polarity_chart_question_{}".format(question_id)) # saves the figure as a file

    print("Percentage of positive responses out of textual responses among all students: {}%".format((num_positive/num_aggregate_responses)*100))
    print("Percentage of negative responses out of textual responses among all students: {}%".format((num_negative/num_aggregate_responses)*100))
    print("Percentage of objective responses out of textual responses among all students: {}%".format((num_objective/num_aggregate_responses)*100))
    print("Percentage of subjective responses out of textual responses among all students: {}%".format((num_subjective/num_aggregate_responses)*100))
    print("Percentage of neutral responses out of textual responses among all students: {}%".format((num_neutral/num_aggregate_responses)*100))
    
    # pie charts
    labels = 'Subjective', 'Objective'
    sizes = [(num_subjective/num_aggregate_responses)*360, (num_objective/num_aggregate_responses)*360]
    colors = ['gold', 'yellowgreen']
    explode = (0, 0.1)
    subjectivity_chart = plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title("Subjectivity Chart for All Student Textual Responses")
    plt.savefig(output_path + "subjectivity_chart") # saves the figure as a file

    labels = 'Positive', 'Negative'
    sizes = [(num_positive/num_aggregate_responses)*360, (num_negative/num_aggregate_responses)*360]
    colors = ['gold', 'yellowgreen']
    explode = (0, 0.1)
    polarity_chart = plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Polarity Chart for All Student Textual Responses')
    plt.axis('equal')
    plt.savefig(output_path + "polarity_chart") # saves the figure as a file
            
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
                numeric_question_dict[int(row[0])] = [0]*num_choices
            else:
                student_dict[student_count].append(row[2])
            line_count+=1

        for key, response_list in student_dict.items(): # tally the responses for each numeric question
            for index, response in enumerate(response_list):
                if response.isnumeric():
                    numeric_question_dict[index+1][int(response)-1]+=1
                else:
                    textual_question_dict[index+1] = []


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
    write_csv()

analytics_dict = {} # processed results in the form of a dictionary for output to csv
numeric_question_dict = {} # containing responses for each numeric question
textual_question_dict = {} # containing question ID used as dummy holder for each textual question
student_dict = {} # dictionary containing lists of student responses

num_questions = 9
num_choices = 5
student_count = 0
output_path = ""

questions_file = sys.argv[1]
answers_file = sys.argv[2]
if len(sys.argv) > 3:
    output_path = sys.argv[3]

#hard coded values indicating if this is text or numeric

if __name__ == '__main__':
    main()
    plt.show() # show all the figures