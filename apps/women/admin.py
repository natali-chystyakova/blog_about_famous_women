from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.women.models import Woman, Category

# admin.site.register(Woman, WomanAdmin) усли нету декоратора


# Register your models here.
@admin.register(Woman)
class WomanAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "get_html_photo", "time_create", "time_update", "is_published"]
    list_display_links = ("id", "title")  # какие поля будут ссылками
    list_editable = ["content", "is_published"]
    search_fields = ["title", "content"]  # по каким полям можно искать
    list_filter = ["is_published", "time_create"]
    prepopulated_fields = {"slug": ("title",)}
    # fields = ("title", "content", "photo", "cat",  "is_published")
    readonly_fields = ["time_create", "time_update", "get_html_photo"]
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50 >")

    get_html_photo.short_description = "Фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]  # какие поля будут ссылками
    prepopulated_fields = {"slug": ("name",)}

    search_fields = ["name"]  # по каким полям можно искать


admin.site.site_title = "Админ-панель сайта о женщинах"
admin.site.site_header = "Админ-панель сайта о женщинах"
