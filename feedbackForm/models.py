from django.db import models

# Create your models here.

class RatingQuestion(models.Model):
	RATINGS = (
		("1", "Strongly Disagree"), 
		("2", "Disagree"), 
		("3", "Neutral"), 
		("4", "Agree"), 
		("5", "Strongly Agree"),
	)
	questionName = models.CharField(max_length = 256)
	rating = models.CharField(max_length = 120, choices = RATINGS, blank=True, help_text = "Indicate your opinion by selecting one of the options")
	rateDate = models.DateTimeField(blank=True)

class Users(models.Model):
	username = models.CharField(max_length = 256)
	secretHash = models.CharField(max_length=32)
	privateKey = models.CharField(max_length = 4096)
	publicKey = models.CharField(max_length = 4096)
	courses = models.ManyToManyField("Courses")
	def __str__(self):
		return "Student: " + self.username

class Feedbacks(models.Model):
	feedbackString = models.CharField(max_length = 4096)
	professorPrivate = models.CharField(max_length = 65536)
	studentPrivate = models.CharField(max_length = 65536)
	studentPublicKey = models.CharField(max_length = 65536)

	course = models.ForeignKey("Courses")
	def __str__(self):
		return "Feedback for course: " + str(self.course.id)

class Professors(models.Model):
	name = models.CharField(max_length = 255)
	privateKey = models.CharField(max_length = 4096)
	publicKey = models.CharField(max_length = 4096)
	def __str__(self):
		return "Professor: " + self.name
	#feedbacks = models.ManyToManyField("Feedbacks")

class Courses(models.Model):
	courseName = models.CharField(max_length = 512)
	professors = models.ManyToManyField("Professors")
	formFormat = models.CharField(max_length = 4096)

	def __str__(self):
		return "Course: " + self.courseName

#from feedbackForm.models import RatingQuestion; from feedbackForm.models import RatingQuestion
#from feedbackForm.models import RatingQuestion