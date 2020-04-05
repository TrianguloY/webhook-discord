import requests
from flask import Flask, request

app = Flask(__name__)


###############
# The request #
###############

def getEmbed(data):
    result = {
        "author": {
            "name": data['app']['name'],
            "url": f"{data['app']['name']}.herokuapp.com",
        },
        "timestamp": data['created_at'],
        "title": f"{data['action']} ({data['resource']})",
        "fields": [],
    }

    if data['resource'] == 'dyno':
        result['fields'].append({
            "name": "State",
            "value": data['data']['state'],
        })

    if data['resource'] == 'build':
        result['fields'].append({
            "name": "Status",
            "value": data['data']['status'],
        })
        result['fields'].append({
            "name": "User",
            "value": data['data']['user']['email'],
        })

    if data['resource'] == 'release':
        result['description'] = data['data']['description']
        result['fields'].append({
            "name": "Version",
            "value": data['data']['version'],
        })
        result['fields'].append({
            "name": "Status",
            "value": data['data']['status'],
        })
        result['fields'].append({
            "name": "Current",
            "value": data['data']['current'],
        })
        result['fields'].append({
            "name": "User",
            "value": data['data']['user']['email'],
        })

    return result


@app.route('/<id>/<token>', methods=['POST'])
def respond(id, token):
    url = f"https://discordapp.com/api/webhooks/{id}/{token}"

    try:
        embed = getEmbed(request.json)
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
