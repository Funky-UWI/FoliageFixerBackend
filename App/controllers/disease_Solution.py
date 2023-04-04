from flask import jsonify
from App.models import DiseaseSolution
from App.database import db


# to save a solution to the database on its classification.. creating new solution object and setting its attributes 
def add_solution(classification_id, solution):
    newSolution=DiseaseSolution(classification_id=classification_id, solution=solution)
    db.session.add(newSolution)
    db.session.commit()
    return 'solution added'

# change to id
def get_solutions_by_classification(classification_id):
    solutions = DiseaseSolution.query.filter_by(classification_id=classification_id)
    solutions_json = [solution.get_json() for solution in solutions]
    if solutions_json:
        return solutions_json
    else:
        return f'no Solution found for classification "{classification_id}".'

def get_all_solutions():
    return DiseaseSolution.query.all()

def get_all_solutions_json():
    solutions = DiseaseSolution.query.all()
    if not solutions:
        return []
    solutions = [solution.get_json() for solution in solutions]
    return solutions