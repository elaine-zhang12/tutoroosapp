from django.db import models


class Review(models.Model):
    review_title = models.CharField(default="", max_length=100)
    review = models.CharField(default="", max_length=400)

class Course(models.Model):
    mnemonic = models.CharField(max_length=10)
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=256)

    def __str__(self):
        return "%s %s" % (self.mnemonic, self.course_name)


class Tutor(models.Model):
    name = models.CharField(max_length=256)
    last_name = models.CharField(default="",max_length=256)
    email = models.CharField(max_length=256)
    price = models.DecimalField(default=15.00,max_digits=7, decimal_places=2 )
    subject = models.CharField(default="",max_length=256)
    courses = models.ManyToManyField(Course, blank=True)
    rating = models.FloatField(default=0.0)
    numRatings = models.IntegerField(default=0)
    availability=models.TextField(default='',blank=True)#This is basically an int array that stores the selection made by the tutors for the times they are avaliable, however there is no array in django models, so instead its a comma seperates string :(
    pendingRequests=models.ManyToManyField('Request', blank=True, related_name='pending')
    acceptedReqests=models.ManyToManyField('Request',blank=True,related_name='accepted')
    reviews = models.ManyToManyField(Review, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    def __str__(self):
        return self.name
    def addRating(self, newRating):
        self.rating = (self.rating*self.numRatings + newRating)/(self.numRatings+1)
        self.numRatings += 1

class Student(models.Model):
    email= models.CharField(max_length=256,default='')
    name= models.CharField(max_length=256,default='')
    last_name=models.CharField(max_length=256, default="")
    pendingRequests=models.ManyToManyField('Request',blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    def __str__(self):
        return self.name


class TutorCourse(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=10)
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=256)

class Request(models.Model):
    course=models.ForeignKey(Course, blank=True, on_delete=models.DO_NOTHING,null=True)
    number = models.IntegerField(default=0)
    day=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    status=models.CharField(max_length=20, default='No')
    Student=models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    Tutor=models.ForeignKey(Tutor, on_delete=models.DO_NOTHING)



