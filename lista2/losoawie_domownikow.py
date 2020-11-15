import random

elements = 96
ilosc_obecnych_domownikow = []


def gernerowanie_danych(elements):
    for i in range(elements):
        ilosc_obecnych_domownikow.append(random.randint(1, 3))


gernerowanie_danych(elements)

print(ilosc_obecnych_domownikow)

