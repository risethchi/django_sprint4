from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

def filter_published_posts(queryset):
    """
    Фильтрация опубликованных записей
    """
    # Важно: timezone.now() возвращает время с учетом микросекунд
    # Для более точного сравнения и включения постов текущего дня:
    now = timezone.now()
    
    # Для отладки
    print(f"Current time for filtering: {now}")
    
    filtered_queryset = queryset.filter(
        is_published=True,
        pub_date__lte=now,  # Используем меньше или равно
        category__is_published=True
    )
    
    # Для отладки - выводим найденные посты и их даты публикации
    for post in filtered_queryset:
        print(f"Post ID: {post.id}, Title: {post.title}, Pub Date: {post.pub_date}")
        print(f"  Is visible: {post.pub_date <= now}")
    
    return filtered_queryset

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