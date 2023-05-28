import json
import os
import requests

from function import Payload

APP_CHAT_ID = os.environ.get("APP_CHAT_ID")

SECRETS = {}

secrets_src = ("tg-k-devops",)

for s in secrets_src:
    with open(f"/var/openfaas/secrets/{s}") as fp:
        SECRETS[s] = fp.read().strip()


def handle(req: str) -> dict:
    """handle a request to the function
    Args:
        req (str): request body
    """

    try:
        payload = Payload(**json.loads(req))
    except Exception as e:
        return e

    message = "\n".join(
        (
            "🤖 Update from Keel",
            "",
            f">{payload.message}",
        ),
    )

    url = f"https://api.telegram.org/bot{SECRETS.get('tg-k-devops')}/sendMessage"

    try:
        resp = requests.post(
            url,
            json={
                "chat_id": APP_CHAT_ID,
                "text": message,
            },
        ).json()
    except Exception as e:
        return e

    return json.dumps(
        {
            "result": True,
            "echo": payload,
            "tg_response": resp,
        },
    )
