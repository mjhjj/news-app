from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from django.db.models import F

from newsApp.models import Comment, Like, NewsPost, Ip

# Create your views here.

# Метод для получения айпи


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # В REMOTE_ADDR значение айпи пользователя
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Страница самого поста
def post_view(request, id):
    post = NewsPost.objects.get(id=id)

    ip = get_client_ip(request)

    if Ip.objects.filter(ip=ip).exists():
        post.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        post.views.add(Ip.objects.get(ip=ip))

    # Check if user has liked this post
    liked = False
    if request.user.is_authenticated:
        if Like.objects.filter(post=post, reporter=request.user).exists():
            liked = True

    context = {
        'post': post,
        'commentaries': post.comments.all().order_by('-time'),
        'liked': liked
    }
    return render(request, 'newsApp/newspost_detail.html', context)


class IndexView(ListView):
    model = NewsPost
    paginate_by = 5
    template_name = "newsApp/index.html"
    ordering = ['-id']  # Show newest posts first


def about_view(request):
    return render(request, 'newsApp/about.html')


def contacts_view(request):
    return render(request, 'newsApp/contacts.html')


@login_required
def like_post(request, post_id):
    if isinstance(request.user, AnonymousUser):
        return
    post = NewsPost.objects.filter(id=post_id)
    if len(post) != 1:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    post = post[0]
    like = Like.objects.filter(post=post, reporter=request.user)
    if len(like) != 1:
        new_like = Like(reporter=request.user, post=post)
        new_like.save()
        NewsPost.objects.filter(id=post_id).update(likes=F('likes') + 1)
        return HttpResponseRedirect(reverse('post-detail', args=[post_id]) + "#like")
    else:
        like.delete()
        NewsPost.objects.filter(id=post_id).update(likes=F('likes') - 1)

    return HttpResponseRedirect(reverse('post-detail', args=[post_id]) + "#like")


class NewsPostForm(forms.ModelForm):
    class Meta(object):
        model = NewsPost
        # user will be set in views.ResumeNew
        # other fields will be set as model default
        exclude = ('likes', 'reporter', 'views', 'comments')


class CommentPostForm(forms.ModelForm):
    class Meta(object):
        model = Comment
        # user will be set in views.ResumeNew
        # other fields will be set as model default
        exclude = ('reporter',)


def project_comment_view(request, pk):
    obj = Comment
    if request.method == 'POST':
        form = CommentPostForm(request.POST)
        form.instance.project = obj
        if form.is_valid():
            com = form.save(commit=False)
            com.reporter = request.user
            com.save()

            post = NewsPost.objects.get(pk=pk)
            post.comments.add(com.pk)
            return redirect('post-detail', pk)
    else:
        form = CommentPostForm()
    context = {
        'form': form,
        'object': obj,
    }
    return render(request, 'newsApp/comment_form.html', context)


class NewsPostCreate(generic.CreateView):
    model = NewsPost
    form_class = NewsPostForm
    success_url = reverse_lazy('profile')

    def get_initial(self):
        initial = super(NewsPostCreate, self).get_initial()
        initial.update({'reporter_id': self.request.user.id})
        return initial

    def form_valid(self, form):
        """Force the user to request.user"""
        self.object = form.save(commit=False)
        self.object.reporter_id = self.request.user.id
        self.object.save()

        return super(NewsPostCreate, self).form_valid(form)


class NewsPostEdit(generic.UpdateView):
    model = NewsPost
    fields = ['title', 'description', 'text']
    success_url = reverse_lazy('profile')
    template_name = 'newsApp/post_edit.html'


class NewsPostDelete(generic.DeleteView):
    model = NewsPost
    success_url = reverse_lazy('profile')
