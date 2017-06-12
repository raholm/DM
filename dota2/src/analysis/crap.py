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

def cl_major_events():
    drafts = get_drafts_from_major_events()
    team_comps = get_team_composition_from(drafts, by_team=False)

    print(team_comps.shape)
    cluster_team_comps_with_rock(team_comps)
