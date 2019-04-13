from django.contrib.auth import (
    # authenticate,
    # get_user_model,
    login,
    logout,

)
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .forms import LoginForm, RegisterForm, UserUpdateForm, UserFollowForm, UserUnfollowForm
from .models import User


def login_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        next = request.GET.get('next')
        title = "Login"
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get("user_obj")
            login(request, user_obj)
            if next:
                return redirect(next)
            return redirect("/accounts/user")
        return render(request, "login_form.html", {"form": form, "title": title})
    else:
        return redirect("/accounts/user")


def register_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        next = request.GET.get('next')
        title = "Register"
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            if next:
                return redirect(next)
            return redirect("/login")

        context = {
            "form": form,
            "title": title
        }
        return render(request, "login_form.html", context)
    else:
        return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/login")


def profile_view(request):
    '''
    [user profile]
    [user detal information]
    '''
    if request.user.is_authenticated:
        # user_obj = User.objects.filter(request.user).first()
        user_obj = request.user
        # print(user_obj.name)
        follows = user_obj.follows.all()
        followers = User.objects.filter(follows=user_obj)
        # print(followers)
        context = {
            'instance': user_obj,
            'follows': follows,
            'followers': followers,
            'title': "Profile"
        }
        return render(request, "profile_view.html", context)
        # return render(request, "profile_page.html", context)
    else:
        return redirect("/login")


def profile_update_view(request):
    if not request.user.is_authenticated:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    instance = request.user
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        # Finish saving the selected M2M relationships
        form.save_m2m()

        messages.success(request, f"User updation has saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update User information",
        "instance": instance,
        "form": form,
    }
    return render(request, "profile_update_view.html", context)


def user_view(request, id):
    '''
    any other user
    '''
    if request.user.is_authenticated:
        # Note: id is a str so need to convert int to compare
        # now it working using : <int:id>
        if request.user.id == id:
            return redirect("/accounts/user")
            # return profile_view(request)
        user_obj = User.objects.filter(id=id).first()

        # request.user is following or not
        is_following = False

        form = UserFollowForm(request.POST or None)
        # https://docs.djangoproject.com/en/2.1/ref/models/relations/#django.db.models.fields.related.RelatedManager
        if user_obj.user_set.filter(id=request.user.id):
            is_following = True

        if is_following:
            if form.is_valid():
                messages = request.user.follows.remove(user_obj)
                print(messages)
                is_following = False
        else:
            if form.is_valid():
                messages = request.user.follows.add(user_obj)
                print(messages)
                is_following = True

        follows = user_obj.follows.all()
        followers = user_obj.user_set.all()

        context = {
            'instance': user_obj,
            'follows': follows,
            'followers': followers,
            'is_following': is_following,
            'form': form,
            'title': "Profile"
        }
        return render(request, "user_view.html", context)
    else:
        return redirect("/login")


def user_list_view(request):
    if request.user.is_authenticated:
        user_obj_list = User.objects.all()
        context = {
            'user_objects': user_obj_list,
            'title': "All user"
        }
        return render(request, "user_list_view.html", context)
    else:
        return redirect("/login")
