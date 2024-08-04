# Grateful

This is a lightweight Flask app that receives an SMS response from Twilio, loads the result into Google BigQuery, and processes a word cloud.

See `prod.env.template` for the required environment variables to make this thing go. You'll want to put your credentials in a `prod.env` file before running.

```
# Run the app locally
make build-app
```
