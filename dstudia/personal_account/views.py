from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .utils import *


def main_page(request):
    context = {
        'name_page': 'main_page',
        'applications': Application.objects.filter(status='c').order_by('-time_create')[0:4],
        'applications_amount': Application.objects.filter(status='a').count(),
    }
    return render(request, 'personal_account/main.html', context=context)


def registration_handler(request):
    context = {'name_page': 'registration_page'}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['repeat_password']
            user = CustomUser.objects.create_user(**form.cleaned_data)
            login(request, user)
            return redirect('account_page')
        else:
            context = {'form': form, 'errors_messages': show_errors(form)}
            return render(request, 'personal_account/auth/registration.html', context)
    else:
        form = RegistrationForm()
        context['form'] = form
        return render(request, 'personal_account/auth/registration.html', context=context)


def login_handler(requets):
    context = {'name_page': 'login_page'}
    if requets.method == 'POST':
        form = LoginForm(requets.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = CustomUser.objects.get(username=username)
            login(requets, user)
            return redirect('account_page')
        else:
            context = {'form': form, 'errors_messages': show_errors(form)}
            return render(requets, 'personal_account/auth/login.html', context=context)
    else:
        form = LoginForm()
        context['form'] = form
        return render(requets, 'personal_account/auth/login.html', context=context)

@login_required
def logout_handler(request):
    logout(request)
    return redirect('main_page')


@login_required
def account_page(request):
    if request.user.role == 'CUSTOMER':
        return redirect('show_applications')
    elif request.user.role == 'MANAGER':
        return redirect('applications_management')


def show_no_access(request):
    return render(request, 'personal_account/auth/no_access.html')

@login_required
def create_application(request):
    if request.user.role == 'CUSTOMER':
        context = {
            'name_page': 'create_application'
        }
        if request.method == 'POST':
            form = CreateApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = Application.objects.create(current_user=request.user, **form.cleaned_data)
                return redirect('show_application_info', application_pk=application.pk)
            else:
                context['form'] = form
                context['errors_messages'] = show_errors(form)
                return render(request, 'personal_account/applications/create.html', context=context)
        else:
            form = CreateApplicationForm()
            context['form'] = form
            return render(request, 'personal_account/applications/create.html', context=context)
    elif request.user.role == 'MANAGER':
        return redirect('no_access')


def show_application_info(request, application_pk):

    current_application = Application.objects.get(pk=application_pk)
    context = {
        'application': current_application,
        'form_accept_popup': ChangeStatusAcceptForm(),
        'form_complete_popup': ChangeStatusCompleteForm(),
        'application_comments': current_application.applicationcomment_set.all().order_by('-time_create')
    }
    return render(request, 'personal_account/applications/application_info.html', context=context)

@login_required
def delete_application(request, application_pk):
    if request.user.role == 'CUSTOMER':
        user_applications = request.user.application_set.all()
        application_deleted = Application.objects.get(pk=application_pk)
        if application_deleted in user_applications:
            application = Application.objects.get(pk=application_pk)
            url_application_info = reverse('show_application_info', kwargs={'application_pk': application.pk})
            application.delete()
            if url_application_info in request.META.get('HTTP_REFERER'):  # Перенаправление после удаления
                return redirect('account_page')
            else:
                return redirect('show_applications')
        else:
            return redirect('no_access')
    elif request.user.role == 'MANAGER':
        return redirect('no_access')

@login_required
def edit_application(request, application_pk):
    if request.user.role == 'CUSTOMER':
        if request.method == 'POST':
            form = CreateApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = Application.objects.update_or_create(pk=application_pk, defaults=form.cleaned_data)
                return redirect('show_application_info', application_pk=application_pk)
            else:
                context = {'form': form, 'errors_messages': show_errors(form)}
                return render(request, 'personal_account/applications/edit.html', context=context)
        else:
            current_application = Application.objects.values().get(pk=application_pk)
            application_form_data = {
                'title': current_application['title'],
                'description': current_application['description'],
                'image': current_application['image'],
                'cat': current_application['cat_id'],
            }
            form = CreateApplicationForm(application_form_data)
            context = {'form': form, 'application': Application.objects.get(pk=application_pk)}
            return render(request, 'personal_account/applications/edit.html', context=context)
    elif request.user.role == 'MANAGER':
        return redirect('no_access')

@login_required
def show_applications(request):
    if request.user.role == 'CUSTOMER':
        context = {'name_page': 'show_applications', 'form_filtering': FilterApplicationForm(), }
        if request.method == 'POST':
            if request.POST['field'][0] == 's':
                context['users_applications'] = request.user.application_set.order_by('-time_create')
                return render(request, 'personal_account/applications/show.html', context=context)
            else:
                users_applications = request.user.application_set.filter(status=request.POST['field'][0])
                context['users_applications'] = users_applications.order_by('-time_create')
                return render(request, 'personal_account/applications/show.html', context=context)
        else:
            context['users_applications'] = request.user.application_set.order_by('-time_create')
            return render(request, 'personal_account/applications/show.html', context=context)
    elif request.user.role == 'MANAGER':
        return redirect('no_access')


@login_required
def category_page(request):
    if request.user.role == 'CUSTOMER':
        return redirect('no_access')
    elif request.user.role == 'MANAGER':
        context = {'name_page': 'category_page', }
        if request.method == 'POST':
            form = CreateCategoryForm(request.POST)
            if form.is_valid():
                Category.objects.create(**form.cleaned_data)
                return redirect('category_page')
            else:
                context['form'] = form
                context['errors_messages'] = show_errors(form)
                return render(request, 'personal_account/categories/show.html', context=context)
        else:
            context['form'] = CreateCategoryForm()
            context['categories'] = Category.objects.all()
            return render(request, 'personal_account/categories/show.html', context=context)

@login_required
def delete_category(request, category_pk):
    if request.user.role == 'CUSTOMER':
        return redirect('no_access')
    elif request.user.role == 'MANAGER':
        Category.objects.filter(pk=category_pk).delete()
        return redirect('category_page')

@login_required
def applications_management(request):
    if request.method == 'POST':
        if 'application_status' in request.POST:
            if request.POST['application_status'][0] == 'a':
                form = ChangeStatusAcceptForm(request.POST)
                if form.is_valid():
                    comment_data = form.cleaned_data
                    print(request.POST['application_pk'])
                    comment_data.update(
                        {
                            'status': request.POST['application_status'][0],
                            'application': Application.objects.get(pk=request.POST['application_pk']),
                        },
                    )
                    current_comment = ApplicationComment.objects.create(**comment_data)
                    Application.objects.filter(pk=current_comment.application.pk).update(status=current_comment.status)
                    return redirect(request.META.get('HTTP_REFERER'))
            elif request.POST['application_status'][0] == 'c':
                form = ChangeStatusCompleteForm(request.POST, request.FILES)
                if form.is_valid():
                    comment_data = form.cleaned_data
                    comment_data.update(
                        {
                            'status': request.POST['application_status'][0],
                            'application': Application.objects.get(pk=request.POST['application_pk']),
                        },
                    )
                    current_comment = ApplicationComment.objects.create(**comment_data)
                    Application.objects.filter(pk=current_comment.application.pk).update(status=current_comment.status)
                    return redirect(request.META.get('HTTP_REFERER'))
        elif 'users' in request.POST and 'field' in request.POST:
            context = {
                'name_page': 'applications_management',
                'form_accept_popup': ChangeStatusAcceptForm(),
                'form_complete_popup': ChangeStatusCompleteForm(),
                'form_filtering': FilterApplicationForm()
            }
            if request.POST['users'] == '' and request.POST['field'] == 's':
                return redirect('applications_management')
            elif request.POST['users'] == '' and request.POST['field'] != 's':
                context['applications'] = Application.objects.filter(status=request.POST['field'])
                context['form_filtering'] = FilterApplicationForm(request.POST)
                return render(request, 'personal_account/applications/manager_show.html', context=context)
            elif request.POST['users'] != '':
                user = CustomUser.objects.get(pk=request.POST['users'])
                if request.POST['field'] == 's':
                    context['applications'] = user.application_set.all()
                    context['form_filtering'] = FilterApplicationForm(request.POST)
                    return render(request, 'personal_account/applications/manager_show.html', context=context)
                else:
                    context['applications'] = user.application_set.filter(status=request.POST['field'])
                    context['form_filtering'] = FilterApplicationForm(request.POST)
                    return render(request, 'personal_account/applications/manager_show.html', context=context)
    else:
        if request.user.role == 'CUSTOMER':
            return redirect('no_access')
        elif request.user.role == 'MANAGER':
            context = {
                'name_page': 'applications_management',
                'applications': Application.objects.all().order_by('-time_create'),
                'form_accept_popup': ChangeStatusAcceptForm(),
                'form_complete_popup': ChangeStatusCompleteForm(),
                'form_filtering': FilterApplicationForm()
            }
            return render(request, 'personal_account/applications/manager_show.html', context=context)

