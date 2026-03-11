#!/usr/bin/env python3

import argparse
from enum import Enum
import os

"""
Input file format:
M, Steve Smith
F, Taylor Swift
f, Helen Parr
m, Bob Parr
M, Jacob
M, Tim F Jones
m, Tim A Jones
"""

class Gender(Enum):
    Male = 1
    Female = 2

class Team():
    def __init__(self, male1, male2, female1, female2):
        if male1.gender != Gender.Male or male2.gender != Gender.Male:
            raise ValueError("Cannot add female as male player: %s or %s" % (str(male1), str(male2)))
        if female1.gender != Gender.Female or female2.gender != Gender.Female:
            raise ValueError("Cannot add male as female player: %s or %s" % (str(female1), str(female2)))
        self.male1 = male1
        self.male2 = male2
        self.female1 = female1
        self.female2 = female2
        self.male1.add_teammates(male2, female1, female2)
        self.male2.add_teammates(male1, female1, female2)
        self.female1.add_teammates(female2, male1, male2)
        self.female2.add_teammates(female1, male1, male2)
    def add_opponent(self, other_team):
        self.male1.add_opposing_team(other_team)
        self.male2.add_opposing_team(other_team)
        self.female1.add_opposing_team(other_team)
        self.female2.add_opposing_team(other_team)
    def __str__(self):
        return self.male1.name + ", " + self.male2.name + ", " + self.female1.name + ", " + self.female2.name

class Player():
    def __init__(self, name, gender):
        self.gender = gender
        self.name = name
        self.same_gender_teammates = []
        self.opposite_gender_teammates = []
        self.same_gender_opponents = []
        self.opposite_gender_opponents = []
        self.same_teammate_frequency = {}
        self.opposite_teammate_frequency = {}
        self.same_opponent_frequency = {}
        self.opposite_opponent_frequency = {}
    def add_same_gender_partner(self, partner_name):
        self.same_gender_teammates.append(partner_name)
        try:
            self.same_teammate_frequency[partner_name] += 1
        except KeyError:
            self.same_teammate_frequency[partner_name] = 1
    def add_opposite_gender_partner(self, partner_name):
        self.opposite_gender_teammates.append(partner_name)
        try:
            self.opposite_teammate_frequency[partner_name] += 1
        except KeyError:
            self.opposite_teammate_frequency[partner_name] = 1
    def add_teammates(self, same_partner, opposite_partner1, opposite_partner2):
        self.add_same_gender_partner(same_partner.name)
        self.add_opposite_gender_partner(opposite_partner1.name)
        self.add_opposite_gender_partner(opposite_partner2.name)
    def add_same_gender_opponent(self, opponent_name):
        self.same_gender_oppoents.append(opponent_name)
        try:
            self.same_opponent_frequency[opponent_name] += 1
        except KeyError:
            self.same_opponent_frequency[opponent_name] = 1
    def add_opposite_gender_opponent(self, opponent_name):
        self.opposite_gender_opponents.append(opponent_name)
        try:
            self.opposite_opponent_frequency[opponent_name] += 1
        except KeyError:
            self.opposite_opponent_frequency[opponent_name] = 1
    def add_opposing_team(self, team):
        if self.gender == Gender.Male:
            self.add_same_gender_opponent(team.male1.name)
            self.add_same_gender_opponent(team.male2.name)
            self.add_opposite_gender_opponent(team.female1.name)
            self.add_opposite_gender_opponent(team.female2.name)
        else:
            self.add_same_gender_opponent(team.female1.name)
            self.add_same_gender_opponent(team.female2.name)
            self.add_opposite_gender_opponent(team.male1.name)
            self.add_opposite_gender_opponent(team.male2.name)
    def score_potential_same_gender_teammates(self, names):
        name_to_score = {}
        for name in names:
            score = self.same_teammate_frequency[name] if name in self.same_teammate_frequency else 0
            score *= len(self.same_gender_teammates)
            for i in range(len(self.same_gender_teammates) - 1, -1, -1):
                if self.same_gender_teammates[i] == name:
                    score += i
                    break
            name_to_score[name] = score
        return name_to_score    
    def score_potential_opposite_gender_teammates(self, names):
        name_to_score = {}
        for name in names:
            score = self.opposite_teammate_frequency[name] if name in self.opposite_teammate_frequency else 0
            score *= len(self.opposite_gender_teammates)
            for i in range(len(self.opposite_gender_teammates) - 1, -1, -1):
                if self.opposite_gender_teammates[i] == name:
                    score += i
                    break
            name_to_score[name] = score
        return name_to_score    
    def __str__(self):
        return self.name + ", " + str(self.gender)

def choose_first_male_player(available_male_indices):
    for index in available_male_indices:
        return index
    raise ValueError("No available male players.")

def choose_second_male_player(first_male_player, available_male_indices, male_players):
    name_to_score = first_male_player.score_potential_same_gender_teammates([player.name for player in male_players])
    index_to_score = {i: name_to_score[male_players[i].name] for i in available_male_indices}
    return min(available_male_indices, key=lambda i: index_to_score[i])

def choose_first_female_player(male1, male2, available_female_indices, female_players):
    name_to_score1 = male1.score_potential_opposite_gender_teammates([player.name for player in female_players])
    name_to_score2 = male2.score_potential_opposite_gender_teammates([player.name for player in female_players])
    index_to_score = {i: name_to_score1[female_players[i].name] + name_to_score2[female_players[i].name] for i in available_female_indices}
    return min(available_female_indices, key=lambda i: index_to_score[i])

def choose_second_female_player(female1, male1, male2, available_female_indices, female_players):
    name_to_score0 = female1.score_potential_same_gender_teammates([player.name for player in female_players])
    name_to_score1 = male1.score_potential_opposite_gender_teammates([player.name for player in female_players])
    name_to_score2 = male2.score_potential_opposite_gender_teammates([player.name for player in female_players])
    index_to_score = {i: name_to_score0[female_players[i].name] + name_to_score1[female_players[i].name] + name_to_score2[female_players[i].name] for i in available_female_indices}
    return min(available_female_indices, key=lambda i: index_to_score[i])

def main():
    parser = argparse.ArgumentParser(description="Create a pickleball schedule from input text file of names.")
    parser.add_argument("-n", "--names-file", required=True, help="Path to text file of names")
    parser.add_argument("-o", "--output-file", required=True, help="Path to output text file")
    parser.add_argument("-w", "--num-weeks", required=True, type=int, help="Number of weeks to make schedule for")
    parser.add_argument("-m", "--num-matchups", default=2, type=int, help="Number of matchups per week")

    args = parser.parse_args()

    male_names = []
    female_names = []
    unique_names = set()
    f = open(args.names_file, 'r', encoding='utf-8')
    for line in f:
        if len(line.split(',')) > 2:
            raise ValueError("Either a line has more than one comma or there is a comma in someone's name: %s" % (line))
        elif len(line.split(',')) < 2:
            raise ValueError("Line does not have a comma: %s" % (line))
        gender_char, name = line.split(',')
        name = name.strip()
        if gender_char.lower() == 'm':
            if name.lower() in unique_names:
                raise ValueError("Name appears twice: %s" % (name))
            unique_names.add(name.lower())
            male_names.append(name)
        elif gender_char.lower() == 'f':
            if name.lower() in unique_names:
                raise ValueError("Name appears twice: %s" % (name))
            unique_names.add(name.lower())
            female_names.append(name)
        else:
            raise ValueError("Invalid gender character: %s" % (gender_char))
    f.close()

    if len(male_names) != len(female_names):
        raise ValueError("Unequal number of male (%d) and female (%d) players." % (len(male_names), len(female_names)))
    if (len(male_names) + len(female_names)) % 4 != 0:
        raise ValueError("Total number of players must be divisible by 4, but %d is not." % (len(male_names) + len(female_names)))

    male_names.sort()
    female_names.sort()

    male_players = [Player(name, Gender.Male) for name in male_names]
    female_players = [Player(name, Gender.Female) for name in female_names]

    num_teams = (len(male_names) + len(female_names)) // 4

    for i in range(args.num_weeks):
        available_male_indices = set([i for i in range(0, len(male_names))])
        available_female_indices = set([i for i in range(0, len(female_names))])
        teams = []
        for j in range(num_teams):
            male1_index = choose_first_male_player(available_male_indices)
            available_male_indices.remove(male1_index)
            male1 = male_players[male1_index]
            male2_index = choose_second_male_player(male1, available_male_indices, male_players)
            available_male_indices.remove(male2_index)
            male2 = male_players[male2_index]
            #male1.add_same_gender_partner(male2.name)
            #male2.add_same_gender_partner(male1.name)
            female1_index = choose_first_female_player(male1, male2, available_female_indices, female_players)
            available_female_indices.remove(female1_index)
            female1 = female_players[female1_index]
            female2_index = choose_second_female_player(female1, male1, male2, available_female_indices, female_players)
            available_female_indices.remove(female2_index)
            female2 = female_players[female2_index]
            teams.append(Team(male1, male2, female1, female2))
        print("Week %d" % (i + 1))
        print("=============================")
        for j in range(len(teams)):
            print("Team %d: %s" % (j + 1, str(teams[j])))

    print("Teammate strings")
    for player in male_players:
        s = ""
        for name in male_names:
            if name == player.name:
                s += 'x'
            elif name in player.same_teammate_frequency:
                s += str(player.same_teammate_frequency[name])
            else:
                s += '0'
        print(player.name)
        print("Male partners: " + s)
        s = ""
        for name in female_names:
            if name in player.opposite_teammate_frequency:
                s += str(player.opposite_teammate_frequency[name])
            else:
                s += '0'
        print("Female partners: " + s)

if __name__ == "__main__":
    main()
