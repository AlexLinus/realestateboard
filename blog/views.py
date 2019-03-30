from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View
from .models import Post
# Create your views here.
from django.core.paginator import Paginator

class BlogView(View):
    def get(self, request):
        post_objects = Post.objects.filter(is_active=True)
        paginator = Paginator(post_objects, 6)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except:
            posts = paginator.page(1)

        current_page = posts.number - 1  # возвращает минимум 1, а так как у нас индексы с 0 начинаются, ,поэтому отнимаем 1
        start_index = current_page - 3
        if start_index < 0:
            start_index = 0
        max_pages = paginator.num_pages  # то же самое как и с currentp_page4
        end_index = current_page + 3
        if end_index > max_pages:
            end_index = max_pages
        page_range = list(paginator.page_range)[start_index:end_index]

        return render(request, 'blog.html', context={'posts': posts, 'page_range': page_range})


class PostView(View):
    def get(self, request, post_slug):
        post = Post.objects.get(is_active=True, slug__iexact=post_slug)
        posts = Post.objects.filter(is_active=True)
        most_viewed_posts = posts.order_by('-views')[:5]
        #queryset = Post.objects.filter(is_active=True).values("pub_date").order_by('-pub_date')
        #queryset = Post.objects.filter(is_active=True).values("pub_date__date") Вариант Dan Tyan
        #queryset = posts.objects.annotate(year=models.functions.ExtractYear('pub_date'), month=models.functions.ExtractMonth('pub_date'),).values('year', 'month').distinct('year', 'month').order_by('-year', '-month')
        #queryset = Post.objects.filter(is_active=True).values("pub_date__date__month", "pub_date__date__year").order_by()
        queryset = Post.objects.filter(is_active=True).values("pub_date__date").order_by().annotate(Count('id'))
        #queryset = Post.objects.annotate(year=models.functions.ExtractYear('pub_date'), month=models.functions.ExtractMonth('pub_date'), ).values('year', 'month').annotate(total_posts=Count('id')).order_by('-year', '-month')
        for item in queryset:
            for i in item:
                print(item[i])
        #for item in queryset:
        #   print(queryset(item).strftime('%B'))

        #print('Конец queryset!')
        #archive_dates = []
        #for item in posts:
        #    item_dates = (item.pub_date.month, item.pub_date.year)
        #    if item_dates not in archive_dates:
        #        archive_dates.append(item_dates)
        #print(archive_dates)
        #archive_dates = sorted(archive_dates, key=lambda x: x[::-1], reverse=True)
        #print(archive_dates)
        try:
            post_views = request.session['post_views_id_{}'.format(post.id)]
        except:
            request.session['post_views_id_{}'.format(post.id)] = post.id
            post.views += 1
            post.save()
        try:
            year = post.pub_date.year
            print(year)
            month = post.pub_date.strftime('%B')
            print(month)
        except:
            print('Не сработало!')
        return render(request, 'post_detail.html', context={'post': post, 'most_viewed_posts': most_viewed_posts, 'queryset': queryset})

class BlogArchiveView(View):
    def get(self, request, month, year):
        posts = Post.objects.filter(pub_date__month=month, pub_date__year=year)
        print(posts)
        return render(request, 'blog_archive.html', context={'posts': posts})

class BlogSearchView(View):
    def get(self, request):
        search_query = request.GET.get('blog-search-field', '')

        if search_query:
            posts = Post.objects.filter(post_title__icontains=search_query, is_active=True)
            return render(request, 'blog_search.html', context={'posts': posts, 'search_query': search_query})
        else:
            return render(request, 'blog_search.html', context={'search_query': '- Вы ничего не указали!'})