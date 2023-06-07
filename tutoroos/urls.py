from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tutors/', views.tutors, name='tutors'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.tutorregistration, name='tutorreg'),
    path('register/results', views.addClasses, name='addClasses'),
    path('profile/', views.profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='editprofile'),
    path('editprof/', views.editprof, name='edit_prof'),
    path('tutorInfo/<int:tutor_id>', views.tutor_info, name='tutorinfo'),
    path('review/<int:tutor_id>', views.writeReview, name='review'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('addClass/', views.justAddClasses,name='classreg'),
    path('addClass/results', views.addClassPrivate, name='addClassPrivate'),
    path('removeClass/', views.deleteClass, name="removeClass"),

    #For Google Login
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('test/',views.hasAccount,name="test"),
    path('makeNewTutor/',views.makeNewTutor,name="MakeNewTutor"),
    path('makeNewStudent/',views.makeNewStudent,name="MakeNewStudent"),
    path('showtype/',views.showTutorOrStudent,name="ShowType"),
    path('populate/',views.Populate,name="Populate"),
    path('availability/',views.tableAval, name="table"),
    path('storeCheckedBoxes/',views.storeCheckedBoxes, name='storeCheckedBoxes'),
    path('showAval/<int:tutor_id>', views.showAval, name="ShowAvailability"),
    path('saverequest/<int:tutor_id>', views.StoreRequest,name="StoreRequest"),
    path('showRequests/', views.ShowRequests,name="Show Requests"),
    path('showRequestsTutor/', views.ShowRequestsTutor,name="Show Requests Tutor"),
    path('showRequestsStudent/', views.ShowRequestsStudent,name="Show Requests Student"),
    path('DeleteRequest/', views.DeleteRequest, name="Delete Request"),
    path('AcceptRequest/',views.AcceptRequest,name="Accept Request"),
    path('CancelRequest/',views.CancelRequest, name='Cancel Request'),
    path('EndRequest/', views.EndRequest, name='End Request'),
    path('afterlogin/', views.afterLogin, name='After Login'),
    path('editAvail/', views.editAvail, name="Edit Availability"),
    path('storeEditedAvail/', views.storedEditedBoxes, name="Store Edited Boxes")
]