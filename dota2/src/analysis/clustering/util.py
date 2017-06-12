import json
from collections import defaultdict

import numpy as np

from src.analysis.data import get_team_compositions_by_name


def create_clusters_dict(clusters, data):
    cluster_dict = {}

    for cluster_id, cluster in enumerate(clusters):
        cluster_dict[cluster_id] = data.iloc[cluster]

    return cluster_dict


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