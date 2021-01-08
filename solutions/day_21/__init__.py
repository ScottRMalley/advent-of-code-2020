from collections import defaultdict

from shared import main
import re


def preprocess(data_input):
    lines = data_input.strip().split('\n')
    foods = []
    for line in lines:
        d = {}
        ingredients = re.search(r'(.*?)\(.*?\)', line).groups()[0].strip().split(' ')
        d['ingredients'] = ingredients
        allergens = re.search(r'\(contains\s([a-z\s,]+)\)', line).groups()[0].split(', ')
        d['allergens'] = allergens
        foods.append(d)
    return foods


def check_selection_possible(allergen, ingredient, foods):
    for food in foods:
        if allergen in food['allergens'] and ingredient not in food['ingredients']:
            return False
    return True


def find_impossible_allergen_selections(foods):
    ingredients = get_ingredient_set(foods)
    allergens = get_allergen_set(foods)

    allergens_possible = defaultdict(list)
    for ingredient in ingredients:
        for allergen in allergens:
            if check_selection_possible(allergen, ingredient, foods):
                allergens_possible[ingredient].append(allergen)
    return allergens_possible


def count_appearances(ingredient, foods):
    count = 0
    for food in foods:
        if ingredient in food['ingredients']:
            count += 1
    return count


def get_ingredient_set(foods):
    ingredients = set()
    for food in foods:
        ingredients.update(food['ingredients'])
    return ingredients


def get_allergen_set(foods):
    allergens = set()
    for food in foods:
        allergens.update(food['allergens'])
    return allergens


def match_allergens(foods):
    allergens = get_allergen_set(foods)
    allergens_possible = find_impossible_allergen_selections(foods)
    matched_allergens = {}
    while len(matched_allergens) < len(allergens):
        for ingred in allergens_possible:
            if len(allergens_possible[ingred]) == 1:
                matched_allergens[allergens_possible[ingred][0]] = ingred
                break
        normalize_allergen_possibilities(matched_allergens, allergens_possible)
    return matched_allergens


def normalize_allergen_possibilities(matched_allergens, allergens_possible):
    for m_allergen in matched_allergens:
        for ingredient in allergens_possible:
            if m_allergen in allergens_possible[ingredient]:
                allergens_possible[ingredient].remove(m_allergen)


def part1(data_input):
    values = preprocess(data_input)
    allergens_possible = find_impossible_allergen_selections(values)
    ingredients = get_ingredient_set(values)
    total = 0
    for ingredient in ingredients:
        if len(allergens_possible[ingredient]) == 0:
            total += count_appearances(ingredient, values)
    return total


def part2(data_input):
    values = preprocess(data_input)
    matched_allergens = match_allergens(values)
    return ','.join([item[1] for item in sorted(list(matched_allergens.items()))])


if __name__ == '__main__':
    main('input.txt', part1, part2)
