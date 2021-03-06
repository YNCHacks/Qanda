from app import application, db, twilio_client
from twilio import twiml
from models import Question, Tag
from flask import render_template, flash, redirect, session, url_for, request, Response
from datetime import datetime
from forms import AnswerForm
from nlp import *
from config import *

from twilio_control import *

verbose = get_verbose()
twilio_number = "+15136572632"

@application.route("/", methods=["GET", "POST"])
@application.route("/index", methods=["GET", "POST"])
def index():
    questions = Question.objects.all()
    return render_template("index.html", 
            title = "Home",
            questions = questions)

@application.route("/answer/<questionid>", methods=["GET", "POST"])
def answer(questionid):
    form = AnswerForm()
    question = Question.objects.get_or_404(id=questionid)
    if form.validate_on_submit():
        question.answer = form.answer.data
        question.save()
        flash("Your answer has been saved.")
        return redirect(url_for("index"))
    return render_template("answer.html", form=form, question=question)

@application.route("/message", methods=["POST"])
def message():
    messages = twilio_client.messages.iter(to=twilio_number)
    phone_numbers = []
    questions = []
    for message in messages:
        phone_numbers.append(message.from_)
        questions.append(message.body)
    receive_sms(phone_numbers[0], questions[0])
    return ""

def set_verbose(val):
    if(bool(val)==True):
        verbose=True
    else:
        verbose=False

def get_verbose():
    return verbose

#ask function to actually ask the question. Looks for matching questions in the database

def ask(question_source, question):

    #edit this threshold to make question matching tighter
    if(verbose):
        print "Received Question from "+question_source+": "+question
    threshold = 0.3

    #Generate tags
    gen_tags = keywordize(question);
    if(verbose==True):
        print "Tags Generated: "
        print gen_tags    
    
    #Search db using the tags to get similar questions and answers
    similar_questions = search_by_tags(gen_tags);
    similarity = []

    if(verbose==True):
        print "Found "+str(len(similar_questions))+" possible question matches:"

    for sim_question in similar_questions:
        similarity.append(nlp_string_match(question,sim_question.question))
        sim_question.answer = Question.objects.get(id=sim_question.id).answer

        if(verbose==True):
            print "Question: "+sim_question.question+", id = "+str(sim_question.id)+", Compatibility score: "+str(similarity[len(similarity)-1])
            if(sim_question.answer != None):
                print "Fina-fuckin-ly! Answer: "+sim_question.answer


    #if we have some matches

    if(len(similarity)>0):
        best_q = 0
        for i in range(0,len(similarity)):
            if(similarity[i]>similarity[best_q]):
                if(similar_questions[i].answer != None or 
                        similar_questions[best_q] == None):
                    best_q = i
        if(verbose==True):
            print "Best question: "+similar_questions[best_q].question+" is the closest match. The threshold is "+str(threshold)
        #Check to see if there is a match
        if(similarity[best_q]>=threshold):
            if(verbose==True):
                print "Match found! Answer: "+similar_questions[best_q].answer
            if(similar_questions[best_q].answer != None):
                if(verbose==True):
                    print "Answer found for match: " + similar_questions[best_q].answer
                return similar_questions[best_q].answer

    if(verbose==True):
        print "No Match Found. Querying Knowledge Engine..."
    #Ask WolframAlpha for an answer
    wolf_ans = askwolf(question)

    #Wolf Answer found!
    if(wolf_ans != '404' and wolf_ans != ""):
        if(verbose==True):
            print "Knowledge engine computations succeeded. Answer: "+wolf_ans
        return wolf_ans

    #All avenues exhausted, add the question and exit
    if(verbose==True):
        print "No answers found. Registering question: "
 
    upload_new_question(question_source,question,gen_tags)
    return None

#Upload a new question if there is no prior example
#Returns the new question's id
def upload_new_question(question_source, question, tags):
    new_question = Question(question = question, question_source=question_source)
    new_question.save()
    tags_final = []

    for tag in tags:
        try:
            search_tag = Tag.objects.get(tag=tag)
            tags_final.append(search_tag)
            continue
        except Tag.DoesNotExist:
            new_tag = Tag(tag=tag)
            new_tag.save()
            tags_final.append(new_tag)
            continue
        continue
    
    for tag in tags_final:
        print tag.tag

    for tag in tags_final:
        tag.questions.append(new_question)
        tag.save()
        continue

    return new_question.id

#Search the database for relevant questions/answers with tags as parameters
def search_by_tags(tags_param):
    tags = []
    for tag in tags_param:
        try:
            tag_search = Tag.objects.get(tag=tag)
            tags.append(tag_search)
        except Tag.DoesNotExist:
            continue

    questions = []
    for tag in tags:
        for question in tag.questions:
            questions.append(question)
    #TODO: Get rid of the answers section later
    '''
    answers = []
    for question in questions:
        if question.answer != []:
            answers.append(question.answer)
        continue
    '''
    return questions

#Returns an array of potential answers
def has_answer(question, tags):
    answers = []
    try:
        question=Question.objects.get(question=question)
        answers.append(question.answer)
    except Question.DoesNotExist:
        answers = search_by_tags(tags)
    return answers

#Adds answer to a question. Takes the question id as input
def add_answer(questionid, answer):
    question = Question.objects.get(id=questionid)
    question.answer = answer
    try:
        question.save()
    except:
        return False

    tags = Tag.objects.all()
    for tag in tags:
        q_id = []
        for q in tag.questions:
            q_id.append(q.id)
        if question.id in q_id:
            tag.questions[q_id.index(question.id)].answer = answer
            tag.save()

    return True

def receive_sms(fromno, message):
    parts = message.split('#')
    lang = 'en'
    prefix = 'mes'
    #check to see if the first part is indeed a number

    #See if it is a well formatted message
    if(len(parts)==3):
        lang = parts[1][0:3]
        prefix = parts[0][0:2]
        ans = ask(fromno,parts[2])
        print ans
    else:
        ans = ask(fromno,message)
        print ans

    if(ans==None):
        ans = "Your question has been registered."

    if(verbose==True):
        print "Sending sms to "+fromno+"..."
    send_message(ans,fromno)
    
    if(verbose==True):
        print "The answer is: "+ans+". Translating into "+lang+"..."
    speak(ans,lang,prefix);

    return None
