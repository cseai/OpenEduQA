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

from .forms import McqForm
from .models import Mcq
from course.models import Subject
from article.models import Article
# Create your views here.


def mcq_list(request):
    today = timezone.now().date()
    # queryset_list = Mcq.objects.active()  # .order_by("-timestamp")
    # if request.user.is_staff or request.user.is_superuser:
    #     queryset_list = Mcq.objects.all()

    # queryset_list = Mcq.objects.all()
    queryset_list = Mcq.objects.extra(select={'length': 'cardinality(answer)'})
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
        "title": "Multiple Choice Questions",
        "today": today,
        "length": len(queryset_list),
    }
    # return render(request, "mcq_list.html", context)
    return render(request, "mcq_list_checkbox.html", context)


def mcq_create(request):
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

    form = McqForm(request.POST or None, request.FILES or None)
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
    return render(request, "mcq_form.html", context)


def mcq_detail(request, id):
    instance = get_object_or_404(Mcq, id=id)
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
    share_string = quote_plus(instance.question)

    # initial_data = {
    #     "content_type": instance.get_content_type,
    #     "object_id": instance.id
    # }

    context = {
        "title": "MCQ Detail",
        "instance": instance,
        "share_string": share_string,
        # "comments": comments,
        # "comment_form": form,
    }
    return render(request, "mcq_detail.html", context)


def mcq_update(request, id):
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
    instance = get_object_or_404(Mcq, id=id)
    # check this user has permission to do it - final_step
    if not instance or not (request.user == instance.user or request.user.is_superuser or request.user.is_staff):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    form = McqForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Update MCQ",
        "instance": instance,
        "form": form,
    }
    return render(request, "mcq_form.html", context)


def mcq_delete(request, id):
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
    instance = get_object_or_404(Mcq, id=id)
    # check this user has permission to do it - final_step
    # check this user has permission to do it - final_step
    if not instance or not (request.user == instance.user or request.user.is_superuser or request.user.is_staff):
        response = HttpResponse("You do not have permission to do this.")
        response.status_code = 403
        return response
    if request.method == "POST":
        parent_obj_url = reverse("mcq:list")    # obj.get_absolute_url()
        instance.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "title": "Confirm delete MCQ",
        "object": instance
    }
    return render(request, "mcq_delete.html", context)


def index_page(request):
    today = timezone.now().date()
    # queryset_list = Mcq.objects.active()  # .order_by("-timestamp")
    # if request.user.is_staff or request.user.is_superuser:
    #     queryset_list = Mcq.objects.all()

    # queryset_list = Mcq.objects.all()
    queryset_list = Mcq.objects.extra(select={'length': 'cardinality(answer)'})
    context = {
        "object_list": queryset_list,
        "title": "MCQ List",
        "today": today,
    }
    # return render(request, "mcq_list.html", context)
    return render(request, "index.html", context)
    # return render(request, "login_form.html", context)


def subject_content_list(request, id):
    today = timezone.now().date()
    subject_obj = Subject.objects.get(id=id)
    queryset_list = Article.objects.filter(subject=subject_obj, draft=False)  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Article.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__name__icontains=query) |
            Q(user__username__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
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
        "title": "Articles",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "subject_content_list.html", context)


def latex_editor(request):
    return render(request, "latex_editor.html", {})


def vme_editor(request):
    return render(request, "vme.html", {})


def openvme(request):
    return render(request, "VisualMathEditor.html", {})
