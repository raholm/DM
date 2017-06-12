import json
from collections import defaultdict

import pandas as pd
import numpy as np

from kmodes.kmodes import KModes
from pyclustering.cluster.rock import rock

from src.analysis.data import get_team_compositions_by_name, \
    get_team_composition_from, \
    get_drafts_from_manila_major, get_drafts_from_shanghai_major
from src.database.heroes import Heroes
from src.resources.ROCK.data_point import DataPoint
from src.resources.ROCK.rock_algorithm import RockAlgorithm


def get_rock_clusters(data, min_clusters, threshold, pyclustering=True):
    if isinstance(data, pd.DataFrame):
        cl_data = data.values.tolist()
    else:
        cl_data = data

    if pyclustering:
        # rock_instance = rock(cl_data, 0.4, min_clusters, threshold, False)
        rock_instance = rock(cl_data, 0.4, min_clusters, threshold, True)
        rock_instance.process()
        clusters = rock_instance.get_clusters()
        return create_clusters_dict(clusters, data)
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
        return create_rock_clusters_dict(cluster_set)


def create_clusters_dict(clusters, data):
    cluster_dict = {}

    for cluster_id, cluster in enumerate(clusters):
        cluster_dict[cluster_id] = data.iloc[cluster]

    return cluster_dict


def create_rock_clusters_dict(clusters):
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


def summarize_clusters_by_frequency(clusters, min_freq, **kwargs):
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


def summarize_clusters_by_sampling(clusters, n_samples, **kwargs):
    clusters_dict = {}

    for cluster_id, cluster in clusters.items():
        readable_cluster = get_team_compositions_by_name(cluster, **kwargs)
        samples = readable_cluster.sample(n_samples)
        clusters_dict[cluster_id] = samples.values.tolist()

    print(json.dumps(clusters_dict, indent=4, sort_keys=True))


def summarize_clusters_by_hero_score(clusters, min_samples, min_size=0, **kwargs):
    def get_hero_scores(cluster):
        hero_scores = defaultdict(int)

        for _, obs in cluster.iterrows():
            for hero in obs.values:
                hero_scores[hero] += 1

        return hero_scores

    def sort_cluster_obs_by_hero_scores(cluster, hero_scores):
        obs_scores = []

        for _, obs in cluster.iterrows():
            score = 0
            for hero in obs.values:
                score += hero_scores[hero]
            obs_scores.append(score)

        order = np.argsort(np.array(obs_scores))[::-1]
        ordered_cluster = cluster.iloc[order]
        ordered_cluster.reset_index(drop=True, inplace=True)
        return ordered_cluster

    cluster_summary = {}
    sample_portion = 0.05

    for cluster_id, cluster in clusters.items():
        cluster_size = cluster.shape[0]
        num_of_samples = np.max([min_samples, int(cluster_size * sample_portion)])

        if cluster_size < min_size:
            continue

        hero_scores = get_hero_scores(cluster)
        sorted_cluster = sort_cluster_obs_by_hero_scores(cluster, hero_scores)

        cluster = sorted_cluster.iloc[:num_of_samples]
        readable_cluster = get_team_compositions_by_name(cluster, **kwargs)

        cluster_output = []
        for obs, readable_obs in zip(cluster.values.tolist(), readable_cluster.values.tolist()):
            hero_and_score = {}
            for ob, rob in zip(obs, readable_obs):
                hero_and_score[rob] = hero_scores[ob]

            cluster_output.append(hero_and_score)

        cluster_summary[cluster_id] = [{"size": cluster_size}, cluster_output]

    # print(json.dumps(cluster_summary, indent=4, sort_keys=True))
    return cluster_summary


def cl_manila_major_with_rock():
    drafts = get_drafts_from_manila_major()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)

    cluster_team_comps_with_rock(team_comps)


def cl_shanghai_major_with_rock():
    drafts = get_drafts_from_shanghai_major()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)
    cluster_team_comps_with_rock(team_comps)


def cluster_team_comps_with_rock(team_comps):
    heroes = Heroes()

    min_clusters = 150
    threshold = 0.6
    min_freq = 10
    n_samples = 2
    min_size = 10
    clusters = get_rock_clusters(team_comps, min_clusters, threshold)
    # print_rock_clusters(clusters, heroes=heroes)
    # summarize_clusters_by_frequency(clusters, min_freq, heroes=heroes)
    cluster_summary = summarize_clusters_by_hero_score(clusters, n_samples, min_size, heroes=heroes)
    cluster_summary_to_latex_table(cluster_summary)


def cl_manila_major_with_kmodes():
    drafts = get_drafts_from_manila_major()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)
    cluster_team_comps_with_kmodes(team_comps)


def cl_shanghai_major_with_kmodes():
    drafts = get_drafts_from_shanghai_major()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)
    cluster_team_comps_with_kmodes(team_comps)


def cluster_team_comps_with_kmodes(team_comps):
    heroes = Heroes()

    n_clusters = 10
    min_freq = 10
    n_samples = 2
    clusters, centroids = get_kmodes_clusters(team_comps, n_clusters)
    # summarize_clusters_by_frequency(clusters, min_freq, heroes=heroes)
    # summarize_clusters_by_sampling(clusters, n_samples, heroes=heroes)
    cluster_summary = summarize_clusters_by_hero_score(clusters, n_samples, heroes=heroes)
    cluster_summary_to_latex_table(cluster_summary)


def print_kmodes_centroids(centroids, heroes):
    for centroid_id, centroid in enumerate(centroids):
        readable_centroid = [heroes.heroes[hero_id] for hero_id in centroid]
        print("Centroid %i: %s" % (centroid_id, readable_centroid))


def cluster_summary_to_latex_table(cluster_summary):
    prefix = """
    \\begin{table}[H]
    \\centering
    \\begin{tabular}{ | c | p{12.5cm} | }
    \\hline
    \\multicolumn{2}{ | c | }{Clusters} \\\\
    \\hline
    Size & Samples \\\\ \hline
    """

    postfix = """
    \\end{tabular}
    \caption{}
    \label{}
    \end{table}
    """

    content = ""
    total_points = 0

    for cluster_id, cluster in cluster_summary.items():
        cluster_size = cluster[0]["size"]
        total_points += cluster_size
        num_of_obs = len(cluster[1])

        table_entry = "\\multirow{%i}{*}{%i}\n" % (num_of_obs, cluster_size)

        for obs in cluster[1]:
            table_entry += "& "
            for hero, count in obs.items():
                table_entry += "%s: %i, " % (hero, count)

            table_entry = table_entry[:-2]
            table_entry += " \\\\\n"

        content += table_entry + "\\hline\n"

    table = prefix + content[:-1] + postfix
    print(table)
    print(total_points)


def get_kmodes_clusters(data, n_clusters, **kwargs):
    def dissimilarity(a, b):
        dissimilarities = []

        for element in a:
            mismatch_count = 0
            if element not in b:
                mismatch_count += 1
            dissimilarities.append(mismatch_count)

        return dissimilarities

    if isinstance(data, pd.DataFrame):
        cl_data = data.values.tolist()
    else:
        cl_data = data

    # kmodes_instance = KModes(n_clusters=n_clusters, cat_dissim=dissimilarity, **kwargs)
    kmodes_instance = KModes(n_clusters=n_clusters, **kwargs)
    cluster_labels = kmodes_instance.fit_predict(cl_data)

    clusters = {label: [] for label in range(0, n_clusters)}

    for row, label in enumerate(cluster_labels):
        clusters[label].append(row)

    clusters = [cluster for cluster in clusters.values()]

    return create_clusters_dict(clusters, data), kmodes_instance.cluster_centroids_


def main():
    # print("All Major Events")
    # cl_major_events()
    print("Manila Major")
    cl_manila_major_with_rock()
    # cl_manila_major_with_kmodes()
    print("Shanghai Major")
    cl_shanghai_major_with_rock()
    # cl_shanghai_major_with_kmodes()


if __name__ == '__main__':
    main()
