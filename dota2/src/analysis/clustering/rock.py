import pandas as pd
from pyclustering.cluster.rock import rock

from src.analysis.clustering.util import create_clusters_dict, summarize_clusters_by_hero_score, \
    cluster_summary_to_latex_table
from src.analysis.data import get_team_compositions_by_name, get_drafts_from_manila_major, get_team_composition_from, \
    get_drafts_from_shanghai_major
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


def create_rock_clusters_dict(clusters):
    cluster_dict = {}

    for cluster_id, cluster in enumerate(clusters.get_all_clusters()):
        cluster_elements = [element.attr
                            for element in cluster.elements]
        cluster_elements_df = pd.DataFrame(cluster_elements)
        cluster_dict[cluster_id] = cluster_elements_df

    return cluster_dict


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


def print_rock_clusters(clusters, **kwargs):
    for cluster_id, cluster in clusters.items():
        print("Cluster %i\n%s" % (cluster_id, get_team_compositions_by_name(cluster, **kwargs),))


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


def main():
    print("Manila Major")
    cl_manila_major_with_rock()
    print("Shanghai Major")
    cl_shanghai_major_with_rock()


if __name__ == '__main__':
    main()
