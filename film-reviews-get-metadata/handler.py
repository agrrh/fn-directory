import json

# import os
# import requests

import re

from kinopoisk_dev import KinopoiskDev

# from nocodb.nocodb import NocoDBProject, APIToken
# from nocodb.infra.requests_client import NocoDBRequestsClient

# NOCODB_ADDR = os.environ.get("NOCODB_ADDR")
# NOCODB_ORG = os.environ.get("NOCODB_ORG")
# NOCODB_PROJECT = os.environ.get("NOCODB_PROJECT")

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

# noco_client = NocoDBRequestsClient(
#     APIToken(SECRETS["api-token"]),
#     NOCODB_ADDR,
# )
#
# project = NocoDBProject(
#     NOCODB_ORG,
#     NOCODB_PROJECT,
# )


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
        i["kinopoisk_id"] = re.search(r"/(movie|series)/(\d+)/?", i["url"]).group()[1]
        items.append(i)

    # kinopoisk_id = 5012  # Gattaca
    # kinopoisk_id = 777031  # Библиотекарь

    # kinopoisk_data = kinopoisk_client.find_one_movie(kinopoisk_id)
    # print(kinopoisk_data)

    # noco_client.table_row_update(project, NOCODB_TABLE_METADATA, row_id, row_info)

    return json.dumps(
        {
            "result": True,
            "items": items,
            "echo": req,
        },
    )
