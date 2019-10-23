import logging
import os

from dotenv import load_dotenv
from flask import Flask, request, json, abort
from google_hangouts_chat_bot.commands import Commands
from google_hangouts_chat_bot.event_handler import EventHandler
from google_hangouts_chat_bot.responses import create_text_response
from google_hangouts_chat_bot.security import (
    check_bot_authenticity,
    check_allowed_domain,
)

import tech_gallery_bot.commands
from config import load_configs
from tech_gallery_bot.dependencies import get_dependencies

load_dotenv()

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING").upper())

app = load_configs(Flask(__name__))

dependencies = get_dependencies(config=app.config)

commands = Commands()
commands.add_commands_from_module(tech_gallery_bot.commands)

logging.info(
    "Commands available: [\n  %s\n]"
    % "\n  ".join(
        [
            f'{k} [{"hidden," if v.hidden else ""}{"alias," if k in v.command_aliases else ""}]: {v}'
            for k, v in commands.get_commands().items()
        ]
    )
)


@app.before_request
def before_request_func():
    if app.debug or app.testing or request.path == "/health":
        return

    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        check_bot_authenticity(token, audience=app.config["GOOGLE_APPLICATION_ID"])
    except Exception as e:
        logging.exception(e)
        abort(403)

    try:
        payload = request.get_json()
        check_allowed_domain(payload["user"]["email"], app.config["ALLOWED_DOMAINS"])
    except Exception as e:
        logging.exception(e)
        return json.jsonify(create_text_response("_Domain not allowed_"))


@app.route("/", methods=["POST"])
def main():
    payload = request.get_json()

    logging.debug(f"Payload: {payload}")

    response = EventHandler(payload, commands, **dependencies).process()

    logging.debug(f"Response: {response}")

    return json.jsonify(response)


@app.route("/health", methods=["GET"])
def ping():
    return "OK"


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # app.run(host='127.0.0.1', port=8080)
    app.run(host="127.0.0.1", port=8080, debug=True)
