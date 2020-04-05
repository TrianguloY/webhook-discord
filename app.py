import json

import requests
from flask import Flask, request

app = Flask(__name__)


###############
# The request #
###############

def getMessage(data):
    return [
        {
            "timestamp": data['created_at'],
            "title": f"{data['action']} ({data['resource']})",
        },
        {
            "title": "data",
            "description": json.dumps(data['data']),
        },
    ]


@app.route('/<id>/<token>', methods=['POST'])
def respond(id, token):
    url = f"https://discordapp.com/api/webhooks/{id}/{token}"

    try:
        embeds = getMessage(request.json)
    except Exception as e:
        embeds = {
            "title": "Error on webhook",
            "description": str(e),
        }

    data = {
        "username": "Heroku",
        "avatar_url": "https://www.herokucdn.com/favicons/favicon.ico",
        "embeds": embeds,
    }

    r = requests.post(url, json=data)
    return r.content, r.status_code, r.headers.items()


###################
# Invalid request #
###################

app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(Exception)
def page_not_found(e):
    return 'Invalid request, for more information go to the <a href="https://github.com/TrianguloY/webhook-discord">GitHub page</a>', 404


########
# Main #
########

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
