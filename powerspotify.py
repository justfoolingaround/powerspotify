import os
import pathlib

import flask
from librespot.core import Session

dotenv_path = pathlib.Path(__file__).parent / ".env"

if dotenv_path.exists():
    import dotenv

    dotenv.load_dotenv(dotenv_path)

SPOTIFY_USERNAME = os.environ["SPOTIFY_USERNAME"]
SPOTIFY_PASSWORD = os.environ["SPOTIFY_PASSWORD"]
PORT = os.environ.get("PORT", 8080)


session = Session.Builder().user_pass(SPOTIFY_USERNAME, SPOTIFY_PASSWORD).create()
audio_key = session.audio_key()


app = flask.Flask(__name__)


@app.route("/<gid>/<file_id>")
def fetch_file_id_for(gid, file_id):
    key = audio_key.get_audio_key(
        bytes.fromhex(gid),
        bytes.fromhex(file_id),
    ).hex()

    return flask.Response(
        headers={
            "X-Audio-Key": key,
        }
    )


if __name__ == "__main__":
    import subprocess

    import waitress

    NGROK_DOMAIN = os.environ.get("NGROK_DOMAIN")
    NGROK_TOKEN = os.environ["NGROK_TOKEN"]

    auth_command = [
        "ngrok",
        "config",
        "add-authtoken",
        NGROK_TOKEN,
    ]

    portforward_command = [
        "ngrok",
        "http",
        PORT,
    ]

    if NGROK_DOMAIN:
        portforward_command.append(f"--domain={NGROK_DOMAIN}")

    subprocess.run(auth_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pf_process = subprocess.Popen(
        portforward_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    waitress.serve(app, host="0.0.0.0", port=PORT)
    pf_process.kill()
