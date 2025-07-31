from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from .env
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Define the headers with your secure key
HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com"
}

@app.route("/", methods=["GET", "POST"])
def index():
    workout_plan = None

    if request.method == "POST":
        goal = request.form["goal"]
        fitness_level = request.form["fitness_level"]
        preferences = request.form.getlist("preferences")
        days = int(request.form["days"])
        duration = int(request.form["duration"])
        weeks = int(request.form["weeks"])

        payload = {
            "goal": goal,
            "fitness_level": fitness_level,
            "preferences": preferences,
            "health_conditions": ["None"],
            "schedule": {
                "days_per_week": days,
                "session_duration": duration
            },
            "plan_duration_weeks": weeks,
            "lang": "en"
        }

        # Send POST request to the API
        response = requests.post(
            "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/generateWorkoutPlan?noqueue=1",
            json=payload,
            headers=HEADERS
        )

        if response.status_code == 200:
            workout_plan = response.json()
        else:
            workout_plan = {"error": f"API error: {response.status_code}"}

    return render_template("index.html", workout_plan=workout_plan)

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json()
    payload = {
        "goal": data.get("goal", ""),
        "fitness_level": data.get("fitness_level", "Beginner"),
        "preferences": data.get("preferences", ["Cardio"]),
        "health_conditions": data.get("health_conditions", ["None"]),
        "schedule": {
            "days_per_week": data.get("schedule", {}).get("days_per_week", 3),
            "session_duration": data.get("schedule", {}).get("session_duration", 30)
        },
        "plan_duration_weeks": data.get("plan_duration_weeks", 4),
        "lang": data.get("lang", "en")
    }
    try:
        response = requests.post(
            "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/generateWorkoutPlan?noqueue=1",
            json=payload,
            headers=HEADERS
        )
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API error: {response.status_code}", "details": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/workoutPlan", methods=["POST"])
def workout_plan():
    data = request.get_json()
    payload = {
        "goal": data.get("goal", ""),
        "fitness_level": data.get("fitness_level", "Beginner"),
        "preferences": data.get("preferences", ["Cardio"]),
        "health_conditions": data.get("health_conditions", ["None"]),
        "schedule": {
            "days_per_week": data.get("schedule", {}).get("days_per_week", 3),
            "session_duration": data.get("schedule", {}).get("session_duration", 30)
        },
        "plan_duration_weeks": data.get("plan_duration_weeks", 4),
        "lang": data.get("lang", "en")
    }
    try:
        response = requests.post(
            "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/generateWorkoutPlan?noqueue=1",
            json=payload,
            headers=HEADERS
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/nutritionAdvice", methods=["POST"])
def nutrition_advice():
    data = request.get_json()
    payload = {
        "goal": data.get("goal", ""),
        "diet_type": data.get("diet_type", "Balanced"),
        "lang": data.get("lang", "en")
    }
    try:
        response = requests.post(
            "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/nutritionAdvice?noqueue=1",
            json=payload,
            headers=HEADERS
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/exerciseDetails", methods=["POST"])
def exercise_details():
    data = request.get_json()
    payload = {
        "exercise_name": data.get("exercise_name", ""),
        "lang": data.get("lang", "en")
    }
    try:
        response = requests.post(
            "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/exerciseDetails?noqueue=1",
            json=payload,
            headers=HEADERS
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/analyzeFoodPlate", methods=["POST"])
def analyze_food_plate():
    data = request.get_json()
    image_url = data.get("imageUrl", "")
    lang = data.get("lang", "en")
    try:
        response = requests.post(
            f"https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/analyzeFoodPlate?imageUrl={image_url}&lang={lang}&noqueue=1",
            headers=HEADERS
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/customWorkoutPlan", methods=["POST"])
def custom_workout_plan():
    data = request.get_json()
    payload = {
        "goal": data.get("goal", ""),
        "custom_exercises": data.get("custom_exercises", []),
        "lang": data.get("lang", "en")
    }
    try:
        response = requests.post(
            "https://ai-workout-planner-exercise-fitness-nutrition-guide.p.rapidapi.com/customWorkoutPlan?noqueue=1",
            json=payload,
            headers=HEADERS
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)