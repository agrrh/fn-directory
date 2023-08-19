import json

import os

# import requests

from kinopoisk_dev import KinopoiskDev

from nocodb.nocodb import NocoDBProject, APIToken
from nocodb.infra.requests_client import NocoDBRequestsClient

# from function import Payload

NOCODB_ADDR = os.environ.get("NOCODB_ADDR")
NOCODB_ORG = os.environ.get("NOCODB_ORG")
NOCODB_PROJECT = os.environ.get("NOCODB_PROJECT")

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

    # https://fn.agrrh.com/function/film_reviews_get_metadata_from_kinopoisk
    #
    # X-Auth-Token: qwerty
    #
    # {
    #   "type": "records.after.insert",
    #   "id": "81958d64-3bf6-481e-b446-0742a8a792c6",
    #   "data": {
    #     "table_id": "md_9tu40rkohb66hv",
    #     "table_name": "kinopoisk_metadata",
    #     "view_id": "vw_6my3t1p1ag2wwa",
    #     "view_name": "movies",
    #     "rows": [
    #       {
    #         "Id": 1,
    #         "url": "https://nocodb.com",
    #         "CreatedAt": "2023-08-19T11:00:22.646Z",
    #         "UpdatedAt": "2023-08-19T11:00:22.646Z",
    #         "title": "Sample Text",
    #         "title_local": "Sample Text",
    #         "genres": "Sample Text",
    #         "countries": "Sample Text",
    #         "year": "Sample Text",
    #         "duration": "Sample Text",
    #         "seasons": "Sample Text",
    #         "episodes": "Sample Text",
    #         "ageRestrictions": "Sample Text",
    #         "rating": 123.1,
    #         "topPosition": 123,
    #         "image": [
    #           {
    #             "url": "https://nocodb.com/dummy.png",
    #             "title": "image.png",
    #             "mimetype": "image/png",
    #             "size": 0
    #           }
    #         ]
    #       }
    #     ]
    #   }
    # }

    kinopoisk_id = 5012  # Gattaca
    # kinopoisk_id = 777031  # Библиотекарь

    kinopoisk_data = kinopoisk_client.find_one_movie(5012)
    print(kinopoisk_data)

    # try:
    #     payload = Payload(**json.loads(req))
    # except Exception as e:
    #     return e

    # noco_client.table_row_update(project, NOCODB_TABLE_METADATA, row_id, row_info)

    return json.dumps(
        {
            "result": True,
            "echo": json.loads(req),
            "kinopoisk_data": kinopoisk_data,
        },
    )
