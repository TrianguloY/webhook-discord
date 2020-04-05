import requests
from flask import Flask, request

app = Flask(__name__)


###############
# The request #
###############

@app.route('/<id>/<token>', methods=['POST'])
def valid(id, token):
    url = f"https://discordapp.com/api/webhooks/{id}/{token}"

    try:
        # convert from heroku to discord
        embed = heroku2Discord(ExtendedJson(request.json))
    except Exception as e:
        # if error, show generic
        embed = {
            "title": "Error on webhook",
            "description": f"{e}\n{request.data}",
        }

    # create and send
    data = {
        "username": "Heroku",
        "avatar_url": "https://avatars.io/twitter/heroku",
        "embeds": [embed],
    }
    r = requests.post(url, json=data)
    # return same response
    return r.content, r.status_code, r.headers.items()


def heroku2Discord(eJson):
    """
    converts a heroku webhook payload to a discord webhook embed
    """

    # common object
    result = {
        "author": {
            "name": eJson['actor:email'],
        },
        "title": f"[{eJson['data:app:name']}] {eJson['action']} ({eJson['resource']})",
        "url": f"https://{eJson['data:app:name']}.herokuapp.com",
        "timestamp": eJson['created_at'],
    }

    # Adds a field to the object
    def field(name, names):
        if 'fields' not in result: result['fields'] = []
        result['fields'].append({
            "name": name,
            "value": eJson[names],
            "inline": True,
        })

    # check each event

    if eJson['resource'] == 'dyno':
        field("State", 'data:state')

    if eJson['resource'] == 'build':
        field("Status", 'data:status')
        field("User", 'data:user:email')

    if eJson['resource'] == 'release':
        result['description'] = eJson['data:description']
        field("Version", 'data:version')
        field("Current", 'data:current')
        field("Status", 'data:status')
        field("User", 'data:user:email')

    return result


###################
# Invalid request #
###################

app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(Exception)
def invalid(e):
    return 'Invalid request, for more information go to the <a href="https://github.com/TrianguloY/webhook-discord">GitHub page</a>', 404


#########
# Utils #
#########

class ExtendedJson:
    """
    a json object that can chain getters and has error checks: json['a']['b']['c'] -> eJson['a:b:c']
    """

    def __init__(self, bJson):
        self.bJson = bJson

    def __getitem__(self, names):
        item = self.bJson
        for param in names.split(":"):
            if param in item:
                item = item[param]
            else:
                item = f"-No '{param}' in object: {item}-"
                break
        return item


########
# Main #
########

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
