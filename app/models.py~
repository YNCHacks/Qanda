from app import db
from flask import url_for
import datetime

class Question(db.Document):
    question = db.StringField(max_length = 511, required=True)
    answer = db.StringField(max_length =4095 )
    tags = db.ListField(db.EmbeddedDocumentField("Tag"))
    created_at = db.DateTimeField(default = datetime.datetime.now, required=True)
    answer_source = db.StringField(max_length = 63)
    answered_at = db.DateTimeField()
    question_source = db.StringField(max_length = 63, required=True)

    def get_question(self):
        return self.question


class Tag(db.Document):
    tag = db.StringField(max_length = 63, required=True)
    questions = db.ListField(db.EmbeddedDocumentField("Question"))
