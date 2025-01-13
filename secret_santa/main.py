import json
import logging
from pathlib import Path
import os
import random
import time
from typing import Union

from secret_santa.emails import EmailConfig, EmailSender, MessageVariables
from secret_santa.matching import Matching, find_matching
from secret_santa.structs import MatchGroup, Participant


logging.basicConfig(level=logging.INFO)


class Settings:
    group_path = Path(os.environ['WICHTELN_GROUP_CONFIG_PATH'])
    email_map = Path(os.environ['WICHTELN_EMAIL_CONFIG_PATH'])
    _save_matching_to_raw = os.environ.get('WICHTELN_SAVE_TO')
    save_matching_to = Path(_save_matching_to_raw) if _save_matching_to_raw else None
    max_attempts = int(os.environ.get('WICHTELN_MATCHING_MAX_ATTEMPTS', 1000))


def main():
    if Settings.save_matching_to is None:
        confirm_not_saving_matching()

    logging.info(f'Importing participants information from {Settings.group_path}.')
    random.seed(int(time.time()))
    group = import_match_group(path=Settings.group_path)
    logging.info('Finding matching.')
    matching = find_matching(group=group, max_attempts=Settings.max_attempts)

    logging.info(f'Importing email-config form {Settings.email_map}.')
    email_config = import_email_config(path=Settings.email_map)
    sender = EmailSender(config=email_config)
    logging.info(f'Sending emails.')
    send_emails_for_matching(sender, matching)

    if Settings.save_matching_to is not None:
        save_matching(path=Settings.save_matching_to, matching=matching)


def confirm_not_saving_matching():
    valid_input = False
    value = input(
        "Environment variable WICHTELN_SAVE_TO is unset, meaning the "
        "secret-santa matching will be sent without you knowing. Sure you don't"
        " want to save it, e.g. to exclude whom had who this year for next "
        "year?"
        "Continue? Type 'y' to continue and 'n' to abort."
    )
    while not valid_input:
        if value == 'y':
            valid_input = True
        elif value == 'n':
            exit(0)
        else:
            value = input(
                f"{value} is not a valid response. "
                f"Continue? Type 'y' to continue and 'n' to abort."
            )


def import_match_group(path: Union[Path, str]) -> MatchGroup:
    with open(path, mode='r') as fp:
        return MatchGroup(participants=[Participant(**d) for d in json.load(fp)])


def import_email_config(path: Union[Path, str]) -> EmailConfig:
    with open(path, mode='r') as fp:
        return EmailConfig(**json.load(fp))


def send_emails_for_matching(sender: EmailSender, matching: Matching) -> None:
    for pair in matching:
        logging.info(f'Sending mail to {pair.giver}.')
        sender.send(
            to=pair.taker.email,
            message_vars=MessageVariables(taker=pair.taker.name),
        )


def save_matching(path: Union[Path, str], matching: Matching) -> None:
    with open(path, mode='w') as fp:
        json.dump(
            [{'giver': pair.giver.name, 'taker': pair.taker.name} for pair in matching],
            fp,
            indent=2
        )


if __name__ == '__main__':
    main()
