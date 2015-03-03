from app import twilio_client
#from app import views, nlp

twilio_number = "+15136572632"

#Send a message to the question_source
def send_message(answer, question_source):
    twilio_client.messages.create(to=question_source, from_=twilio_number,
            body=answer)

#Make a call to the question_source with the audio file(s)
def make_call(answer, question_source, file_name):
    twilio_client.calls.create(to=question_source, from_=twilio_number,
            url=file_name)


