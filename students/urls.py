from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('register/',
         views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/',
         views.StudentCourseListView.as_view(),
         name='student_course_list'),
# apply the cache_page decorator to the student_course_detail and student_course_detail_module URL patterns
    path('course/<pk>/',
     #     the result for the StudentCourseDetailView is cached for 15 minutes.
         cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/',
         cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
         name='student_course_detail_module'),
]
