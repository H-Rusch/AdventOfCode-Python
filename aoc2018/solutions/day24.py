import re
from copy import deepcopy


class Group:
    def __init__(self, units: int, hp: int, attack: int, attack_type: str,
                 initiative: int, immune: set, weak: set):
        self.units = units
        self.hp = hp
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.immune = immune
        self.weak = weak

    def calc_power(self):
        return self.units * self.attack

    def calc_damage_to(self, other: "Group"):
        mult = 0 if self.attack_type in other.immune else 2 if self.attack_type in other.weak else 1

        return mult * self.calc_power()

    def __repr__(self):
        return f"GROUP: (units: {self.units}, hp: {self.hp}, attack: {self.attack}, attack_type: {self.attack_type}" \
               f", initiative: {self.initiative}, immune: {self.immune}, weak: {self.weak})"


class Event:
    def __init__(self, attacker: Group, defender: Group, attackers: list, defenders: list):
        self.attacker = attacker
        self.defender = defender
        self.attackers = attackers
        self.defenders = defenders

    def execute(self):
        if self.attacker.units > 0:
            damage = self.attacker.calc_damage_to(self.defender)

            killed = damage // self.defender.hp
            self.defender.units -= killed
            if self.defender.units <= 0:
                self.defenders.remove(self.defender)

    def __repr__(self):
        return f"EVENT: (attacker: {self.attacker}, defender: {self.defender}, damage: " \
               f"{self.attacker.calc_damage_to(self.defender)})"


def part1(input: str) -> int:
    immune_army, infection_army = parse(input)

    fight(immune_army, infection_army)

    return sum(map(lambda g: g.units, immune_army + infection_army))


def part2(input: str) -> int:
    immune_army, infection_army = parse(input)

    boost = 1
    while True:
        copy_immune, copy_infection = deepcopy(
            immune_army), deepcopy(infection_army)
        result = fight(copy_immune, copy_infection, boost)

        if result == 1:
            break

        boost += 1

    return sum(map(lambda g: g.units, copy_immune + copy_infection))


def fight(immune: list, infection: list, boost: int = 0) -> int:
    for group in immune:
        group.attack += boost

    while len(immune) > 0 and len(infection) > 0:
        no_change = True
        events = []
        events.extend(get_all_targetings(infection, immune))
        events.extend(get_all_targetings(immune, infection))

        events = sorted(
            events, key=lambda e: e.attacker.initiative, reverse=True)
        for event in events:
            before = event.defender.units

            event.execute()

            after = event.defender.units
            if no_change and before != after:
                no_change = False

        if no_change:
            return 0

    return 1 if len(immune) > len(infection) else -1


def get_all_targetings(attackers: list, defenders: list) -> list:
    attackers = sorted(attackers, key=lambda g: (
        g.calc_power(), g.initiative), reverse=True)
    to_attack = defenders[:]
    events = []

    for attacker in attackers:
        targeted = get_targeting(attacker, to_attack)

        if targeted is not None:
            to_attack.remove(targeted)
            events.append(Event(attacker, targeted, attackers, defenders))

    return events


def get_targeting(attacker: Group, to_attack: list) -> Group or None:
    if len(to_attack) == 0:
        return None

    targets = sorted([defender for defender in to_attack if attacker.calc_damage_to(defender) > 0],
                     key=lambda g: (attacker.calc_damage_to(g), g.calc_power(), g.initiative), reverse=True)
    if len(targets) > 0:
        return targets[0]


def parse(input: str):
    lines = input.strip().split("\n")
    team = 0
    immune_system, infection = [], []

    for line in lines:
        if line.startswith("Immune"):
            team = 0
            continue
        elif line.startswith("Infection"):
            team = 1
            continue
        elif len(line) == 0:
            continue

        immunities = set()
        weaknesses = set()

        units, hp, extra, attack, attack_type, initiative = re.search(
            r"(\d+) units each with (\d+) hit points (?:\((.*?)\) )?with an attack that does (\d+) (.*?) damage at initiative (\d+)",
            line).groups()

        units, hp, attack, initiative = tuple(
            map(int, (units, hp, attack, initiative)))
        if extra is not None:
            for part in extra.split("; "):
                if part.startswith("immune to"):
                    for immunity in part[10:].split(", "):
                        immunities.add(immunity)
                elif part.startswith("weak to"):
                    for weak in part[8:].split(", "):
                        weaknesses.add(weak)

        group = Group(units, hp, attack, attack_type,
                        initiative, immunities, weaknesses)
        if team == 0:
            immune_system.append(group)
        else:
            infection.append(group)

    return immune_system, infection
