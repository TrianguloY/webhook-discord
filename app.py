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
        petition = json.loads(request.body)
        message = request.body
    except Exception as e:
        message = f"Error on webhook: {e}"

    data = {
        "username": "Heroku",
        "avatar_url": "https://www.herokucdn.com/favicons/favicon.ico",
        "embeds": [{
            "description": message,
        }],
    }

    r = requests.post(url, json=data)
    return r.content, r.status_code, r.headers.items()


###################
# Invalid request #
###################

app.config['TRAP_HTTP_EXCEPTIONS'] = True


@app.errorhandler(Exception)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return 'Invalid request, for more information go to the <a href="https://github.com/TrianguloY">GitHub page</a>', 404


########
# Main #
########

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
