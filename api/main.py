import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from klondike.bigquery.bigquery import BigQueryConnector
from twilio.rest import Client
from utils.logger import logger
from utils.twilio_helpers import handle_daily_reminder, handle_incoming_traffic
from utils.word_cloud_helpers import generate_word_cloud

##########

api = Flask(__name__)
api.logger.handlers = logger.handlers
api.logger.level = logger.level


@api.route("/", methods=["GET"])
def index():
    """
    This route displays a word-cloud of all affirmations
    """

    return render_template("index.html")


@api.route("/refreshCloud", methods=["GET", "POST"])
def refresh_cloud():
    "This route refreshes the word cloud on the landing page"

    NOW = datetime.now()
    logger.info(f"Refreshing the word cloud at {NOW}")

    BIGQUERY = BigQueryConnector()
    OUTPATH = os.path.join(api.static_folder, "wordCloud.png")
    logger.debug(f"Writing word cloud to {OUTPATH}...")

    generate_word_cloud(bq=BIGQUERY, outpath=OUTPATH)

    if request.args.get("webhook"):
        return "OK"

    logger.debug("Redirecting to index...")
    return redirect(url_for("index"))


@api.route("/sms", methods=["GET", "POST"])
def sms():
    """
    This route handles incoming traffic from Twilio
    """

    NOW = datetime.now()
    logger.info(f"Receiving an incoming text at {NOW}")

    BIGQUERY = BigQueryConnector()
    TRAFFIC = request.values

    handle_incoming_traffic(bq=BIGQUERY, traffic=TRAFFIC)

    return redirect(url_for("refresh_cloud", webhook=True))


@api.route("/reminder", methods=["GET"])
def reminder():
    """
    Determines whether or not Kane has sent in her gratitudes today
    """

    NOW = datetime.now()
    logger.info(f"Sending a gratitude reminder at {NOW}")

    TWILIO_CLIENT = Client(
        os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]
    )

    handle_daily_reminder(twilio_client=TWILIO_CLIENT)

    return "OK"
