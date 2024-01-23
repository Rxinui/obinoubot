import json
import pytest
from utils.parser import PropertyParser
from utils.botconfig import BotConfig


@pytest.fixture
def botconfig() -> dict:
    return BotConfig("./tests/bot.test.json")


@pytest.fixture
def parser(botconfig) -> PropertyParser:
    parser = PropertyParser(botconfig)
    yield parser


def test_parse_one_properties(botconfig: BotConfig, parser: PropertyParser):
    assert (
        parser.parse(botconfig.commands["test_one_properties"].args.message)
        == "*Entrer vos PRs [via ce formulaire](https://docs.google.com/forms/d/e/1FAIpQLSeEomm3cNsaDCmhAfWVHP8dqGP1jGwo_MFcnEsEj2tRyLHcyQ/viewform?usp=sf_link)*"
    )


def test_parse_multiple_properties(botconfig: BotConfig, parser: PropertyParser):
    assert (
        parser.parse(botconfig.commands["test_multiple_properties"].args.message)
        == "https://docs.google.com/spreadsheets/d/1ZgHSYOkEw6VC27ZsQ930pB9pOBSwI_bvuVDaAnu7DE4/edit#gid=947482314 et https://docs.google.com/forms/u/0/d/e/1FAIpQLSeEomm3cNsaDCmhAfWVHP8dqGP1jGwo_MFcnEsEj2tRyLHcyQ/formResponse"
    )


def test_empty_properties(botconfig: BotConfig, parser: PropertyParser):
    assert (
        parser.parse(botconfig.commands["test_empty_properties"].args.message)
        == "Pas de properties"
    )
