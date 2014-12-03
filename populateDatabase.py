from feedbackForm.models import Users, Courses, Professors, Feedbacks
from feedbackForm.databaseManager import registerNewUser, registerNewProfessor

professorData = [("Dr. Santosh Biswas", "passy"), ("Dr. Saswata Shannigrahi", "passy"), ("Dr. Hemangee Kapoor", "passy"), ("Prof. Sajith Gopalan", "passy"), ("Dr. Aashish Anand", "passy"), ("Dr. Swaroop Nandan Bora", "passy"), ("Dr. Benny George", "passy"), ("Prof. Rafikul Alam", "passy"), ("Dr. Arunanshu Sil", "passy"), ("Prof. S.B. Santra", "passy"), ("Prof. S.K. Bose", "passy"), ("Prof. Govinda B. Shreshta", "passy")]

coursesData =  [("CS221", ["Dr. Santosh Biswas", "Dr. Hemangee Kapoor"]), ("CS202", ["Prof. Sajith Gopalan", "Dr. Aashish Anand"]), ("CS241", ["Dr. Santosh Biswas"]), ("MA201", ["Dr. Swaroop Nandan Bora"]), ("CS201", ["Dr. Saswata Shannigrahi"])]
coursesData += [("MA101", ["Prof. Rafikul Alam"]), ("PH101", ["Dr. Arunanshu Sil", "Prof. S.B. Santra"]), ("EE101", ["Prof. S.K. Bose", "Prof. Govinda B. Shreshta"])]

studentsData =  [("Student1", "spassy", ["CS221", "CS202", "CS241", "MA201", "CS201"])]
studentsData += [("Student2", "spassy", ["CS221", "CS202", "CS241", "MA201", "CS201"])]
studentsData += [("Student3", "spassy", ["CS221", "CS202", "CS241", "MA201", "CS201"])]
studentsData += [("Student4", "spassy", ["CS221", "CS202", "CS241", "MA201", "CS201"])]

studentsData += [("Student5", "spassy", ["MA101", "PH101", "EE101"])]
studentsData += [("Student6", "spassy", ["MA101", "PH101", "EE101"])]
studentsData += [("Student7", "spassy", ["MA101", "PH101", "EE101"])]
studentsData += [("Student8", "spassy", ["MA101", "PH101", "EE101"])]











#[{"type":"ratingOption", "description":"Please rate the professor overall", "name":"overall"}, {"type":"text", "name":"comments", "description":"Please give constructive comments if any"}]
#[{"type":"ratingSectionHeader", "description":"About the Instructor"}, {"type":"ratingOption", "description":"Please rate the professor overall", "name":"overall"}, {"type":"ratingOption", "name":"profRegularity", "description":"Has the professor been taking classes regularly?"}, {"type":"text", "name":"comments", "description":"Please give constructive comments if any"}]
#[{"type":"ratingSectionHeader", "description":"About the Instructor"}, {"type":"ratingOption", "description":"Please rate the professor overall", "name":"overall"}, {"type":"ratingOption", "name":"profRegularity", "description":"Has the professor been taking classes regularly?"}, {"type":"text", "name":"comments", "description":"Please give constructive comments if any"}, {"type":"ratingSectionHeader", "description":"About the TA"}, {"type":"ratingOption", "description":"Please rate the TA overall", "name":"taOverall"}, {"type":"ratingOption", "name":"taRegularity", "description":"Has the TA been taking classes regularly?"}, {"type":"text", "name":"taComments", "description":"Please give constructive comments if any"}]

'''Populate Professors'''
#professorData = [("ABC", "pAB"), ("BCD", "pCD"), ("CDE", "PDE")]

for x in professorData:
	registerNewProfessor(name = x[0], password = x[1])

'''Populate Courses'''

sampleFormFormat = "[{\"type\":\"ratingOption\", \"description\":\"Please rate the professor overall\", \"name\":\"overall\"}, {\"type\":\"text\", \"name\":\"comments\", \"description\":\"Please give constructive comments if any\"}]"
#coursesData = [("MA101", ["ABC"]), ("PH101", ["BCD", "CDE"])]

for x in coursesData:
	p = Courses(courseName = x[0], formFormat = "[]")
	p.save()
	print x
	for y in x[1]:
		try: p.professors.add(Professors.objects.filter(name=y)[0])
		except: print "Unique constraint failed for "+x; continue

'''Populate Users'''
#studentsData = [("User1", "Hi", ["MA101"]), ("User2", "Hello", ["MA101", "PH101"])]


for x in studentsData:
	registerNewUser(x[0], x[1], x[2])
	#for y in x[2]:
	#	Users.objects.filter(username=x[0]).add(Courses.objects.filter(courseName=y))
