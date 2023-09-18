import pickle
from flask import Flask, request, render_template, url_for, flash, jsonify
import numpy as np



app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("home.html")
    else:

        frequency = float(request.form.get("frequency"))
        angle = float(request.form.get("angle"))
        chord_length = float(request.form.get("Chord length"))
        velocity = float(request.form.get("Velocity"))
        suction_side = float(request.form.get("Suction side"))

        if frequency == "" or angle == "" or chord_length == "" or velocity == "" or suction_side == "":
            flash("One or more empty fields")
            return render_template("home.html")
        else:
            model = pickle.load(open("model_unscaled.pkl", "rb"))
            arr = np.array([[frequency, angle, chord_length, velocity, suction_side]])
            pred = model.predict(arr)
            return render_template("result.html", data=np.round(pred,2))
        
@app.route("/predict_postman", methods=["GET", "POST"])
def prediction():
    if request.method == "GET":
        return render_template("home.html")
    else:
        
        frequency = float(request.json["frequency"])
        angle = float(request.json["angle"])
        chord_length = float(request.json["Chord length"])
        velocity = float(request.json["Velocity"])
        suction_side = float(request.json["Suction side"])

        if frequency == "" or angle == "" or chord_length == "" or velocity == "" or suction_side == "":
            flash("One or more empty fields")
            return render_template("home.html")
        else:
            model = pickle.load(open("model_unscaled.pkl", "rb"))
            arr = np.array([[frequency, angle, chord_length, velocity, suction_side]])
            pred = model.predict(arr)
            data=np.round(pred,2)
            return jsonify((data))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")