import mysql.connector as connector

config = {
    'user' : 'root',
    'password' : '1123581321',
    'host' : '127.0.0.1',
    'database' : 'fitnesstrackerdb',
    'raise_on_warnings' : True
}

try:
  cnx = connector.connect(**config)
except connector.Error as err:
    print(err)
    exit(1)

cursor = cnx.cursor()

def checkCred(user, passkey):
    cursor.execute('''select userid from user where username like '{}' and password like '{}';'''.format(user, passkey))
    res = cursor.fetchone()
    if res != None:
        # print(res)
        return int(str(res)[1:-2])
    return 0

def terminateConnection():
    cursor.close()
    cnx.commit()
    cnx.close()

def getActivitiesList():
    cursor.execute('''select activityname from activity;''')
    res = cursor.fetchall()
    activities = []
    for row in res:
        activities.append(str(row)[2:-3])

    return activities
# print(getActivitiesList())

def getWorkoutsList():
    cursor.execute('''select workoutname from workout;''')
    res = cursor.fetchall()
    workouts = []
    for row in res:
        workouts.append(str(row)[2:-3])

    return workouts
# print(getWorkoutsList())

def getNutritionsList():
    cursor.execute('''select nutritionname from nutrition;''')
    res = cursor.fetchall()
    nutritions = []
    for row in res:
        nutritions.append(str(row)[2:-3])

    return nutritions
# print(getNutritionsList())

def fillActivityLog(userid):
    cursor.execute('''select al.date, a.activityname, al.distance, al.calories_burnt from ( select * from activitylog where userid = {} ) as al join activity a on al.activityid=a.activityid;'''.format(userid))
    res = cursor.fetchone()
    log = []
    while res is not None:
        log.append(res)
        if log.__len__() > 7:
            log.pop(0)
        res = cursor.fetchone()
    log.reverse()

    activityLog.clear()
    for l in log:
        row = []
        for ele in l:
            row.append(str(ele))
        activityLog.append(row)

    # print(activityLog)

def fillWorkoutLog(userid):
    cursor.execute('''select wl.date, w.workoutname, wl.sets, wl.calories_burnt from ( select * from workoutlog where userid = {} ) as wl join workout w on wl.workoutid=w.workoutid;'''.format(userid))
    res = cursor.fetchone()
    log = []
    while res is not None:
        log.append(res)
        if log.__len__() > 7:
            log.pop(0)
        res = cursor.fetchone()
    log.reverse()

    workoutLog.clear()
    for l in log:
        row = []
        for ele in l:
            row.append(str(ele))
        workoutLog.append(row)

    # print(workoutLog)

def fillNutritionLog(userid):
    cursor.execute('''select nl.date, n.nutritionname, nl.quantity, nl.calory_intake from ( select * from nutritionlog where userid = {} ) as nl join nutrition n on nl.nutritionid=n.nutritionid;'''.format(userid))
    res = cursor.fetchone()
    log = []
    while res is not None:
        log.append(res)
        if log.__len__() > 7:
            log.pop(0)
        res = cursor.fetchone()
    log.reverse()

    nutritionLog.clear()
    for l in log:
        row = []
        for ele in l:
            row.append(str(ele))
        nutritionLog.append(row)

    # print(nutritionLog)

def getActivityLog(i, j):
    if activityLog.__len__() > 0:
        return activityLog[i][j]
    return ''

def getWorkoutLog(i, j):
    if workoutLog.__len__() > 0:
        return workoutLog[i][j]
    return ''

def getNutritionLog(i, j):
    if nutritionLog.__len__() > 0:
        return nutritionLog[i][j]
    return ''

def insertActivityLog(log):
    activities = getActivitiesList()
    activityid = None
    for i in range(activities.__len__()):
        if log[1] == activities[i]:
            activityid = str(i+1)
            break

    cursor.execute('''insert into activitylog (userid, activityid, date, distance) values ({}, {}, '{}', {})'''.format(int(log[0]), activityid, log[2], float(log[3])))
    cursor.execute('''update activitylog al join activity a on al.activityid = a.activityid set al.calories_burnt = al.distance*a.calory_per_unit where al.calories_burnt is null;''')
    cnx.commit()
    # print(log)

def insertWorkoutLog(log):
    workouts = getWorkoutsList()
    workoutid = None
    for i in range(workouts.__len__()):
        if log[1] == workouts[i]:
            workoutid = str(i+1)
            break

    cursor.execute('''insert into workoutlog (userid, workoutid, date, sets) values ({}, {}, '{}', {})'''.format(int(log[0]), workoutid, log[2], int(log[3])))
    cursor.execute('''update workoutlog wl join workout w on wl.workoutid = w.workoutid set wl.calories_burnt = wl.sets*w.calories_burnt_per_set where wl.calories_burnt is null;''')
    cnx.commit()
    # print(log)

def insertNutritionLog(log):
    nutritions = getNutritionsList()
    nutritionid = None
    for i in range(nutritions.__len__()):
        if log[1] == nutritions[i]:
            nutritionid = str(i+1)
            break

    cursor.execute('''insert into nutritionlog (userid, nutritionid, date, quantity) values ({}, {}, '{}', {})'''.format(int(log[0]), nutritionid, log[2], float(log[3])))
    cursor.execute('''update nutritionlog nl join nutrition n on nl.nutritionid = n.nutritionid set nl.calory_intake = nl.quantity*n.calory_per_gram where nl.calory_intake is null;''')
    cnx.commit()
    # print(log)

activityLog = []
workoutLog = []
nutritionLog = []

# cursor.close()
# cnx.close()