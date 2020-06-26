import sqlite3
import datetime
import matplotlib.pyplot as plt
import os
import csv
from matplotlib import style
style.use("fivethirtyeight")
from tabulate import tabulate

dt = datetime.datetime.today()

#Basic SQLite commands
# conn = sqlite3.connect('expense.db')
# c = conn.cursor()
# conn.commit()
# conn.close()


#Create database & table (Comment out once database is created)
def create_database():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS expense (
                    id integer PRIMARY KEY,
                    year integer,
                    month integer,
                    day integer,
                    item text,
                    category text,
                    count integer,
                    price real
        )""")
        conn.commit()
        conn.close()
    except:
        pass

create_database()

########################################################################################################################
#ADDING EXPENSES FUNCTIONS

#Category definition (Pre-set to better sort database)
def pick_category():
    user_input = input("""What is the category?
    (1) Rent
    (2) Utilities
    (3) Household
    (4) Insurance
    (5) Auto
    (6) Groceries
    (7) Eating Out
    (8) Gifts
    (9) Education
    (10) Entertainment
    (11) Clothing
    """)
    if user_input == "1":
        category = "RENT"
        return category
    elif user_input == "2":
        category = "UTILITIES"
        return category
    elif user_input == "3":
        category = "HOUSEHOLD"
        return category
    elif user_input == "4":
        category = "INSURANCE"
        return category
    elif user_input == "5":
        category = "AUTO"
        return category
    elif user_input == "6":
        category = "GROCERIES"
        return category
    elif user_input == "7":
        category = "EATING OUT"
        return category
    elif user_input == "8":
        category = "GIFTS"
        return category
    elif user_input == "9":
        category = "EDUCATION"
        return category
    elif user_input == "10":
        category = "ENTERTAINMENT"
        return category
    elif user_input == "11":
        category = "CLOTHING"
        return category
    else:
        print("Please provide one of the listed categories!")
        pick_category()


#Adding expense (today/specific)
def ask_exp():
    user = input("Are you adding an expense for today? (Y/N)")
    if user.upper() == "Y":
        year = dt.year
        month = dt.month
        day = dt.day
        item = input("Item?")
        category = pick_category()
        count = input("Count?")
        price = float(input("Price?"))
        add(year, month, day, item, category, count, price)
    elif user.upper() == "N":
        year = input("What is the year?")
        month = input("What is the month?")
        day = input("What is the day?")
        try:
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            try:
                year_month_input = datetime.datetime(year=year_int, month=month_int, day=day_int)
            except:
                print("Please provide a valid date!")
                ask_exp()
        except:
            print("Please provide the year and month as an integer!")
            ask_exp()
        item = input("Item?")
        category = pick_category()
        count = input("Count?")
        price = float(input("Price?"))
        add(year_int, month_int, day_int, item, category, count, price)
    else:
        print("Please provide the correct input!")
        ask_exp()


#Adding expense to database
def add(year, month, day, item, category, count, price):
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    id = None
    c.execute("""INSERT INTO expense
                 VALUES (?,?,?,?,?,?,?,?)
    """, (id, year, month, day, item, category, count, price))
    conn.commit()
    print("Expense successfully entered!")
    conn.close()

#Add another expense function
def add_another_expense():
    user_input_2 = input("Would you like to add another expense? (Y/N)")
    if user_input_2.upper() == "Y":
        ask_exp()
        add_another_expense()
    elif user_input_2.upper() == "N":
        print("Thank you have a nice day!")
    else:
        print("Please provide the correct input")
        add_another_expense()


########################################################################################################################
#SHOWING EXPENSES FUNCTION

#A master list of existing year and months
def year_month_list():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT year, month
                 FROM expense
    """)
    items = c.fetchall()
    year_list = []
    month_list = []
    for item in items:
        if item[0] not in year_list:
            year_list.append(item[0])
        else:
            pass
        if item[1] not in month_list:
            month_list.append(item[1])
        else:
            pass
    conn.commit()
    conn.close()
    return year_list, month_list

year_list, month_list = year_month_list()


#Shows all expense entry
def show_all_expenses():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expense")
    items = c.fetchall()
    items_tup = []
    for item in items:
        items_tup.append(item)
    print(tabulate(items_tup, headers=["ID","Year","Month,","Day","Item","Category","Count","Price"]))
    conn.commit()
    conn.close()

#Shows expenses LIST this month
def show_expenses_list(year, month):
    year = dt.year
    month = dt.month
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM expense
                 WHERE year = (?) AND month = (?)
    """, (year, month))
    items = c.fetchall()
    items_tup = []
    for item in items:
        items_tup.append(item)
    print(tabulate(items_tup, headers=["ID", "Year", "Month,", "Day", "Item", "Category", "Count", "Price"]))
    conn.commit()
    conn.close()

#Shows expenses LIST based on specific year and month
def show_expenses_month_year():
    year = input("Year?")
    month = input("Month?")
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT *
                 FROM expense
                 WHERE year = (?) AND month = (?)
    )""", (year, month))
    items = c.fetchall()
    items_tup = []
    for item in items:
        items_tup.append(item)
    print(tabulate(items_tup, headers=["ID", "Year", "Month,", "Day", "Item", "Category", "Count", "Price"]))
    conn.commit()
    conn.close()

#Shows expenses categories based on THIS MONTH (INCOMPLETE)
def show_categories_this_month():
    year = dt.year
    month = dt.month
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT category 
                 FROM expense
                 WHERE year = (?) AND month = (?)
        )""", (year, month))
    items = c.fetchall()
    items_tup = []
    for item in items:
        items_tup.append(item)
    conn.commit()
    conn.close()
    return items_tup

#Shows expenses categories based on YEAR (INCOMPLETE)
def show_categories_year():
    year = input("Year?")
    category = input("Category?")
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT rowid,
                    FROM expense
                    WHERE year = (?)
                    GROUP BY category
        )""", year)
    items = c.fetchall()

    for item in items:
        print(item)
    conn.commit()
    conn.close()



#Function to query the database for the category data with specified year & month
def query_category_dict(year, month):
    year = year
    month = month
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT category, price
                     FROM expense
                     WHERE year = (?) AND month = (?)
        """, (year, month))
    items = c.fetchall()
    empty_dict = {}
    for item in items:
        if item[0] not in empty_dict:
            empty_dict[item[0]] = []
            empty_dict[item[0]].append(item[1])
        else:
            empty_dict[item[0]].append(item[1])
    conn.commit()
    conn.close()
    return empty_dict

#Function to create pie chart
def piechart(query_dict):
    category_dict = query_dict
    labels = []
    items = []
    for item in category_dict:
        labels.append(item)
        items.append(sum(category_dict[item]))
    plt.pie(items, #autopct='%1.1f%%',
            shadow=False, startangle=90, wedgeprops={"edgecolor": "black"})
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Monthly Category Breakdown", fontname = "Arial", y = 1.05)
    total = sum(items)
    plt.legend(
        labels = ['%s, %1.1f %%' % (l, (float(s) / total) * 100) for l, s in zip(labels, items)],
        loc = "upper left",
        bbox_to_anchor = (0.75,1),
    )
    plt.show()


########################################################################################################################
#DELETE ENTRY FUNCTIONS


#Deletes expenses based on rowid
def del_expenses_ID ():
    id = input("Which entry would you like to delete (Based on ID)")
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""DELETE from expense
                 WHERE id = (?)
    """, id)
    conn.commit()
    print("Entry successfully removed!")
    conn.close()


########################################################################################################################
#EXPORT TO CSV FUNCTION

def export_db_to_csv():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("""SELECT *
                 FROM expense
    """)
    with open("ExpenseTracker.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in c.description])
        csv_writer.writerows(c)

    dirpath = os.getcwd() + "/ExpenseTracker.csv"
    print("Data exported successfully into {}".format(dirpath))
    conn.commit()
    conn.close()

########################################################################################################################
#MENU FUNCTIONS


#This month expense menu
def show_specific_expense(year, month):
    user_input_2 = input("""Which would you like to check?
    (1) Pie chart
    (2) List
    (3) Previous menu
    (4) Main menu
    """)
    if user_input_2 == "1":
        this_month_dict = query_category_dict(year, month)
        piechart(this_month_dict)
    elif user_input_2 == "2":
        show_expenses_list(year, month)
    elif user_input_2 == "3":
        check_expense()
    elif user_input_2 == "4":
        main_menu()
    else:
        print("Please provide the correct input!")
        show_specific_expense()


#Check expense menu
def check_expense():
    user_input = input("""
    What would you like to check?
    (1) This month
    (2) Specific month and year
    (3) All
    (4) Previous menu
    """)
    if user_input == "1":
        year = dt.year
        month = dt.month
        show_specific_expense(year, month)
    elif user_input == "2":
        year = input("Year?")
        month = input("Month?")
        try:
            year_int = int(year)
            month_int = int(month)
            if year_int in year_list:
                if month_int in month_list:
                    show_specific_expense(year_int, month_int)
                else:
                    print("No month found!")
                    check_expense()
            else:
                print("No record found!")
                check_expense()
        except:
            print("Please enter the year and month as integer!")
            check_expense()
    elif user_input == "3":
        show_all_expenses()
    elif user_input == "4":
        main_menu()
    else:
        print("Please provide the correct input!")
        check_expense()

#Function for main menu
def main_menu():
    user_input = input("""
    What would you like to do?
    (1) Add an expense
    (2) Check expense
    (3) Remove expense
    (4) Export database .csv file
    (5) Exit
    """)
    if user_input == "1":
        ask_exp()
        add_another_expense()
    elif user_input == "2":
        check_expense()
    elif user_input == "3":
        del_expenses_ID()
    elif user_input == "4":
        export_db_to_csv()
    elif user_input == "5":
        print("Thank you have a nice day!")
    else:
        print("Please provide the correct input!")
