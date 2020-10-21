from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .forms import PostForm, FeedbackForm
from .models import Post, Feedback


class PostList(ListView):
    model = Post
    context_object_name = 'posts'


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs.get('pk'))

class PostEdit(View):
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid() and 'pk' in self.kwargs:
                data_to_update = form.save(commit=False)
                title = data_to_update.title
                text = data_to_update.text
                post = Post.objects.get(pk=self.kwargs["pk"])
                post.published_date = timezone.now()
                post.text = text
                post.title = title
                post.save()
                instance = post
                ser_instance = serializers.serialize('json', [instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == 'GET':
            if 'pk' in self.kwargs:
                post = Post.objects.get(pk=self.kwargs["pk"])
                form = self.form_class(instance=post)

                return render(request, self.template_name, {'form': form})
            else:
                form = PostForm()
        return render(request, self.template_name, {'form': form})


class FeedbackView(View):
    template_name = 'blog/feedback.html'

    def get(self, request):
        form = FeedbackForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.created_date = timezone.now()
            feedback.save()
            return redirect('post_list')
        else:
            messages.error(request, "Error")
            return render(request, self.template_name, {'form': form})


class SeeFeedback(ListView):
    model = Feedback
    context_object_name = 'feedbacks'

# def post_list(request):
#     posts = Post.objects.all().order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})
#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
#
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})
#
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})
