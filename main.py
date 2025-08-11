import os
import psycopg2
from flask import Flask, render_template, request, redirect, session, Response
from urllib.parse import urlparse
app = Flask(__name__)

DB_NAME = "scrapesafe.obstacles"
DB_COLUMN = "(type,longitude,latitude,region)"
DB_FORMAT = "({type},{longitude},{latitude},{region})"
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
    return f"Hello {name}!"
@app.route("/obstacles",methods=["GET"])
def getObstacleInRegion():
    conn = get_connection()
    if request.method == "GET" and conn:
        region = request.args['region']
        curr = conn.cursor()
        curr.execute("SELECT * FROM {name} WHERE region = '{region}'".format(name=DB_NAME,region=region))
        data = curr.fetchall()
        result = []
        for row in data:
            result.append(row)
        conn.close()
        return result
    else:
        conn.close()
@app.route("/obstacles",methods=["POST"])
def addObstacle():
    conn = get_connection()
    if request.method == "POST" and conn:
        region = request.form.get('region')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
        t = request.form.get('type')
        curr = conn.cursor()
        curr.execute("INSERT INTO {name} {columns} VALUES({values})".format(
            name=DB_NAME,
            columns=DB_COLUMN,
            values=DB_FORMAT.format(
                region=region,
                longitude=longitude,
                latitude=latitude,
                type=t
            )
        ))
        conn.close()
        return Response("posted",status=200)
    else:
        conn.close()







if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))