import random
from typing import Iterable, List

from secret_santa.structs import MatchGroup, MatchPair


Matching = List[MatchPair]


def find_matching(group: MatchGroup, max_attempts: int) -> Matching:
    for _ in range(max_attempts):
        try:
            return _get_matching(group)
        except RuntimeError:
            continue
    else:
        raise NotImplementedError(
            f"Tried {max_attempts} times. Maybe there is no valid solution."
        )


def _get_matching(group: MatchGroup) -> Matching:
    participants_map = {
        participant.name: participant for participant in group.participants
    }
    available_as_taker = set(participants_map.keys())
    available_as_giver = set(participants_map.keys())
    matching = []
    while available_as_giver:
        givers_name = _random_choice(available_as_giver)
        giver = participants_map[givers_name]

        takers_to_choose_from = set(available_as_taker).difference(giver.exclusions)
        if not takers_to_choose_from:
            raise RuntimeError('Ran into deadend.')

        takers_name = _random_choice(takers_to_choose_from)
        matching.append(MatchPair(giver, taker=participants_map[takers_name]))
        available_as_taker.remove(takers_name)
        available_as_giver.remove(givers_name)

    return matching


def _random_choice(iterable: Iterable):
    return random.choice(list(iterable))  # needs to support index -> convert to list
