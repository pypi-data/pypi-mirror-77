#importing the necessary libraries
import pandas as pd
from pandas_profiling import ProfileReport

class xplore:
    def __init__(self, data):
        #writing the pop-up vscode  guide as a block comment
        '''
        xplore is a python package built with pandas for light-weight python projects in data science and analytics, AI and ML.\n
        The xplore() function takes the argument of whatever variable assigned to the read file path/url of a labelled dataset.\n
        xplore converts the labelled dataset to a DataFrame and performs some predefined exploratory data analysis on the dataset.
        '''
        #converting the structured data to a dataframe
        data = pd.DataFrame(data)
        print('------------------------------------')
        print('The fist 5 entries of your dataset are:\n')
        print(data.head()) #printing the first 5 entries of the dataset
        print('\n')

        print('------------------------------------')
        print('The last 5 entries of your dataset are:\n')
        print(data.tail()) #printing the last 5 entries of the dataset
        print('\n')

        print('------------------------------------')
        print('Stats on your dataset:\n')
        print(data.describe) #printing a descriptipn of the dataset
        print('\n')

        print('------------------------------------')
        print('The Value types of each column are:\n')
        print(data.dtypes) #printing value types of each column
        print('\n')

        print('------------------------------------')
        print('Info on your Dataset:\n')
        print(data.info) #printing value types of each column
        print('\n')

        print('------------------------------------')
        print('The shape of your dataset in the order of rows and columns is:\n')
        print(data.shape) #printing the shape of the dataset
        print('\n')

        print('------------------------------------')
        print('The features of your dataset are:\n')
        print(data.columns) #printing features
        print('\n')

        print('------------------------------------')
        print('The total number of null values from individual columns of your data set are:\n')
        print(data.isnull().sum()) #printing the total number of null values in the dataset
        print('\n')

        print('------------------------------------')
        print('The number of rows in your dataset are:\n')
        print(len(data)) #printing number of rows
        print('\n')

        print('------------------------------------')
        print('The values in your dataset are:\n')
        print(data.values) #printing values
        print('\n')
    
        print('------------------------------------')
        print('\n')
        print('Do you want to generate a detailed report on the exploration of your dataset?')
        response = input('[y/n]: ').lower()

        if response == 'y' or response == 'yes':
            print("Generating report...", '\n')
            prof = ProfileReport(data)
            prof.to_file(output_file='output.html')
            print('Your Report has been generated and saved as \'output.html\'')

        elif response == 'n' or response == 'no':

            print('Process Completed')

        else:
            print('Process Completed')

#df = pd.read_csv('tests/fifa_ranking.csv')
#xplore(df)
