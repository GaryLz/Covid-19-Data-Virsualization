from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import utils


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/time')
def get_time():
    return utils.getTime()

@app.route('/update')
def get_last_update_time():
    return utils.get_last_update_time()

@app.route("/c1")
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm": data[0], "suspect": data[1], "heal": data[2], "dead": data[3]})

@app.route("/c2")
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        # print(tup)
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})

@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data:
        day.append(a.strftime("%m-%d")) # a是datatime类型
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})

@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day,confirm_add,heal_add,dead_add = [],[],[],[]
    for a,b,c,d in data:
        day.append(a.strftime("%m-%d")) # a是datatime类型
        confirm_add.append(b)
        heal_add.append(c)
        dead_add.append(d)
    return jsonify({"day": day, "confirm_add": confirm_add, "heal_add": heal_add, "dead_add": dead_add})

@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    city,confirm = [],[]
    for a,b in data:
        city.append(a)
        confirm.append(b)
    return jsonify({"city": city, "confirm": confirm})

@app.route("/r2")
def get_r2_data():
    res = []
    for tup in utils.get_r2_data():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@app.route('/ajax', methods=["get", "post"])
def hello_world1():
    name = request.values.get("name")
    score = request.values.get("score")
    print(f"name:{name}, score:{score}")
    return '10000'


@app.route('/template')
def hello_world2():
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
