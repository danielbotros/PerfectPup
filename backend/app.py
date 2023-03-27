import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = ""
MYSQL_PORT = 3306
MYSQL_DATABASE = "breeds"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db(os.path.join(
    os.environ['ROOT_PATH'], 'dogbreeddata.sql'))

app = Flask(__name__)
CORS(app)

# # Sample search, the LIKE operator in this case is hard-coded,
# # but if you decide to use SQLAlchemy ORM framework,
# # there's a much better and cleaner way to do this
# def sql_search(episode):
#     query_sql = f"""SELECT * FROM episodes WHERE LOWER( title ) LIKE '%%{episode.lower()}%%' limit 10"""
#     keys = ["id","title","descr"]
#     data = mysql_engine.query_selector(query_sql)
#     return json.dumps([dict(zip(keys,i)) for i in data])

@app.route("/")
def home():
    return render_template('base.html', title="sample html")


@app.route("/perfectpupper")
def episodes_search():
    print("request: ", request)
    hours = request.args.get("hours")
    space = request.args.get("space")
    trait1 = request.args.get("trait1")
    trait2 = request.args.get("trait2")
    trait3 = request.args.get("trait3")
    return time_commitment(hours, space, trait1, trait2, trait3)


def time_commitment(hours, space, trait1, trait2, trait3):
    print("hours: ",  hours)
    size = space_commitment(space)  # change this later
    print("size: ", size)
    print("trait1: ",  trait1)
    print("trait2: ",  trait2)
    print("trait3: ",  trait3)
    query_sql = f"""SELECT breed_name, trainability_value, descript, temperament 
    FROM breeds 
    WHERE trainability_value <= {hours} 
    AND max_height <= {size*10} 
    AND (temperament LIKE '%%{trait1}%%' 
    OR temperament LIKE '%%{trait2}%%' 
    OR temperament LIKE '%%{trait3}%%')
    limit 10"""
    data = mysql_engine.query_selector(query_sql)
    keys = ["breed_name", "trainability_value", "descript", "temperament"]
    # keys = ["breed_name", "descript", "temperament", "popularity", "min_height", "max_height",
    #         "min_weight",
    #         "max_weight",
    #         "min_expectancy", 
    #         "max_expectancy",
    #         "dog_group",
    #         "grooming_frequency_value",
    #         "grooming_frequency_category",
    #         "shedding_value",
    #         "shedding_category",
    #         "energy_level_value",
    #         "energy_level_category",
    #         "trainability_value",
    #         "trainability_category",
    #         "demeanor_value",
    #         "demeanor_category"]
    # keys = ["breed_name", "trainability_value",
    #         "energy_level_value", "grooming_frequency_value"]
    print(data)
    return json.dumps([dict(zip(keys, i)) for i in data])
# WHERE 2*(trainability_value) <= '%%{hours}%% AND '%%{hours}%%' < 2*(trainability_value);"""


def space_commitment(size):
    size = size.lower()
    if size == "small":
        size = 2
    elif size == "medium":
        size = 4
    else:
        size = 6
    return size


app.run(debug=True)
