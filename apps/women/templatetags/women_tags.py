from django import template
from apps.women.models import Category

# создание обьекта класса Libraryдля регистрации наших новых тегов
register = template.Library()


# Функция возвращает категории для постов
@register.simple_tag(name="getcats")
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag("women/list_categories.html")
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}
