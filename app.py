import colorsys
import hashlib

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
        # ignore message
        if embed is None: return '', 204
    except Exception as e:
        # if error, show generic
        embed = {
            "title": "Error on webhook",
            "url": "https://github.com/TrianguloY/webhook-discord/issues",
            "description": f"Click to open bot page.\nException: {e}\nFull response: {request.data}",
        }

    # create and send
    data = {
        "username": "Heroku",
        "avatar_url": "https://www.herokucdn.com/favicons/apple-touch-icon-152x152.png",
        "embeds": [embed],
    }
    r = requests.post(url, json=data)
    # return same response
    return r.content, r.status_code, r.headers.items()


def heroku2Discord(eJson):
    """
    converts a heroku webhook payload to a discord webhook embed
    """

    # elements
    resource = eJson['resource']
    title = f"[{eJson['data:app:name']}] {resource}"
    author = eJson['actor:email']
    description = None
    fields = []

    # Adds a field to the object
    def field(name, names):
        fields.append({
            "name": name,
            "value": eJson[names],
            "inline": True,
        })

    # detail for each event
    if resource == 'dyno':
        title += f" {eJson['data:state']}"

    elif resource == 'build':
        status = eJson['data:status']
        if status == 'pending': status = "in progress"  # specific rename
        title += f" {status}"
        author = eJson['data:user:email']

    elif resource == 'release':
        status = eJson['data:status']
        if status == 'succeeded' and eJson['action'] == 'update': return  # specific ignore
        title += f" {status}"
        description = eJson['data:description']
        author = eJson['data:user:email']
        field("Version", 'data:version')
        field("Current", 'data:current')

    else:  # default
        title += f"-{eJson['action']}"

    # embed
    return {
        "color": uniqueColor(resource),
        "author": {
            "name": author,
        },
        "title": title,
        "url": f"https://{eJson['data:app:name']}.herokuapp.com",
        "description": description,
        "fields": fields,
        "timestamp": eJson['created_at'],
    }


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
                raise KeyError(f"-No '{param}' while getting '{names}'-")
        return item


def uniqueColor(string):
    """
    Returns a color from the string.
    Same strings will return same colors, different strings will return different colors ('randomly' different)
    Internal: string =md5(x)=> hex =x/maxhex=> float [0-1] =hsv_to_rgb(x,1,1)=> rgb =rgb_to_int=> int
    :param string: input string
    :return: int color
    """
    return sum(round(c * 255) << d for c, d in zip(colorsys.hsv_to_rgb(int(hashlib.md5(string.encode('utf-8')).hexdigest(), 16) / 2 ** 128, 1, 1), [16, 8, 0]))


########
# Main #
########

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
