# from pickle import FALSE

from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from rest_framework.views import APIView
# from rest_framework.response import Response


from .models import Woman, Category
from .forms import AddPostForm, ContactForm
from .permissions import IsAdminOrReadOnly
from .utils import DataMixin
from django.views.generic import ListView, DetailView, CreateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics
from .serializers import WomenSerializer

# from django.forms import model_to_dict
# from django.utils.text import slugify


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


# class WomenAPIView(generics.ListAPIView):
#     queryset = Woman.objects.all()  # берем все записи
#     serializer_class = WomenSerializer


# класс для пагинации
class WomenAPIListPagination(PageNumberPagination):
    page_size = 3
    # page_query_param = "page_size"
    page_size_query_param = "page_size"
    max_page_size = 2


# в этих 3 классах повторяющийся код, без ViewSet
class WomenAPIList(generics.ListCreateAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = WomenAPIListPagination


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomenSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # authentication_classes = (TokenAuthentication, ) # кто получает доступ по токену


class WomenAPIDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Woman.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminOrReadOnly,)


# class WomenViewSet(viewsets.ModelViewSet):
#     #queryset = Woman.objects.all()
#     serializer_class = WomenSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#         if not pk:
#             return Woman.objects.all()[:3]
#         return Woman.objects.filter(pk=pk)
#
#
#
#     @action(methods=["get"], detail=True)
#     def category(self, request, pk = None):
#         #cats = Category.objects.all()
#         cats = Category.objects.get(pk=pk)
#         #return Response({"cats": [c.name for c in cats]})
#         return Response({"cats": cats.name})


# class WomenAPIView(APIView):
#     def get(self, request):
#         w = Woman.objects.all()
#         # return Response({"title": "Angelina Jolie"})
#         return Response({"posts": WomenSerializer(w, many=True).data})
#
#
#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#
#         # post_new = Woman.objects.create(
#         #     title = request.data["title"],
#         #     content = request.data["content"],
#         #     cat_id = request.data["cat_id"],
#         # )
#         # return Response({ "post": WomenSerializer(post_new).data})
#         return Response({"post": serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk :
#             return Response({"error": "Method PUT not allowed"})
#         try:
#             instance = Woman.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#         serializer = WomenSerializer(data = request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"}, status=400)
#
#         try:
#             woman = Woman.objects.get(pk=pk)
#             woman.delete()
#             return Response({"message": f"Post {pk} deleted successfully"}, status=204)
#         except Woman.DoesNotExist:
#             return Response({"error": "Object does not exist"}, status=404)
