from flask import Flask, request
import sqlite3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# -------- TRAIN MODEL --------
def train_model():
    conn = sqlite3.connect("housing.db")
    data = pd.read_sql_query("SELECT * FROM housing", conn)
    conn.close()

    if len(data) < 2:
        return None

    data["Status"] = data["Status"].map({"OnTime": 0, "Delayed": 1})
    X = data[["Budget", "Days_Taken"]]
    y = data["Status"]

    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model


# -------- DASHBOARD DATA --------
def get_dashboard_data():
    conn = sqlite3.connect("housing.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM housing")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM housing WHERE Status='Delayed'")
    delayed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM housing WHERE Status='OnTime'")
    ontime = cursor.fetchone()[0]

    conn.close()
    return total, delayed, ontime


# -------- HOME (DASHBOARD) --------
@app.route("/")
def home():
    total, delayed, ontime = get_dashboard_data()

    return f"""
    <html>
    <head>
        <title>Rural Housing MIS</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">

    <div class="container mt-5">

        <h1 class="text-center mb-4">Rural Housing MIS Dashboard</h1>

        <div class="row text-center mb-4">
            <div class="col">
                <div class="card shadow p-3">
                    <h5>Total Projects</h5>
                    <h2>{total}</h2>
                </div>
            </div>
            <div class="col">
                <div class="card shadow p-3 text-danger">
                    <h5>Delayed Projects</h5>
                    <h2>{delayed}</h2>
                </div>
            </div>
            <div class="col">
                <div class="card shadow p-3 text-success">
                    <h5>OnTime Projects</h5>
                    <h2>{ontime}</h2>
                </div>
            </div>
        </div>

        <div class="card shadow p-4">
            <h4>Add Housing Project</h4>
            <form method="POST" action="/add">
                <div class="mb-3">
                    <label>Budget</label>
                    <input type="number" name="budget" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label>Days Taken</label>
                    <input type="number" name="days" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label>Status</label>
                    <select name="status" class="form-control">
                        <option value="OnTime">OnTime</option>
                        <option value="Delayed">Delayed</option>
                    </select>
                </div>

                <button type="submit" class="btn btn-primary">Submit</button>
                <a href="/predict" class="btn btn-success ms-2">Predict</a>
            </form>
        </div>

    </div>

    </body>
    </html>
    """


# -------- ADD DATA --------
@app.route("/add", methods=["POST"])
def add_data():
    budget = request.form["budget"]
    days = request.form["days"]
    status = request.form["status"]

    conn = sqlite3.connect("housing.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO housing (Budget, Days_Taken, Status) VALUES (?, ?, ?)",
        (budget, days, status),
    )

    conn.commit()
    conn.close()

    return "<h3 class='text-center mt-5'>Data Added Successfully ✅</h3><div class='text-center'><a href='/' class='btn btn-primary'>Back to Dashboard</a></div>"


# -------- PREDICTION PAGE --------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        budget = int(request.form["budget"])
        days = int(request.form["days"])

        model = train_model()

        if model is None:
            return "Not enough data"

        prediction = model.predict([[budget, days]])
        result = "Delayed" if prediction[0] == 1 else "OnTime"

        return f"""
        <div class="container text-center mt-5">
            <h2>Prediction Result: {result}</h2>
            <a href="/" class="btn btn-primary mt-3">Back to Dashboard</a>
        </div>
        """

    return """
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    <div class="container mt-5">
        <div class="card shadow p-4">
            <h4>Predict Project Status</h4>
            <form method="POST">
                <div class="mb-3">
                    <label>Budget</label>
                    <input type="number" name="budget" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label>Days Taken</label>
                    <input type="number" name="days" class="form-control" required>
                </div>

                <button type="submit" class="btn btn-success">Predict</button>
                <a href="/" class="btn btn-secondary ms-2">Back</a>
            </form>
        </div>
    </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
