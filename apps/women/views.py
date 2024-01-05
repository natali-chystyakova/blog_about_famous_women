from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from .models import Woman, Category
from .forms import AddPostForm, ContactForm
from .utils import DataMixin
from django.views.generic import ListView, DetailView, CreateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin


class WomenHome(DataMixin, ListView):
    # paginate_by = 3
    model = Woman
    template_name = "women/home_about_women.html"
    context_object_name = "posts"
    # extra_context = {"title": "Women Главная страница"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["title"] = "Women Главная страница"
        # context["cat_selected"] = 0
        c_def = self.get_user_context(title="Women")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Woman.objects.filter(is_published=True).select_related("cat")


def archive(request, year):
    if int(year) > 2024:
        return redirect("women:about_women", permanent=True)
    return HttpResponse(f"<h1> Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена</h1>")


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/add_text.html"
    success_url = reverse_lazy("women:about_women")
    # login_url = "/admin/"
    login_url = reverse_lazy("women:about_women")
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["title"] = "Добавить статью"
        c_def = self.get_user_context(title="Добавить статью")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy("women:about_women")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("women:about_women")


class ShowPost(DataMixin, DetailView):
    model = Woman
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["title"] = context["post"]
        c_def = self.get_user_context(title=context["post"])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class WomenCategory(DataMixin, ListView):
    model = Woman
    template_name = "women/home_about_women.html"
    context_object_name = "posts"
    allow_empty = False
    # paginate_by = 3

    def get_queryset(self):
        return Woman.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["title"] = "Категория - "+ str(context["posts"][0].cat)
        # context["cat_selected"] = context["posts"][0].cat_id
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(title="Категория-" + str(c.name), cat_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context
