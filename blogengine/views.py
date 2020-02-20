from django.shortcuts import render, redirect, reverse
from .models import *
from django.views.generic import View
from .forms import *
from django.core.paginator import Paginator


def main_page(request):
    return render(request, 'blogengine/base.html')


def posts_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page', 1)
    current_page = paginator.get_page(page_num)
    posts_list = current_page.object_list
    prev_page_url = '?page={}'.format(current_page.previous_page_number()) if current_page.has_previous() else ''
    next_page_url = '?page={}'.format(current_page.next_page_number()) if current_page.has_next() else ''

    context = {
        'posts': posts_list,
        'paginator': paginator,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'current_page': current_page,
    }
    return render(request, 'blogengine/posts_list.html', context=context)


def detailed_post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blogengine/detailed_post.html', {'post': post})


def tags_list(request):
    tags = Tag.objects.all()
    paginator = Paginator(tags, 10)
    page_number = request.GET.get('page', 1)
    current_page = paginator.get_page(page_number)
    tags_list = current_page.object_list
    prev_page_url = '?page={}'.format(current_page.previous_page_number()) if current_page.has_previous() else ''
    next_page_url = '?page={}'.format(current_page.next_page_number()) if current_page.has_next() else ''

    context = {
        'tags': tags_list,
        'paginator': paginator,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url
    }
    return render(request, 'blogengine/tags_list.html', context=context)


def detailed_tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    # related_posts = Post.objects.filter(tags=tag)
    return render(request, 'blogengine/detailed_tag.html', {'tag': tag})


class TagCreate(View):
    def get(self, request):
        form = TagForm()
        return render(request, 'blogengine/tag_create.html', {'form': form})

    def post(self, request):
        bound_form = TagForm(request.POST)
        slug = request.POST.get('slug')
        changed = True if Tag.objects.filter(slug=slug) else False
        if bound_form.is_valid():
            tag = bound_form.save()
            if changed:
                return redirect(reverse('changed_tag_url', kwargs={'slug': tag.slug}))
            return redirect(tag)
        return render(request, 'blogengine/tag_create.html', {'form': bound_form})


def changed_tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    return render(request, 'blogengine/changed_tag.html', {'tag': tag})


def changed_post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blogengine/changed_post.html', {'post': post})


class PostCreate(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blogengine/post_create.html', {'form': form})

    def post(self, request):
        bound_form = PostForm(request.POST)
        slug = request.POST.get('slug')
        changed = True if Post.objects.filter(slug=slug) else False
        if bound_form.is_valid():
            post = bound_form.save()
            if changed:
                return redirect(reverse('changed_post_url', kwargs={'slug': post.slug}))
            return redirect(post)
        return render(request, 'blogengine/post_create.html', {'form': bound_form})


class EditTag(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        bound_form = TagForm(instance=tag)
        return render(request, 'blogengine/edit_tag.html', {'form': bound_form, 'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        bound_form = TagForm(request.POST, instance=tag)
        new_slug = request.POST.get('slug')
        changed = True if new_slug != tag.slug and Tag.objects.filter(slug=new_slug) else False
        if bound_form.is_valid():
            edited_tag = bound_form.save()
            if changed:
                return redirect(reverse('changed_tag_url', kwargs={'slug': edited_tag.slug}))
            return redirect(edited_tag)
        return render(request, 'blogengine/edit_tag.html', {'form': bound_form, 'tag': tag})


class EditPost(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        form = PostForm(instance=post)
        return render(request, 'blogengine/edit_post.html', {'form': form, 'post': post})

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        bound_form = PostForm(request.POST, instance=post)
        new_slug = request.POST.get('slug')
        changed = True if new_slug != post.slug and Post.objects.filter(slug=new_slug) else False
        if bound_form.is_valid():
            edited_post = bound_form.save()
            if changed:
                return redirect(reverse('changed_post_url', kwargs={'slug': edited_post.slug}))
            return redirect(edited_post)
        return render(request, 'blogengine/edit_post.html', {'form': bound_form, 'post': post})


class DeletePost(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(request, 'blogengine/delete_post.html', {'post': post})

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        return redirect(reverse('posts_list_url'))


class DeleteTag(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        return render(request, 'blogengine/delete_tag.html', {'tag': tag})

    def post(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        tag.delete()
        return redirect(reverse('tags_list_url'))
