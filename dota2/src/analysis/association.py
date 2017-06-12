import json

import pandas as pd

from src.analysis.data import get_team_composition_from, \
    get_team_compositions_against, get_drafts_from_major_events, get_hero_pick_statistics
from src.database.heroes import Heroes
from src.resources.fpgrowth.pyfpgrowth import find_frequent_patterns, generate_association_rules


def get_association_rules(data, min_support, min_confidence):
    if isinstance(data, pd.DataFrame):
        data = data.values.tolist()

    patterns = find_frequent_patterns(data, min_support)
    print("Number of frequent patterns: %i" % (len(patterns)))
    rules = generate_association_rules(patterns, min_confidence)
    print("Number of rules: %i" % (len(rules)))
    return rules


def print_association_rules(rules, **kwargs):
    heroes = kwargs["heroes"].heroes

    readable_rules = list()

    for antecedent, consequent in rules.items():
        readable_antecedent = str(tuple(heroes[hero] for hero in antecedent))
        readable_consequent = str(tuple(heroes[hero] for hero in consequent[0]))
        readable_rules.append({readable_antecedent: readable_consequent})

    print(json.dumps(readable_rules, indent=4, sort_keys=True))


def print_association_rules_with(rules, hero_id, **kwargs):
    heroes = kwargs["heroes"].heroes

    readable_rules = list()

    for antecedent, consequent in rules.items():
        consequent = consequent[0]

        if hero_id not in antecedent and hero_id not in consequent:
            continue

        readable_antecedent = str(tuple(heroes[hero] for hero in antecedent))
        readable_consequent = str(tuple(heroes[hero] for hero in consequent))
        readable_rules.append({readable_antecedent: readable_consequent})

    print(json.dumps(readable_rules, indent=4, sort_keys=True))


def ass_international2015():
    pass


def ass_major_events():
    heroes = Heroes()

    picks_bans = get_drafts_from_major_events()
    team_comps = get_team_composition_from(picks_bans)
    team_comps = pd.concat([team_comps["team0"], team_comps["team1"]])

    min_supports = [10, 25, 50, 100]
    min_confidences = [0.8, 0.25, 0.2, 0.5]

    for min_support, min_confidence in zip(min_supports, min_confidences):
        print("Support=%i, Confidence=%.2f" % (min_support, min_confidence,))
        rules = get_association_rules(team_comps, min_support, min_confidence)
        print_association_rules(rules, heroes=heroes)


def ass_all_against_antimage():
    heroes = Heroes()

    picks_bans = get_drafts_from_major_events()
    team_comps = get_team_composition_from(picks_bans)

    hero_id = heroes.inverse["Anti-Mage"]
    team_comps_against = get_team_compositions_against(team_comps, hero_id, positions=[4, 5])

    print(team_comps_against.shape)
    print(heroes.heroes[hero_id])

    min_supports = [5]
    min_confidences = [0.5]

    for min_support, min_confidence in zip(min_supports, min_confidences):
        print("Support=%i, Confidence=%.2f" % (min_support, min_confidence,))
        rules = get_association_rules(team_comps_against, min_support, min_confidence)
        print_association_rules(rules, heroes=heroes)

    antimage_statistics = get_hero_pick_statistics(pd.concat([team_comps["team0"],
                                                              team_comps["team1"]]),
                                                   hero_id,
                                                   heroes)
    print(antimage_statistics)


def ass_all_against_clinkz():
    heroes = Heroes()

    picks_bans = get_drafts_from_major_events()
    team_comps = get_team_composition_from(picks_bans)

    hero_id = heroes.inverse["Clinkz"]
    team_comps_against = get_team_compositions_against(team_comps, hero_id, positions=[4, 5])

    print(team_comps_against.shape)
    print(heroes.heroes[hero_id])

    min_supports = [5]
    min_confidences = [0.5]

    for min_support, min_confidence in zip(min_supports, min_confidences):
        print("Support=%i, Confidence=%.2f" % (min_support, min_confidence,))
        rules = get_association_rules(team_comps_against, min_support, min_confidence)
        print_association_rules(rules, heroes=heroes)

    clinkz_statistics = get_hero_pick_statistics(pd.concat([team_comps["team0"],
                                                              team_comps["team1"]]),
                                                   hero_id,
                                                   heroes)
    print(clinkz_statistics)


def ass_all_with_wisp():
    heroes = Heroes()

    picks_bans = get_drafts_from_major_events()
    team_comps = get_team_composition_from(picks_bans, by_team=False)

    hero_id = heroes.inverse["Io"]
    # team_comps_with = get_team_compositions_with(team_comps, hero_id)
    print(heroes.heroes[hero_id])
    # print(team_comps_with.shape)
    print(team_comps.shape)

    min_supports = [10]
    min_confidences = [0.5]

    for min_support, min_confidence in zip(min_supports, min_confidences):
        print("Support=%i, Confidence=%.2f" % (min_support, min_confidence,))
        rules = get_association_rules(team_comps, min_support, min_confidence)
        print_association_rules_with(rules, hero_id, heroes=heroes)

    io_statistics = get_hero_pick_statistics(team_comps,
                                             hero_id,
                                             heroes)
    print(io_statistics)


def ass_all_with_magnus():
    heroes = Heroes()

    picks_bans = get_drafts_from_major_events()
    team_comps = get_team_composition_from(picks_bans, by_team=False)

    hero_id = heroes.inverse["Magnus"]
    # team_comps_with = get_team_compositions_with(team_comps, hero_id)
    print(heroes.heroes[hero_id])
    # print(team_comps_with.shape)
    print(team_comps.shape)

    min_supports = [5]
    min_confidences = [0.5]

    for min_support, min_confidence in zip(min_supports, min_confidences):
        print("Support=%i, Confidence=%.2f" % (min_support, min_confidence,))
        rules = get_association_rules(team_comps, min_support, min_confidence)
        print_association_rules_with(rules, hero_id, heroes=heroes)

    magnus_statistics = get_hero_pick_statistics(team_comps,
                                                 hero_id,
                                                 heroes)
    print(magnus_statistics)


def main():
    # ass_major_events()
    ass_all_against_antimage()
    ass_all_against_clinkz()
    # ass_all_with_wisp()
    # ass_all_with_magnus()


if __name__ == '__main__':
    main()
