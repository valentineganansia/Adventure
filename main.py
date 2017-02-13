from bottle import route, run, template, static_file, request
import random
import json
import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com', user='sql11157852', password='3CCGQMva6k',db='sql11157852', charset='utf8', cursorclass = pymysql.cursors.DictCursor)

@route("/", method="GET")
def index():
    return template("adventure.html")

@route("/start", method="POST")
def start(): #I just change everything here Olivia.

    with connection.cursor() as cursor:

        username = request.POST.get("username")
        question_id = request.POST.get("question_id")
        user_id = 0
        print (username)
        sql = "SELECT username, user_id FROM Users where username='{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            print("User already exists in database")
        else:
            print("Adding user to database")
            newUser = "INSERT INTO Users (username, question_id) VALUES ('{0}', '{1}')".format(username,question_id)
            cursor.execute(newUser)
            connection.commit()
            print("new username result:",username)
        question = get_question_text(question_id)
        list_of_options = get_Option_text(question_id)
        optionId = get_Option_ID(question_id)

        # next_q_id = nextQuestions(optionId)
        picture = get_picture(question_id)
    return json.dumps({'username': username,
                       'questionId': question_id,
                       'question_text':question,
                       'options': list_of_options,
                       "picture": picture,
                       # "next_question_id": next_q_id,
                       "optionId": optionId
                    })

def UserInfo():
    with connection.cursor() as cursor:
        username = request.POST.get("username")
        sql = "SELECT * from users where '{}'".format(username)
        cursor.execute(sql)
        user_id = cursor.fetchone()
    print(user_id)
    return user_id

def get_Option_text(question_id):
      with connection.cursor() as cursor:
        sql = "SELECT option_text from Options where question_id='{}' ORDER BY option_id ASC".format(question_id)
        cursor.execute(sql)
        result = cursor.fetchall() # now have option_id set to result (in the format as a list of dictionaries. 4 dicts with one element in each)
        print(result)
        return result

def get_Option_ID(question_id):
    with connection.cursor() as cursor:
        sql = "SELECT option_id from Options where question_id='{}' ORDER BY option_id ASC".format(question_id)
        cursor.execute(sql)
        result = cursor.fetchall()  # now have option_id set to result (in the format as a list of dictionaries. 4 dicts with one element in each)
        print(result)
        return result

def get_question_text(question_id):
    with connection.cursor() as cursor:
        sql = "SELECT question_text FROM Questions WHERE question_id={}".format(question_id)
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchone()
        return result["question_text"]


def nextQuestions (option_id):
    with connection.cursor() as cursor:
        sql = "SELECT next_question_id FROM Options WHERE option_id='{}'".format(option_id)
        print(sql)

        cursor.execute(sql)
        result = cursor.fetchall()
        print("next_question_id")#with or without brackets ?
        return result[0]["next_question_id"] #this will return the integer value of the next question id

def updateUser(coins,life,next_question_id,question_id):
    with connection.cursor() as cursor:
        sql = "UPDATE user_id SET question_id='{}',coins='{}',life='{}' WHERE user_id='{}'".format(coins,life,next_question_id,question_id)
        cursor.execute(sql)
        connection.commit()
        return coins,life,next_question_id,question_id #is this what should be returned?

def getCoinsAndLife(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT coins, life from Users WHERE user_id='{}' ".format(user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0]["coins"], result[1]["life"] #will this work?

def insert_user_name(username):
    with connection.cursor() as cursor:
        sql = "INSERT INTO users(`username`) VALUES (%s)"
        cursor.execute(sql, username)
        connection.commit()
        return insert_user_name()

def gameOver(user_id):
    with connection.cursor() as cursor:
        end = True
        print(end)
        sql = "UPDATE Users SET question_id='{}',coins='{}',life='{}' WHERE user_id='{}'".format(10,100,user_id)
        cursor.execute(sql)
        connection.commit()
        return True

def knowTheOptions (question_id, option_id,option_text):
    with connection.cursor() as cursor:
        sql = "select question_id, option_text from options WHERE option_id = '{}' AND question_id ='{}'AND option_text='{}'".format(question_id, option_id,option_text)
        cursor.execute(sql)
        result = cursor.fetchall() #this returns a list of dictionaries: we want to convert them to their values--how to do this for multiple key-value pairs?
        return result

def get_picture(question_id):
    with connection.cursor() as cursor:
        sql="SELECT picture FROM Questions WHERE question_id='{}'".format(question_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result[0]["picture"] #get the resulting picture as the string of the selected image


@route("/story", method="POST")

def story():
    user_id = request.POST.get("username") #what are these POST requests doing? Necessary if we are getting the info from functions?
    option_id = request.POST.get("next") #this is what the user chose - use it!

    user_id_recieved = UserInfo()
    next_question_id = nextQuestions(question_id, option_id)
    next_options = get_Option_text(next_question_id) #list of 4 dicts

    coin, life = getCoinsAndLife(user_id)
    picture_selected = get_picture(question_id)


    return json.dumps({"username": user_id_recieved,
                       "questionId": question_id,
                       "nextquestion": next_question_id,
                       "options": next_options,
                       "picture":picture_selected
                       })

 # except:

 # return json.dumps({'error': 'something is wrong with the DB})



@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=8005)

if __name__ == '__main__':
    main()

