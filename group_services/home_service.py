from lib.sql_handler import SQLHandlerFacade


def fetch_quiz_grades():
    query = SQLHandlerFacade('SELECT * FROM mdl_quiz_grades')
    result = query.operation()[0]
    return result


def do_something_with_user_id(user_id):
    print(f'The current user id is: {user_id}')
    data = {
        "id": user_id,
        "content": "This is just some string"
    }
    return data
