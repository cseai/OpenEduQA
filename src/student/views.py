from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Student
from .forms import StudentUpdateForm
from accounts.forms import UserFollowForm


def student_list_view(request):
    if request.user.is_authenticated:
        # student_obj_list = Student.objects.all()
        student_obj_list = Student.objects.active()

        context = {
            'student_objects': student_obj_list,
            'title': "All Student"
        }
        return render(request, "student_list_view.html", context)
    else:
        return redirect("/login")


def student_update_view(request):
    if not request.user.is_authenticated:
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    # instance = request.user.student
    instance = Student.objects.filter(user=request.user).first()
    if not instance:
        response = HttpResponse("You are not a student OR You do not have permission to do this.")
        response.status_code = 403
        return response

    form = StudentUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # if the user is a teacher then need to update the teacher model/table too
        instance.save()
        form.save_m2m()
        messages.success(request, f"<a href='{ instance.get_absolute_url() }'>Student</a> updation has saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update Student information",
        "instance": instance,
        "form": form,
    }
    return render(request, "student_update_view.html", context)


def student_profile_view(request):
    '''
    [student profile]
    [student detal information]
    '''
    # print(request, request.user)
    if request.user.is_authenticated:
        # user_obj = User.objects.filter(request.user).first()
        # student_obj = Student.objects.filter(user=request.user).first()
        student_obj = get_object_or_404(Student, user=request.user)
        # print('student_obj', student_obj)
        if not student_obj:
            response = HttpResponse("You are not a student OR You do not have permission to do this.")
            response.status_code = 403
            return response
        # print(user_obj.name)
        # follows = user_obj.follows.all()
        # followers = User.objects.filter(follows=user_obj)
        # print(followers)
        context = {
            'instance': student_obj,
            # 'follows': follows,
            # 'followers': followers,
            'title': "Student Profile"
        }
        return render(request, "student_profile_view.html", context)
    else:
        return redirect("/login")


def student_view(request, id):
    '''
    any other user
    '''
    if request.user.is_authenticated:
        # Note: id is a str so need to convert int to compare
        # student_obj = Student.objects.filter(id=id).first()
        student_obj = get_object_or_404(Student, id=id)
        # if request.user.is_student and request.user.student.id == int(id):
        if student_obj and student_obj.user == request.user:
            return redirect("/student/profile")
        # return profile_view(request)
        # student_obj = Student.objects.filter(id=id).first()
        user_obj = student_obj.user
        # request.user is following or not
        is_following = False

        form = UserFollowForm(request.POST or None)
        # https://docs.djangoproject.com/en/2.1/ref/models/relations/#django.db.models.fields.related.RelatedManager
        if student_obj.user.user_set.filter(id=request.user.id):
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
            'instance': student_obj,
            'follows': follows,
            'followers': followers,
            'is_following': is_following,
            'form': form,
            'title': "Profile"
        }
        return render(request, "student_view.html", context)
    else:
        return redirect("/login")
