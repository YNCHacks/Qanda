# -*- coding: utf-8 -*-

from app.views import *

questions = [unicode("Are Long Term Visit Pass holders entitled to child care leave?"),	unicode("Are non-Singapore citizens such as Permanent Resident, Dependant Pass, Long Term Visit Pass, S-Pass, R-Pass and Employment Pass holders entitled to childcare leave?"),
						unicode("Are part-time employees covered by the Employment Act?"),
						unicode("What is online submission of documents?"),
						unicode("Who can do eSubmission?")]
answers = [unicode("Part IX of the Employment Act (EA) and Part III of the Child Development Co-Savings Act (CDSA) provide childcare leave entitlements for employees."),
						unicode("Are non-Singapore citizens such as Permanent Resident, Dependant Pass, Long Term Visit Pass, S-Pass, R-Pass and Employment Pass holders entitled to childcare leave?"),
						unicode("Part-time employees (except managers or executives earning a basic monthly salary of more than $4,500, domestic workers and seafarers) are covered under the Employment Act."),
						unicode("It refers to the electronic submission (eSubmission) of documents via EP Online during issuance renewal of pass. With eSubmission, we are able to verify the pass holders documents online. The pass holder company representative need not visit our centre with documents anymore. Just login to EP Online, scan and upload the necessary documents before you issue or renew the pass."),
						unicode("Business Employer/ Employment Agency with a valid EP Online account while Personalised Employment Pass/EntrePass holders with a SingPass account will be able to access eSubmission.")]

def upload_faq_ans(ques,ans):
	add_answer(upload_new_question('MOMFAQ',ques,keywordize(ques)),ans)

def upload_lib():
	for i in range(0,len(questions)):
		add_answer(upload_new_question('MOMFAQ',questions[i],keywordize(questions[i])),answers[i])
