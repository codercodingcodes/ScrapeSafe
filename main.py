import os
import psycopg2
from flask import Flask, render_template, request, redirect, session, Response
from urllib.parse import urlparse
app = Flask(__name__)

DB_OBST_NAME = "scrapesafe.obstacles"
DB_ROAD_NAME = "scrapesafe.roads"
DB_OBST_COLUMN = '("type","road","region","country")'
DB_ROAD_COLUMN = '("longitude","latitude","place_id")'
DB_OBST_FORMAT = "({type},{road},{region},{country})"
DB_ROAD_FORMAT = "({longitude},{latitude},'{place_id}')"
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
@app.route("/obstacles",methods=["POST","GET"])
def obstacleDB():
    conn = get_connection()
    if request.method == "POST" and conn:
        region = request.form.get('region')
        country = request.form.get('country')
        road = request.form.get('road')
        t = request.form.get('type')
        print(region,country,road,t)
        curr = conn.cursor()
        curr.execute('''
        BEGIN;
        INSERT INTO {name} {columns} VALUES {values};
        COMMIT;'''.format(
            name=DB_OBST_NAME,
            columns=DB_OBST_COLUMN,
            values=DB_OBST_FORMAT.format(
                region=region,
                road=road,
                type=t,
                country=country
            )
        ))
        conn.close()
        return Response("posted",status=200)
    elif request.method == "GET" and conn:
        region = request.args.get('region')
        country = request.args.get('country')
        curr = conn.cursor()
        curr.execute("SELECT * FROM {name} WHERE region='{region}' AND country='{country}'".format(name=DB_OBST_NAME,region=region,country=country))
        data = curr.fetchall()
        result = []
        for row in data:
            result.append(row)
        conn.close()
        return result
    else:
        conn.close()
@app.route("/roads",methods=["POST","GET"])
def roadDB():
    conn = get_connection()
    if request.method == "POST" and conn:
        longitude = request.form.get("longitude")
        latitude = request.form.get("latitude")
        placeID = request.form.get("placeID")
        print(longitude,latitude,placeID)
        curr = conn.cursor()
        curr.execute('''
        BEGIN;
        INSERT INTO {name} {columns} VALUES {values};
        COMMIT;'''.format(
            name=DB_ROAD_NAME,
            columns=DB_ROAD_COLUMN,
            values=DB_ROAD_FORMAT.format(
                longitude = longitude,
                latitude = latitude,
                place_id = placeID
            )
        ))
        conn.close()
        return Response("posted",status=200)
    elif request.method == "GET" and conn:
        placeID = request.args.get('placeID')
        curr = conn.cursor()
        curr.execute("SELECT * FROM {name} WHERE place_id='{placeID}'".format(name=DB_ROAD_NAME,placeID=placeID))
        data = curr.fetchall()
        result = []
        for row in data:
            result.append(row)
        conn.close()
        return result
    else:
        conn.close()





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))