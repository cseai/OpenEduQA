from django.shortcuts import render
from django.utils import timezone

from urllib.parse import quote_plus  # python 3

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# Create your views here.

from .models import CqExam
from .forms import CqExamForm
from cq.models import Cq


def cqexam_list(request):
    today = timezone.now().date()
    queryset_list = CqExam.objects.all()

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
        "title": "CQ Exams",
        "today": today,
    }
    return render(request, "cqexam_list.html", context)


def cqexam_create(request):
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

    form = CqExamForm(request.POST or None, request.FILES or None)
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
    return render(request, "cqexam_form.html", context)


def cqexam_detail(request, id):
    instance = get_object_or_404(CqExam, id=id)
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
        cq = Cq.objects.get(id=q)
        if cq:
            qlist.append(cq)
    context = {
        "title": instance.title,
        "instance": instance,
        "object_list": qlist,
        "share_string": share_string,
        # "comments": comments,
        # "comment_form": form,
    }
    return render(request, "cqexam_detail.html", context)


def cqexam_update(request, id):
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
    instance = get_object_or_404(CqExam, id=id)

    # check this user has permission to do it - final_step
    if not instance or not (request.user == instance.user or request.user.is_superuser or request.user.is_staff):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    form = CqExamForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, f"<a href='{ instance.get_absolute_url() }'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update CQ Exam",
        "instance": instance,
        "form": form,
    }
    return render(request, "cqexam_form.html", context)


def cqexam_delete(request, id):
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
    instance = get_object_or_404(CqExam, id=id)

    # check this user has permission to do it - final_step
    if not instance or not (request.user == instance.user or request.user.is_superuser or request.user.is_staff):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response

    if request.method == "POST":
        parent_obj_url = reverse("cqexam:list")    # obj.get_absolute_url()
        instance.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "title": "Confirm delete CQ Exam",
        "object": instance
    }
    return render(request, "cqexam_delete.html", context)
