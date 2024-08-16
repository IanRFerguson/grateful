import os
from datetime import datetime

from klondike.bigquery.bigquery import BigQueryConnector
from polars import DataFrame
from twilio.rest import Client

##########


def handle_incoming_traffic(bq: BigQueryConnector, traffic: object) -> None:
    """
    Logs incoming message from Twilio SMS to Google BigQuery
    """

    # Reshape to standard dict object
    traffic_meta = {k: v for k, v in traffic.items()}

    # Reshape to Polars DataFrame object
    traffic_meta_df = DataFrame(data=traffic_meta)
    traffic_meta_df["_load_timestamp"] = datetime.now()

    # Get destination table name from env
    destination_table_name = (
        f"{os.environ['DESTINATION_SCHEMA']}.{os.environ['DESTINATION_TABLE']}"
    )

    # Write Polars DF to BigQuery
    bq.write_dataframe(
        df=traffic_meta_df, table_name=destination_table_name, if_exists="append"
    )


def handle_daily_reminder(twilio_client: Client) -> None:
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
    if not latest_message_from_kane == today:
        send_reminder_text(twilio_client=twilio_client)


def send_reminder_text(twilio_client: Client):
    message_body = """Hi Kane!\n
It's getting late and it looks like you haven't
sent in your gratitudes for the day. Respond to this text
with five things you're grateful for.\n
Peace and love,
The Gratitude Robot
    """

    twilio_client.messages.create(
        to=os.environ["KANES_PHONE_NUMBER"],
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        body=message_body,
    )
