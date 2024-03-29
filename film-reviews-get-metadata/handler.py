import json

import os

import re

from kinopoisk_dev import KinopoiskDev

from nocodb.nocodb import NocoDBProject, APIToken
from nocodb.infra.requests_client import NocoDBRequestsClient

NOCODB_ADDR = os.environ.get("NOCODB_ADDR")
NOCODB_ORG = os.environ.get("NOCODB_ORG")
NOCODB_PROJECT = os.environ.get("NOCODB_PROJECT")
NOCODB_TABLE_METADATA = os.environ.get("NOCODB_TABLE_METADATA")

SECRETS = {}

secrets_src = (
    "api-token",
    "auth-token",
    "kinopoisk-dev-token",
)

for s in secrets_src:
    with open(f"/var/openfaas/secrets/{s}") as fp:
        SECRETS[s] = fp.read().strip()

kinopoisk_client = KinopoiskDev(token=SECRETS["kinopoisk-dev-token"])

noco_client = NocoDBRequestsClient(
    APIToken(SECRETS["api-token"]),
    NOCODB_ADDR,
)

project = NocoDBProject(
    NOCODB_ORG,
    NOCODB_PROJECT,
)


def handle(req: str) -> dict:
    """handle a request to the function
    Args:
        req (str): request body
    """

    payload = json.loads(req)

    items = []
    for item in payload.get("data", {}).get("rows", []):
        i = {
            "row_id": item.get("Id") or item.get("id"),
            "url": item.get("url"),
        }
        i["kinopoisk_id"] = re.search(r"/(film|series)/(\d+)/?", i["url"]).groups()[1]
        items.append(i)

    for item in items:
        kinopoisk_data = kinopoisk_client.find_one_movie(item["kinopoisk_id"])

        if kinopoisk_data.type == "movie":
            seasons = 0
            episodes = 0
        elif isinstance(kinopoisk_data.seasonsInfo, tuple):
            seasons = len(list(filter(lambda season: season.episodesCount > 0, kinopoisk_data.seasonsInfo)))
            episodes_count_list = [season.episodesCount for season in kinopoisk_data.seasonsInfo]
            if min(episodes_count_list) != max(episodes_count_list):
                episodes = f"{min(episodes_count_list)}-{max(episodes_count_list)}"
            else:
                episodes = episodes_count_list[0]
        else:
            seasons = 1
            episodes = kinopoisk_data.seasonsInfo.episodesCount

        row_info = {
            "url": item["url"],
            "title": kinopoisk_data.alternativeName,
            "title_local": kinopoisk_data.name,
            "genres": ", ".join([g.name for g in kinopoisk_data.genres]),
            "countries": ", ".join([c.name for c in kinopoisk_data.countries]),
            "year": kinopoisk_data.year,
            "seasons": seasons,
            "episodes": episodes,
            "duration": int(kinopoisk_data.movieLength or 0) * 60,
            "ageRestrictions": kinopoisk_data.ageRating,
            "rating": kinopoisk_data.rating.kp,
            "topPosition": kinopoisk_data.top250,
            "image": kinopoisk_data.poster.url,
        }

        noco_client.table_row_update(project, NOCODB_TABLE_METADATA, item["row_id"], row_info)

    return json.dumps(
        {
            "result": True,
            "items": items,
            "echo": req,
        },
    )
