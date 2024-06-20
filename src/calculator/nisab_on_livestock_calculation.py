from src.calculator.schemas import Animal


def calculate_camels(camels: int) -> list[Animal]:
    calculated_animals = []
    if camels > 5 and camels <= 9:
        calculated_animals.append(Animal(type="Sheep", quantity=1, age=1))
    elif camels > 9 and camels <= 14:
        calculated_animals.append(Animal(type="Sheep", quantity=2))
    elif camels > 14 and camels <= 19:
        calculated_animals.append(Animal(type="Sheep", quantity=3))
    elif camels > 19 and camels <= 24:
        calculated_animals.append(Animal(type="Sheep", quantity=4))
    elif camels > 24 and camels <= 35:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=1))
    elif camels > 35 and camels <= 45:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=2))
    elif camels > 45 and camels <= 60:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=4))
    elif camels > 60 and camels <= 75:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=5))
    elif camels > 75 and camels <= 90:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=1))
    elif camels > 90 and camels <= 120:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
    elif camels > 120 and camels <= 129:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=1))
    elif camels > 130 and camels <= 134:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=2))
    elif camels > 134 and camels <= 139:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=3))
    elif camels > 139 and camels <= 144:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=4))
    elif camels > 144 and camels <= 149:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Camel", quantity=1, age=1))
    elif camels > 149 and camels <= 154:
        calculated_animals.append(Animal(type="Camel", quantity=3, age=4))
    elif camels > 154 and camels <= 159:
        calculated_animals.append(Animal(type="Camel", quantity=3, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=1))
    return calculated_animals


def calculate_cows(cows: int) -> list[Animal]:
    calculated_animals = []
    if cows >= 30 and cows < 40:
        calculated_animals.append(Animal(type="Cow", quantity=1, age=1))
    elif cows >= 40 and cows < 60:
        calculated_animals.append(Animal(type="Cow", quantity=1, age=2))
    elif cows >= 60 and cows < 70:
        calculated_animals.append(Animal(type="Cow", quantity=2, age=1))
    elif cows >= 70 and cows < 80:
        calculated_animals.append(Animal(type="Cow", quantity=1, age=1))
        calculated_animals.append(Animal(type="Cow", quantity=1, age=2))
    elif cows >= 80 and cows < 90:
        calculated_animals.append(Animal(type="Cow", quantity=2, age=2))
    elif cows >= 90 and cows < 100:
        calculated_animals.append(Animal(type="Cow", quantity=3, age=1))
    elif cows >= 100 and cows < 110:
        calculated_animals.append(Animal(type="Cow", quantity=2, age=1))
        calculated_animals.append(Animal(type="Cow", quantity=1, age=2))

    return calculated_animals


def calculate_buffaloes(buffaloes: int) -> list[Animal]:
    calculated_animals = []
    if buffaloes >= 30 and buffaloes < 40:
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=1))
    elif buffaloes >= 40 and buffaloes < 60:
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=2))
    elif buffaloes >= 60 and buffaloes < 70:
        calculated_animals.append(Animal(type="Buffaloe", quantity=2, age=1))
    elif buffaloes >= 70 and buffaloes < 80:
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=1))
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=2))
    elif buffaloes >= 80 and buffaloes < 90:
        calculated_animals.append(Animal(type="Buffaloe", quantity=2, age=2))
    elif buffaloes >= 90 and buffaloes < 100:
        calculated_animals.append(Animal(type="Buffaloe", quantity=3, age=1))
    elif buffaloes >= 100 and buffaloes < 110:
        calculated_animals.append(Animal(type="Buffaloe", quantity=2, age=1))
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=2))

    return calculated_animals


def calculate_sheep(sheep: int):
    calculated_animals = []
    if sheep >= 40 and sheep < 121:
        calculated_animals.append(Animal(type="Sheep", quantity=1))
    elif sheep >= 121 and sheep < 201:
        calculated_animals.append(Animal(type="Sheep", quantity=2))
    elif sheep >= 201 and sheep < 399:
        calculated_animals.append(Animal(type="Sheep", quantity=3))
    elif sheep >= 300 and sheep < 599:
        calculated_animals.append(Animal(type="Sheep", quantity=4))

    return calculated_animals


def calculate_goats(goats: int):
    calculated_animals = []
    if goats >= 40 and goats < 121:
        calculated_animals.append(Animal(type="Goat", quantity=1))
    elif goats >= 121 and goats < 201:
        calculated_animals.append(Animal(type="Goat", quantity=2))
    elif goats >= 201 and goats < 399:
        calculated_animals.append(Animal(type="Goat", quantity=3))
    elif goats >= 300 and goats < 599:
        calculated_animals.append(Animal(type="Goat", quantity=4))

    return calculated_animals


def calculate_horses(horses_value: int) -> int:
    return horses_value * 0.025
