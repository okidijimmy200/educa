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
# from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Course, Module, Content
# from .forms import ModuleFormSet

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


# class CourseModuleUpdateView(TemplateResponseMixin, View):
#     template_name = 'courses/manage/module/formset.html'
#     course = None

#     def get_formset(self, data=None):
#         return ModuleFormSet(instance=self.course,
#                              data=data)

#     def dispatch(self, request, pk):
#         self.course = get_object_or_404(Course,
#                                         id=pk,
#                                         owner=request.user)
#         return super().dispatch(request, pk)

#     def get(self, request, *args, **kwargs):
#         formset = self.get_formset()
#         return self.render_to_response({'course': self.course,
#                                         'formset': formset})

#     def post(self, request, *args, **kwargs):
#         formset = self.get_formset(data=request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect('manage_course_list')
#         return self.render_to_response({'course': self.course,
#                                         'formset': formset})


# class ContentCreateUpdateView(TemplateResponseMixin, View):
#     module = None
#     model = None
#     obj = None
#     template_name = 'courses/manage/content/form.html'

#     def get_model(self, model_name):
#         if model_name in ['text', 'video', 'image', 'file']:
#             return apps.get_model(app_label='courses',
#                                   model_name=model_name)
#         return None

#     def get_form(self, model, *args, **kwargs):
#         Form = modelform_factory(model, exclude=['owner',
#                                                  'order',
#                                                  'created',
#                                                  'updated'])
#         return Form(*args, **kwargs)

#     def dispatch(self, request, module_id, model_name, id=None):
#         self.module = get_object_or_404(Module,
#                                        id=module_id,
#                                        course__owner=request.user)
#         self.model = self.get_model(model_name)
#         if id:
#             self.obj = get_object_or_404(self.model,
#                                          id=id,
#                                          owner=request.user)
#         return super().dispatch(request, module_id, model_name, id)

#     def get(self, request, module_id, model_name, id=None):
#         form = self.get_form(self.model, instance=self.obj)
#         return self.render_to_response({'form': form,
#                                         'object': self.obj})

#     def post(self, request, module_id, model_name, id=None):
#         form = self.get_form(self.model,
#                              instance=self.obj,
#                              data=request.POST,
#                              files=request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.owner = request.user
#             obj.save()
#             if not id:
#                 # new content
#                 Content.objects.create(module=self.module,
#                                        item=obj)
#             return redirect('module_content_list', self.module.id)

#         return self.render_to_response({'form': form,
#                                         'object': self.obj})


# class ContentDeleteView(View):
#     def post(self, request, id):
#         content = get_object_or_404(Content,
#                                     id=id,
#                                     module__course__owner=request.user)
#         module = content.module
#         content.item.delete()
#         content.delete()
#         return redirect('module_content_list', module.id)


# class ModuleContentListView(TemplateResponseMixin, View):
#     template_name = 'courses/manage/module/content_list.html'

#     def get(self, request, module_id):
#         module = get_object_or_404(Module,
#                                    id=module_id,
#                                    course__owner=request.user)

#         return self.render_to_response({'module': module})


# class ModuleOrderView(CsrfExemptMixin,
#                       JsonRequestResponseMixin,
#                       View):
#     def post(self, request):
#         for id, order in self.request_json.items():
#             Module.objects.filter(id=id,
#                    course__owner=request.user).update(order=order)
#         return self.render_json_response({'saved': 'OK'})


# class ContentOrderView(CsrfExemptMixin,
#                        JsonRequestResponseMixin,
#                        View):
#     def post(self, request):
#         for id, order in self.request_json.items():
#             Content.objects.filter(id=id,
#                        module__course__owner=request.user) \
#                        .update(order=order)
#         return self.render_json_response({'saved': 'OK'})
