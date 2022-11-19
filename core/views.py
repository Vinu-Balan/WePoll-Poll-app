from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Poll, FollowersCount,SubmitVote
from itertools import chain
import random


# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []
    vote_list = []
    votes = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Poll.objects.filter(user=usernames)
        vote_lists = SubmitVote.objects.filter(user = request.user.username)
        votes.append(vote_lists)
        feed.append(feed_lists)
    cur_user = SubmitVote.objects.filter(user=request.user.username)
    # polls = Poll.objects.get(id = )
    # print(feed)
    # print(len(votes))
    vote_list = list(chain(*votes))

    feed_list = list(chain(*feed))
    post_ids = []
    poll_vote = []
    for i in feed_list:
        post_ids.append(i.id)
    for i in post_ids:
        k=0
        for vote in vote_list:
            if str(vote.poll_id)==str(i) and vote.voted and str(vote.user)==str(request.user.username):
                poll_vote.append(True)
                k=1
                break
        if k==0:
            poll_vote.append(False)
    print(feed_list,poll_vote)
    # print(feed_list)
    # print(vote_list)
    poll_votes = []
    for i in range(len(poll_vote)):
        poll_votes.append([feed_list[i],poll_vote[i]])

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile,"poll_vote":poll_votes,"username":user_object, 'posts': feed_list,'votelist':poll_vote,
                                          'suggestions_username_profile_list': suggestions_username_profile_list[:4]})


@login_required(login_url='signin')
def uploadPoll(request):
    if request.method == 'POST':
        user = request.user.username
        # image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        classA = request.POST['classA']
        classB = request.POST['classB']


        new_post = Poll.objects.create(user=user,classAName=classA,classBName=classB,classAPercent=0,classBPercent=0, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')
@login_required(login_url='signin')
def submitvote(request):
    if request.method == 'POST':
        user = request.user.username
        # image = request.FILES.get('image_upload')
        option = request.POST['options']
        if option=='classA':
            decision = True
        else:
            decision = False
        user_object = User.objects.get(username=request.user.username)
        poll_id = request.GET.get('poll_id')
        poll_obj = Poll.objects.get(id = poll_id)
        new_vote = SubmitVote.objects.create(user=user,decision=decision,poll_id=poll_id,voted=True)
        new_vote.save()
        a = poll_obj.classAno
        b = poll_obj.classBno
        if decision:
            a+=1
            poll_obj.classAno = a
            poll_obj.classAPercent = int((a/(a+b))*100)
            poll_obj.classBPercent = 100-poll_obj.classAPercent
            # print(poll_obj.classAPercent,poll_obj.classBPercent)
        else:
            b += 1
            poll_obj.classBno = b
            poll_obj.classBPercent = int((b / (a + b)) * 100)
            poll_obj.classAPercent = 100 - poll_obj.classBPercent
        poll_obj.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html',
                  {'user_profile': user_profile, 'username_profile_list': username_profile_list})


# @login_required(login_url='signin')
# def like_post(request):
#     username = request.user.username
#     post_id = request.GET.get('post_id')
#
#     post = Post.objects.get(id=post_id)
#
#     like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
#
#     if like_filter == None:
#         new_like = LikePost.objects.create(post_id=post_id, username=username)
#         new_like.save()
#         post.no_of_likes = post.no_of_likes+1
#         post.save()
#         return redirect('/')
#     else:
#         like_filter.delete()
#         post.no_of_likes = post.no_of_likes-1
#         post.save()
#         return redirect('/')

@login_required(login_url='signin')
def myprofile(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Poll.objects.filter(user=request.user.username)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = request.user.username
    pk = user
    if request.method == 'POST':
        delete_poll = Poll.objects.filter(post_id=request.GET.get('delete')).first()
        print(request.GET.get('delete'))
        delete_poll.delete()
        user_posts.save()
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    feed = []
    feed_lists = Poll.objects.filter(user=user_object)
    feed.append(feed_lists)
    feed_list = list(chain(*feed))
    feed_list.reverse()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        # 'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'polls': feed_list
    }
    # print(feed_list)

    return render(request, 'myprofile.html', context)
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Poll.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        # 'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')