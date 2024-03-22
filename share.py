import os
import random
import string
import json
from dotenv import load_dotenv

import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from hashids import Hashids
from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
cors = CORS(app, resources={r"/share": {"origins": "https://fiftylist.vercel.app/"}})

data = None  
domain_url = "https://fiftylistbackend.vercel.app/"
hashids_salt = "".join(random.choices(string.ascii_letters + string.digits, k=10))
hashids = Hashids(salt=hashids_salt, min_length=4)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_SSLMODE = os.getenv("DB_SSLMODE")
PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")

google_credentials = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
credentials = service_account.Credentials.from_service_account_info(google_credentials)
client = storage.Client(credentials=credentials, project=PROJECT_ID)
bucket = client.get_bucket(BUCKET_NAME)
blobs = bucket.list_blobs()

connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME,
    sslmode=DB_SSLMODE,
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS urls (
        id SERIAL PRIMARY KEY,
        original_url VARCHAR(2048) NOT NULL,
        short_url VARCHAR(255) NOT NULL,
        export_id VARCHAR(255) NOT NULL
    )
"""
)


@app.route("/generate_short_url", methods=["POST"])
def generate_short_url():
    global data
    short_url_id = hashids.encode(random.randint(1, 10000))
    short_url = f"{domain_url}{short_url_id}"

    export_id = hashids.encode(random.randint(1, 10000))
    cursor.execute(
        "INSERT INTO urls (original_url, short_url, export_id) VALUES (%s, %s, %s)",
        (f"/card/{export_id}", short_url, export_id),
    )

    html_content = request.data.decode("utf-8")
    with open("static/css/card.css", "r") as css_file:
        css_content = css_file.read()

    css_blob = bucket.blob(f"{export_id}.css")
    css_blob.upload_from_string(css_content)
    html_blob = bucket.blob(f"{export_id}.html")
    css_blob = bucket.blob(f"{export_id}.css")
    html_blob.upload_from_string(html_content)
    css_blob.upload_from_string(css_content)
    session["short_url_id"] = short_url_id
    return redirect(url_for("redirect_to_original_url", short_url=short_url_id))


@app.route("/share", methods=["GET", "POST"])
def share():
    global data
    data = request.data.decode("utf-8")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT userid, displayname, imageurl, uri FROM users ORDER BY created_at DESC LIMIT 1"
            )
            user_data = cursor.fetchone()
    except psycopg2.Error as e:
        print("Error retrieving data from 'users':", e)
        user_data = None
    if user_data:
        userid, displayname, imageurl, uri = user_data
        session["user_data"] = {
            "userid": userid,
            "displayname": displayname,
            "imageurl": imageurl,
            "uri": uri,
        }
    else:
        print("No se encontraron datos en la tabla 'users'.")

    return render_template("share.html")


@app.route("/card", methods=["GET", "POST"])
def share_socials():
    global data
    user_data = session.get("user_data")
    if user_data:
        userid = user_data["userid"]
        displayname = user_data["displayname"]
        imageurl = user_data["imageurl"]
        uri = user_data["uri"]
        uri_id = uri.split(':')[-1] 
        uri = f"https://open.spotify.com/user/{uri_id}"
    else:
        pass
    short_url = request.args.get("short_url")
    static_url = session.get("static_url")
    if request.method == "POST":
        static_url = request.form.get("static_url")
        session["static_url"] = static_url
        if static_url is None:
            return "Static_url no encontrada", 404
    return render_template(
        "card.html",
        data=data,
        short_url=short_url,
        static_url=static_url,
        userid=userid,
        displayname=displayname,
        imageurl=imageurl,
        uri=uri,
    )


@app.route("/shared/<short_url>")
def redirect_to_original_url(short_url):
    static_url = f"{domain_url}shared/{short_url}"
    session["static_url"] = static_url
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT export_id FROM urls WHERE short_url = %s",
            (f"{domain_url}{short_url}",),
        )
        result = cursor.fetchone()
        if result:
            export_id = result[0]

            html_blob = bucket.blob(f"{export_id}.html")
            css_blob = bucket.blob(f"{export_id}.css")

            html_content_bytes = html_blob.download_as_string()
            css_content_bytes = css_blob.download_as_string()
            html_content = html_content_bytes.decode("utf-8")
            css_content = css_content_bytes.decode("utf-8")

            return render_template(
                "shared.html",
                html_content=html_content,
                css_content=css_content,
                static_url=static_url,
            )
        else:
            return "URL no encontrada", 404


@app.route("/definitive_url_handler", methods=["GET", "POST"])
def definitive_url_handler():
    if request.method == "POST":
        pass
    static_url = session.get("static_url")
    return jsonify({"definitive_url": static_url})

if __name__ == "__main__":
    app.run(debug=False)
