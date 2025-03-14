import csv 
import sqlite3 

def create_connection():
    try:
        con = sqlite3.connect("users.sqlite3")
        return con
    
    

def create_table(con):
    CREATE_USER_TABLE_QUERY ="""
        create table IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL, 
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web text
        );
    """
    cur = con.cursor()
    cur.execute(CREATE_USER_TABLE_QUERY)
    print('User id created sucessfully.')
        
    except Exception as e:
        print('error',e)

        # open git bash
        # git config --global user.name "Prayush Neupane"
        # git config --global user.email "kprayush999@gmail.com"

        # git init => first time only / it init git repository

        # for every time after you change code
        # git add . 
        # git commit -m " Your commit message " => k kaam garoo bhanni yesma 

        # git status => to check the status of files
        # git diff => to check change in files
        # copy paste from github from code
        # git push

        # git checkout -b feature name => to make branch


def create_table(con):
    CREATE_USER_TABLE_QUERY ="""
        create table IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL, 
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web text
        );
    """
    cur = con.cursor()
    cur.execute(CREATE_USER_TABLE_QUERY)
    print('User id created sucessfully.')


INPUT_STRING = '''
Enter The Option:
    1. CREATE TABLE
    2. DUMP users from csv INTO user TABLE
    3. ADD new users INTO the TABLE
    4. QUERY all users from TABLE
    5. QUERY user by id from TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE users by id
    9. UPDATE user
    10.Press any key to EXIT
'''

def read_csv():
    users=[]
    with open ('sample_user.csv','r')as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))

    return users[1:]

def insert_users(con,users):
    user_add_query = """
        INSERT INTO users
        ( 
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)

    """
    cur = con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f'{len(users)} users were imported sucessfully.')


def select_users(con):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)

def select_user_by_id(con,user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users where id = ?;",(user_id))
    for user in users:
        print(user)

def select_specified_records(con,num_records):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users LIMIT ?;",(num_records,))
    for user in users:
        print(user)

def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print('all users were deleted sucessfully')

def delete_users_by_id(con,user_id):
    cur = con.cursor()
    cur.execute("DELETE FROM users where id =?",(user_id,))
    con.commit()
    print(f' users with id [{user_id}] was deleted sucessfully')

COLUMNS = (

    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)

def get_current_user_data(con,user_id):
    cur = con.cursor()
    cur.execute("SELECT *FROM users WHERE id = ?;",(user_id,))
    return cur.fetchone()

def update_user(con,user_id,user_data):
    current_data = get_current_user_data(con,user_id)

    updated_data = [
        new_value if new_value is not None else current_value
        for new_value,current_value in zip(user_data,current_data[1:])
    ]

    update_query = """
        UPDATE users
        SET first_name = ?,
            last_name = ?,
            company_name = ?,
            address = ?,
            city = ?,
            county = ?,
            state = ?,
            zip = ?,
            phone1 = ?,
            phone2 = ?,
            email = ?,
            web = ?
        WHERE id = ?;
    """
    cur = con.cursor()
    cur.execute(update_query,(*updated_data,user_id))
    con.commit()
    print(f'user with id [{user_id}] was sucessfully updated.')


def main():
    con = create_connection() 
    user_input = input(INPUT_STRING)
    if user_input == "1":
        create_table(con)

    elif user_input == "2":
       users= read_csv()
       insert_users(con,users)

    elif user_input == "3":
        user_data = []
        for column in COLUMNS:
            column_value = input(f'enter the value of {column}:')
            user_data.append(column_value)
        insert_users(con,[tuple(user_data)])


    elif user_input == "4":
        select_users(con)

    elif user_input == "5":
        user_id = input('enter the user id: ')
        select_user_by_id(con,user_id)

    elif user_input == "6":
        num_records = input('enter te number of records you want to display: ')
        if num_records.isdigit():
            select_specified_records(con,num_records)

    elif user_input == "7":
        delete_users(con)

    elif user_input == "8":
        user_id = input('enter the user id:')
        if user_id.isdigit():
            delete_users_by_id(con,user_id)

    elif user_input == "9":
        user_id = input('enter the user id to update:')
        if user_id.isdigit():
            current_data = get_current_user_data(con,user_id)
            if not current_data:
                print(f'no user with id [{user_id}] is found.')
                return
            user_data = []
        
            for column in COLUMNS:
                column_value = input(f'enter the new value for {column} (leave blank to keep the current): ' )
                user_data.append(column_value if column_value else None)
            update_user(con,user_id,user_data)
        
        else:
            print('invalid user id . please insert a numeric value.')

    else:
        exit()

    


main()
