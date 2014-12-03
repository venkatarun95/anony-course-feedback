import json
import math
from feedbackForm.models import Feedbacks, Courses
import nltk

def __getFeedbackArray(courseName):
	course = Courses.objects.filter(courseName = courseName)
	responses = Feedbacks.objects.filter(course = course)
	res = []
	for x in responses:
		res += [json.loads(x.feedbackString)]
	return res

#Returns mean and stddev (global and question-wise)
def getStatistics(courseName):
	course = __getFeedbackArray(courseName)
	question_wise = {}
	rating={"Strongly Disagree":1,"Disagree":2,"Neutral":3,"Agree":4,"Strongly Agree":5, "Cannot Comment":0}
	for i in course:
		for j in i.keys():
			
			if i[j] in rating.keys():
				if j in question_wise.keys():
					(question_wise[j])[0] += rating[i[j]]
					(question_wise[j])[1] += 1
				else:
					question_wise[j] = [rating[i[j]],1]
	avg = {}
	total = 0
	total_ques = 0
	for i in question_wise.keys():
		avg[i] = (question_wise[i])[0]/(question_wise[i])[1]
		total+=avg[i]
		total_ques+=1
	overallavg = 0
	
	overallavg = total/total_ques
	#overallavg = overall average
	#avg dictionary containing questionwise avg
	#Treat the first feedback as template

def getGraphsData(courseName):
	course = __getFeedbackArray(courseName)
	formDescription = json.loads(Courses.objects.filter(courseName=courseName)[0].formFormat)
	question_wise = {}
	rating={"Strongly Disagree":1,"Disagree":2,"Neutral":3,"Agree":4,"Strongly Agree":5, "Cannot Comment":0}
	for i in course:
		for j in i.keys():
			if i[j] in rating.keys():
				if j in question_wise.keys():
					(question_wise[j])[i[j]]+=1
				else:
					question_wise[j] = {"Strongly Disagree":0,"Disagree":0,"Neutral":0,"Agree":0,"Strongly Agree":0,"Cannot Comment":0 }
					for x in formDescription:
						if 'name' in x:
							if x["name"] == j:
								(question_wise[j])['description'] = x["description"] 
					(question_wise[j])[i[j]]=1
	ans={}
	for i in question_wise.keys():
		ans[i] = {}
		(ans[i])["StronglyDisagree"]=(question_wise[i])["Strongly Disagree"]
		(ans[i])["Disagree"]=(question_wise[i])["Disagree"]
		(ans[i])["Neutral"]=(question_wise[i])["Neutral"]
		(ans[i])["StronglyAgree"]=(question_wise[i])["Strongly Agree"]
		(ans[i])["Agree"]=(question_wise[i])["Agree"]
		(ans[i])["CannotComment"]=(question_wise[i])["Cannot Comment"]
		(ans[i])["description"]=(question_wise[i])["description"]
	rating={"StronglyDisagree":1,"Disagree":2,"Neutral":3,"Agree":4,"StronglyAgree":5, "CannotComment":0}
	for i in ans:
		sm=0
		total=0.0
		for j in ans[i]:
			if j in rating:
				total+=ans[i][j]*rating[j]
				sm+=ans[i][j]
		avg=0.0
		if sm !=0:
			avg=total/sm
		ans[i]['average']=avg
	variance=0
	for i in ans:
		for j in ans[i]:
			if j in rating:
				variance+=(ans[i][j]*rating[j]-ans[i][j]*ans[i]['average'])**2
		if sm!=0:
			variance/=sm
		variance=variance**(0.5)
		ans[i]['deviation']=(str(variance)+"00000")[:4]
		ans[i]['average'] = (str(ans[i]['average']) + "00000")[:4]
	return ans

def getOverall(courseName):
	course = __getFeedbackArray(courseName)
	rating={"Strongly Disagree":0,"Disagree":0,"Neutral":0,"Agree":0,"Strongly Agree":0,"Cannot Comment":0}
	for i in course:
		for j in i.keys():
			if i[j] in rating.keys():
				rating[i[j]] += 1
	rating2={}
	rating2["StronglyDisagree"]=rating["Strongly Disagree"]
	rating2["Disagree"]=rating["Disagree"]
	rating2["Neutral"]=rating["Neutral"]
	rating2["StronglyAgree"]=rating["Strongly Agree"]
	rating2["CannotComment"]=rating["Cannot Comment"]
	rating2["Agree"]=rating["Agree"]
	rating={"StronglyDisagree":1,"Disagree":2,"Neutral":3,"Agree":4,"StronglyAgree":5,"CannotComment":0}
	avg=0.0
	total=0
	for i in rating2:
		avg+=rating[i]*rating2[i]
		total+=rating2[i]
	if total!=0:
		avg/=total
	else:
		avg=0.0
	variance=0.0
	for i in rating2:
		variance+=(rating2[i]*rating[i]-rating2[i]*avg)**2
	if total!=0:
		variance/=total
	variance=variance**0.5
	rating2['average']=(str(avg)+"00000")[:4]
	rating2['deviation']=(str(variance)+"00000")[:4]
	return rating2

def getComments(courseName):
	course = __getFeedbackArray(courseName)
	comments=[]
	rating=["Strongly Disagree","Disagree","Neutral","Agree","Strongly Agree","Cannot Comment"]
	j=0
	for i in course:
		comments+=[{}]
		for k in i:
			if i[k] not in rating:
				(comments[j])[k] = i[k]
		j+=1
	return comments

def getComments_Question(courseName):
	formDescription = json.loads(Courses.objects.filter(courseName=courseName)[0].formFormat)
	commentsQues={}
	for i in formDescription:
		if i['type'] =='text':
			commentsQues[i['name']] = i['description']
	return commentsQues

def get_csv(courseName):
	feedback=__getFeedbackArray(courseName)
	formDescription = json.loads(Courses.objects.filter(courseName=courseName)[0].formFormat)
	CSV=[]
	CSVstr=""
	for j in feedback[0]:
		for k in formDescription:
			if "name" in k:
				if j == k["name"]:
					CSVstr+=k["description"]
					CSVstr+=", "
	CSV+=[CSVstr[:-2]]
	for i in feedback:
		CSVstr=""
		for j in i:
			if j != 'course':
				CSVstr+=i[j]
				CSVstr+=", "
		CSV+=[CSVstr[:-2]]
	return CSV
def getWordCloud(courseName):
	comments = getComments(courseName)
	questions = getComments_Question(courseName)
	words = {}
	for feedback in comments:
		for x in feedback:
			toks = nltk.word_tokenize(feedback[x])
			
			if x == "course":continue
			#x = questions[x]
			#if x not in words:
			#	words[x] = {}

			for w in toks:
				w = w.lower()
				if w in words:
					words[w] += 1
				else:
					words[w] = 1
	return words