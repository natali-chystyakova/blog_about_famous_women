from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import TemplateView

from apps.women.utils import DataMixin


def index(request: WSGIRequest):
    return render(
        request=request,
        template_name="index.html",
    )


class AboutUsView(DataMixin, TemplateView):
    template_name = "base/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "about_us"
        c_def = self.get_user_context(title="about_us")
        context = dict(list(context.items()) + list(c_def.items()))
        return context
