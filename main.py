from flask import Flask, request, render_template, send_from_directory
import json

app = Flask(__name__)
global json_mbti_stuff
json_mbti_stuff = json.load(open("mbti-stuff.json"))

global globalData
globalData = {
    "type_main": "XXXX",
    "type_shadow": "XXXX",
    "type_main_str": "XXXX",
    "type_shadow_str": "XXXX",
    "dominant": "Xx",
    "auxiliary": "Xx",
    "tertiary": "Xx",
    "inferior": "Xx",
    "shadow_opposing": "Xx",
    "shadow_critical": "Xx",
    "shadow_trickster": "Xx",
    "shadow_transformative": "Xx"
}

def getShadowFunction(function):
    fnl = list(function)
    if fnl[1].lower() == "e":
        fnl[1] = "i"
    elif fnl[1].lower() == "i":
        fnl[1] = "e"
    else:
        raise ValueError("Invalid function - Second letter incorrect!")
    return "".join(fnl)

def getTypeFromFunction(dominant, auxiliary, tertiary, inferior) -> list[str]:
    mbti = [None, None, None, None]

    for entry in json_mbti_stuff["types"]: 
        e = entry["functions"]
        if e["dominant"].lower() == dominant and e["auxiliary"].lower() == auxiliary and e["tertiary"].lower() == tertiary and e["inferior"].lower() == inferior:
            mbti = list(entry["type"])
            break    
    print([dominant, auxiliary, tertiary, inferior])
    print(mbti)
    return mbti
@app.route("/")
def index():
    return render_template("index.html", debug=app.debug)

@app.route("/static/<path:path>")
def _static(path):
    return send_from_directory("static", path)

@app.route("/api/submitCurrentstate", methods=["POST"])
def submitCurrentState():
    print(request.json)
    globalData.update(request.json)
    globalData["shadow_opposing"] = getShadowFunction(globalData["dominant"])
    globalData["shadow_critical"] = getShadowFunction(globalData["auxiliary"])
    globalData["shadow_trickster"] = getShadowFunction(globalData["tertiary"])
    globalData["shadow_transformative"] = getShadowFunction(globalData["inferior"])

    globalData["type_main"] = getTypeFromFunction(globalData["dominant"], globalData["auxiliary"], globalData["tertiary"], globalData["inferior"])
    globalData["type_shadow"] = getTypeFromFunction(globalData["shadow_opposing"], globalData["shadow_critical"], globalData["shadow_trickster"], globalData["shadow_transformative"])
    
    # add new key for string
    globalData["type_main_str"] = "".join(globalData["type_main"])
    globalData["type_shadow_str"] = "".join(globalData["type_shadow"])
    return "OK"

@app.route("/api/accessInternals")
def accessInternals():
    return globalData

@app.route("/api/accessInternals/<string:key>")
def getInternals(key):
    try:
        return globalData[key]
    except KeyError:
        return "Key not found", 500

@app.route("/api/getState")
def getState():
    return render_template("state.html", data=globalData)

@app.route("/api/getStack")
def getStack():
    return render_template("stackTable.html", stacks=[
        "dominant", 
        "auxiliary", 
        "tertiary", 
        "inferior",
        "shadow_opposing",
        "shadow_critical",
        "shadow_trickster",
        "shadow_transformative"])
if __name__ == "__main__":
    app.run()