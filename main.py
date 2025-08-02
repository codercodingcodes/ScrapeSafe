import os
import psycopg2
from flask import Flask, render_template, request, redirect, session
from urllib.parse import urlparse
app = Flask(__name__)

def get_connection():
    result = urlparse("postgresql://neondb_owner:npg_Y8eVbNFOHc2i@ep-shy-pond-afxptmom-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    try:
         return psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname
        )
    except:
        return False

@app.route("/")
def main():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    # print(get_connection())
    return f"Hello {name}!"
@app.route("/obstacles",methods=["GET"])
def getObstacleInRegion():
    conn = get_connection()
    if request.method == "GET" and conn:
        city = request.args['city']
        curr = conn.cursor()
        curr.execute("SELECT * FROM scrapesafe.obstacles WHERE region = '{}'".format(city))
        data = curr.fetchall()
        result = []
        for row in data:
            result.append(row)
        conn.close()
        return result






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))