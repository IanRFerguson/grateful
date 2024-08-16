import os

from flask import Flask, render_template, request
from klondike.bigquery.bigquery import BigQueryConnector
from twilio.rest import Client
from utils.twilio_helpers import handle_daily_reminder, handle_incoming_traffic

##########

api = Flask(__name__)


@api.route("/")
def index():
    """
    This route displays a word-cloud of all affirmations
    """

    return render_template("index.html")


@api.route("/log")
def log():
    """
    This route shows a table of all incoming messages
    """

    pass


@api.route("/refreshCloud")
def refresh_cloud():
    "This route refreshes the word cloud on the landing page"

    pass


@api.route("/sms", methods=["GET", "POST"])
def sms():
    """
    This route handles incoming traffic from Twilio
    """

    BIGQUERY = BigQueryConnector()
    TRAFFIC = request.values

    handle_incoming_traffic(bq=BIGQUERY, traffic=TRAFFIC)

    return "OK"


@api.route("/reminder", methods=["GET"])
def reminder():
    """
    Determines whether or not Kane has sent in her gratitudes today
    """

    TWILIO_CLIENT = Client(
        os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]
    )

    handle_daily_reminder(twilio_client=TWILIO_CLIENT)

    return "OK"
