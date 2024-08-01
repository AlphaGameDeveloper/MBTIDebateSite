from flask import Flask, request, render_template, send_from_directory, redirect, Response
import json

app = Flask(__name__)
global json_mbti_stuff
global request_count
request_count = 0
json_mbti_stuff = json.load(open("mbti-stuff.json"))

global globalData
global globalDataTemplate
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

# In the case that we want to reset the internal
# memory (globalData dictionary) via API::Reset
# (GET /api/reset), this copy will be applied.
globalDataTemplate = globalData.copy()

def getShadowFunction(function):
    """Function to get the shadow function of a given cognitive function."""
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
    return _re

def getTypeFromFunction(dominant, auxiliary, tertiary, inferior) -> list[str]:
    """Gets a Myers-Briggs personality type from the four cognitive functions.

    Returns XXXX should an invalid function stack be passed."""
    mbti = ["X", "X", "X", "X"]

    for entry in json_mbti_stuff["types"]: 
        e = entry["functions"]
        if e["dominant"].lower() == dominant and e["auxiliary"].lower() == auxiliary and e["tertiary"].lower() == tertiary and e["inferior"].lower() == inferior:
            mbti = list(entry["type"])
            break    
    return mbti

@app.route("/")
def index():
    global request_count

    request_count += 1
    args = str(request.args.to_dict())
    cookies = str(request.cookies.to_dict())
    username = request.cookies.get("username")
    if username == None:
        return redirect("/session/userConfiguration?from=index&reason=UserCookieNonexistant")
    debugSwitch = request.args.get('debug')
    if debugSwitch == None: # debug mode will be automatically disabled.
        debug = False
        force_debug_no = True
    else:
        debug = (debugSwitch.lower() in ["1", "on", "true"])
        force_debug_no = (debugSwitch.lower() in ["0", "off", "false"])
    debug = (app.debug or debug) and not force_debug_no
    return render_template("index.html", args=args, cookies=cookies, debug=debug, title="MBTI Debate Site", username=username, show_debug_enable_option=app.debug)

@app.route("/api/reset")
def reset():
    """Resets the internal memory.  A debug mode enabled will be assumed,
    as (at least in the app UI) this button is only enabled there."""
    globalData.update(globalDataTemplate)
    return redirect("/?debug=1&debugEnableSource=GrandFatheredInAfterReset&actionResult=SUCCESS")
    
@app.route("/api/userConfigHandler", methods=["GET"])
def userConfigHandler():
    username = request.args.get("username")
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
    return Response(json.dumps(globalData, indent=4), status=200, mimetype="application/json")

@app.route("/api/accessInternals/<string:key>")
def getInternals(key):
    global request_count
    request_count += 1
    isCogFunc = request.args.get("cf") != None
    isStrict = request.args.get("strict") != None
    try:
        d = globalData[key]
        if isCogFunc:
            _d = list(d)
            if len(_d) != 2:
                return "Doesn't have the correct length to be a cognitive function..."
            _d[0] = _d[0].upper()
            return "".join(_d)
            
        return globalData[key]
    except KeyError:
        return "Key not found", 500

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
    # this app should be started with:
    # FLASK_APP=main flask run (--debug)
    app.run()
