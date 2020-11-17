from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from courses.models import Course
# from .forms import CourseEnrollForm

# use the generic CreateView, which provides the functionality for creating model objects
class StudentRegistrationView(CreateView):
    # template_name: The path of the template to render this view.
    template_name = 'students/student/registration.html'
# form_class: The form for creating objects, which has to be ModelForm. You use Django's UserCreationForm as the registration form to create User objects
    form_class = UserCreationForm
# success_url: The URL to redirect the user to when the form is successfully submitted. You reverse the URL named student_course_list, which you are going to create in the Accessing the course contents section for listing the courses that students are enrolled on.
    success_url = reverse_lazy('student_course_list')

# The form_valid() method is executed when valid form data has been posted. It has to return an HTTP response. You override this method to log the user in after they have successfully signed up.
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


# class StudentEnrollCourseView(LoginRequiredMixin, FormView):
#     course = None
#     form_class = CourseEnrollForm

#     def form_valid(self, form):
#         self.course = form.cleaned_data['course']
#         self.course.students.add(self.request.user)
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('student_course_detail',
#                             args=[self.course.id])


# class StudentCourseListView(LoginRequiredMixin, ListView):
#     model = Course
#     template_name = 'students/course/list.html'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(students__in=[self.request.user])


# class StudentCourseDetailView(DetailView):
#     model = Course
#     template_name = 'students/course/detail.html'

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(students__in=[self.request.user])

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # get course object
#         course = self.get_object()
#         if 'module_id' in self.kwargs:
#             # get current module
#             context['module'] = course.modules.get(
#                                     id=self.kwargs['module_id'])
#         else:
#             # get first module
#             context['module'] = course.modules.all()[0]
#         return context
