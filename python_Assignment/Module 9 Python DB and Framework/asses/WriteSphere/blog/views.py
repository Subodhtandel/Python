from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Post, PostLike

UserModel = get_user_model()


def posts_visible_for(request):
    base = Post.objects.select_related("author", "category").prefetch_related("tags")
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        if user.is_superuser or getattr(user, "role", "") == UserModel.Role.ADMIN:
            return base
        return base.filter(Q(is_published=True) | Q(author=user))
    return base.filter(is_published=True)


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        u = self.request.user
        return u.is_authenticated and getattr(u, "can_publish_posts", lambda: False)()


class OwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        post = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        if post.author_id == u.pk:
            return True
        return u.is_superuser or getattr(u, "role", "") == UserModel.Role.ADMIN


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = posts_visible_for(self.request).annotate(like_count=Count("likes", distinct=True))
        params = self.request.GET
        author = params.get("author")
        if author:
            qs = qs.filter(author__username__iexact=author.strip())

        cat = params.get("category")
        if cat:
            qs = qs.filter(category__slug__iexact=cat.strip())

        df = parse_date(params.get("date_from", "") or "")
        dt = parse_date(params.get("date_to", "") or "")
        tz = timezone.get_current_timezone()
        if df:
            qs = qs.filter(created_at__date__gte=df)
        if dt:
            qs = qs.filter(created_at__date__lte=dt)

        tag = params.get("tag")
        if tag:
            qs = qs.filter(tags__slug__iexact=tag.strip())

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_author"] = self.request.GET.get("author", "")
        ctx["filter_category"] = self.request.GET.get("category", "")
        ctx["filter_date_from"] = self.request.GET.get("date_from", "")
        ctx["filter_date_to"] = self.request.GET.get("date_to", "")
        ctx["filter_tag"] = self.request.GET.get("tag", "")
        from .models import Category, Tag

        ctx["categories"] = Category.objects.all()
        ctx["tags"] = Tag.objects.all()
        ctx["authors"] = (
            UserModel.objects.filter(blog_posts__isnull=False)
            .distinct()
            .order_by("username")
        )
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return posts_visible_for(self.request).prefetch_related(
            "comments__author",
            "tags",
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user
        ctx["comment_form"] = (
            CommentForm() if user.is_authenticated else None
        )
        ctx["like_count"] = post.likes.count()
        ctx["user_liked"] = (
            user.is_authenticated
            and post.likes.filter(user=user).exists()
        )
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to comment.")
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = self.object
            c.author = request.user
            c.save()
            messages.success(request, "Comment added.")
            return redirect(self.object.get_absolute_url())
        ctx = self.get_context_data(object=self.object)
        ctx["comment_form"] = form
        return self.render_to_response(ctx)


class PostCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_queryset(self):
        return posts_visible_for(self.request)

    def form_valid(self, form):
        messages.success(self.request, "Post updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:list")

    def get_queryset(self):
        return posts_visible_for(self.request)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted.")
        return super().delete(request, *args, **kwargs)


class AuthorProfileView(DetailView):
    model = UserModel
    template_name = "blog/author_profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        u = self.object
        request_user = self.request.user
        ctx["author_posts"] = u.blog_posts.filter(is_published=True)[:12]
        ctx["followers_count"] = u.followers_set.count()
        ctx["following_count"] = u.following_set.count()
        ctx["is_following"] = (
            request_user.is_authenticated
            and request_user.pk != u.pk
            and Follow.objects.filter(follower=request_user, following=u).exists()
        )
        return ctx


class CommentOwnerMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        c = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        if c.author_id == u.pk:
            return True
        return u.is_superuser or getattr(u, "role", "") == UserModel.Role.ADMIN


class CommentUpdateView(LoginRequiredMixin, CommentOwnerMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, CommentOwnerMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Comment removed.")
        return super().delete(request, *args, **kwargs)


@login_required
@require_http_methods(["POST"])
def toggle_like(request, slug):
    post = get_object_or_404(posts_visible_for(request), slug=slug)
    like = PostLike.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
        messages.info(request, "Like removed.")
    else:
        PostLike.objects.create(user=request.user, post=post)
        messages.success(request, "Thanks for the like.")
    return redirect(post.get_absolute_url())


@login_required
@require_http_methods(["POST"])
def toggle_follow(request, username):
    author = get_object_or_404(UserModel, username=username)
    if author.pk == request.user.pk:
        messages.warning(request, "You cannot follow yourself.")
        return redirect("blog:author_profile", username=username)
    rel = Follow.objects.filter(follower=request.user, following=author).first()
    if rel:
        rel.delete()
        messages.info(request, "Unfollowed.")
    else:
        Follow.objects.create(follower=request.user, following=author)
        messages.success(request, "You are now following this author.")
    return redirect("blog:author_profile", username=username)
