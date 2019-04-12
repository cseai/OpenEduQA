from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Teacher
from .forms import TeacherUpdateForm
from accounts.forms import UserFollowForm


def teacher_list_view(request):
    if request.user.is_authenticated:
        # teacher_obj_list = Teacher.objects.all()
        teacher_obj_list = Teacher.objects.active()
        context = {
            'teacher_objects': teacher_obj_list,
            'title': "All Teacher"
        }
        return render(request, "teacher_list_view.html", context)
    else:
        return redirect("/login")


def teacher_update_view(request):
    if not request.user.is_authenticated:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    # instance = request.user.teacher
    instance = Teacher.objects.filter(user=request.user).first()
    if not instance:
        response = HttpResponse("You are not a teacher OR You do not have permission to do this.")
        response.status_code = 403
        return response

    form = TeacherUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # if the user is a teacher then need to update the teacher model/table too
        instance.save()
        form.save_m2m()
        messages.success(request, f"Teacher updation has saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update Teacher information",
        "instance": instance,
        "form": form,
    }
    return render(request, "teacher_update_view.html", context)


def teacher_profile_view(request):
    '''
    [teacher profile]
    [teacher detal information]
    '''
    # print(request, request.user)
    if request.user.is_authenticated:
        # user_obj = User.objects.filter(request.user).first()
        # teacher_obj = Teacher.objects.filter(user=request.user).first()
        teacher_obj = get_object_or_404(Teacher, user=request.user)
        # print('teacher_obj', teacher_obj)
        if not teacher_obj:
            response = HttpResponse("You are not a teacher OR You do not have permission to do this.")
            response.status_code = 403
            return response
        # print(user_obj.name)
        # follows = user_obj.follows.all()
        # followers = User.objects.filter(follows=user_obj)
        # print(followers)
        context = {
            'instance': teacher_obj,
            # 'follows': follows,
            # 'followers': followers,
            'title': "Teacher Profile"
        }
        return render(request, "teacher_profile_view.html", context)
    else:
        return redirect("/login")


def teacher_view(request, id):
    '''
    any other user
    '''
    if request.user.is_authenticated:
        # Note: id is a str so need to convert int to compare
        # teacher_obj = Teacher.objects.filter(id=id).first()
        teacher_obj = get_object_or_404(Teacher, id=id)
        # if request.user.is_teacher and request.user.teacher.id == int(id):
        if teacher_obj and teacher_obj.user == request.user:
            return redirect("/teacher/profile")
            # return profile_view(request)
        # teacher_obj = Teacher.objects.filter(id=id).first()
        user_obj = teacher_obj.user
        # request.user is following or not
        is_following = False

        form = UserFollowForm(request.POST or None)
        # https://docs.djangoproject.com/en/2.1/ref/models/relations/#django.db.models.fields.related.RelatedManager
        if teacher_obj.user.user_set.filter(id=request.user.id):
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
            'instance': teacher_obj,
            'follows': follows,
            'followers': followers,
            'is_following': is_following,
            'form': form,
            'title': "Profile"
        }
        return render(request, "teacher_view.html", context)
    else:
        return redirect("/login")
