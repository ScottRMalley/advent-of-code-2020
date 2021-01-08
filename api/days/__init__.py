from flask import Blueprint
import solutions
import re

solutions_blueprint = Blueprint('days', __name__)

from api.days import day_1


def day_from_module_name(module_name):
    return int(re.search(r'\d+', module_name).group())


available_modules = [i.name for i in pkgutil.iter_modules(solutions.__path__)]
day_modules = {
    day_from_module_name(name): __import__(f'solutions.{name}', fromlist=[''])
    for name in available_modules
}


@solutions_blueprint.route('/<day>/<part>')
def get_solution(day, part):


