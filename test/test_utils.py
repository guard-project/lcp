import json
import os


def loadExampleFile(filename):
    json_file = os.path.dirname(__file__) + \
                    "/examples/" + filename
    with open(json_file) as f:
        file_data = f.read()
    return json.loads(file_data)


def getAuthorizationHeaders():
    return {"Authorization": "Basic bGNwOmd1YXJk"}
