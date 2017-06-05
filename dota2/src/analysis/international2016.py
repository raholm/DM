from collections import defaultdict

import pandas as pd
import numpy as np
import json

from src.database.client import Dota2DBClient
from src.database.queries import get_match_ids_in_league, get_match_picks_bans_df, get_heroes_dict
from src.resources.ROCK.data_point import DataPoint
from src.resources.ROCK.rock_algorithm import RockAlgorithm
from src.resources.fpgrowth.pyfpgrowth import find_frequent_patterns, generate_association_rules


class Heroes(object):
    def __init__(self):
        self.__heroes = None
        self.__inverse = None

    @property
    def heroes(self):
        if self.__heroes is None:
            with Dota2DBClient() as client:
                self.__heroes = get_heroes_dict(client)

        return self.__heroes

    @property
    def inverse(self):
        if self.__inverse is None:
            self.__inverse = {v: k for k, v in self.heroes.items()}

        return self.__inverse


def get_picks_bans():
    with Dota2DBClient() as client:
        match_ids = [match_id for match_id in
                     get_match_ids_in_league(client, "The International 2015")]
        picks_bans = get_match_picks_bans_df(client, match_ids)

    return picks_bans


def get_team_compositions_by_id(picks_bans):
    def create_team_compositions(picks_bans):
        team_size = 5
        number_of_rows = int(picks_bans.shape[0] / 5)
        team_compositions = pd.DataFrame(index=np.arange(0, number_of_rows),
                                         columns=[1, 2, 3, 4, 5])

        for i in range(0, number_of_rows):
            start_idx = i * team_size
            end_idx = start_idx + team_size

            team_picks = picks_bans.iloc[start_idx:end_idx].hero_id
            team_composition = team_picks.values
            team_compositions.loc[i] = team_composition

        return team_compositions

    picks = picks_bans[picks_bans.is_pick]

    team0_picks = picks[picks.team == 0]
    team1_picks = picks[picks.team == 1]

    return {"team0": create_team_compositions(team0_picks),
            "team1": create_team_compositions(team1_picks)}


def get_team_compositions_by_name(team_compositions_ids, **kwargs):
    heroes = kwargs["heroes"].heroes
    return team_compositions_ids.applymap(lambda x: heroes[x])


def get_association_rules(data, min_support, min_confidence):
    if isinstance(data, pd.DataFrame):
        data = data.values.tolist()

    patterns = find_frequent_patterns(data, min_support)
    rules = generate_association_rules(patterns, min_confidence)
    return rules


def print_association_rules(rules, **kwargs):
    heroes = kwargs["heroes"].heroes

    readable_rules = list()

    for antecedent, consequent in rules.items():
        readable_antecedent = str(tuple(heroes[hero] for hero in antecedent))
        readable_consequent = str(tuple(heroes[hero] for hero in consequent[0]))
        readable_rules.append({readable_antecedent: readable_consequent})

    print(json.dumps(readable_rules, indent=4, sort_keys=True))


def get_team_compositions_against(team_comps, hero_id):
    def get_indexes(team_comps, hero_id):
        return [idx
                for idx, values in team_comps.iterrows()
                if hero_id in values.values]

    team0_comps = team_comps["team0"]
    team1_comps = team_comps["team1"]

    team0_idx = get_indexes(team0_comps, hero_id)
    team1_idx = get_indexes(team1_comps, hero_id)

    return pd.concat([team0_comps.iloc[team1_idx], team1_comps.iloc[team0_idx]])


def get_rock_clusters(data, min_clusters, threshold):
    if isinstance(data, pd.DataFrame):
        data = data.values.tolist()

    points = [DataPoint(i, d)
              for i, d in enumerate(data)]

    rock_instance = RockAlgorithm(points, min_clusters, threshold)
    rock_clusters = rock_instance.cluster()

    # goodness = [float(measure)
    #             for measure in rock_clusters.level_labels[1:]][::-1]
    # if len(goodness) == 0:
    #     return None
    #
    # best_level = len(rock_clusters.level_labels) - np.argmax(goodness) - 1

    cluster_set = rock_clusters.entry_map[rock_clusters.next_level - 1]
    clusters = create_clusters_dict(cluster_set)
    return clusters


def create_clusters_dict(clusters):
    cluster_dict = {}

    for cluster_id, cluster in enumerate(clusters.get_all_clusters()):
        cluster_elements = [element.attr
                            for element in cluster.elements]
        cluster_elements_df = pd.DataFrame(cluster_elements)
        cluster_dict[cluster_id] = cluster_elements_df

    return cluster_dict


def print_rock_clusters(clusters, **kwargs):
    for cluster_id, cluster in clusters.items():
        print("Cluster %i\n%s" % (cluster_id, get_team_compositions_by_name(cluster, **kwargs),))


def summarize_rock_clusters(clusters, **kwargs):
    clusters_dict = {}
    min_frequency = 2

    for cluster_id, cluster in clusters.items():
        readable_cluster = get_team_compositions_by_name(cluster, **kwargs)

        clusters_dict[cluster_id] = {}
        cluster_dict = defaultdict(int)

        for _, cls in readable_cluster.iterrows():
            for hero in cls.values:
                cluster_dict[hero] += 1

        for key, val in cluster_dict.items():
            if val >= min_frequency:
                clusters_dict[cluster_id][key] = val

    print(json.dumps(clusters_dict, indent=4, sort_keys=True))


def main():
    heroes = Heroes()
    # print(heroes.heroes)

    picks_bans = get_picks_bans()
    team_comps = get_team_compositions_by_id(picks_bans)

    hero_id = heroes.inverse["Storm Spirit"]
    team_comps_against = get_team_compositions_against(team_comps, hero_id)
    print(heroes.heroes[hero_id])

    min_clusters = 2
    threshold = 0.3
    clusters = get_rock_clusters(team_comps_against, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    summarize_rock_clusters(clusters, heroes=heroes)

    min_support = int(team_comps_against.shape[0] * 0.04)
    min_confidence = 0.9
    rules = get_association_rules(team_comps_against, min_support, min_confidence)
    print_association_rules(rules, heroes=heroes)


if __name__ == '__main__':
    main()
