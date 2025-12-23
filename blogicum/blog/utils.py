from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

def filter_published_posts(queryset):
    """
    Фильтрация опубликованных записей
    """
    from .models import Post 
    if queryset is None:
        queryset = Post.objects.all()
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )

def annotate_comments_count(queryset):
    """
    Аннотация количества комментариев для каждого поста
    """
    return queryset.annotate(comment_count=Count('comments'))

def paginate_queryset(request, queryset, per_page=10):
    """
    Пагинация для queryset
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)