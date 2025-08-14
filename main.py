import os
import psycopg2
from flask import Flask, render_template, request, redirect, session, Response
from urllib.parse import urlparse
app = Flask(__name__)

DB_OBST_NAME = "scrapesafe.obstacles"
DB_ROAD_NAME = "scrapesafe.roads"
DB_OBST_COLUMN = '("type","road","region","country")'
DB_ROAD_COLUMN = '("start_lat","start_long","end_lat","end_long")'
DB_OBST_FORMAT = "({type},{road},{region},{country})"
DB_ROAD_FORMAT = "({slat},{slong},{elat},{elong})"
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
        region = "ARRAY"+request.form.get('region')
        country = "ARRAY"+request.form.get('country')
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
        curr.execute("SELECT * FROM {name} WHERE '{region}' = ANY(region) AND '{country}' = ANY(country)".format(name=DB_OBST_NAME,region=region,country=country))
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
        startLat = request.form.get('startLat')
        startLong = request.form.get('startLong')
        endLat = request.form.get('endLat')
        endLong =request.form.get('endLong')
        print(startLat,startLong,endLat,endLong)
        curr = conn.cursor()
        curr.execute('''
        BEGIN;
        INSERT INTO {name} {columns} VALUES {values};
        COMMIT;'''.format(
            name=DB_ROAD_NAME,
            columns=DB_ROAD_COLUMN,
            values=DB_ROAD_FORMAT.format(
                slat=startLat,
                slong=startLong,
                elat=endLat,
                elong=endLong
            )
        ))
        conn.close()
        return Response("posted",status=200)
    elif request.method == "GET" and conn:
        startLat = request.args.get('startLat')
        startLong = request.args.get('startLong')
        endLat = request.args.get('endLat')
        endLong = request.args.get('endLong')
        curr = conn.cursor()
        curr.execute("SELECT * FROM {name} WHERE start_lat={slat} AND start_long={slong} AND end_lat={elat} AND end_long={elong}".format(
            name=DB_ROAD_NAME,
            slat=startLat,
            slong=startLong,
            elat=endLat,
            elong=endLong
        ))
        data = curr.fetchall()
        return data
    else:
        conn.close()






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))