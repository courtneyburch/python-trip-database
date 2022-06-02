import sqlite3
from bottle import route, run, request, response, template
import hashlib


@route('/', method='GET')
def index():
    return template('login')


@route('/login', method='POST')
def login_result():
    name = request.forms.get('username')  # get HTML form data
    pwd = request.forms.get('password')
    pwd_encode = pwd.encode('utf-8')
    hashed_pwd = hashlib.sha1(pwd_encode).hexdigest()

    # validate user credentials
    conn = sqlite3.connect('travel_expenses.db')
    c = conn.cursor()

    # user info in database?
    sql = "SELECT username, password FROM members WHERE username = ? and password = ?"
    c.execute(sql, (name, hashed_pwd))
    result = c.fetchall()

    if result:
        data = {'username': name}
        return template("menu", data)
    else:
        return 'Incorrect name or password.'

    c.close()


@route('/find_trips', method='GET')
def get_username():
    return template("get_trip_info")


@route('/find_trips', method='POST')
def find_trips():
    name = request.forms.get('username')

    conn = sqlite3.connect('travel_expenses.db')
    c = conn.cursor()
    sql = "SELECT * FROM trips where username = ?"
    c.execute(sql, (name,))

    result = c.fetchall()
    if not result:
        return "No trips found."
    else:
        data = {'rows': result}
        return template("found_trips", data)

    c.close()


@route('/add_trip', method='GET')
def add_trip_info():
    return template('add_trip_info')


@route('/add_trip', method="POST")
def add_trip():
    name = request.forms.get('username')
    date = request.forms.get('date')
    dest = request.forms.get('destination')
    miles = request.forms.get('miles')
    gals = request.forms.get('gallons')
    data = {"name": name, "date": date,
            "dest": dest, "miles": miles, "gals": gals}
    print(data)
    if name != "" and date != "" and dest != "" and miles != "" and gals != "":
        try:
            conn = sqlite3.connect('travel_expenses.db')
            c = conn.cursor()
            sql = "INSERT INTO trips (username, date, destination, miles, gallons) VALUES (?, ?, ?, ?, ?)"
            c.execute(sql, (name, date, dest, miles, gals))
            conn.commit()
            msg = {'op': 'INSERT', 'status': 'successful'}
            return template('success', data, msg)

        except sqlite3.Error as er:
            msg = {'op': 'Add trip', 'status': 'unsuccessful'}

            print('SQLite error: %s' % (' '.join(er.args)))
        
            return template('error', msg)

        finally:
            c.close()

    else:
        msg = {'op': 'Add trip', 'status': 'unsuccessful'}
        return template('error', msg)


run(host='localhost', port=8080)

# @route('/catalog', method='GET')
