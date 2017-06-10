import json
from collections import defaultdict

import pandas as pd
from pyclustering.cluster.rock import rock

from src.analysis.data import get_team_compositions_by_name, \
    get_team_composition_from, get_team_compositions_against, get_drafts_from_major_events, get_team_compositions_with, \
    get_drafts_from_manila_major, get_drafts_from_shanghai_major
from src.database.heroes import Heroes
from src.resources.ROCK.data_point import DataPoint
from src.resources.ROCK.rock_algorithm import RockAlgorithm


def get_rock_clusters(data, min_clusters, threshold, pyclustering=True):
    if isinstance(data, pd.DataFrame):
        cl_data = data.values.tolist()

    cl_data = [sorted(d) for d in cl_data]

    if pyclustering:
        rock_instance = rock(cl_data, 0.4, min_clusters, threshold)
        rock_instance.process()
        clusters = rock_instance.get_clusters()
        return create_clusters_pyclustering_dict(clusters, data)
    else:
        points = [DataPoint(i, d)
                  for i, d in enumerate(data)]

        rock_instance = RockAlgorithm(points, min_clusters, threshold)
        rock_clusters = rock_instance.cluster()
        #
        # goodness = [float(measure)
        #             for measure in rock_clusters.level_labels[1:]][::-1]
        # if len(goodness) == 0:
        #     return None
        #
        # best_level = len(rock_clusters.level_labels) - np.argmax(goodness) - 1

        cluster_set = rock_clusters.entry_map[rock_clusters.next_level - 1]
        return create_clusters_dict(cluster_set)


def create_clusters_pyclustering_dict(clusters, data):
    cluster_dict = {}

    for cluster_id, cluster in enumerate(clusters):
        cluster_dict[cluster_id] = data.iloc[cluster]

    return cluster_dict


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


def summarize_rock_clusters(clusters, min_freq, **kwargs):
    clusters_dict = {}

    for cluster_id, cluster in clusters.items():
        readable_cluster = get_team_compositions_by_name(cluster, **kwargs)

        clusters_dict[cluster_id] = {}
        cluster_dict = defaultdict(int)

        for _, cls in readable_cluster.iterrows():
            for hero in cls.values:
                cluster_dict[hero] += 1

        for key, val in cluster_dict.items():
            if val >= min_freq:
                clusters_dict[cluster_id][key] = val

        for key in list(clusters_dict.keys()):
            if not clusters_dict[key]:
                del clusters_dict[key]

    print(json.dumps(clusters_dict, indent=4, sort_keys=True))


def cl_manila_major():
    drafts = get_drafts_from_manila_major()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)

    cluster_team_comps(team_comps)


def cl_shanghai_major():
    drafts = get_drafts_from_shanghai_major()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)
    cluster_team_comps(team_comps)


def cluster_team_comps(team_comps):
    heroes = Heroes()

    min_clusters = 150
    threshold = 0.6
    min_freq = 10
    clusters = get_rock_clusters(team_comps, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    summarize_rock_clusters(clusters, min_freq, heroes=heroes)


def cl_major_events():
    heroes = Heroes()

    drafts = get_drafts_from_major_events()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)

    min_clusters = 25
    threshold = 0.5
    min_freq = 10
    clusters = get_rock_clusters(team_comps, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    summarize_rock_clusters(clusters, min_freq, heroes=heroes)


def cl_all_against_antimage():
    heroes = Heroes()

    drafts = get_drafts_from_major_events()
    team_comps = get_team_composition_from(drafts)

    hero_id = heroes.inverse["Anti-Mage"]
    team_comps_against = get_team_compositions_against(team_comps, hero_id)
    print(heroes.heroes[hero_id])
    print(team_comps_against.shape)

    min_clusters = 15
    threshold = 0.25
    min_freq = 10
    clusters = get_rock_clusters(team_comps_against, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    summarize_rock_clusters(clusters, min_freq, heroes=heroes)


def cl_all_with_wisp():
    heroes = Heroes()

    drafts = get_drafts_from_major_events()
    team_comps = get_team_composition_from(drafts)

    hero_id = heroes.inverse["Io"]
    team_comps_with = get_team_compositions_with(team_comps, hero_id)
    print(heroes.heroes[hero_id])
    print(team_comps_with.shape)

    min_clusters = 25
    threshold = 0.4
    min_freq = 10
    clusters = get_rock_clusters(team_comps_with, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    summarize_rock_clusters(clusters, min_freq, heroes=heroes)


def main():
    # cl_major_events()
    print("Manila Major")
    cl_manila_major()
    print("Shanghai Major")
    cl_shanghai_major()
    # cl_all_against_antimage()
    # cl_all_with_wisp()


if __name__ == '__main__':
    main()
