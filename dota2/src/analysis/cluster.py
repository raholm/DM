import json
from collections import defaultdict

import pandas as pd

from src.analysis.data import get_team_compositions_by_name, get_picks_bans_international2015, \
    get_team_compositions_by_id, get_team_compositions_against
from src.database.heroes import Heroes
from src.resources.ROCK.data_point import DataPoint
from src.resources.ROCK.rock_algorithm import RockAlgorithm


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


def cl_international2015():
    pass


def cl_major_events():
    pass


def cl_all_against_antimage():
    # Check antimage order count
    heroes = Heroes()
    # print(heroes.heroes)

    picks_bans = get_picks_bans_international2015()
    team_comps = get_team_compositions_by_id(picks_bans)

    hero_id = heroes.inverse["Anti-Mage"]
    team_comps_against = get_team_compositions_against(team_comps, hero_id)
    print(heroes.heroes[hero_id])

    min_clusters = 2
    threshold = 0.3
    clusters = get_rock_clusters(team_comps_against, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    summarize_rock_clusters(clusters, heroes=heroes)


def cl_all_with_wisp():
    # Check wisp order count
    pass


def main():
    # Sort rows before clustering
    pass


if __name__ == '__main__':
    main()
