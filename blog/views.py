import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages

from .forms import PostForm, FeedbackForm
from .models import Post, Feedback

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, PostSerializer


# class PostView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostList(ListView):
    queryset = Post.objects.all().order_by('published_date')
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'


# def post_list(request):
#     posts = Post.objects.all().order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})

class PostDelete(generics.DestroyAPIView):
    queryset = Post

# def post_delete(request, pk, *args, **kwargs):
#     if request.is_ajax and request.method == "GET":
#         Post.objects.filter(pk=pk).delete()
#         return JsonResponse({"result": "okay"}, status=200)
#
#     return JsonResponse({"result": "bad"}, status=400)


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    queryset = Post.objects.all()
    # def get_queryset(self):
    #     return Post.objects.filter(pk=self.kwargs.get('id'))


#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})


class PostNew(CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)


class PostNewChaker(View):
    template_name = 'blog/post_new.html'
    form_class = PostForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def after_form_isvalid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        return post

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = self.after_form_isvalid(form)
            post.save()
            return redirect('post_detail', pk=post.pk)


class PostNew0(PostNewChaker):
    def after_form_isvalid(self, form):
        post = super(PostNew0, self).after_form_isvalid(form)
        if self.request.user in []:
            post.author = None
        return post


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


# class PostEdit(UpdateView):
#     model = Post
#     fields = ['title', 'text']
#     template_name = 'blog/post_edit.html'
#
#     def form_invalid(self, form):
#         response = super().form_invalid(form)
#         if self.request.is_ajax():
#             # print(form.errors)
#             # data = serializers.serialize('json', form.errors, fields=('structure',))
#             return JsonResponse(form.errors, status=400)
#
#     def form_valid(self, form):
#         # We make sure to call the parent's form_valid() method because
#         # it might do some processing (in the case of CreateView, it will
#         # call form.save() for example).
#         response = super().form_valid(form)
#         if self.request.is_ajax():
#             return JsonResponse(form.cleaned_data, status=200)

class PostEdit(generics.RetrieveUpdateAPIView):
    queryset = Post
    serializer_class = PostSerializer

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    # def patch(self, request, *args, **kwargs):
    #     return self.partial_update(request, *args, **kwargs)
    # def update(self, request, *args, **kwargs):
    #     print("here")
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     print(serializer)
    #     return Response(serializer.data)
    # def perform_update(self, serializer):
    #     print(serializer)

# class PostEdit(View):
#     template_name = 'blog/post_edit.html'
#     form_class = PostForm
#
#     def post(self, request, *args, **kwargs):
#         if self.request.is_ajax and self.request.method == "POST":
#             form = self.form_class(self.request.POST)
#             if form.is_valid() and 'pk' in self.kwargs:
#                 data_to_update = form.save(commit=False)
#                 title = data_to_update.title
#                 text = data_to_update.text
#                 post = Post.objects.get(pk=self.kwargs["pk"])
#                 post.published_date = timezone.now()
#                 post.text = text
#                 post.title = title
#                 post.save()
#                 instance = post
#                 ser_instance = serializers.serialize('json', [instance, ])
#                 # send to client side.
#                 return JsonResponse({"instance": ser_instance}, status=200)
#             else:
#                 return JsonResponse({"error": form.errors}, status=400)
#
#     def get(self, request, *args, **kwargs):
#         if self.request.is_ajax and self.request.method == 'GET':
#             if 'pk' in self.kwargs:
#                 post = Post.objects.get(pk=self.kwargs["pk"])
#                 form = self.form_class(instance=post)
#
#                 return render(request, self.template_name, {'form': form})
#             else:
#                 form = PostForm()
#         return render(request, self.template_name, {'form': form})

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

class FeedbackAPI(generics.CreateAPIView):
    queryset = Feedback

class FeedbackView(CreateView):
    form_class = FeedbackForm
    template_name = 'blog/feedback.html'

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.created_date = timezone.now()
        feedback.save()
        return redirect('post_list')
    # def get(self, request):
    #     form = FeedbackForm()
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = FeedbackForm(request.POST)
    #     if form.is_valid():
    #         feedback = form.save(commit=False)
    #         feedback.created_date = timezone.now()
    #         feedback.save()
    #         return redirect('post_list')
    #     else:
    #         messages.error(request, "Error")
    #         return render(request, self.template_name, {'form': form})


class SeeFeedback(ListView):
    model = Feedback
    context_object_name = 'feedbacks'

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
