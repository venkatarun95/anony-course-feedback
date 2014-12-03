import json
import copy

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from feedbackForm.dataAnalytics import getStatistics,getGraphsData,getOverall
from feedbackForm.models import Users, Courses, Professors
import databaseManager

# Create your views here.
def index(request):
	return render(request, '')

def loginPage(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/feedback/student_home')
			else:
				return render(request, 'login.html', {"error_message": 'Sorry your account has been disabled.'})
		else:
			return render(request, 'login.html', {"error_message": 'Atleast one of the given username and password is incorrect.'})
	elif request.method == 'GET':
		return render(request, 'login.html')

@login_required
def student_home(request):
	#assert(False)
	username = str(request.user)
	if len(Users.objects.filter(username = username)) != 0:
		courses, courseID = [], 1
		for x in Users.objects.filter(username = username)[0].courses.all():
			profs = []
			for y in x.professors.all():
				profs += [y.name]
			#Calculate percentage completed
			feedbackStr = json.loads(databaseManager.getUsersFormStr(username, User.objects.filter(username = username)[0].password, courseID))
			noCompleted, totalFields = 0,0
			for y in feedbackStr:
				if y == 'course': continue
				if feedbackStr[y] != "": noCompleted += 1
				totalFields += 1
			if totalFields == 0: percentCompleted = 100
			else: percentCompleted = (noCompleted*100)/totalFields
			courses += [{"courseName": x.courseName, "profs": profs, "details": "xyz", "percentCompleted": percentCompleted}]
			courseID += 1
		return render(request, 'student_home.html', {"courses": courses})
	elif len(Professors.objects.filter(name = username)) != 0:
		courses = []
		for x in Courses.objects.all():
			if len(x.professors.filter(name = username)) != 0:
				profs = []
				for y in x.professors.all():
					profs += [y.name]
				courses += [{"courseName": x.courseName, "profs": profs, "details": "xyz"}]
		#assert(False)
		return render(request, 'professor_course_dashboard.html', {"courses": courses})
	else:
		pass

@login_required
def student_feedback_form(request):
	#XYZNOTE SECURITY WARNING - One could fill the form for one course and give POST request for another user
	username = str(request.user)
	user = Users.objects.filter(username = username)[0]
	passwordHash = User.objects.filter(username = username)[0].password

	if request.method == "GET":
		courseName = request.GET.get('course', '')
		if courseName == '':
			return HttpResponse("Please specify a course")
		course = Users.objects.filter(username = username)[0].courses.filter(courseName = courseName)
		if len(course) == 0:
			return HttpResponse("Sorry, you are not registered for this course.")
		assert(len(course) == 1)
		course = course[0]
		formFormat = json.loads(course.formFormat)

		#Populate it with data from previous feedback
		courseID = user.courses.filter(courseName = courseName)[0].id
		prevForm = json.loads(databaseManager.getUsersFormStr(username, passwordHash, courseID))
		print prevForm
		for x in range(len(formFormat)):
			if "name" in formFormat[x] and formFormat[x]["name"] in prevForm:
				formFormat[x]["prevValue"] = prevForm[formFormat[x]["name"]]
			else:
				formFormat[x]["prevValue"] = ""

		#Get discussion data
		privateMessagesStr = databaseManager.readPrivateStudMessageStr(username, passwordHash, courseID)
		privateMessages = []
		for x in json.loads(privateMessagesStr):
			privateMessages += [json.loads(x)]
		print privateMessages
		return render(request, 'student_feedback_form.html', {"formFormat": formFormat, "course": courseName, "messages": privateMessages})

	elif request.method == "POST":
		course = request.POST.dict()["course"]
		courseID = user.courses.filter(courseName = course)[0].id
		record = copy.deepcopy(request.POST.dict())
		record.pop('csrfmiddlewaretoken')
		record.pop('privateMessage')
		databaseManager.setUsersFormStr(username, passwordHash, courseID, json.dumps(record))
		
		newMsg = request.POST.dict()["privateMessage"]
		print "Message: ", newMsg
		if newMsg != "":
			newMsg = "{\"from\":\"student\", \"msg\": \""+newMsg+"\"}"
			databaseManager.addPrivateMessageStr(username, passwordHash, courseID, newMsg)
		return HttpResponse("Your response has been recorded")

def form_creator(request):
	if request.method == "GET":
		courseName = request.GET.get("course", '')
		if courseName == '':
			return HttpResponse("Please specify a course")
		#course = Users.objects.filter(username = username)[0].courses.filter(courseName = courseName)
		#if len(course) == 0:
		#	return HttpResponse("Sorry, you are not registered for this course.")
		#assert(len(course) == 1)

		courseForm = json.loads(Courses.objects.filter(courseName = courseName)[0].formFormat)
		return render(request, 'form_creator.html', {"courseForm": courseForm, "course": courseName})
	elif request.method == "POST":
		courseName = request.POST.dict()["course"]
		formFields = request.POST.dict()
		res = []
		print formFields 
		for x in formFields:
			if x[:8] == "question":
				y = formFields["radioQuestion"+x[8:]]
				f = {"description": formFields[x], "name": "field"+str(len(res)), "type": y}
				res += [f]
		Courses.objects.filter(courseName = courseName).update(formFormat = json.dumps(res))
		return HttpResponse("Your form has been recorded.")
@login_required
def analytics_page(request):
	#verify later
	courseName=request.GET.get('course', '')
	a=getGraphsData(courseName)
	b=getOverall(courseName)
	questionWise=[]
	j=0
	for i in a:
		questionWise+=[{}]
		for k in a[i]:
			(questionWise[j])[k] = (a[i])[k]
		(questionWise[j])['name'] = i
		j+=1

	#assert(False)
	return render(request, 'profcoursepage1.html', {"overall": b,"questionWise" : questionWise,"courseName":courseName })
