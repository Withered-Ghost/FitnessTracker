import tkinter as tk
import fitnesstracking_backend as backend

userid = 0

def login():
    global userid
    userid = backend.checkCred(username_entry.get(), password_entry.get())
    if userid > 0:
        show_page(dashboard_frame)
        refreshDashboard()

def logout():
    global userid
    userid = 0
    forgetAll()
    login_frame.pack(pady=20)
    clear()

def exit():
    backend.terminateConnection()
    forgetAll()
    root.destroy()

def clear():
    username_entry.delete(0, 'end')
    password_entry.delete(0, 'end')

def show_page(frame):
    forgetAll()
    navigation_frame.pack(pady=10)
    frame.pack(pady=20)

def forgetAll():
    login_frame.pack_forget()
    dashboard_frame.pack_forget()
    activity_frame.pack_forget()
    workout_frame.pack_forget()
    nutrition_frame.pack_forget()
    navigation_frame.pack_forget()

def refreshDashboard():
    forgetAll()
    generateDashboard()
    show_page(dashboard_frame)

def getLabel(frame, str):
    label = tk.Label(frame, text=str, borderwidth=1, relief='solid', width=15)
    return label

def getTitles():
    titles = []

    titles.append(getLabel(dashboard_frame, 'Date'))
    titles.append(getLabel(dashboard_frame, 'Activity'))
    titles.append(getLabel(dashboard_frame, 'Distance (km)'))
    titles.append(getLabel(dashboard_frame, 'Calories Burnt (kcal)'))
    titles.append(getLabel(dashboard_frame, 'Date'))
    titles.append(getLabel(dashboard_frame, 'Workout'))
    titles.append(getLabel(dashboard_frame, 'Sets'))
    titles.append(getLabel(dashboard_frame, 'Calories Burnt (kcal)'))
    titles.append(getLabel(dashboard_frame, 'Date'))
    titles.append(getLabel(dashboard_frame, 'Meal'))
    titles.append(getLabel(dashboard_frame, 'Amount'))
    titles.append(getLabel(dashboard_frame, 'Calorie Intake (kcal)'))

    for i in range(12):
        titles[i].grid(row=1, column=i)
    return titles

def generateDashboard():
    backend.fillActivityLog(userid)
    backend.fillWorkoutLog(userid)
    backend.fillNutritionLog(userid)

    # Dashboard Page
    dashboard_grid = []
    dashboard_title = []
    title = tk.Label(dashboard_frame, text='DashBoard', relief='flat')
    title.grid(row=0, columnspan=12)
    dashboard_title.append(title)
    dashboard_grid.append(dashboard_title)
    dashboard_grid.append(getTitles())

    blanks = []
    for i in range(12):
        l = tk.Label(dashboard_frame, text='')
        l.grid(row=2, column=i)
        blanks.append(l)
    dashboard_grid.append(blanks)

    for i in range(7):
        grid_row = []
        for j in range(4):
            label = tk.Label(dashboard_frame, text='''{}'''.format(backend.getActivityLog(i, j)), borderwidth=1, relief='ridge', width=15)
            label.grid(row=i+3, column=j)
            grid_row.append(label)
        dashboard_grid.append(grid_row)

    for i in range(7):
        grid_row = []
        for j in range(4):
            label = tk.Label(dashboard_frame, text='''{}'''.format(backend.getWorkoutLog(i, j)), borderwidth=1, relief='ridge', width=15)
            label.grid(row=i+3, column=j+4)
            grid_row.append(label)
        dashboard_grid.append(grid_row)

    for i in range(7):
        grid_row = []
        for j in range(4):
            label = tk.Label(dashboard_frame, text='''{}'''.format(backend.getNutritionLog(i, j)), borderwidth=1, relief='ridge', width=15)
            label.grid(row=i+3, column=j+8)
            grid_row.append(label)
        dashboard_grid.append(grid_row)

    for i in range(10):
        dashboard_frame.rowconfigure(i, weight=1)
    for i in range(12):
        dashboard_frame.columnconfigure(i, weight=1)

def submit_activity():
    log = []
    log.append(userid)
    log.append(activityoption.get())
    log.append(activity_date_entry.get())
    log.append(distance_entry.get())
    # print(log)

    if log.__len__() == 4:
        backend.insertActivityLog(log)

def submit_workout():
    log = []
    log.append(userid)
    log.append(workoutoption.get())
    log.append(workout_date_entry.get())
    log.append(sets_entry.get())
    # print(log)

    if log.__len__() == 4:
        backend.insertWorkoutLog(log)

def submit_nutrition():
    log = []
    log.append(userid)
    log.append(nutritionoption.get())
    log.append(nutrition_date_entry.get())
    log.append(quantity_entry.get())
    # print(log)

    if log.__len__() == 4:
        backend.insertNutritionLog(log)



# UI Design
root = tk.Tk()
root.title("Fitness App")

# Login Page
login_frame = tk.Frame(root)

tk.Label(login_frame, text="Username").grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

tk.Label(login_frame, text="Password").grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

clear_button = tk.Button(login_frame, text="Clear", command=clear)
clear_button.grid(row=2, column=0, columnspan=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=1, columnspan=1)

exit_buton = tk.Button(login_frame, text="Exit", command=exit)
exit_buton.grid(row=2, column=2, columnspan=1)
login_frame.pack(pady=20)

# User Dashboard
dashboard_frame = tk.Frame(root)
generateDashboard()
refresh_button = tk.Button(dashboard_frame, text='Refresh', command=refreshDashboard)
refresh_button.grid(row=10, columnspan=12)

# Submission Pages
activity_frame = tk.Frame(root)
workout_frame = tk.Frame(root)
nutrition_frame = tk.Frame(root)

# Navigation Bar
navigation_frame = tk.Frame(root)



# Activity Page
tk.Label(activity_frame, text="Activity").grid(row=0, column=0)
activityoption = tk.StringVar()
activityoption.set('')
activity_dropdown = tk.OptionMenu(activity_frame, activityoption, *(backend.getActivitiesList()))
activity_dropdown.grid(row=0, column=1)

tk.Label(activity_frame, text="Date (yy-mm-dd)").grid(row=1, column=0)
activity_date_entry = tk.Entry(activity_frame)
activity_date_entry.grid(row=1, column=1)

tk.Label(activity_frame, text="Distance (km)").grid(row=2, column=0)
distance_entry = tk.Entry(activity_frame)
distance_entry.grid(row=2, column=1)

# tk.Label(activity_frame, text="Calories Burnt").grid(row=4, column=0)
# calory_entry = tk.Entry(activity_frame)
# calory_entry.grid(row=4, column=1)

submit_activity_button = tk.Button(activity_frame, text="Submit", command=submit_activity)
submit_activity_button.grid(row=3, columnspan=2)




# Workout Page
tk.Label(workout_frame, text="Workout").grid(row=0, column=0)
workoutoption = tk.StringVar()
workoutoption.set('')
workout_dropdown = tk.OptionMenu(workout_frame, workoutoption, *(backend.getWorkoutsList()))
workout_dropdown.grid(row=0, column=1)

tk.Label(workout_frame, text="Date (yy-mm-dd)").grid(row=1, column=0)
workout_date_entry = tk.Entry(workout_frame)
workout_date_entry.grid(row=1, column=1)

tk.Label(workout_frame, text="Sets").grid(row=2, column=0)
sets_entry = tk.Entry(workout_frame)
sets_entry.grid(row=2, column=1)

# tk.Label(workout_frame, text="Calories Burnt").grid(row=3, column=0)
# workout_calory_entry = tk.Entry(workout_frame)
# workout_calory_entry.grid(row=3, column=1)

submit_workout_button = tk.Button(workout_frame, text="Submit", command=submit_workout)
submit_workout_button.grid(row=3, columnspan=2)




# Nutrition Page
tk.Label(nutrition_frame, text="Nutrition").grid(row=0, column=0)
nutritionoption = tk.StringVar()
nutritionoption.set('')
nutrition_dropdown = tk.OptionMenu(nutrition_frame, nutritionoption, *(backend.getNutritionsList()))
nutrition_dropdown.grid(row=0, column=1)

tk.Label(nutrition_frame, text="Date (yy-mm-dd)").grid(row=1, column=0)
nutrition_date_entry = tk.Entry(nutrition_frame)
nutrition_date_entry.grid(row=1, column=1)

tk.Label(nutrition_frame, text="Quantity (g)").grid(row=2, column=0)
quantity_entry = tk.Entry(nutrition_frame)
quantity_entry.grid(row=2, column=1)

# tk.Label(nutrition_frame, text="Calorie Intake").grid(row=3, column=0)
# nutrition_calory_entry = tk.Entry(nutrition_frame)
# nutrition_calory_entry.grid(row=3, column=1)

submit_nutrition_button = tk.Button(nutrition_frame, text="Submit", command=submit_nutrition)
submit_nutrition_button.grid(row=3, columnspan=2)




# Navigation Buttons

dashboard_button = tk.Button(navigation_frame, text="Dashboard", command=lambda: show_page(dashboard_frame))
dashboard_button.grid(row=0, column=0, padx=10)

activity_button = tk.Button(navigation_frame, text="Activity", command=lambda: show_page(activity_frame))
activity_button.grid(row=0, column=1, padx=10)

workout_button = tk.Button(navigation_frame, text="Workout", command=lambda: show_page(workout_frame))
workout_button.grid(row=0, column=2, padx=10)

nutrition_button = tk.Button(navigation_frame, text="Nutrition", command=lambda: show_page(nutrition_frame))
nutrition_button.grid(row=0, column=3, padx=10)

logout_button = tk.Button(navigation_frame, text="Logout", command=logout)
logout_button.grid(row=0, column=5, padx=10)


# Start the application
root.mainloop()