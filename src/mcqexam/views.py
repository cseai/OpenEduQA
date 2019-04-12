from django.shortcuts import render

from urllib.parse import quote_plus  # python 3

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
# Create your views here.
from .forms import McqExamForm
from .models import McqExam
from mcq.models import Mcq


def mcqexam_list(request):
    today = timezone.now().date()
    # need to change as McqExam.objects.active()
    queryset_list = McqExam.objects.all()

    paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "MCQ Exams",
        "today": today,
    }
    return render(request, "mcqexam_list.html", context)


def mcqexam_create(request):
    # check this user has permission to do it - first_step
    if not request.user.is_authenticated:
        print("request.user.is_authenticated is False,", "AnonymousUser!")
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    elif (not request.user.is_staff) and (not request.user.is_superuser) and (not request.user.is_teacher):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response

    form = McqExamForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "mcqexam_form.html", context)


def mcqexam_detail(request, id):
    instance = get_object_or_404(McqExam, id=id)
    # if not published or draft then check access of it
    if instance.publish > timezone.now().date() or instance.draft:
        # check this user has permission to do it - first_step
        if not request.user.is_authenticated:
            print("request.user.is_authenticated is False,", "AnonymousUser!")
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response
        elif (not request.user.is_staff) and (not request.user.is_superuser) and (request.user != instance.user):  # staff, admin or author are allowed
            response = HttpResponse("You do not have permission to do this.")
            response.status_code = 403
            return response
    share_string = quote_plus(instance.description)

    qlist = []
    for q in instance.qlist:
        mcq = Mcq.objects.get(id=q)
        if mcq:
            qlist.append(mcq)

    context = {
        "title": instance.title,
        "instance": instance,
        "object_list": qlist,
        "share_string": share_string,
        # "comments": comments,
        # "comment_form": form,
    }
    return render(request, "mcqexam_detail.html", context)


def mcqexam_update(request, id):
    # check this user has permission to do it - first_step
    if not request.user.is_authenticated:
        print("request.user.is_authenticated is False,", "AnonymousUser!")
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    elif (not request.user.is_staff) and (not request.user.is_superuser) and (not request.user.is_teacher):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    # get the instance
    instance = get_object_or_404(McqExam, id=id)

    # check this user has permission to do it - final_step
    if not instance or not (request.user == instance.user or request.user.is_superuser or request.user.is_staff):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    form = McqExamForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, f"<a href='{ instance.get_absolute_url() }'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update MCQ Exam",
        "instance": instance,
        "form": form,
    }
    return render(request, "mcqexam_form.html", context)


def mcqexam_delete(request, id):
    '''
    need some updation or fixing

    like:
    1. when post deleted but comments doesnot delete at all in database
    2. confirmation page update
    '''
    # check this user has permission to do it - first_step
    if not request.user.is_authenticated:
        print("request.user.is_authenticated is False,", "AnonymousUser!")
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    elif (not request.user.is_staff) and (not request.user.is_superuser) and (not request.user.is_teacher):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    # get the instance
    instance = get_object_or_404(McqExam, id=id)

    # check this user has permission to do it - final_step
    if not instance or not (request.user == instance.user or request.user.is_superuser or request.user.is_staff):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    if request.method == "POST":
        parent_obj_url = reverse("mcqexam:list")    # obj.get_absolute_url()
        instance.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "title": "Confirm delete MCQ Exam",
        "object": instance
    }
    return render(request, "mcqexam_delete.html", context)
