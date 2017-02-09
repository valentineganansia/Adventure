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
        question_id = 0
        print (username)
        sql = "SELECT username, user_id FROM Users where username='{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            print("User already there", result)
        else:
            print("else, no username")
            newUser = "INSERT INTO Users (username, question_id) VALUES ('{0}', '{1}')".format(username,
                                                                                               question_id)
            cursor.execute(newUser)
            connection.commit()
            print("new username result:",username)
    return json.dump({"username": user_name,
                       "questionId": question_id,
                        "nextquestion":nextquestion,
                       "coins": coins,
                       "life": life,
                       "option": option,

                      adventure
                       })
            # next_steps_results = [
            #     {"id": 1, "option_text": "I fight it"},
            #     {"id": 2, "option_text": "I give him 10 coins"},
            #     {"id": 3, "option_text": "I tell it that I just want to go home"},
            #     {"id": 4, "option_text": "I run away quickly"}
            #     ]

    #todo add the next step based on db
            # return json.dumps({"user": user_id,
                                # "username":username,
            #                    "questionId": question_id,
            #                    "nextQuestion": next_question_id, #is this right?????
            #                    "image": "troll.png",
            #                    "options": option_id,
            #                    })
    # except Exception as a:
    #     print(repr(a))

def UserInfo():
    with connection.cursor() as cursor:
        username = request.POST.get("username")
        sql = "SELECT * from users where '{}'".format(username)
        cursor.execute(sql)
        user_id = cursor.fetchone()
    print(user_id)
    return user_id

def Options(option_id): #I'm really not sure about this one but I don't had any error message so I think it works.
      with connection.cursor() as cursor:
        sql = "SELECT option_id from Options where question_id='{}' ORDER BY option_id ASC".format(option_id)
        cursor.execute(sql)
        print(["option_id"])
        return option_id

def nextQuestions (question_id,next_question_id):
       with connection.cursor() as cursor:
         sql = "SELECT next_question_id from options WHERE question_id='{}' and option_id='{}'".format(question_id,next_question_id)
         cursor.execute(sql)
         print(["next_question_id"])
         return question_id,next_question_id

def updateUser(coins,life,next_question_id,question_id):
       with connection.cursor() as cursor:
           sql = "UPDATE user_id SET question_id='{}',coins='{}',life='{}' WHERE user_id='{}'".format(coins,life,next_question_id,question_id)
           cursor.execute(sql)
           connection.commit()
           print(coins,life,next_question_id,question_id)

def insert_user_name(username):
      with connection.cursor() as cursor:
           sql = "INSERT INTO users(`username`) VALUES (%s)"
           cursor.execute(sql, username)
           connection.commit()

def gameOver(user_id):
      with connection.cursor() as cursor:
          end = True
          print(end)
          sql = "UPDATE Users SET question_id='{}',coins='{}',life='{}' WHERE user_id='{}'".format(10,100,user_id)
          cursor.execute(sql)
          connection.commit()
          return True

@route("/story", method="POST")
# def story():
#     user_id = request.POST.get("user")
#     question_id = request.POST.get("adventure")
#     next_question_id = request.POST.get("next") #this is what the user chose - use it!
#     option_id = [
#         {"id": 1, "option_text": "I run!"},
#         {"id": 2, "option_text": "I hide!"},
#         {"id": 3, "option_text": "I sleep!"},
#         {"id": 4, "option_text": "I fight!"}
#         ]
#     random.shuffle(next_question_id) #todo change - used only for demonstration purpouses
#
#     todo add the next step based on db
    # return json.dumps({"user": user_id,
    #                    "adventure": question_id,
    #                    "next": next_question_id,
    #                    "text":{},
    #                    "image": "choice.jpg",
    #                    "options": option_id
    #                    })

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

