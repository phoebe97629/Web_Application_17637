from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import *
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from socialnetwork.MyMemoryList import MyMemoryList

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json
from socialnetwork.models import *

ENTRY_LIST = MyMemoryList()

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global'))


@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def global_action(request):
    return render(request, 'socialnetwork/global.html')


@login_required
def follower_action(request):
    return render(request, 'socialnetwork/follower.html')


@login_required
def follower_profile_action(request):
    return render(request, 'socialnetwork/other_profile.html')


@login_required
def my_profile_action(request):
    if request.method == 'GET':
        context = {
            'profile': request.user.profile,
            'form': ProfileForm(initial={'bio': request.user.profile.bio})
        }
        return render(request, 'socialnetwork/profile.html', context)

    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'profile': request.user.profile, 'form': form}
        return render(request, 'socialnetwork/profile.html', context)

    pic = form.cleaned_data['picture']
    print('Upload picture {} (type={}) succefully'.format(pic, type(pic)))
    pro = request.user.profile
    pro.picture = pic
    pro.bio = form.cleaned_data['bio']
    pro.content_type = form.cleaned_data['picture'].content_type
    pro.save()

    context = {
        'profile': request.user.profile,
        'form': ProfileForm(initial={'bio': request.user.profile.bio})
    }
    return render(request, 'socialnetwork/profile.html', context)


@login_required
def get_photo(request, id):
    user = get_object_or_404(User, id=id)
    item = user.profile

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)



def get_list_json_dumps_serializer(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {}
    response_comment = []
    response_post = []
    for model_item in Post.objects.all():
        my_item = {
            'post_id': model_item.id,
            'text': model_item.text,
            'first': model_item.created_by.first_name,
            'last': model_item.created_by.last_name,
            'time': model_item.created_time.isoformat(),
            'user_id': model_item.created_by.id
        }
        response_post.append(my_item)

    for comment_item in Comments.objects.all().order_by('-created_time'):
        my_item = {
            'comm_id': comment_item.id, 
            'comment' : comment_item.text, 
            'first': comment_item.created_by.first_name, 
            'last': comment_item.created_by.last_name,
            'time': comment_item.created_time.isoformat(), 
            'post_id': comment_item.post.id, 
            'user_id': comment_item.created_by.id

        }
        response_comment.append(my_item)


    response_data['post'] = response_post
    response_data['comment'] = response_comment
    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json') 
    return response


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_item(request):
    if not request.user.id: 
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'item' in request.POST or not request.POST['item']:
        return _my_json_error_response("You must enter an item to add.", status=400)


    if not 'csrfmiddlewaretoken' in request.POST or not request.POST['csrfmiddlewaretoken']: 
        return _my_json_error_response("csrf token error.", status=403)


    new_post = Post(text=request.POST['item'], created_by=request.user, created_time=timezone.now())
    new_post.save()

    return get_list_json_dumps_serializer(request)


def add_comment_item(request):
    if not request.user.id: 
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)


    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an item to add.", status=400)

    if not 'csrfmiddlewaretoken' in request.POST or not request.POST['csrfmiddlewaretoken']: 
        return _my_json_error_response("csrf token error.", status=403)

    if not 'post_id' in request.POST or not request.POST['post_id']: 
        return _my_json_error_response("You must enter a post_id to add.", status=400)

    try: 
        val = int(request.POST['post_id']) 
    except ValueError: 
        return _my_json_error_response("Invalid type of post_id", status=400) 

    try: 
        p = Post.objects.get(id=request.POST['post_id']) 
    except Post.DoesNotExist: 
        return _my_json_error_response("Invalid post_id", status=400)

    print('HHHH1')
    # post = Post.objects.get(id = request.POST['post_id']) 
    print('HHHH2')
    new_comment = Comments(text=request.POST['comment_text'], created_by=request.user, created_time=timezone.now(), post = p )
    new_comment.save()

    print('HHHH3')

    return get_list_json_dumps_serializer(request)


def add_follower_comment_item(request):
    if not request.user.id: 
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an item to add.", status=400)

    
    post = Post.objects.get(id = request.POST['post_id']) 
    new_comment = Comments(text=request.POST['comment_text'], created_by=request.user, created_time=timezone.now(), post = post )
    new_comment.save()

    return get_list_follower(request)


def get_list_follower(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {}
    response_comment = []
    response_post = []
    relative_post_id = []
    for model_item in Post.objects.all():
        my_item = {
            'post_id': model_item.id,
            'text': model_item.text,
            'first': model_item.created_by.first_name,
            'last': model_item.created_by.last_name,
            'time': model_item.created_time.isoformat(),
            'user_id': model_item.created_by.id
        }
        if model_item.created_by in request.user.profile.following.all():
            response_post.append(my_item)
            relative_post_id.append(model_item.id)


    for comment_item in Comments.objects.all().order_by('-created_time'):
        my_item = {
            'comm_id': comment_item.id, 
            'comment' : comment_item.text, 
            'first': comment_item.created_by.first_name, 
            'last': comment_item.created_by.last_name,
            'time': comment_item.created_time.isoformat(), 
            'post_id': comment_item.post.id, 
            'user_id': comment_item.created_by.id

        }
        if comment_item.post.id in relative_post_id: 
            response_comment.append(my_item)


    response_data['post'] = response_post
    response_data['comment'] = response_comment
    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json') 
    return response


@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other_profile.html', {'profile': user_to_unfollow.profile})


@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other_profile.html', {'profile': user_to_follow.profile})


@login_required
def other_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'socialnetwork/other_profile.html', {'profile': user.profile})


def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

    new_user.save()

    # profile = Profile(user = new_user)
    new_profile = Profile(user=User.objects.get(username=form.cleaned_data['username']), bio='')
    new_profile.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))
