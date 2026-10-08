import sqlite3

conn = sqlite3.connect("housing.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS housing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Budget INTEGER,
    Days_Taken INTEGER,
    Status TEXT
)
""")

# Clear old data
cursor.execute("DELETE FROM housing")

# Insert sample data
data_list = [
(1000000,120,'OnTime'),
(1500000,200,'Delayed'),
(900000,100,'OnTime'),
(1400000,210,'Delayed'),
(1100000,130,'OnTime'),
(1600000,220,'Delayed'),
(800000,90,'OnTime'),
(1700000,230,'Delayed'),
(950000,110,'OnTime'),
(1550000,205,'Delayed')
]

for row in data_list:
    cursor.execute("INSERT INTO housing (Budget, Days_Taken, Status) VALUES (?,?,?)", row)

conn.commit()
conn.close()

print("Database Ready")
