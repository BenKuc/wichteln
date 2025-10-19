from collections import Counter, Hashable
from dataclasses import dataclass, field
from typing import Iterable, List, Set


@dataclass
class Participant:
    name: str
    email: str
    exclusions: Set[str] = field(default_factory=set)

    def __post_init__(self):
        self.exclusions = set(self.exclusions)
        self.exclusions.add(self.name)


def get_duplicated_values(values: Iterable[Hashable]):
    counter = Counter(values)
    return [value for value, count in counter.items() if count > 1]


@dataclass
class MatchGroup:
    participants: List[Participant]

    def __post_init__(self):
        all_names = [participant.name for participant in self.participants]

        duplicated_names = get_duplicated_values(all_names)
        if duplicated_names:
            raise ValueError(
                f"Names must be unique. Got duplications: {duplicated_names}"
            )

        exclusion_errors = {}
        all_names = set(all_names)
        for participant in self.participants:
            unknown_names = participant.exclusions.difference(all_names)
            if unknown_names:
                exclusion_errors[participant.name] = unknown_names

        if exclusion_errors:
            raise ValueError(
                "Exclusions of the following participants do not contain known names"
                f" of participants: {exclusion_errors}"
            )


@dataclass
class MatchPair:
    giver: Participant
    taker: Participant
