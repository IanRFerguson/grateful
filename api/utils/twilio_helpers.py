import os
import random
from datetime import datetime

import polars as pl
from klondike.gcp.bigquery import BigQueryConnector
from twilio.rest import Client
from utils.logger import logger

##########


def handle_incoming_traffic(bq: BigQueryConnector, traffic: object) -> None:
    """
    Logs incoming message from Twilio SMS to Google BigQuery
    """

    # Reshape to standard dict object
    traffic_meta = {k: v for k, v in traffic.items()}

    # Reshape to Polars DataFrame object
    traffic_meta_df = pl.DataFrame(data=traffic_meta)
    traffic_meta_df = traffic_meta_df.with_columns(_load_timestamp=datetime.now())

    # Get destination table name from env
    destination_table_name = (
        f"{os.environ['DESTINATION_SCHEMA']}.{os.environ['DESTINATION_TABLE']}"
    )

    # Write Polars DF to BigQuery
    bq.write_dataframe(
        df=traffic_meta_df, table_name=destination_table_name, if_exists="append"
    )


def handle_daily_reminder(twilio_client: Client, force: bool = False) -> None:
    """
    Checks to see if Kane has sent in a gratitude today. If
    she hasn't, we'll send her a gentle reminder
    """

    # Get a list of all messages that Kane has sent
    all_messages = [
        x.date_sent.date()
        for x in twilio_client.messages.list()
        if x.from_ == os.environ["KANES_PHONE_NUMBER"]
    ]

    # Compare today's date with the most recent gratitude submitted
    latest_message_from_kane = max(all_messages)
    today = datetime.now().date()

    # Send Kane a reminder text if we haven't received a gratitude today
    if not latest_message_from_kane == today or force:
        logger.info(f"Sending remdiner message")
        send_reminder_text(twilio_client=twilio_client)
    else:
        logger.info(f"Last received message @ {latest_message_from_kane}")


def send_reminder_text(twilio_client: Client):
    salutations = [
        "Peace and love",
        "Elvis and I love you so much",
        "You're the light of our lives",
        "I hope you have a great day",
    ]

    option = random.choice(salutations)

    message_body = f"""Good morning Kane!\n
Respond to this text with five things you're grateful for.\n
You can also visit https://grateful-dev-928973048225.us-central1.run.app any time to see
all the things that have brought you joy lately.\n
{option},
The Gratitude Robot
    """

    if os.environ.get("PROD") == "true":
        destination_number = os.environ["KANES_PHONE_NUMBER"]
    else:
        destination_number = os.environ["IANS_PHONE_NUMBER"]

    twilio_client.messages.create(
        to=destination_number,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        body=message_body,
    )
