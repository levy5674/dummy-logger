"""
This is not suitable for any purpose other than debugging.

messages posted to the log actually get written into a cache
that will eventually expire and erase them
"""

import flask
import json
import os
from werkzeug.contrib.cache import FileSystemCache

app = flask.Flask(__name__)

PATH_KEY="ROOT_PATH"
DEFAULT_PATH = "./logs"
DEFAULT_CHANNEL = "."

PATH = os.environ.get(PATH_KEY, DEFAULT_PATH)

if not os.path.isdir(PATH):
    os.mkdir(PATH)

CACHE = FileSystemCache(PATH, threshold=1000000, default_timeout=60*60*24*31)

def logEvent(obj):
    channel = obj.get("channel", DEFAULT_CHANNEL)
    values = CACHE.get(channel)
    values = values if values else []
    values.append(obj)
    CACHE.set(channel, values)
    return {"channel": channel, "count": len(values)}

@app.route("/", methods=['POST'])
def logEventRoute():
    obj = flask.request.json
    resp = logEvent(obj)
    return flask.Response(json.dumps(resp), mimetype="application/json")

@app.route("/<channel>", methods=['GET'])
def readLog(channel):
    limit = flask.request.args.get("limit")
    limit = None if not limit else int(limit)
    values = CACHE.get(channel) or []
    return flask.Response(json.dumps(values[::-1][:limit]), mimetype="application/json")

if __name__ == '__main__':
    app.run()
