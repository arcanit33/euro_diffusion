STARTING_NUMBER_OF_COINS = 1_000_000
PART_TO_GIVE = 1000
DAYS = 100000

class City:
    def __init__(self, x: int, y: int, balance: dict):
        self.x = x
        self.y = y
        self.balance = balance
        self.new_balance = {}
        self.neighbors: list[City] = []

    def add_new_balance(self):
        for country_name, country_value in self.new_balance.items():
            if country_name in self.balance:
                self.balance[country_name] += country_value
            else:
                self.balance[country_name] = country_value

        self.new_balance = {}

    def distribute_money(self, money_to_give):
        for country_name, country_value in money_to_give.items():
            if country_name in self.new_balance:
                self.new_balance[country_name] -= country_value * len(self.neighbors)
            else:
                self.new_balance[country_name] = -country_value * len(self.neighbors)

            for neighbor in self.neighbors:
                if country_name in neighbor.new_balance:
                    neighbor.new_balance[country_name] += country_value
                else:
                    neighbor.new_balance[country_name] = country_value
                    
    def is_completed(self) -> bool:
        return len(self.balance) == countries_number


class Country:
    def __init__(self, name: str, xl: int, yl: int, xh: int, yh: int):
        self.name = name
        self.cities = [
            City(x, y, {self.name: STARTING_NUMBER_OF_COINS})
            for y in range(yl, yh + 1)
            for x in range(xl, xh + 1)
        ]
        self.completion_date = -1

    def is_completed(self) -> bool:
        return all([c.is_completed() for c in self.cities])


class DaysGoBy:
    def __init__(self, countries: list[Country]):
        self.countries: list[Country] = countries
        self.cities: list[City] = []
        self.days = 0

    def init_neighbors(self):
        for country in self.countries:
            for city in country.cities:
                self.cities.append(city)
                for neighbor_country in self.countries:
                    for neighbor_city in neighbor_country.cities:
                        if (abs(city.x - neighbor_city.x) + abs(city.y - neighbor_city.y)) == 1:
                            city.neighbors.append(neighbor_city)

    def check_completions(self) -> bool:
        for country in self.countries:
            if country.is_completed() and country.completion_date == -1:
                country.completion_date = self.days

        return all([country.is_completed() for country in self.countries])

 def next_day(self):
        money_to_give = {}

        for country_name, country_value in self.balance.items():
            if country_value // PART_TO_GIVE > 0:
                money_to_give[country_name] = country_value // PART_TO_GIVE

        self.distribute_money(money_to_give)
        self.add_new_balance()

        self.days += 1

    def run(self):
        while not self.check_completions() and self.days < DAYS:
            self.next_day()


def validate_coordinates(xl: int, yl: int, xh: int, yh: int):
    if xl > xh or yl > yh:
        raise ValueError("xl > xh or yl > yh")
    if xl < 0 or yl < 0 or xh < 0 or yh < 0:
        raise ValueError("xl < 0 or yl < 0 or xh < 0 or yh < 0")
    if xl > 10 or yl > 10 or xh > 10 or yh > 0:
        raise ValueError("xl > 10 or yl > 10 or xh > 10 or yh > 10")

def read_case(lines, current_line, num_lines):
    countries: list[Country] = []
    for i in range(num_lines):
        line: str = lines[current_line + i]
        vals = line.rstrip().split(' ')
        validate_coordinates(int(vals[1]), int(vals[2]), int(vals[3]), int(vals[4]))
        countries.append(Country(vals[0], int(vals[1]), int(vals[2]), int(vals[3]), int(vals[4])))
    return countries


cases = []
countries_number = 0
input_file = open("input.txt", "r")

lines = input_file.readlines()

line = 0
num = int(lines[line])

while num != 0:
    cases.append(read_case(lines, line + 1, num))
    line += num + 1
    num = int(lines[line])

# case_n = 1
# for case in cases:
#     countries_number = len(case)
#     game = DaysGoBy(case)
#     game.init_neighbors()
#     game.run()

#     print('-----------------------------------')
#     print(f'Case Number: {case_n}\n')
#     case_n += 1

#     game.countries.sort(key=lambda country: country.completion_date if country.completion_date != -1 else float('inf'))

#     for country in game.countries:
#         completion_date = country.completion_date if country.completion_date != -1 else 'N/A'
#         print(f'{country.name}: {completion_date}')
case_n = 1
for case in cases:
    countries_number = len(case)
    game = DaysGoBy(case)
    game.init_neighbors()
    game.run()

    print('-----------------------------------')
    print(f'Case Number: {case_n}\n')
    case_n += 1

    sorted_countries = sorted([(country.name, country.completion_date) for country in game.countries], key=lambda x: x[0])
    for country_name, completion_date in sorted_countries:
        completion_date = completion_date if completion_date != -1 else 'N/A'
        print(f'{country_name}: {completion_date}')

