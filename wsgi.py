import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.controllers.disease_Solution import *
from App.controllers.classification import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')
    create_classification("Healthy")
    create_classification("Bacterial Spot")
    create_classification("Early Blight")
    create_classification("Late Blight")
    create_classification("Leaf Mold")
    create_classification("Septoria Leaf Spot")
    create_classification("Tomato Mosaic Virus")
    create_classification("Yellow Leaf Curl Virus")
    add_solution(1,"There is no solution needed for healthy leaves.")
    add_solution(2, "Soak seeds of susceptible plants in a 10%% bleach solution before planting.")
    add_solution(2,"Soak seeds of susceptible plants in a 10%% bleach solution before planting.")
    add_solution(3, "Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate or Bonide Tomato & Vegetable.")
    add_solution(3,"Stake or cage tomato plants so that foliage grows vertically, off the ground.")
    add_solution(4,"Apply a copper based fungicide (2 oz/ gallon of water) every 7 days or less, following heavy rain or when the amount of disease is increasing rapidly.")
    add_solution(5,"Try to keep the leaves dry when watering the plants.")
    add_solution(5, "Calcium chloride sprays are among the most highly recommended types for leaf mold.")
    add_solution(6, "Stake plants to improve air circulation and drying of leaves.")
    add_solution(6, "Use fungicides listed as effective against Septoria leaf spot.")
    add_solution(7, "You can try covering your plants with a floating row cover or aluminum foil mulches to prevent these insects from infecting your plants.")
    add_solution(7, "Soak seeds of susceptible plants in a 10%% bleach solution before planting.")
    add_solution(8,"Water regularly and make sure to water the roots, not the leaves.")

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


classiciation_cli = AppGroup('classification', help='Classification object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@classiciation_cli.command("create", help="Creates a disease/classification.")
@click.argument("name", default="Healthy")
def create_classification_command(name):
    classification = create_classification(name)
    print(f'{classification} created!')

@classiciation_cli.command("list", help="Lists classifications in the database")
@click.argument("format", default="")
def list_classifications_command(format):
    if format == 'string':
        print(get_all_classifications())
    else:
        print(get_all_classifications_json())

app.cli.add_command(classiciation_cli) # add the group to the cli


solution_cli = AppGroup('solution', help='Solution object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@solution_cli.command("create", help="Creates a solution.")
@click.argument("classification_id", default=1)
@click.argument("solution", default="No solution needed.")
def create_solution_command(classification_id, solution):
    solution = add_solution(classification_id, solution)
    print(f'{solution} created!')

@solution_cli.command("list", help="Lists classifications in the database")
@click.argument("format", default="")
def list_solutions_command(format):
    if format == 'string':
        print(get_all_solutions()())
    else:
        print(get_all_solutions_json())

app.cli.add_command(solution_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    
app.cli.add_command(test)