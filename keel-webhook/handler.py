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


def telegram_text_escape(text: str) -> str:
    chars = ("_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!")

    for c in chars:
        text = text.replace(c, f"\\{c}")

    return text


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
            "```",
            f"{telegram_text_escape(payload.message)}",
            "```",
        ),
    )

    url = f"https://api.telegram.org/bot{SECRETS.get('tg-k-devops')}/sendMessage"

    try:
        resp = requests.post(
            url,
            json={
                "chat_id": APP_CHAT_ID,
                "text": message,
                "parse_mode": "MarkdownV2",
                "disable_web_page_preview": True,
            },
        ).json()
    except Exception as e:
        return e

    return json.dumps(
        {
            "result": True,
            "echo": json.loads(payload.json()),
            "tg_response": resp,
        },
    )
