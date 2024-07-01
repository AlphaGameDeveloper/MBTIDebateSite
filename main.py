from flask import Flask, request, render_template, send_from_directory, redirect
import json

app = Flask(__name__)
global json_mbti_stuff
global request_count
request_count = 0
json_mbti_stuff = json.load(open("mbti-stuff.json"))

global globalData
globalData = {
    "changed_by": "SYSTEM",
    "type_main": ["X", "X", "X", "X"],
    "type_shadow": ["X", "X", "X", "X"],
    "type_main_str": "",
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
    elif fnl[1].lower() == "x":
        return
    else:
        raise ValueError("Invalid function - Second letter incorrect!")
    _re = "".join(fnl).lower()
    print(_re)
    return _re

def getTypeFromFunction(dominant, auxiliary, tertiary, inferior) -> list[str]:
    mbti = ["X", "X", "X", "X"]

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
    global request_count

    request_count += 1

    username = request.cookies.get("username")
    if username == None:
        return redirect("/session/userConfiguration?from=index&reason=UserCookieNonexistant")
    debugSwitch = request.args.get('debug')
    d = (debugSwitch.lower() in ["1", "on", "true"])
    fdn = (debugSwitch.lower() in ["0", "off", "false"])
    debug = (app.debug or d) and not fdn
    return render_template("index.html", debug=debug, title="MBTI Debate Site", username=username)

@app.route("/api/userConfigHandler", methods=["GET"])
def userConfigHandler():
    username = request.args.get("username")
    print(username)
    r = redirect("/?debug=0&debugDisableSource=UserConfigurationDefault")
    r.set_cookie('username', username)
    return r

@app.route("/session/userConfiguration")
def userConfig():
    username = request.cookies.get("username")
    return render_template("username.html", username=username)
     
@app.route("/static/<path:path>")
def _static(path):
    global request_count

    request_count += 1
    return send_from_directory("static", path)

def formatFunction(function):
    return function[0].upper() + function[1].lower()

@app.route("/api/submitCurrentstate", methods=["POST"])
def submitCurrentState():
    global request_count
    request_count += 1

    globalData.update(request.json)
    globalData["changed_by"] = request.cookies.get('username')
    globalData["shadow_opposing"] = formatFunction(getShadowFunction(globalData["dominant"])).lower()
    globalData["shadow_critical"] = formatFunction(getShadowFunction(globalData["auxiliary"])).lower()
    globalData["shadow_trickster"] = formatFunction(getShadowFunction(globalData["tertiary"])).lower()
    globalData["shadow_transformative"] = formatFunction(getShadowFunction(globalData["inferior"])).lower()

    globalData["type_main"] = getTypeFromFunction(globalData["dominant"], globalData["auxiliary"], globalData["tertiary"], globalData["inferior"])
    globalData["type_shadow"] = getTypeFromFunction(globalData["shadow_opposing"], globalData["shadow_critical"], globalData["shadow_trickster"], globalData["shadow_transformative"])
    
    # add new key for string
    globalData["type_main_str"] = "".join(globalData["type_main"])
    globalData["type_shadow_str"] = "".join(globalData["type_shadow"])
    return "OK"

@app.route("/api/accessInternals")
def accessInternals():
    global request_count
    request_count += 1
    return globalData

@app.route("/api/accessInternals/<string:key>")
def getInternals(key):
    global request_count
    request_count += 1
    try:
        return globalData[key]
    except KeyError:
        return "Key not found", 500

@app.route("/api/getState")
def getState():
    global request_count
    request_count += 1
    return render_template("state.html", data=globalData)

@app.route("/api/getStack")
def getStack():
    global request_count
    request_count += 1
    return render_template("stackTable.html", stacks=[
        "dominant", 
        "auxiliary", 
        "tertiary", 
        "inferior",
        "shadow_opposing",
        "shadow_critical",
        "shadow_trickster",
        "shadow_transformative"])

@app.route("/api/requestCount")
def requestCount():
    global request_count
    return str(request_count)

if __name__ == "__main__":
    app.run()
