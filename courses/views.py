from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count
from django.core.cache import cache
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Course, Module, Content, Subject
from django.views.generic.detail import DetailView
from .forms import ModuleFormSet

class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

# OwnerMixin implements the get_queryset() method, which is used by the views to get the base QuerySet
class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


# OwnerEditMixin implements the form_valid() method, which is used by views that use Django's ModelFormMixin mixin, that is, views with forms or model
# forms such as CreateView and UpdateView. form_valid() is executed when the submitted form is valid
class OwnerEditMixin(object):
    def form_valid(self, form):
# The default behavior for this method is saving the instance (for model forms) and redirecting the user to success_url. You override this method to automatically set the current user in the owner attribute of the object being saved
        form.instance.owner = self.request.user
        return super().form_valid(form)

# define an OwnerCourseMixin class that inherits OwnerMixin
class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
# model: The model used for QuerySets; it is used by all views.
    model = Course
# fields: The fields of the model to build the model form of the CreateView and UpdateView views.
    fields = ['subject', 'title', 'slug', 'overview']
# success_url: Used by CreateView, UpdateView, and DeleteView toredirect the user after the form is successfully submitted or the object is deleted
    success_url = reverse_lazy('manage_course_list')

# OwnerCourseEditMixin mixin
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
# template_name: The template you will use for the CreateView and UpdateView views
    template_name = 'courses/manage/course/form.html'
# -----------------------------------------------------------------------------------
# following views that subclass OwnerCourseMixin:

# ManageCourseListView: Lists the courses created by the user. It inherits from OwnerCourseMixin and ListView. It defines a specific template_name attribute for a template to list courses.
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
# PermissionRequiredMixin checks that the user accessing the view has the permission specified in the permission_required attribute
    permission_required = 'courses.view_course'
# CourseCreateView: Uses a model form to create a new Course object. It uses the fields defined in OwnerCourseMixin to build a model
# form and also subclasses CreateView. It uses the template defined in OwnerCourseEditMixin
class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

# CourseUpdateView: Allows the editing of an existing Course object. It uses the fields defined in OwnerCourseMixin to build a model
# form and also subclasses UpdateView. It uses the template defined in OwnerCourseEditMixin
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

# CourseDeleteView: Inherits from OwnerCourseMixin and the generic DeleteView. It defines a specific template_name attribute for a template to confirm the course deletion
class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

# CourseModuleUpdateView view handles the formset to add, update, and delete modules for a specific course
class CourseModuleUpdateView(TemplateResponseMixin, View): #View: The basic class-based view provided by Django
# TemplateResponseMixin: This mixin takes charge of rendering templates and returning an HTTP response. It requires a template_name attribute
# that indicates the template to be rendered and provides the render_to_ response() method to pass it a context and render the template.
    template_name = 'courses/manage/module/formset.html'
    course = None
# get_formset(): You define this method to avoid repeating the code to build the formset. You create a ModuleFormSet object for the given Course object with optional data.
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)
# dispatch(): This method is provided by the View class. It takes an HTTP request and its parameters and attempts to delegate to a lowercase method that matches the HTTP method used. A GET request is delegated to the get()
# method and a POST request to post(), respectively. In this method, you use the get_object_or_404() shortcut function to get
    def dispatch(self, request, pk):
# you use the get_object_or_404() shortcut function to get the Course object for the  given id parameter that belongs to the current user.
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
# include this code in the dispatch() method because you need to retrieve the course for both GET and POST requests. You save it into the course attribute of the view to make
# it accessible to other methods
        return super().dispatch(request, pk)

# get(): Executed for GET requests. You build an empty ModuleFormSet formset and render it to the template together with the current
# Course object using the render_to_response() method provided by TemplateResponseMixin.
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
# post(): Executed for POST requests.
    def post(self, request, *args, **kwargs):
        # You build a ModuleFormSet instance using the submitted data
        formset = self.get_formset(data=request.POST)
# You execute the is_valid() method of the formset to validate all of its forms.
        if formset.is_valid():
# If the formset is valid, you save it by calling the save() method. At this point, any changes made, such as adding, updating, or marking modules for deletion, are applied to the database. Then, you redirect
# users to the manage_course_list URL. If the formset is not valid, you render the template to display any errors instead
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

# ContentCreateUpdateView. It will allow you to create and update different models' contents
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'
# get_model(): Here, you check that the given model name is one of the four content models: Text, Video, Image, or File
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
# Then, you use Django's apps module to obtain the actual class for the given model name. If the given model name is not one of the valid ones, you return None.
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None
# get_form(): You build a dynamic form using the modelform_factory() function of the form's framework. Since you are going to build a form for the Text, Video, Image, and File models, you use the exclude parameter
# to specify the common fields to exclude from the form and let all other attributes be included automatically.
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)
# dispatch(): It receives the following URL parameters and stores the corresponding module, model, and content object as class attributes:
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
# module_id: The ID for the module that the content is/will be associated with
                                       id=module_id,
                                       course__owner=request.user)
# model_name: The model name of the content to create/update
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                    # id: The ID of the object that is being updated. It's None to create new objects.
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)
# get(): Executed when a GET request is received. You build the model form for the Text, Video, Image, or File instance that is being updated.
    def get(self, request, module_id, model_name, id=None):
# Otherwise, you pass no instance to create a new object, since self.obj is None if no ID is provided
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})
# post(): Executed when a POST request is received. You build the model form, passing any submitted data and files to it
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                            files=request.FILES)
# If the form is valid, you create a new object and assign request.user as its owner before saving it to the database.
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
# You check for the id parameter. If no ID is provided, you know the user is creating a new object instead of updating an existing one. If this is a new object, you create a Content object for the given module and associate the new content with it.
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})

# ContentDeleteView class retrieves the Content object with the given ID.
class ContentDeleteView(View):
    # It deletes the related Text, Video, Image, or File object.
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
# it deletes the Content object and redirects the user to the module_content_list URL to list the other contents of the module.
        return redirect('module_content_list', module.id)

# ModuleContentListView view. This view gets the Module object with the given ID that belongs to the current user and renders a template with the given module
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module})

# view that receives the new order of module IDs encoded in JSON.
class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                   course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

# view to order a module's contents
class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                       module__course__owner=request.user) \
                       .update(order=order)
        return self.render_json_response({'saved': 'OK'})

# CourseListView view. It inherits from TemplateResponseMixin and View.
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = cache.get('all_subjects')
        if not subjects:
# You retrieve all subjects, using the ORM's annotate() method with the Count() aggregation function to include the total number of courses for each subject
            subjects = Subject.objects.annotate(
                            total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
# You retrieve all available courses, including the total number of modules contained in each course
        all_courses = Course.objects.annotate(
                           total_modules=Count('modules'))
        if subject:
# If a subject slug URL parameter is given, you retrieve the corresponding subject object and limit the query to the courses that belong to the given subject
            subject = get_object_or_404(Subject, slug=subject)
            key = f'subject_{subject.id}_courses'
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
# You use the render_to_response() method provided by TemplateResponseMixin to render the objects to a template and return an HTTP response
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


# view inherits from the generic DetailView provided by Django. You specify the model and template_name attributes.
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'
# DetailView expects a primary key (pk) or slug URL parameter to retrieve a single object for the given model.
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['enroll_form'] = CourseEnrollForm(
    #                                initial={'course':self.object})
    #     return context
