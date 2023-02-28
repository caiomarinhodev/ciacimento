from django.apps import apps
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, FormView

from database_manager.forms import FileUploadForm
from database_manager.utils import dump_database


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        data = {}
        for app in apps.get_app_configs():
            data[app.label] = []
            for model in apps.get_app_config(app.label).get_models():
                data[app.label].append(
                    {
                        'name': model.__name__,
                        'count': model.objects.count(),
                        'models': model.objects.all()
                    }
                )
        context['data'] = data
        return context


class DumpDatabaseRedirectView(RedirectView):
    url = '/database'

    def get(self, request, *args, **kwargs):
        try:
            filename = dump_database()
            self.url = '/media/' + filename
        except Exception as e:
            print(e)
            messages.error(request, 'Error while dumping database')
        return super().get(request, *args, **kwargs)


class LoadDatabaseView(FormView):
    template_name = 'load_database.html'
    form_class = FileUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.save():
            messages.success(self.request, 'Database loaded successfully')
        else:
            messages.error(self.request, 'Error while loading database')
        return super().form_valid(form)

    def get_success_url(self):
        return '/database'
