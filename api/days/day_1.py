from api.days import solutions_blueprint

PATH_PREFIX = '/day_1'


@solutions_blueprint.route(PATH_PREFIX + '/a')
def get_part_a():
    return {
        'answer': 'hello'
    }
