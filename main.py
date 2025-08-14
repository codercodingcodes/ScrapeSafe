import os
import psycopg2
from flask import Flask, render_template, request, redirect, session, Response
from urllib.parse import urlparse
app = Flask(__name__)

DB_OBST_NAME = "scrapesafe.obstacles"
DB_ROAD_NAME = "scrapesafe.obstacles"
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
@app.route("/obstacles",methods=["GET"])
def getObstacleInRegion():
    conn = get_connection()
    if request.method == "GET" and conn:
        region = request.args['region']
        country = request.args['country']
        curr = conn.cursor()
        curr.execute("SELECT * FROM {name} WHERE region = '{region}' AND country = '{country}'".format(name=DB_OBST_NAME,region=region,country=country))
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
        region = list(request.form.get('region'))
        country = list(request.form.get('country'))
        fregion = '{'
        fcountry = '{'
        i=0
        while i<len(region):
            if i==0:
                fregion += '"'+region[i]+'"'
            else:
                fregion += ',"' + region[i] + '"'
            i+=1
        fregion += "}"
        i = 0
        while i < len(country):
            if i == 0:
                fcountry += '"' + country[i] + '"'
            else:
                fcountry += ',"' + country[i] + '"'
            i+=1
        fcountry += "}"
        road = request.form.get('road')
        t = request.form.get('type')
        print(fregion,fcountry,road,t)
        curr = conn.cursor()
        curr.execute('''
        BEGIN;
        INSERT INTO {name} {columns} VALUES {values};
        COMMIT;'''.format(
            name=DB_OBST_NAME,
            columns=DB_OBST_COLUMN,
            values=DB_OBST_FORMAT.format(
                region=fregion,
                road=road,
                type=t,
                country=fcountry
            )
        ))
        conn.close()
        return Response("posted",status=200)
    else:
        conn.close()
@app.route("/roads",methods=["GET"])
def getRoadID():
    conn = get_connection()
    if request.method == "GET" and conn:
        startLat = request.args['startLat']
        startLong = request.args['startLong']
        endLat = request.args['endLat']
        endLong = request.args['endLong']
        curr = conn.cursor()
        curr.execute("SELECT * FROM {name} WHERE start_lat={slat} AND start_long={slong} AND end_lat={elat} AND end_long={elong}".format(
            name=DB_ROAD_NAME,
            slat=startLat,
            slong=startLong,
            elat=endLat,
            elong=endLong
        ))
        data = curr.fetchone()
        return data
    else:
        conn.close()
@app.route("/roads",methods=["POST"])
def addRoad():
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
    else:
        conn.close()






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))