import json
from lib.sql_handler import SQLHandlerFacade
import pandas as pd


# #########################################
# Fetching data and pass them to frontend #
# #########################################

def operation(user_id) -> dict:
        """
          Returns a list of quiz and assumption grades and pass them to the frontend.
                  Parameters:
                          ! current_user (int): the logged-in user can be added as a parameter.
                  Returns:
                          list_df (dict): Values of grades as new dictionary
                          initialized from a mapping object's (key, value) pairs.
        """
        # logged in user
        current_user = 181
        #current_user = int(user_id)-2
        #print(current_user)
        
        # handler = SQLHandlerFacade(app=self.app, query="SELECT * FROM mdl_quiz_grades")
        # operation_result, quiz_grades_df = handler.operation()

        assign_grades_df = pd.read_csv('mdl_assign_grades.csv',
                                       on_bad_lines='skip', encoding='utf-8')
        quiz_grades_df = pd.read_csv('mdl_quiz_grades.csv',
                                     on_bad_lines='skip', encoding='utf-8')

        # Work with pandas.

        # convert the grade type to float
        quiz_grades_df.grade = quiz_grades_df.grade.astype(float)
        quiz_grades_df['grade'] = quiz_grades_df['grade'].fillna(.0).astype(float)

        # display the panda file as float .0
        pd.options.display.float_format = '{:,.0f}'.format

        # changing the values of quiz names
        quiz_grades_df['quiz'] = quiz_grades_df['quiz'].replace(
            {37: 'quiz 1', 38: 'quiz 2', 39: 'quiz 3', 40: 'quiz 4', 41: 'quiz 5', 42: 'quiz 6', 43: 'quiz final',
             -1: 0, 'Null': 0})

        # eliminating invalid values
        quiz_grades_df['grade'] = quiz_grades_df['grade'].replace({-1: 0, 'Null': 0})

        # specifying the current user data for grades
        quiz_grades_df_edited = quiz_grades_df.loc[quiz_grades_df['userid'] == current_user]

        # normalizing the values of the Graph(lazy way)
        quiz1nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 1', 'grade']
        quiz2nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 2', 'grade']
        quiz4nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 4', 'grade']
        quiz6nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 6', 'grade']

        quiz1_changed_value = ((quiz1nor - 0) / (3 - 0)) * 10
        quiz2_changed_value = ((quiz2nor - 0) / (4 - 0)) * 10
        quiz4_changed_value = ((quiz4nor - 0) / (3 - 0)) * 10
        quiz6_changed_value = ((quiz6nor - 0) / (3 - 0)) * 10

        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 1', 'grade'] = quiz1_changed_value
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 2', 'grade'] = quiz2_changed_value
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 4', 'grade'] = quiz4_changed_value
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 6', 'grade'] = quiz6_changed_value

        # changing the values of assignment
        assign_grades_df['assignment'] = assign_grades_df['assignment'].replace(
            {27: 'AS1 - W3', 28: 'AS2 - W5', 30: 'AS3 - W10', 31: 'AS4 - W11', -1: 0, 'Null': 0})

        assign_grades_df['grade'] = assign_grades_df['grade'].replace({-1: 0, 'Null': 0})

        # specifying current user data for assignment
        assign_edited = assign_grades_df.loc[assign_grades_df['userid'] == current_user]

        # Work with json data.
        # converting quiz grades to json data
        user_quiz_grades = quiz_grades_df_edited.to_json(orient="columns")

        # converting assign grades to json data
        user_assign_grades = assign_edited.to_json(orient="columns")

        # combined both data frames in a list
        list_df = [user_quiz_grades, user_assign_grades]

        # convert a subset of Python objects into a json string. (can be used later)
        json_data = json.dumps(list_df)

        return list_df