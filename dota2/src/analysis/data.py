import numpy as np
import pandas as pd
from collections import defaultdict

from src.database.client import Dota2DBClient
from src.database.queries import get_match_ids_in_league, get_draft_from_df


def get_team_composition_from(draft, by_team=True):
    def create_team_compositions(draft):
        team_size = 5
        number_of_rows = int(draft.shape[0] / 5)
        team_compositions = pd.DataFrame(index=np.arange(0, number_of_rows),
                                         columns=[1, 2, 3, 4, 5])

        for i in range(0, number_of_rows):
            start_idx = i * team_size
            end_idx = start_idx + team_size

            team_picks = draft.iloc[start_idx:end_idx].hero_id
            team_composition = team_picks.values
            team_compositions.loc[i] = team_composition

        return team_compositions

    picks = draft[draft.is_pick]

    team0_picks = picks[picks.team == 0]
    team1_picks = picks[picks.team == 1]

    if by_team:
        return {"team0": create_team_compositions(team0_picks),
                "team1": create_team_compositions(team1_picks)}
    else:
        return pd.concat([create_team_compositions(team0_picks),
                          create_team_compositions(team1_picks)])


def get_team_compositions_by_name(team_compositions_ids, **kwargs):
    heroes = kwargs["heroes"].heroes
    return team_compositions_ids.applymap(lambda x: heroes[x])


def get_team_compositions_against(team_comps, hero_id):
    team0_comps = team_comps["team0"]
    team1_comps = team_comps["team1"]

    team0_idx = _get_indexes_with_hero(team0_comps, hero_id)
    team1_idx = _get_indexes_with_hero(team1_comps, hero_id)

    return pd.concat([team0_comps.iloc[team1_idx], team1_comps.iloc[team0_idx]])


def get_team_compositions_with(team_comps, hero_id):
    team0_comps = team_comps["team0"]
    team1_comps = team_comps["team1"]

    team0_idx = _get_indexes_with_hero(team0_comps, hero_id)
    team1_idx = _get_indexes_with_hero(team1_comps, hero_id)

    return pd.concat([team0_comps.iloc[team0_idx], team1_comps.iloc[team1_idx]])


def _get_indexes_with_hero(team_comps, hero_id):
    return [idx
            for idx, values in team_comps.iterrows()
            if hero_id in values.values]


def get_hero_pick_statistics(team_comps, hero_id_or_ids, heroes):
    statistics = {}

    try:
        iter(hero_id_or_ids)
    except TypeError:
        hero_id_or_ids = [hero_id_or_ids]

    for hero_id in hero_id_or_ids:
        hero_name = heroes.heroes[hero_id]
        statistics[hero_name] = defaultdict(int)

    for _, team_comp in team_comps.iterrows():
        team_comp = team_comp.values

        position_hero_gen = ((position, hero_id)
                             for position, hero_id in enumerate(team_comp)
                             if hero_id in hero_id_or_ids)

        for position, hero_id in position_hero_gen:
            hero_name = heroes.heroes[hero_id]
            statistics[hero_name][position + 1] += 1

    return statistics


def get_drafts_from_shanghai_major():
    return get_drafts_from("The Shanghai Major 2016")


def get_drafts_from_manila_major():
    return get_drafts_from("The Manila Major 2016")


def get_drafts_from(league):
    with Dota2DBClient() as client:
        match_ids = [match_id for match_id in
                     get_match_ids_in_league(client, league)]
        draft = get_draft_from_df(client, match_ids)

    return draft


def get_drafts_from_major_events():
    major_events = ["The Frankfurt Major 2015",
                    "The Shanghai Major 2016",
                    "The Manila Major 2016",
                    "The Boston Major 2016",
                    "The Kiev Major 2017",
                    "The International 2012",
                    "The International 2013",
                    "The International 2014",
                    "The International 2015",
                    "The International 2016"]

    match_ids = []

    with Dota2DBClient() as client:
        for league in major_events:
            match_ids += get_match_ids_in_league(client, league)

        draft = get_draft_from_df(client, match_ids)

    return draft
