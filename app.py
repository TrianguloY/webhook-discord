import json

import requests
from flask import Flask, request

app = Flask(__name__)


###############
# The request #
###############

@app.route('/<id>/<token>', methods=['POST'])
def respond(id, token):
    url = f"https://discordapp.com/api/webhooks/{id}/{token}"

    try:
        embed = convertToEmbed(json.loads(request.json))
    except Exception as e:
        embed = {
            "title": "Error on webhook",
            "description": str(e),
        }

    data = {
        "username": "Heroku",
        "avatar_url": "https://avatars.io/twitter/heroku",
        "embeds": [embed],
    }

    r = requests.post(url, json=data)
    return r.content, r.status_code, r.headers.items()


def convertToEmbed(payload):
    """
    converts a heroku webhook payload to a discord webhook embed
    """
    result = {
        "author": {
            "name": payload['data']['app']['name'],
            "url": f"https://{payload['data']['app']['name']}.herokuapp.com",
        },
        "timestamp": payload['created_at'],
        "title": f"{payload['action']} ({payload['resource']})",
        "fields": [],
    }

    if payload['resource'] == 'dyno':
        result['fields'].append(field("State", payload['data']['state']))

    if payload['resource'] == 'build':
        result['fields'].append(field("Status", payload['data']['status']))
        result['fields'].append(field("User", payload['data']['user']['email']))

    if payload['resource'] == 'release':
        result['description'] = payload['data']['description']
        result['fields'].append(field("Version", payload['data']['version']))
        result['fields'].append(field("Current", payload['data']['current']))
        result['fields'].append(field("Status", payload['data']['status']))
        result['fields'].append(field("User", payload['data']['user']['email']))

    return result


def field(name, value):
    """
    utility to build a field
    """
    return {
        "name": name,
        "value": str(value),
        "inline": True,
    }


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
