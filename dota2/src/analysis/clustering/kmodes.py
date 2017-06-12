import pandas as pd
from kmodes.kmodes import KModes

from src.analysis.clustering.util import summarize_clusters_by_hero_score, cluster_summary_to_latex_table, \
    create_clusters_dict
from src.analysis.data import get_drafts_from_manila_major, get_team_composition_from, get_drafts_from_shanghai_major, \
    get_drafts_from_major_events
from src.database.heroes import Heroes


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

    if kwargs.get("mydist", False):
        kmodes_instance = KModes(n_clusters=n_clusters, cat_dissim=dissimilarity, **kwargs)
    else:
        kmodes_instance = KModes(n_clusters=n_clusters, **kwargs)

    cluster_labels = kmodes_instance.fit_predict(cl_data)

    clusters = {label: [] for label in range(0, n_clusters)}

    for row, label in enumerate(cluster_labels):
        clusters[label].append(row)

    clusters = [cluster for cluster in clusters.values()]

    return create_clusters_dict(clusters, data), kmodes_instance.cluster_centroids_


def cluster_team_comps_with_kmodes(team_comps, **kwargs):
    heroes = Heroes()

    kwargs["n_clusters"] = kwargs.get("n_clusters", 10)
    min_freq = kwargs.get("min_freq", 10)
    n_samples = kwargs.get("n_samples", 2)
    clusters, centroids = get_kmodes_clusters(team_comps, **kwargs)
    # summarize_clusters_by_frequency(clusters, min_freq, heroes=heroes)
    # summarize_clusters_by_sampling(clusters, n_samples, heroes=heroes)
    cluster_summary = summarize_clusters_by_hero_score(clusters, n_samples, heroes=heroes)
    cluster_summary_to_latex_table(cluster_summary)


def print_kmodes_centroids(centroids, heroes):
    for centroid_id, centroid in enumerate(centroids):
        readable_centroid = [heroes.heroes[hero_id] for hero_id in centroid]
        print("Centroid %i: %s" % (centroid_id, readable_centroid))


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


def cl_major_events():
    drafts = get_drafts_from_major_events()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)
    cluster_team_comps_with_kmodes(team_comps, n_clusters=50)


def main():
    print("Major Events")
    cl_major_events()
    # print("Manila Major")
    # cl_manila_major_with_kmodes()
    # print("Shanghai Major")
    # cl_shanghai_major_with_kmodes()


if __name__ == '__main__':
    main()
