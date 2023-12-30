from django.urls import path, register_converter
from . import views
from .views import WomenHome, WomenCategory, ShowPost, AddPage, ContactFormView
from django.views.decorators.cache import cache_page
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")


app_name = "women"

urlpatterns = [
    path("", cache_page(60)(WomenHome.as_view()), name="about_women"),
    path("archive/<year4:year>/", views.archive),
    path("add_text/", AddPage.as_view(), name="add_text"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
]
