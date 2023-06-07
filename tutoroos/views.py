from django.shortcuts import render, redirect, reverse
from tutoroos.models import *
from django.template import Context, Template
from django.http import HttpResponse
from django.contrib import messages
#from django.contrib.auth.models import User
# from django.http import HttpResponse
from .models import *
import requests

currPage=0

def home(request):
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True


    return render(request,'index.html',{"authed":loggedIn, "tutor":isTutor})

def signup(request):
    return render(request,'signup.html')

def tutors(request):
    tutors = Tutor.objects.all()
    if 'name' in request.GET or 'number' in request.GET or 'class' in request.GET:
        name = request.GET['name'].upper()
        number = request.GET['number']
        class_name = request.GET['class']

        if name == "" and number == "" and class_name == "":
            tutors = {}
        elif name == "" and class_name == "":
            tutors = Tutor.objects.filter(courses__course_number=number).distinct()
        elif number == "" and class_name == "":
            tutors = Tutor.objects.filter(courses__mnemonic=name).distinct()
        elif number == "" and name == "":
            tutors = Tutor.objects.filter(courses__course_name__iexact=class_name).distinct()
        elif class_name =="":
            tutors = Tutor.objects.filter(courses__course_number=number, courses__mnemonic=name).distinct()
        elif name =="":
            tutors = Tutor.objects.filter(courses__course_number=number, courses__course_name=class_name).distinct()
        elif number =="":
            tutors = Tutor.objects.filter(courses__course_name=class_name, courses__mnemonic=name).distinct()

        else:
            tutors = Tutor.objects.filter(courses__course_name=class_name, courses__mnemonic=name, courses__course_number=number).distinct()
    
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True
    
    return render(request,'tutorsearch.html',{"tutors":tutors, "authed":loggedIn, "tutor":isTutor} )

def about(request):
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True
    return render(request,'about.html',{"authed":loggedIn, "tutor":isTutor} )

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'login.html')

#this is the page taken to after logging in with google, if the user already exists, takes you to the showtype page, if not, shows a registration form
def hasAccount(request):
    if Student.objects.filter(email=request.user.email).exists() or Tutor.objects.filter(email=request.user.email).exists():
        #redirect, they are already a user
        return redirect('/afterlogin/')
    else:
        loggedIn = False
        isTutor = False
        if request.user.is_authenticated:
            loggedIn = True
            if Tutor.objects.filter(email=request.user.email).exists():
                isTutor = True
        context={
            'email': request.user.email,
            "authed":loggedIn,
            "tutor":isTutor
        }
    return render(request,'signup.html',context)


# this makes the user, should always redirect after so shouldnt show a page ussually
def makeNewTutor(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if Tutor.objects.filter(email=request.user.email).exists():
                return redirect('/register/')
        new_first = request.POST['name']
        new_last = request.POST['last_name']
        new_cost = request.POST['cost']
        new_pp = request.FILES.get('pic')
        new_tutor = Tutor(name=new_first, last_name=new_last, email=request.user.email, price=float(new_cost))
        new_tutor.profile_pic = new_pp
        new_tutor.save()
        return redirect('/register/')

    return HttpResponse("Some sort of error has occured because neither a Tutor or Studnet was made, you must have come to this page on a non-Post request, or you didnt check an option in the form")

def makeNewStudent(request):
    if request.method== 'POST':
        if request.user.is_authenticated:
            if Student.objects.filter(email=request.user.email).exists():
                return redirect('/tutors/')
        new_first = request.POST['fname']
        new_last = request.POST['lname']
        new_pp = request.FILES.get('student_pic')

        new_student = Student(email=request.user.email, name=new_first, last_name=new_last)
        new_student.profile_pic = new_pp
        new_student.save()
        return redirect('/tutors/')

    return HttpResponse("Some sort of error has occured because neither a Tutor or Studnet was made, you must have come to this page on a non-Post request, or you didnt check an option in the form")


#this is just to get the sprint3 requirements, just shows whether the current User is a tutor or student
def showTutorOrStudent(request):
    if request.user.is_authenticated:
        if Student.objects.filter(email=request.user.email).exists():
            type="Student"
        if Tutor.objects.filter(email=request.user.email).exists():
            return redirect('/register/')
    else:
        return HttpResponse("you are not logged in")
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True
    context={
        'type': type,
        "authed":loggedIn,
        "tutor":isTutor
    }
    return render(request, "showtype.html", context)

def tutorregistration(request):
    count_courses = Course.objects.all()
    all_courses = {}

    if count_courses.count() == 0:
        page_num = 1
        courses = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=%d' % (
                page_num)).json()
        while not courses == []:
            for i in courses:
                if not Course.objects.filter(course_name=i['descr'], course_number=i['catalog_nbr']).exists():
                    course_data = Course(
                        mnemonic=i['subject'],
                        course_number=i['catalog_nbr'],
                        course_name=i['descr'],
                    )
                    course_data.save()

            page_num += 1
            courses = requests.get(
                'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=%d' % (
                    page_num)).json()
    value = ""
    if 'name' in request.GET or 'number' in request.GET or 'class' in request.GET:
        name = request.GET['name'].upper()
        number = request.GET['number']
        class_name = request.GET['class']

        if name == "" and number == "" and class_name == "":
            all_courses = {}
        elif name == "" and class_name == "":
            all_courses = Course.objects.filter(course_number=number)
        elif number == "" and class_name == "":
            all_courses = Course.objects.filter(mnemonic=name)
        elif number == "" and name == "":
            all_courses = Course.objects.filter(course_name__iexact=class_name)
        elif class_name =="":
            all_courses = Course.objects.filter(course_number=number, mnemonic=name)
        elif name =="":
            all_courses = Course.objects.filter(course_number=number, course_name=class_name)
        elif number =="":
            all_courses = Course.objects.filter(course_name=class_name, mnemonic=name)
        if len(all_courses) == 0:
            value = "No courses found. Search again."
    return render(request, 'tutorregistration.html', {"courses": all_courses, "authed":request.user.is_authenticated, "tutor":Tutor.objects.filter(email=request.user.email).exists(), "empty":value})

def addClasses(request):
    if request.method == 'POST':
        add_courses = request.POST.getlist('add_courses')
        for course in add_courses:
            tutor_user = Tutor.objects.get(email=request.user.email)
            course_to_add = Course.objects.get(pk=int(course))
            if not tutor_user.courses.filter(pk=course_to_add.pk):
                tutor_user.courses.add(course_to_add)
                tutor_user.save()

    return redirect('/confirmation/')


def results(request):
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True
    return render(request, 'results.html', {"authed":loggedIn, "tutor":isTutor})



def Populate(request):
    global currPage
    courses = requests.get('https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=%d' %(currPage) ).json()
    for i in courses:
        if not Course.objects.filter(course_name=i['descr'],course_number=i['catalog_nbr']).exists():
            course_data = Course(
            mnemonic=i['subject'],
            course_number=i['catalog_nbr'],
            course_name=i['descr'],
            )
            course_data.save()
    currPage+=1
    return redirect("/populate/")

def profile(request):
    isTutor = ""
    valid = False
    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            valid = True
        user = {}
        user["name"] = "No account user found."
        user["email"] = "No account email address found."
        if valid:
            user = Tutor.objects.get(email=request.user.email)
            identity = "Tutor"
            return render(request, 'profile.html', {"authed": True, "isTutor": identity,"valid":valid, "user": user})
        else:
            user = Student.objects.get(email=request.user.email)
            identity = "Student"
            return render(request, 'profile.html', {"authed": True, "isTutor": identity, "valid":valid, "user" : user})
    else:
        return render(request, 'profile.html', {"authed": False, "isTutor": isTutor,"valid":valid, "user": {"name": "", "email": ""}})


def edit_profile(request):
    identity = ""
    if Tutor.objects.filter(email=request.user.email).exists():
        user = Tutor.objects.get(email=request.user.email)
        identity="Tutor"
    elif Student.objects.filter(email=request.user.email).exists():
        user = Student.objects.get(email=request.user.email)
        identity="Student"
    return render(request, 'edit_profile.html', {"user": user, "isTutor":identity})

def editprof(request):
    if request.method == 'POST':
        new_first = request.POST['fname']
        new_last = request.POST['lname']
        new_pp = request.FILES.get('profile_pic')
        if Tutor.objects.filter(email=request.user.email).exists():
            new_cost = request.POST['cost']
            user = Tutor.objects.get(email=request.user.email)
            user.name = new_first
            user.last_name = new_last
            user.price = new_cost
            if new_pp:
                user.profile_pic = new_pp
            user.save()
            return redirect('/profile/')
        elif Student.objects.filter(email=request.user.email).exists():
            user = Student.objects.get(email=request.user.email)
            user.name = new_first
            user.last_name = new_last
            if new_pp:
                user.profile_pic = new_pp
            user.save()
            return redirect('/profile/')
    return render(request, 'edit_profile.html')

#display a table of time slots for a tutor to select when they are avaliable to tutor during
def tableAval(request):
    zero7=[1,2,3,4,5,6,7]
    
    #clock={"9:00":1,"10:00":2,"11:00":3}
    #clock=[["9:00",1,2,3,4,5,6,7],["10:00",8,9,10,11,12,13,14],["11:00",1,2,3,4,5,6,7]]

    listOfLists=[["9:00 AM"],["9:30 AM"],["10:00 AM"],["10:30 AM"],["11:00 AM"],["11:30 AM"],["12:00 PM"],["12:30 PM"],
    ["1:00 PM"],["1:30 PM"],["2:00 PM"],["2:30 PM"],["3:00 PM"],["3:30 PM"],["4:00 PM"],["4:30 PM"],
    ["5:00 PM"],["5:30 PM"],["6:00 PM"],["6:30 PM"],["7:00 PM"],["7:30 PM"],["8:00 PM"],["8:30 PM"],["9:00 PM"],["9:30 PM"],
    ["10:00 PM"],["10:30 PM"],["11:00 PM"],["11:30 PM"],["12:00 AM"]]
    
    counter=1
    for list in listOfLists:
        for num in zero7:
            list.append(counter)
            counter+=1



    context = {
        "listOfLists": listOfLists,
    }

    return render(request, 'avaliabilityTable.html', context)


def storeCheckedBoxes(request):
    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            CurrTutor = Tutor.objects.filter(email=request.user.email).get()
        else: 
            return HttpResponse("Error, you should not be here bc you are not a tutor!")
    else:
        return redirect("/login/")


    on=','
    for key in request.POST:
        if request.POST[key]=='on':
            on+=(key+',')

    CurrTutor.availability=on
    CurrTutor.save()



    return redirect('/profile/')

def tutor_info(request, tutor_id):
    tutor_obj = Tutor.objects.get(id=tutor_id)
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True

    context = {
        'tutor_obj': tutor_obj, "authed": loggedIn, "tutor": isTutor,
    }

    return render(request, 'publicTutorPage.html', context=context)

def showAval(request, tutor_id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    #How are we getting a specific tutor??

    #CurrTutorEmail='samuelharless10@gmail.com'
    selected=''



    if Tutor.objects.filter(id=int(tutor_id)).exists():
        CurrTutor=Tutor.objects.filter(id=int(tutor_id)).get()
        selected=CurrTutor.availability


    #now have availabilty in string format, need to convert it to an array
    iterator=1
    selectedNums=[]
    while iterator<len(selected):
        selectedNums.append(int(selected[1:selected.index(',',1)]))
        selected=selected[selected.index(',',1):len(selected)]


    zero7=[1,2,3,4,5,6,7]
    listOfLists=[["9:00 AM"],["9:30 AM"],["10:00 AM"],["10:30 AM"],["11:00 AM"],["11:30 AM"],["12:00 PM"],["12:30 PM"],
    ["1:00 PM"],["1:30 PM"],["2:00 PM"],["2:30 PM"],["3:00 PM"],["3:30 PM"],["4:00 PM"],["4:30 PM"],
    ["5:00 PM"],["5:30 PM"],["6:00 PM"],["6:30 PM"],["7:00 PM"],["7:30 PM"],["8:00 PM"],["8:30 PM"],["9:00 PM"],["9:30 PM"],
    ["10:00 PM"],["10:30 PM"],["11:00 PM"],["11:30 PM"],["12:00 AM"]]
    counter=1
    for list in listOfLists:
        for num in zero7:
            list.append(counter)
            counter+=1

    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True
    context = {
        "listOfLists": listOfLists,
        "selectedNums": selectedNums,
        'CurrTutor': CurrTutor,
        "authed":loggedIn,
        "tutor":isTutor
    }

    return render(request, 'showAval.html', context)




def StoreRequest(request,tutor_id):
    #NEED TO FILL THIS IN WITH REAL 
    
    CurrTutorEmail='samuelharless10@gmail.com'
    CurrStudentEmail='sdh7ksu@virginia.edu'
    
    if request.user.is_authenticated:
        if Student.objects.filter(email=request.user.email).exists():
            CurrStudentEmail=request.user.email


    listOfLists=[['9:00 AM', 1, 2, 3, 4, 5, 6, 7], ['9:30 AM', 8, 9, 10, 11, 12, 13, 14], ['10:00 AM', 15, 16, 17, 18, 19, 20, 21], ['10:30 AM', 22, 23, 24, 25, 26, 27, 28], ['11:00 AM', 29, 30, 31, 32, 33, 34, 35], ['11:30 AM', 36, 37, 38, 39, 40, 41, 42], ['12:00 PM', 43, 44, 45, 46, 47, 48, 49], ['12:30 PM', 50, 51, 52, 53, 54, 55, 56], ['1:00 PM', 57, 58, 59, 60, 61, 62, 63], ['1:30 PM', 64, 65, 66, 67, 68, 69, 70], ['2:00 PM', 71, 72, 73, 74, 75, 76, 77], ['2:30 PM', 78, 79, 80, 81, 82, 83, 84], ['3:00 PM', 85, 86, 87, 88, 89, 90, 91], ['3:30 PM', 92, 93, 94, 95, 96, 97, 98], ['4:00 PM', 99, 100, 101, 102, 103, 104, 105], ['4:30 PM', 106, 107, 108, 109, 110, 111, 112], ['5:00 PM', 113, 114, 115, 116, 117, 118, 119], ['5:30 PM', 120, 121, 122, 123, 124, 125, 126], ['6:00 PM', 127, 128, 129, 130, 131, 132, 133], ['6:30 PM', 134, 135, 136, 137, 138, 139, 140], ['7:00 PM', 141, 142, 143, 144, 145, 146, 147], ['7:30 PM', 148, 149, 150, 151, 152, 153, 154], ['8:00 PM', 155, 156, 157, 158, 159, 160, 161], ['8:30 PM', 162, 163, 164, 165, 166, 167, 168], ['9:00 PM', 169, 170, 171, 172, 173, 174, 175], ['9:30 PM', 176, 177, 178, 179, 180, 181, 182], ['10:00 PM', 183, 184, 185, 186, 187, 188, 189], ['10:30 PM', 190, 191, 192, 193, 194, 195, 196], ['11:00 PM', 197, 198, 199, 200, 201, 202, 203], ['11:30 PM', 204, 205, 206, 207, 208, 209, 210], ['12:00 AM', 211, 212, 213, 214, 215, 216, 217]]
    
    days=["Sunday","Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]

    selectedValue=int(request.POST['button'])
    selectedCourse=request.POST['courseButton']

    letters=selectedCourse[0:selectedCourse.index(' ')]
    numbers=selectedCourse[selectedCourse.index(' ')+1:len(selectedCourse)]

    currCourse=Course.objects.filter(mnemonic=letters, course_number=numbers).get()


    #Get Day of Week and time based on number
    time=''
    day=''
    for list in listOfLists:
        if(selectedValue in list):
            time=list[0]
            day=days[list.index(selectedValue)-1]

    
    newReq=Request(time=time, day=day, number=selectedValue, status="Pending", Student=Student.objects.filter(email=CurrStudentEmail).get(), Tutor=Tutor.objects.filter(id=int(tutor_id)).get(),course=currCourse)
    newReq.save()

    return redirect('/showRequests/')


def ShowRequests(request):
    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            return redirect("/showRequestsTutor/")
        elif Student.objects.filter(email=request.user.email).exists():
            return redirect("/showRequestsStudent/")
        else:
            return HttpResponse("Error, you are logged in but not signed up??")
    else:
        return redirect("/login/")
    

def ShowRequestsTutor(request):
    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True

    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            CurrTutor=Tutor.objects.filter(email=request.user.email).get()
            pendingRequests=Request.objects.filter(Tutor=CurrTutor,status='Pending')
            acceptedRequests=Request.objects.filter(Tutor=CurrTutor,status='Accepted')
        else:
            return HttpResponse("You should not be here you are not a tutor")
    else:
        #TEST WITHOUT LOGIN
        CurrTutor=Tutor.objects.filter(email='samuelharless10@gmail.com').get()
        pendingRequests=Request.objects.filter(Tutor=CurrTutor,status='Pending')
        acceptedRequests=Request.objects.filter(Tutor=CurrTutor,status='Accepted')
    
    context={
        'pendingRequests': pendingRequests,
        'acceptedRequests': acceptedRequests,
        "authed":loggedIn,
        "tutor":isTutor
    }
    return render(request, 'showTutorRequests.html', context)


def ShowRequestsStudent(request):
    #DO THIS
    if request.user.is_authenticated:
        if Student.objects.filter(email=request.user.email).exists():
            CurrStudent=Student.objects.filter(email=request.user.email).get()
            pendingRequests=Request.objects.filter(Student=CurrStudent,status="Pending")
            acceptedRequests=Request.objects.filter(Student=CurrStudent,status="Accepted")
            deniedRequests=Request.objects.filter(Student=CurrStudent,status='Denied')
            endedRequests=Request.objects.filter(Student=CurrStudent,status='Ended')
        else:
            return HttpResponse("You should not be here you are not a tutor")
    else:
        CurrStudent=Student.objects.filter(email='sdh7ksu@virginia.edu').get()
        pendingRequests=Request.objects.filter(Student=CurrStudent,status="Pending")
        acceptedRequests=Request.objects.filter(Student=CurrStudent,status="Accepted")
        deniedRequests=Request.objects.filter(Student=CurrStudent,status='Denied')
        endedRequests=Request.objects.filter(Student=CurrStudent,status='Ended')


    loggedIn = False
    isTutor = False
    if request.user.is_authenticated:
        loggedIn = True
        if Tutor.objects.filter(email=request.user.email).exists():
            isTutor = True
    context={
        'pendingRequests': pendingRequests,
        'acceptedRequests': acceptedRequests,
        'deniedRequests': deniedRequests,
        'endedRequests': endedRequests,
        "authed":loggedIn, 
        "tutor":isTutor
    }
    return render(request, 'showStudentRequests.html', context)

#CAN SHOW ENDED REQUESTS/COMPLETED REQUESTS, and then this is where the review button can be? Very good idea!

def DeleteRequest(request):
    #print(dict(request.POST.items()))
    for key in request.POST:
        if request.POST[key]=='Submit':
            currRequest=Request.objects.filter(id=int(key)).get()
            currRequest.status="Ended"
            currRequest.save()
            CurrTutor=currRequest.Tutor
            CurrTutor.availability=CurrTutor.availability+str(currRequest.number)+','
            CurrTutor.save()

    return redirect('/showRequestsTutor/')


def AcceptRequest(request):
    idToAccept=request.POST['acceptRequestButton']
    if idToAccept[0]=='A':

        currReq=Request.objects.filter(id=int(idToAccept[1:len(idToAccept)])).get()
        currReq.status='Accepted'
        currReq.save()

        CurrTutor=currReq.Tutor
        CurrNumber=currReq.number

        #Deny any other pending requuest at the same time as they cannot do both
        for i in Request.objects.filter(Tutor=CurrTutor,number=CurrNumber,status='Pending').exclude(id=currReq.id):
            i.status='Denied'
            i.save()

        #Take that number out of current availability
        selected=CurrTutor.availability
        iterator=1
        selectedNums=[]
        while iterator<len(selected):
            selectedNums.append(int(selected[1:selected.index(',',1)]))
            selected=selected[selected.index(',',1):len(selected)]

        newAval=','
        for num in selectedNums:
            if num !=CurrNumber:
                newAval=newAval+str(num)+','

        CurrTutor.availability=newAval
        CurrTutor.save()
        return redirect('/showRequestsTutor/')
    elif idToAccept[0]=='D':

        currReq=Request.objects.filter(id=int(idToAccept[1:len(idToAccept)])).get()
        currReq.status='Denied'
        currReq.save()
        return redirect('/showRequestsTutor/')
    else:
        return HttpResponse("Error, invalid request")

#DONE. JUST DELETES REQUEST AND REDIRECTS BACK TO /SHOWREQUESTSSTUDENT
def CancelRequest(request):
    for key in request.POST:
        if request.POST[key]=='on':
            Request.objects.filter(id=int(key)).delete()
    return redirect('/showRequestsStudent/')

def EndRequest(request):
    for key in request.POST:
        if request.POST[key]=='on':
            currRequest=Request.objects.filter(id=int(key)).get()
            currRequest.status="Ended"
            currRequest.save()
            CurrTutor=currRequest.Tutor
            CurrTutor.availability=CurrTutor.availability+str(currRequest.number)+','
            CurrTutor.save()
    return redirect('/showRequestsStudent/')


def writeReview(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    if request.method == 'POST':
        review_title = request.POST['title_text']
        review = request.POST['review']

        review_object = Review(review_title=review_title, review=review)
        review_object.save()

        tutor.reviews.add(review_object)
        tutor.save()

        return redirect('/tutorInfo/' + str(tutor_id))

    return render(request, 'review.html', {'tutor': tutor})

def confirmation(request):
    if request.user.is_authenticated:
        tutor = Tutor.objects.get(email=request.user.email)
    else:
        tutor = 'You are not signed in.'

    return render(request, 'confirmation.html', {'tutor': tutor})



def afterLogin(request):
    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            #if they have any requests, send them to /requests, else send them to their profile page
            currTutor=Tutor.objects.filter(email=request.user.email).get()
            if Request.objects.filter(Tutor=currTutor,status="Accepted").exists():
                return redirect("/showRequests/")
            elif Request.objects.filter(Tutor=currTutor, status="Pending").exists():
                return redirect("/showRequests/")
            else:
                return redirect("/profile/")
        if Student.objects.filter(email=request.user.email).exists():
            #IF a student has any requests, send them to that page
            currStudent=Student.objects.filter(email=request.user.email).get()
            if Request.objects.filter(Student=currStudent).exists():
                return redirect("/showRequests/")
            else:
                return redirect("/tutors/")
            
    return redirect("/")


def editAvail(request):
    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            currTutor=Tutor.objects.filter(email=request.user.email).get()
            selected=currTutor.availability



        #now have availabilty in string format, need to convert it to an array
        iterator=1
        selectedNums=[]
        while iterator<len(selected):
            selectedNums.append(int(selected[1:selected.index(',',1)]))
            selected=selected[selected.index(',',1):len(selected)]



        zero7=[1,2,3,4,5,6,7]
        listOfLists=[["9:00 AM"],["9:30 AM"],["10:00 AM"],["10:30 AM"],["11:00 AM"],["11:30 AM"],["12:00 PM"],["12:30 PM"],
        ["1:00 PM"],["1:30 PM"],["2:00 PM"],["2:30 PM"],["3:00 PM"],["3:30 PM"],["4:00 PM"],["4:30 PM"],
        ["5:00 PM"],["5:30 PM"],["6:00 PM"],["6:30 PM"],["7:00 PM"],["7:30 PM"],["8:00 PM"],["8:30 PM"],["9:00 PM"],["9:30 PM"],
        ["10:00 PM"],["10:30 PM"],["11:00 PM"],["11:30 PM"],["12:00 AM"]]
        counter=1
        for list in listOfLists:
            for num in zero7:
                list.append(counter)
                counter+=1
        loggedIn = False
        isTutor = False
        if request.user.is_authenticated:
            loggedIn = True
            if Tutor.objects.filter(email=request.user.email).exists():
                isTutor = True
        context = {
            "listOfLists": listOfLists,
            "selectedNums": selectedNums,
            'CurrTutor': currTutor,
            "authed":loggedIn,
            "tutor":isTutor
        }
        return render(request, 'editAvail.html', context)
    else:
        return redirect("/login/")
    

def storedEditedBoxes(request):
    if request.user.is_authenticated:
        if Tutor.objects.filter(email=request.user.email).exists():
            CurrTutor = Tutor.objects.filter(email=request.user.email).get()
        else: 
            return HttpResponse("Error, you should not be here bc you are not a tutor!")
    else:
        return redirect("/login/")


    on=','
    for key in request.POST:
        if request.POST[key]=='on':
            on+=(key+',')

    CurrTutor.availability=on
    CurrTutor.save()



    return redirect('/profile/')

def justAddClasses(request):
    count_courses = Course.objects.all()
    all_courses = {}

    if count_courses.count() == 0:
        page_num = 1
        courses = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=%d' % (
                page_num)).json()
        while not courses == []:
            for i in courses:
                if not Course.objects.filter(course_name=i['descr'], course_number=i['catalog_nbr']).exists():
                    course_data = Course(
                        mnemonic=i['subject'],
                        course_number=i['catalog_nbr'],
                        course_name=i['descr'],
                    )
                    course_data.save()

            page_num += 1
            courses = requests.get(
                'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=%d' % (
                    page_num)).json()
    value = ""
    if 'name' in request.GET or 'number' in request.GET or 'class' in request.GET:
        name = request.GET['name'].upper()
        number = request.GET['number']
        class_name = request.GET['class']

        if name == "" and number == "" and class_name == "":
            all_courses = {}
        elif name == "" and class_name == "":
            all_courses = Course.objects.filter(course_number=number)
        elif number == "" and class_name == "":
            all_courses = Course.objects.filter(mnemonic=name)
        elif number == "" and name == "":
            all_courses = Course.objects.filter(course_name__iexact=class_name)
        elif class_name == "":
            all_courses = Course.objects.filter(course_number=number, mnemonic=name)
        elif name == "":
            all_courses = Course.objects.filter(course_number=number, course_name=class_name)
        elif number == "":
            all_courses = Course.objects.filter(course_name=class_name, mnemonic=name)
        if len(all_courses) == 0:
            value = "No courses found. Search again."
    return render(request, 'justaddCourses.html', {"courses": all_courses, "authed": request.user.is_authenticated,
                                                      "tutor": Tutor.objects.filter(email=request.user.email).exists(),
                                                      "empty": value})


def addClassPrivate(request):
    if request.method == 'POST':
        add_courses = request.POST.getlist('add_courses')
        for course in add_courses:
            tutor_user = Tutor.objects.get(email=request.user.email)
            course_to_add = Course.objects.get(pk=int(course))
            if not tutor_user.courses.filter(pk=course_to_add.pk):
                tutor_user.courses.add(course_to_add)
                tutor_user.save()

    return redirect('/addClass/')

def deleteClass(request):
    tutor = Tutor.objects.get(email=request.user.email)
    all_courses = tutor.courses.all()
    value=""
    if len(all_courses) == 0:
        value = "No Classes Added"

    if request.method == 'POST':
        add_courses = request.POST.getlist('add_courses')
        for course in add_courses:
            tutor_user = Tutor.objects.get(email=request.user.email)
            course_to_delete = Course.objects.get(pk=int(course))

            tutor_user.courses.remove(course_to_delete)
            tutor_user.save()

    all_courses = tutor.courses.all()

    return render(request, 'removeClass.html', {"courses": all_courses, "authed": request.user.is_authenticated,
                                                      "tutor": Tutor.objects.filter(email=request.user.email).exists(),
                                                      "empty": value})