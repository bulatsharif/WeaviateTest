from src.calculator.schemas import Animal
from typing import List

"""
This files handles a lot "if-else" in order to calculate Zakat on Livestock
The only purpose is to calculate Zakat.

"""

def calculate_camels(camels: int) -> List[Animal]:
    calculated_animals = []
    if 5 < camels <= 9:
        calculated_animals.append(Animal(type="Sheep", quantity=1, age=1))
    elif 9 < camels <= 14:
        calculated_animals.append(Animal(type="Sheep", quantity=2))
    elif 14 < camels <= 19:
        calculated_animals.append(Animal(type="Sheep", quantity=3))
    elif 19 < camels <= 24:
        calculated_animals.append(Animal(type="Sheep", quantity=4))
    elif 24 < camels <= 35:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=1))
    elif 35 < camels <= 45:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=2))
    elif 45 < camels <= 60:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=4))
    elif 60 < camels <= 75:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=5))
    elif 75 < camels <= 90:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=1))
    elif 90 < camels <= 120:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
    elif 120 < camels <= 129:
        calculated_animals.append(Animal(type="Camel", quantity=1, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=1))
    elif 130 < camels <= 134:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=2))
    elif 134 < camels <= 139:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=3))
    elif 139 < camels <= 144:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=4))
    elif 144 < camels <= 149:
        calculated_animals.append(Animal(type="Camel", quantity=2, age=4))
        calculated_animals.append(Animal(type="Camel", quantity=1, age=1))
    elif 149 < camels <= 154:
        calculated_animals.append(Animal(type="Camel", quantity=3, age=4))
    elif 154 < camels <= 159:
        calculated_animals.append(Animal(type="Camel", quantity=3, age=4))
        calculated_animals.append(Animal(type="Sheep", quantity=1))
    else:
        calculated_animals.append(Animal(type="Camels", quantity=6, age=1))
    return calculated_animals


def calculate_cows(cows: int) -> list[Animal]:
    calculated_animals = []
    if 30 <= cows < 40:
        calculated_animals.append(Animal(type="Cow", quantity=1, age=1))
    elif 40 <= cows < 60:
        calculated_animals.append(Animal(type="Cow", quantity=1, age=2))
    elif 60 <= cows < 70:
        calculated_animals.append(Animal(type="Cow", quantity=2, age=1))
    elif 70 <= cows < 80:
        calculated_animals.append(Animal(type="Cow", quantity=1, age=1))
        calculated_animals.append(Animal(type="Cow", quantity=1, age=2))
    elif 80 <= cows < 90:
        calculated_animals.append(Animal(type="Cow", quantity=2, age=2))
    elif 90 <= cows < 100:
        calculated_animals.append(Animal(type="Cow", quantity=3, age=1))
    elif 100 <= cows < 110:
        calculated_animals.append(Animal(type="Cow", quantity=2, age=1))
        calculated_animals.append(Animal(type="Cow", quantity=1, age=2))

    return calculated_animals


def calculate_buffaloes(buffaloes: int) -> list[Animal]:
    calculated_animals = []
    if 30 <= buffaloes < 40:
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=1))
    elif 40 <= buffaloes < 60:
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=2))
    elif 60 <= buffaloes < 70:
        calculated_animals.append(Animal(type="Buffaloe", quantity=2, age=1))
    elif 70 <= buffaloes < 80:
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=1))
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=2))
    elif 80 <= buffaloes < 90:
        calculated_animals.append(Animal(type="Buffaloe", quantity=2, age=2))
    elif 90 <= buffaloes < 100:
        calculated_animals.append(Animal(type="Buffaloe", quantity=3, age=1))
    elif 100 <= buffaloes < 110:
        calculated_animals.append(Animal(type="Buffaloe", quantity=2, age=1))
        calculated_animals.append(Animal(type="Buffaloe", quantity=1, age=2))
    return calculated_animals


def calculate_sheep(sheep: int):
    calculated_animals = []
    if 40 <= sheep < 121:
        calculated_animals.append(Animal(type="Sheep", quantity=1))
    elif 121 <= sheep < 201:
        calculated_animals.append(Animal(type="Sheep", quantity=2))
    elif 201 <= sheep < 399:
        calculated_animals.append(Animal(type="Sheep", quantity=3))
    elif 300 <= sheep < 599:
        calculated_animals.append(Animal(type="Sheep", quantity=4))

    return calculated_animals


def calculate_goats(goats: int):
    calculated_animals = []
    if 40 <= goats < 121:
        calculated_animals.append(Animal(type="Goat", quantity=1))
    elif 121 <= goats < 201:
        calculated_animals.append(Animal(type="Goat", quantity=2))
    elif 201 <= goats < 399:
        calculated_animals.append(Animal(type="Goat", quantity=3))
    elif 300 <= goats < 599:
        calculated_animals.append(Animal(type="Goat", quantity=4))
    return calculated_animals


def calculate_horses(horses_value: int) -> float:
    return horses_value * 0.025
