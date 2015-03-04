# Qanda
Qanda is an SMS-based Q&amp;A forum that connects foreign workers without smartphones or internet connection to answers they may seek.

It was created for the Manpower Hackathon held in Singapore in February 2015.

#How it works
The user sends a text to a mobile number, which is registered in Qanda's MongoDB database. Qanda queries the database for similar questions and answers. If it doesn't find the answer at this stage, it moves on to the web using Wolfram Alpha's Knowledge Engine. Using Google's translation platform, the answer can be translated into almost any language accurately.

Upon retrieval of the answer, Qanda sends it back to the user, either as a text or an audio file. All interactions between the user and Qanda are handled with the use of the Twilio API.

The web interface is built using Flask and bootstrap.
