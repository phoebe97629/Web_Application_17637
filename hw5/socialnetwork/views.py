from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import *

from socialnetwork.MyMemoryList import MyMemoryList

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

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
    return render(request, 'socialnetwork/global.html', {'posts':Post.objects.all().order_by('-created_time')})

@login_required
def follower_action(request):
    return render(request, 'socialnetwork/follower.html', {'posts':Post.objects.all().order_by('-created_time')})
    

@login_required
def follower_profile_action(request):
    return render(request, 'socialnetwork/other_profile.html')


@login_required
def my_profile_action(request):
    if request.method == 'GET': 
        context = {
        'profile': request.user.profile, 
        'form': ProfileForm(initial = {'bio': request.user.profile.bio})
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
    'form': ProfileForm(initial = {'bio': request.user.profile.bio})
    }
    return render(request, 'socialnetwork/profile.html', context)



@login_required
def get_photo(request, id):
    user = get_object_or_404(User, id = id)
    item = user.profile

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)



@login_required
def post(request): 
    context = {}
    posts = Post.objects.all().order_by('-created_time')
    context['posts'] = posts

    if request.method == 'GET': 
        return render(request, 'socialnetwork/global.html', context)

    if 'text' not in request.POST or not request.POST['text']: 
        context['error'] = 'You must enter the something to post. '
        return render(request, 'socialnetwork/global.html', context)


    new_post = Post(text = request.POST['text'], created_by = request.user, created_time = timezone.now())
    new_post.save()
    return render(request, 'socialnetwork/global.html', {'posts': Post.objects.all().order_by('-created_time')})

    
    
@login_required
def unfollow(request, user_id): 
    user_to_unfollow = get_object_or_404(User, id = user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other_profile.html', {'profile':user_to_unfollow.profile})

@login_required
def follow(request, user_id): 
    user_to_follow = get_object_or_404(User, id = user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other_profile.html', {'profile':user_to_follow.profile})

@login_required
def other_profile(request, user_id): 
    user = get_object_or_404(User, id = user_id)
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
