import sqlite3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Connect DB
conn = sqlite3.connect("housing.db")

# Load data
data = pd.read_sql("SELECT * FROM housing", conn)
conn.close()

# Convert text to number
data["Status"] = data["Status"].map({"OnTime": 0, "Delayed": 1})

# Features & target
X = data[["Budget", "Days_Taken"]]
y = data["Status"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
