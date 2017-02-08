from bottle import route, run, template, static_file, request
import random
import json
import pymysql
connection = pymysql.connect(host='sql11.freesqldatabase.com', user='sql11157852', password='3CCGQMva6k',db='sql11157852', charset='utf8', cursorclass = pymysql.cursors.DictCursor)

@route("/", method="GET")
def index():
    return template("adventure.html")

@route("/start", method="POST")
def start():
    try:
        with connection.cursor() as cursor:
            username = request.POST.get("name")
            current_adv_id = request.POST.get("adventure_id")
            user_id = 0
            current_story_id = 0

            sql = "SELECT name, id, current_step, adventure_id FROM userinfo"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("cursor result:", result)

            for item in result:
                if item["name"] == username:

                    sql1 = "SELECT adventure_id FROM userinfo WHERE name = '{}'".format(username)
                    cursor.execute(sql1)
                    user_adventures = cursor.fetchall()

                    for info in user_adventures:
                        if {"adventure_id": current_adv_id} == info:
                            add_new_adventure = "INSERT INTO userinfo (name, current_step, adventure_id) VALUES ('{0}', '{1}', '{2}')".format(username, current_story_id, current_adv_id)
                            cursor.execute(add_new_adventure)
                            connection.commit()

                    else:
                        sql2 = "SELECT adventure_id, current_step, id FROM userinfo WHERE name = '{}'".format(username)
                        cursor.execute(sql2)
                        username_info = cursor.fetchall()

                        for info in username_info:
                            if info["adventure_id"] == current_adv_id:
                                user_id = item["id"]
                                current_story_id = int(item["current_step"])

                else:
                    print("else, no username")
                    add_user = "INSERT INTO userinfo (name, current_step, adventure_id) VALUES ('{0}', '{1}', '{2}')".format(username, current_story_id, current_adv_id)
                    cursor.execute(add_user)
                    connection.commit()

            next_steps_results = [
                {"id": 1, "option_text": "I fight it"},
                {"id": 2, "option_text": "I give him 10 coins"},
                {"id": 3, "option_text": "I tell it that I just want to go home"},
                {"id": 4, "option_text": "I run away quickly"}
                ]

            #todo add the next step based on db
            return json.dumps({"user": user_id,
                               "adventure": current_adv_id,
                               "current": current_story_id,
                               "next": current_story_id + 1, #is this right?????
                               "text": "You meet a mysterious creature in the woods, what do you do?",
                               "image": "troll.png",
                               "options": next_steps_results
                               })
    except Exception as e:
        print(repr(e))


# def UserInfo(username): #taking the user informations
#     with connection.cursor() as cursor:
#         sql = "SELECT * from users where '{}'".format(username)
#         cursor.execute(sql)
#         user_id = cursor.fetchone()
#         print(user_id)
#         return user_id

# def Options(option_id): #I'm really not sure about this one
#     with connection.cursor() as cursor:
#         sql1 = "SELECT option_id from options where question_id='{}' ORDER BY option_id ASC".format(
#             option_id)
#         cursor.execute(sql1)
#          = cursor.fetchall()
#         print()
#         return

# def nextQuestions (question_id,next_question_id)
#     with connection.cursor() as cursor:
#         sql = "SELECT next_question_id from options WHERE question_id='{}' and option_id='{}'".format(question_id,next_question_id)
#         cursor.execute(sql)
#  = cursor.fetchone()
#  print(["next_question_id"])
# return

# def updateUser(coins,life,next_question_id,question_id):
#     with connection.cursor() as cursor:
#         sql2 = "UPDATE user_id SET question_id='{}',coins='{}',life='{}' WHERE user_id='{}'".format(coins,life,next_question_id,question_id)
#         cursor.execute(sql2)
#         connection.commit()

# def insert_user_name(username):
#     with connection.cursor() as cursor:
#         sql3 = "INSERT INTO users(`username`) VALUES (%s)"
#         cursor.execute(sql3, username)
#         connection.commit()


# def gameOver(user_id):
#     with connection.cursor() as cursor:
#         end = True
#         print(end)
#         sql4 = "UPDATE Users SET question_id='{}',coins='{}',life='{}' WHERE user_id='{}'".format(10,100,user_id)
#         cursor.execute(sql4)
#         connection.commit()
#         return True

@route("/story", method="POST")
def story():
    user_id = request.POST.get("user")
    current_adv_id = request.POST.get("adventure")
    next_story_id = request.POST.get("next") #this is what the user chose - use it!
    next_steps_results = [
        {"id": 1, "option_text": "I run!"},
        {"id": 2, "option_text": "I hide!"},
        {"id": 3, "option_text": "I sleep!"},
        {"id": 4, "option_text": "I fight!"}
        ]
    random.shuffle(next_steps_results) #todo change - used only for demonstration purpouses

    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "next": next_story_id,
                       "text": "New scenario! What would you do?",
                       "image": "choice.jpg",
                       "options": next_steps_results
                       })

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
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()



@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    username = request.POST.get("name")
    current_adv_id = request.POST.get("adventure_id")
    print(username)
    # current_story_id=0

    user_id = 0 #todo check if exists and if not create it
    current_story_id = 0 #todo change
    next_steps_results = [
        {"id": 1, "option_text": "I fight it"},
        {"id": 2, "option_text": "I give him 10 coins"},
        {"id": 3, "option_text": "I tell it that I just want to go home"},
        {"id": 4, "option_text": "I run away quickly"}
        ]



    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "current": current_story_id,
                       "text": "You meet a mysterious creature in the woods, what do you do?",
                       "image": "creature.jpg",
                       "options": next_steps_results
                       })


@route("/story", method="POST")
def story():
    user_id = request.POST.get("user")
    current_adv_id = request.POST.get("adventure")
    next_story_id = request.POST.get("next") #this is what the user chose - use it!
    next_steps_results = [
        {"id": 1, "option_text": "I run!"},
        {"id": 2, "option_text": "I hide!"},
        {"id": 3, "option_text": "I sleep!"},
        {"id": 4, "option_text": "I fight!"}
        ]
    random.shuffle(next_steps_results) #todo change - used only for demonstration purpouses

    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "text": "New scenario! What would you do?",
                       "image": "choice.jpg",
                       "options": next_steps_results
                       })
# def insertUser(username):
#     with connection.cursor() as cursor:
#         sql = "INSERT INTO users(`username`) VALUES (%s)"
#         cursor.execute(sql, username)
#         connection.commit()

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
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()

