#!/usr/bin/env python3

import itertools

def make_schedule(num_players, num_weeks_left, teammate_lists):
    if not is_valid(teammate_lists, num_players):
        return None
    if num_weeks_left == 0:
        return teammate_lists
    for p in itertools.permutations(range(1, num_players + 1)):
        # We don't need to consider permutations where the partners of a team are in the wrong order
        skip = False
        for i in range(0, num_players, 2):
            if p[i] > p[i + 1]:
                skip = True
                break
        if skip:
            continue

        updated_teammate_lists = teammate_lists + [p]
        recursive_result = make_schedule(num_players, num_weeks_left - 1, updated_teammate_lists)
        if recursive_result != None:
            return recursive_result
    return None

def get_frequency_maps(teammate_lists, num_players):
    map_of_maps = {}
    for i in range(1, num_players + 1):
        player_to_frequency = {p: 0 for p in range(1, num_players + 1) if p != i}
        for teammate_list in teammate_lists:
            for j in range(0, len(teammate_list), 2):
                teammate = None
                if teammate_list[j] == i:
                    teammate = teammate_list[j + 1]
                    break
                elif teammate_list[j + 1] == i:
                    teammate = teammate_list[j]
                    break
            player_to_frequency[teammate] += 1
        map_of_maps[i] = player_to_frequency
    return map_of_maps

def frequency_string(i, frequency_map, num_players):
    s = ""
    for p in range(1, num_players + 1):
        if p == i:
            s += '[x]'
        else:
            s += '[' + str(frequency_map[p]) + ']'
    return s

def is_valid(teammate_lists, num_players):
    for i in range(1, num_players + 1):
        player_to_frequency = {p: 0 for p in range(1, num_players + 1) if p != i}
        last_teammate = None
        second_to_last_teammate = None
        for teammate_list in teammate_lists:
            for j in range(0, len(teammate_list), 2):
                teammate = None
                if teammate_list[j] == i:
                    teammate = teammate_list[j + 1]
                    break
                elif teammate_list[j + 1] == i:
                    teammate = teammate_list[j]
                    break
            if teammate == last_teammate or teammate == second_to_last_teammate:
                return False
            player_to_frequency[teammate] += 1
            second_to_last_teammate = last_teammate
            last_teammate = teammate
        max_freq = max([player_to_frequency[f] for f in player_to_frequency if f != i])
        min_freq = min([player_to_frequency[f] for f in player_to_frequency if f != i])
        if max_freq - min_freq > 1:
            return False
    return True

def main():
    N = 12
    W = 16
    teammate_lists = make_schedule(N, W, [])
    print(teammate_lists)
    frequency_maps = get_frequency_maps(teammate_lists, N)
    for i in range(1, N + 1):
        print(i, frequency_string(i, frequency_maps[i], N))

if __name__ == "__main__":
    main()
