from flask import Flask
from flask.ext.mongoengine import MongoEngine
from .momentjs import momentjs
from twilio.rest import TwilioRestClient
from config import twilio_account, twilio_token


application = Flask(__name__)
application.config["MONGODB_SETTINGS"] = {"DB": "mchammer"}
application.config["SECRET_KEY"] = "S3Cr3T"
application.config.from_object("config")
application.jinja_env.globals["momentjs"] = momentjs

db = MongoEngine(application)
twilio_client = TwilioRestClient(twilio_account, twilio_token)


if __name__ == "__main__":
    application.run(host="0.0.0.0")

#last line to avoid improt errors
from app import views, models
