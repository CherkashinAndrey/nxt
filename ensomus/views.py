# -*- coding: utf-8 -*-
"""
Views for NXT LVL
"""
import StringIO
# from collections import OrderedDict
import os
from django.views.decorators.csrf import csrf_exempt
# from pprint import pprint
from django.template.loader import get_template
import ho.pisa as pisa
from os import path
from django.views.decorators.cache import never_cache
from common.util import csv_to_dict, LazyEncoder, logUnauthorizedAccess
from common.LeaderModel import LeaderModel
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
# from django.shortcuts import render_to_response
from models import (
    Employee, File, EmployeeRole, DevelopmentPlanToEmployeeRelation, Role, Company, Goal, GoalAnswer,
    DevelopmentPlan, Competence, CompetencePart, Action, Question, Answer
)
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from forms import (
    EmployeeForm, EditEmployeeForm, UploadEmployeesForm,
    EmployeeRowFormSet, EmployeeManagerRowFormSet, EmployeeNoteForm, MultiLeaderModelForm,
    UploadFileToEmployeyForm, ActionForm, UploadEmployeePhotoForm, DevelopmentPlanForm,
    DevelopmentPlanToEmployeeRelationForm, UploadFileToEmployeyForm,
    ActionForm, UploadEmployeePhotoForm, UploadManyForm, GoalForm,
    ActionCommentForm, ChangeCompanyForm, PasswordResetForm, GoalAnswerForm
)

# from django.core.paginator import Paginator
from django.utils.encoding import smart_str
# from django.utils import timezone, translation
from django.db.models import Q
from django.utils.translation import ugettext as _, get_language
from django.contrib.auth import login, authenticate, logout
from django.template import Context
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
import common.util as util
import logging
from mimetypes import MimeTypes
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from functools import wraps


logger = logging.getLogger(__name__)

data_competence_part = [{"title": "Cooperation", "description": "Engagement er udtryk for en særlig positiv tilstand "
                                                                "hos dig i forhold til dit job, din arbejdsplads og"
                                                                " dine kolleger. Denne positive tilstand er præget "
                                                                "af energi og handlingsparathed samt en evne til at "
                                                                "være fuldt optaget af dit arbejde, således at du har "
                                                                "svært ved at løsrive dig. Engagement og motivation "
                                                                "hænger sammen og begge dele kan udspringe enten fra "
                                                                "dig selv (indre motivation) eller på baggrund af "
                                                                "ydre faktorer (ydre motivation). Engagement og "
                                                                "motivation er særlige drivkræfter, der dels bidrager "
                                                                "til, at du når dine mål og dels er med til at skabe "
                                                                "arbejdsglæde, psykisk sundhed og forøget effektivitet."
                                                                " "}]
data_competence = [{"title": "Passion"}]
data_questions = [{"title": "Hvad i teksten omkring engagement hæfter du dig i særlig grad ved som værende vigtigt for "
                            "dig?"}]


def login_required_403(view):
    """
    Decorator that returns 403 status if user isn't logged in
    instead of redirecting to the LOGIN_URL
    """
    @wraps(view)
    def dec_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({"detail": "You have to log in"}, status=403)

        return view(request, *args, **kwargs)

    return dec_view


class EmailAuthBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


@csrf_exempt
@require_http_methods(['POST'])
def login_user(request):
    data = json.loads(request.body)
    user = authenticate(username=data["email"], password=data["password"])

    if not user:
        return JsonResponse({}, status=401)
    else:
        employee = Employee.objects.filter(user=user).first()

        if not employee:
            raise PermissionDenied("You don't have any employee assigned to you", 401)
        login(request, user)

        return JsonResponse(status=200, data={"email": user.email, "employee_id": employee.id,
                                              "user_id": employee.user.pk})


@csrf_exempt
@require_http_methods(['POST'])
def logout_user(request, *args, **kwargs):
    logout(request)

    return JsonResponse({}, status=200)


@login_required_403
def create_competence_in_db(request):
    for index1, elem1 in enumerate(data_competence_part):
        competence_part = CompetencePart.objects.create(title=elem1["title"], description=elem1["description"])
        for index2, elem2 in enumerate(data_competence):
            if index1 == index2:
                competence = Competence.objects.create(title=elem2["title"], competence_part=competence_part)
                for index3, elem3 in enumerate(data_questions):
                    if index2 == index3:
                        Question.objects.create(title=elem3["title"], competence=competence)
                        # Slider.objects.create(competence=competence)


def start_view(request):
    """
    Decide where to go, dashboard if logged in, login form if not
    """

    if request.user and Employee.objects.filter(user__pk=request.user.pk).exists():
        if Employee.objects.get(user__pk=request.user.pk).is_manager:
            return HttpResponseRedirect('/dashboard')
        else:
            return HttpResponseRedirect('/employee/show/%d/' % request.user.employee_user.first().pk)
    else:
        return HttpResponseRedirect('/login/')


def accesscode(request, code):
    """
    Login with an accesscode
    """
    employee = Employee.objects.get(access_code=code)
    user = employee.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect('/')

@csrf_exempt
@require_http_methods(['POST'])
def password_reset(request):
    """
    Password reset view
    """
    if request.method == "POST":
        form = PasswordResetForm(request.json_body)
        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data={"password": "change"})
        return JsonResponse(status=400, data=json.loads(form.errors.as_json()))

def password_reset_done(request):
    """
    Password reset done
    """

    return TemplateResponse(
        request,
        'reset_done.html',

    )


@login_required_403
@require_http_methods(['POST'])
def change_company(request):
    """
    Change company
    """
    employee = request.user.employee_user.first()
    if not employee.isEnsoUser() and employee.company.pk != request.POST['company']:
        raise PermissionDenied()
    return HttpResponseRedirect("/employee/all/%s" % request.POST['company'])


@login_required
def all_employees(request, company_id=None):
    """
    View for all employees (in company) or for current user dependent on employee role
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    company_super_user = current_employee.isCompanySuperUserOrHigher()
    if company_id:
        company = Company.objects.get(pk=company_id)
    else:
        company = current_employee.company
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        raise PermissionDenied()
    change_company_form = ChangeCompanyForm(initial=dict(company=company))
    return TemplateResponse(
        request,
        'all_employees.html',
        {
            'user': request.user,
            'company_super_user': company_super_user,
            'company': company,
            'change_company_form': change_company_form,
        }
    )


@login_required_403
@never_cache
# def employees_json(request, company_id=None):
#     """
#     Get all employees as json
#     """
#     current_employee = Employee.objects.get(user__pk=request.user.pk)
#     employee_list = Employee.objects.filter(manager=request.user.employee_user)
#     # questionnaire_companies = currnet_employee.company.getAvailableSchemes()
#     company_super_user = current_employee.isCompanySuperUserOrHigher()
#     if company_id:
#         company = Company.objects.get(pk=company_id)
#     else:
#         company = current_employee.company
#     if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
#         raise PermissionDenied()
#     # if company_super_user:
#     #     managers = company.getTopManagers()
#     # else:
#     #     managers = list()
#     #     managers.append(employee_list)
#     employees = list()
#     for manager in employee_list:
#         print manager
#         # employees.append(manager.to_dict())
#         employees.append(model_to_dict(manager))
#     data = {"employees": employees}
#     return JsonResponse(data=data, content_type='application/json', safe=False)

def employees_json(request):
    """
    Get all employees as json
    """
    # current_employee = Employee.objects.get(user__pk=request.user.pk)
    employee_list = Employee.objects.filter(manager=request.user.employee_user)
    employees = list()
    for employee in employee_list:
        manager_dict = model_to_dict(employee)
        manager_dict['first_name'] = employee.user.first_name
        manager_dict['last_name'] = employee.user.last_name
        employees.append(manager_dict)
    data = {"employees": employees}
    return JsonResponse(data=data, content_type='application/json', safe=False)


@login_required
@never_cache
def employees_json_id(request, employee_id):
    """
    Show employee a level below
    """
    curent_employee = Employee.objects.get(pk=int(employee_id))
    if curent_employee.is_manager:
        employee_list = Employee.objects.filter(manager=curent_employee)
        employees = list()
        for employee in employee_list:
            manager_dict = model_to_dict(employee)
            manager_dict['first_name'] = employee.user.first_name
            manager_dict['last_name'] = employee.user.last_name
            manager_dict['photo'] = employee.photo.url if employee.photo else ''
            employees.append(manager_dict)
        data = {"employees": employees}
    else:
        return JsonResponse(status=400, data={"error": "Employee with id={} not is_manager".format(int(employee_id))})
    return JsonResponse(data=data, content_type='application/json', safe=False)


def found_all_managers(manager_list, result_list):
    found_managers = []
    for manager in manager_list:
        manager_filtered_list = Employee.objects.filter(is_manager=True, manager=manager)
        found_managers = [manager_obj for manager_obj in manager_filtered_list if manager_obj not in result_list]
        result_list += manager_filtered_list
    if len(found_managers) > 0:
        return found_all_managers(found_managers, result_list)
    else:
        return result_list


@login_required_403
@never_cache
@csrf_exempt
def employees_manager(request):
    """
    Get all employees manager as json
    """
    # current_employee = Employee.objects.get(user__pk=request.user.pk)
    manager_list = Employee.objects.filter(manager=request.user.employee_user, is_manager=True)
    employee = Employee.objects.get(pk=request.user.employee_user.id)
    employee_dict = model_to_dict(employee)
    employee_dict['first_name'] = employee.user.first_name
    employee_dict['last_name'] = employee.user.last_name
    employee_dict['photo'] = employee.photo.url if employee.photo else ''
    print employee_dict
    if len(manager_list) > 0:
        result_list = list(manager_list)
        all_managers_list = found_all_managers(manager_list, result_list)
    else:
        data = {"employee_managers": employee_dict}
        return JsonResponse(data=data, content_type='application/json', safe=False)
    employees = list()
    for manager in all_managers_list:
        manager_dict = model_to_dict(manager)
        manager_dict['first_name'] = manager.user.first_name
        manager_dict['last_name'] = manager.user.last_name
        manager_dict['photo'] = manager.photo.url if manager.photo else ''
        employees.append(manager_dict)
    employees.append(employee_dict)

    data = {"employee_managers": employees}
    return JsonResponse(data=data, content_type='application/json', safe=False)


@login_required_403
@require_http_methods(['POST'])
@csrf_exempt
def add_employee(request):
    """
    Add employee
    """
    print "ADD EMPLOYEE"
    # from django.contrib.auth.models import User
    data = json.loads(request.body)
    # user = get_user_model().objects.get(pk=request.user.pk)
    # print "MODEL", model_to_dict(user)
    form = EmployeeForm(request, data or None)
    if not form.is_valid():
         # return TemplateResponse(request, 'mus/create_employee_form.html', {'employee_form': form})
        return JsonResponse(status=400, data=form.errors)
    form.save()
    # return HttpResponseRedirect('/employee/all/%d' % form.cleaned_data.get('company').pk)
    # data = json.loads(form.data)
    # print data
    return JsonResponse(status=201, data=data)


def employee_delete_file(request, employee_id, filename):
    """
    Securely download files from user.

    :param request: HttpRequest
    :param employee_id: int
    :param filename: str
    :return:
    """

    current_user = Employee.objects.get(user__pk=request.user.pk)

    if not current_user.hasAccessTo(employee_id):
        logUnauthorizedAccess(
            "User tried to delete file he didnt have access to", request, filename
        )
        return HttpResponse('unauthorized', status=401)

    user_dir = util.get_user_files_dir(employee_id)
    filename = os.path.join(user_dir, filename.replace('..', ''))

    if not os.path.isfile(filename):
        return HttpResponseNotFound('File does not exist')

    os.remove(filename)

    return HttpResponseRedirect(reverse('employee_detail', args=[employee_id]))


def employee_download_file(request, employee_id, filename):
    """
    Securely download files from user.

    :param request: HttpRequest
    :param employee_id: int
    :param filename: str
    :return:
    """

    current_user = Employee.objects.get(user__pk=request.user.pk)

    if not current_user.hasAccessTo(employee_id):
        logUnauthorizedAccess(
            "User tried to download file he didnt have access to", request, filename
        )
        return HttpResponse('unauthorized', status=401)

    user_dir = util.get_user_files_dir(employee_id)
    filename = os.path.join(user_dir, filename.replace('..', ''))

    if not os.path.isfile(filename):
        return HttpResponseNotFound('File does not exist')

    wrapper = FileWrapper(file(filename))

    ext = os.path.splitext(filename)[1].lower()

    response = HttpResponse(
        wrapper,  # i'd rather do this hack than use urllib.pathname2url
        content_type=MimeTypes().guess_type('/bogus/path/bogus_file' + ext)
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['Content-Length'] = os.path.getsize(filename)

    return response


def get_files_for_employee(employee_id):
    """

    :param employee_id: int
    :return: list[str]
    """

    user_dir = util.get_user_files_dir(employee_id)

    return [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]


@login_required_403
def employee_detail(request, employee_id):
    """
    View for detail of employee
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    employee = Employee.objects.get(pk=int(employee_id))
    if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
        raise PermissionDenied()
    actions = employee.action_set.all()
    if not current_employee.pk == int(employee_id):
        if not current_employee.is_manager or not current_employee.company.pk == employee.company.pk:
            if not current_employee.isCompanySuperUserOrHigher():
                return HttpResponse('unauthorized', status=401)

    user_files = get_files_for_employee(employee_id)

    if request.method == 'POST':

        upload_form = UploadFileToEmployeyForm(request.POST, request.FILES)
        form = EmployeeNoteForm(request.POST, instance=employee)

        if 'upload' in request.POST:
            if upload_form.is_valid():
                upload_form.handle_upload(employee_id, request.FILES['file'])

                return HttpResponseRedirect('/employee/show/{}?upload_status=ok#file-list'.format(employee_id))

        else:
            if form.is_valid():
                form.save(request.user, employee)
                return HttpResponseRedirect('/employee/show/%d' % form.instance.pk)

    else:
        form = EmployeeNoteForm(instance=employee)
        upload_form = UploadFileToEmployeyForm()
    data = {}
    data["first_name"] = employee.user.first_name
    data["last_name"] = employee.user.last_name
    data["email"] = employee.user.email
    data["is_manager"] = employee.is_manager
    data["language_code"] = employee.language_code
    employee_role = EmployeeRole.objects.filter(employee=employee).all()
    name_role_list = []
    for obj in employee_role:
        name_role_list.append(obj.role.name)
    data["roles"] = name_role_list
    return JsonResponse(status=201, data=data)
    # return TemplateResponse(
    #     request,
    #     'mus/detail.html',
    #     {
    #         'actions': actions,
    #         'employee': employee,
    #         # 'development_plans': development_plans,
    #         'form': form,
    #         'upload_form': upload_form,
    #         'user_files': user_files
    #     }
    # )


@login_required_403
# @require_http_methods(['POST'])
@csrf_exempt
def get_manager_employees(request):
    """
    View for all employees current user is a manager for with empty development plan
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    manager_employees = Employee.objects.filter(manager=current_employee, development_plan_type=None).all()
    if manager_employees:
        emp_list=[]
        for emp in manager_employees:
            emp_data={}
            emp_data["id"] = emp.id
            emp_data["username"] = emp.user.username
            emp_data["first_name"] = emp.user.first_name
            emp_data["last_name"] = emp.user.last_name
            emp_data["manager_id"] = emp.manager.id
            # emp_data["status_questions"] = emp.status_questions
            # employee_role = EmployeeRole.objects.filter(employee=emp).all()
            # name_role_list = []
            # for obj in employee_role:
            #     name_role_list.append(obj.role.name)
            # emp_data["roles"] = name_role_list
            emp_list.append(emp_data)
        data = {"employees:": emp_list}
        return JsonResponse(status=201, data=data)
    else:
        return JsonResponse("The user with id={} isn't a manager for any user".format(current_employee.user.id),
                            status=404)


# @login_required
@login_required_403
def profile_detail(request, employee_id):
    """
    View for detail of employee
    """
    current_employee = Employee.objects.filter(user__pk=request.user.pk).first()
    employee = Employee.objects.get(pk=int(employee_id))

    if not current_employee:
        raise PermissionDenied("You don't have any employee assigned to you.", 401)

    if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
        raise PermissionDenied()
    actions = employee.action_set.all()
    if not current_employee.pk == int(employee_id):
        if not current_employee.is_manager or not current_employee.company.pk == employee.company.pk:
            if not current_employee.isCompanySuperUserOrHigher():
                return HttpResponse('unauthorized', status=401)

    user_files = get_files_for_employee(employee_id)

    if request.method == 'POST':

        upload_form = UploadFileToEmployeyForm(request.POST, request.FILES)
        form = EmployeeNoteForm(request.POST, instance=employee)

        if 'upload' in request.POST:
            if upload_form.is_valid():
                upload_form.handle_upload(employee_id, request.FILES['file'])

                return HttpResponseRedirect('/employee/show/{}?upload_status=ok#file-list'.format(employee_id))

        else:
            if form.is_valid():
                form.save(request.user, employee)
                return HttpResponseRedirect('/employee/show/%d' % form.instance.pk)

    else:
        form = EmployeeNoteForm(instance=employee)
        upload_form = UploadFileToEmployeyForm()
    data = {}
    data["user"] = employee.user.first_name + " " + employee.user.last_name
    data["id"] = str(employee.user.pk)
    data["title"] = employee.title
    data["email"] = employee.user.email
    data["phone"] = employee.phone
    company_dict = {}
    company_dict["name"] = employee.company.name
    company_dict["id"] = str(employee.company.pk)

    data["company"] = company_dict
    employee_username = ""
    emp = Employee.objects.filter(manager=employee.manager).all()
    for obj in emp:
        employee_username = obj.manager.user.username if obj.manager else ""
        employee_first = obj.manager.user.first_name if obj.manager else ""
        employee_last = obj.manager.user.last_name if obj.manager else ""
    manager_dict = {}
    manager_dict["name"] = employee_username
    manager_dict["id"] = employee_id
    manager_dict["first_last_name"] = employee_first + " " + employee_last
    data["manager"] = manager_dict
    data["date_of_birth"] = employee.date_of_birth
    data["status_questions"] = employee.status_questions
    data["notes"] = employee.notes
    employee_role = EmployeeRole.objects.filter(employee=employee).all()
    name_role_list = []
    for obj in employee_role:
        name_role_list.append(obj.role.name)
    data["roles"] = name_role_list
    data["potenciale"] = employee.potenciale
    data["date_start"] = employee.created_at
    data["is_manager"] = employee.is_manager
    data["date_finish"] = ""
    data['photo'] = employee.photo.url if employee.photo else ''

    return JsonResponse(status=200, data=data)
    # return TemplateResponse(
    #     request,
    #     'mus/detail.html',
    #     {
    #         'actions': actions,
    #         'employee': employee,
    #         # 'development_plans': development_plans,
    #         'form': form,
    #         'upload_form': upload_form,
    #         'user_files': user_files
    #     }
    # )


@login_required_403
@csrf_exempt
def create_employee(request, company_id):
    """
    View for creating employee in company
    """

    company = Company.objects.get(pk=company_id)
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        logUnauthorizedAccess("User tried to create_employee", request)
        raise PermissionDenied()
    form = EmployeeForm(request, initial=dict(company=company))
    form.fields['manager'].queryset = Employee.objects.filter(is_manager=True, company=company)
    # form.fields['development_plan_type'].queryset = DevelopmentPlanType.objects.filter(
    #     Q(company=company) | Q(company__isnull=True))
    # data = {
    #         'employee_form': form.cleaned_data,
    #         'company': company.cleaned_data["name"]
    #     }

    return TemplateResponse(
        request,
        'mus/create_employee_form.html',
        {
            'employee_form': form,
        }
    )
    # data = {
    #         'employee_form': form.cleaned_data,
    #         'company': company.cleaned_data["name"]
    #     }
    # return JsonResponse(status=200, data=data)


@login_required_403
def create_many_employees(request, company_id=None):
    """
    View for creating many employees in company
    """
    company = Company.objects.get(pk=company_id)
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        raise PermissionDenied()
    if "upload" in request.POST:
        form = UploadEmployeesForm(request.POST, request.FILES)
        if form.is_valid():
            data = csv_to_dict(request.FILES['file'])
            request.session['upload_employees'] = data
            return JsonResponse(status=201, data=form.cleaned_data)
            # return TemplateResponse(
            #     request,
            #     'mus/create_many_employees_uploaded.html',
            #     dict(data=data, company=company)
            # )
    elif "next" in request.POST:
        data = request.session['upload_employees']
        marked_data = list()
        fields = request.POST.getlist('field[]')
        for row in data:
            new_row = dict(is_manager=False)
            for i, item in enumerate(row):
                field_id = int(fields[i])
                if field_id == 1:
                    new_row['first_name'] = item
                elif field_id == 2:
                    new_row['last_name'] = item
                elif field_id == 3:
                    p = item.partition(" ")
                    new_row['first_name'] = p[0]
                    new_row['last_name'] = p[2]
                elif field_id == 4:
                    new_row['email'] = item
                elif field_id == 5:
                    new_row['username'] = item
            marked_data.append(new_row)
        formset = EmployeeRowFormSet(initial=marked_data)
        # TypeQS = DevelopmentPlanType.objects.filter(Q(company=company) | Q(company__isnull=True))
        # for form in formset:
        #     form.fields['development_plan_type'].queryset = TypeQS
        return TemplateResponse(
            request,
            'mus/create_many_employees_form.html',
            dict(formset=formset, company=company)
        )
    elif "next2" in request.POST:
        formset = EmployeeRowFormSet(request.POST)
        if formset.is_valid():
            data = list()


@login_required_403
@require_http_methods(['POST'])
@csrf_exempt
def update_employee(request, employee_id):
    """
    Update employee
    """
    employee = Employee.objects.get(pk=int(employee_id))
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
        raise PermissionDenied()
    print "BODY:", request.body
    print "JSON BODY:", request.json_body
    form = EditEmployeeForm(request.user, employee, data=request.json_body or None)
    if 'manager' in form.fields:
        managerQS = Employee.objects.filter(is_manager=True, company__pk=employee.company.pk)
        form.fields['manager'].queryset = managerQS
    if not form.is_valid():
        # is_me = employee.user.pk == request.user.pk
        print "errors", form.errors
        return JsonResponse(status=400, data=json.loads(form.errors.as_json()))
        # return TemplateResponse(
        #     request,
        #     'mus/edit_employee_form.html',
        #     {
        #         'edit_employee_form': form,
        #         'employee_id': employee_id,
        #         'me': is_me,
        #         'name': employee.user.get_full_name()
        #     }
        # )
    form.save()
    data = form.cleaned_data
    if 'manager' in data:
        data['manager'] = str(data['manager'].id)

    data['roles'] = [str(r.name) for r in data['roles']]
    data['company'] = str(data['company'].id)
    # return HttpResponseRedirect('/employee/show/' + employee_id + '/')
    return JsonResponse(status=200, data=data)


@login_required_403
@csrf_exempt
def edit_employee(request, employee_id):
    """
    View for editing employee
    """
    employee = Employee.objects.get(pk=int(employee_id))
    current_employee = Employee.objects.get(user__pk=request.user.pk)

    assert isinstance(employee, Employee)
    assert isinstance(current_employee, Employee)

    # if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
    # raise PermissionDenied()

    if not current_employee.hasAccessTo(employee):
        raise PermissionDenied()

    form = EditEmployeeForm(request.user, employee, {
        'first_name': employee.user.first_name,
        'last_name': employee.user.last_name,
        'email': employee.user.email,
        'manager': employee.manager.id if employee.manager else 0,
        'language_code': employee.language_code,
        # 'development_plan_type': employee.development_plan_type.id,
        'is_manager': employee.is_manager
    })
    if 'manager' in form.fields:
        managerQS = Employee.objects.filter(is_manager=True, company__pk=employee.company.pk)
        form.fields['manager'].queryset = managerQS
        # form.fields['development_plan_type'].queryset = DevelopmentPlanType.objects.filter(
        #     Q(company__pk=employee.company.pk) | Q(company__isnull=True)
        # )
    is_me = employee.user.pk == request.user.pk
    return TemplateResponse(
        request,
        'mus/edit_employee_form.html',
        {
            'edit_employee_form': form,
            'employee_id': employee_id,
            'me': is_me,
            'name': employee.user.get_full_name()
        }
    )


@login_required_403
def files(request):
    fs = File.getMyfiles(request.user)
    return TemplateResponse(
        request,
        'mus/files.html',
        {
            'files': fs
        }
    )


@login_required_403
def get_file(request, file_id):
    f = File.objects.get(pk=int(file_id))
    if not f.canDownload(request.user):
        return HttpResponse('unauthorized', status=401)
    response = HttpResponse(
        f.file.data,
        mimetype=f.mime_type
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(f.file_name)
    response['Content-Length'] = smart_str(f.file_size)
    return response


@login_required_403
def dashboard(request):
    """
    View of dashboard containing overview of relevant information
    """
    employee = request.user.employee_user.first()
    widgets = list()
    # development_plans = employee.getDevelopmentPlans()
    if employee.is_manager:
        widgets.append(dict(
            # template="mus/_widget_waiting_developmentplans.html",
            data=employee.getMyEmployees(),
            # title=_('Expecting preparation guides from')
        ))
        widgets.append(dict(
            # template="mus/_widget_todo_developmentplans.html",
            data=employee.getMyEmployees(),
            # title=_('Preparation guides to do')
        ))
    # widgets.append(dict(
    #        template = "mus/_widget_my_developmentplans.html",
    #        data = development_plans,
    #        title = _('My development plans')
    #    ))
    return JsonResponse(status=200,data={
            # 'widgets': model_to_dict(widgets),
            'employee': model_to_dict(employee),
            # 'development_plans': development_plans
        })


@login_required_403
def action_list(request, employee_id=None):
    """
    View for list of actions of (current) employee
    """
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        current_employee = Employee.objects.get(user__pk=request.user.pk)
        if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
            raise PermissionDenied()
    else:
        employee = request.user.employee_user.first()
    actions = employee.action_set.all()
    return TemplateResponse(
        request,
        'mus/action_list.html',
        dict(
            actions=actions,
            employee=employee
        )
    )


@login_required_403
@require_http_methods(['POST'])
@csrf_exempt
def action_edit(request, action_id):
    """
    View for editing action
    """
    employee = request.user.employee_user.first()
    action = Action.objects.get(pk=action_id)
    if not employee.isEnsoUser() and employee.company.pk != action.employee.company.pk:
        raise PermissionDenied()
    # if request.method == 'POST':
    form = ActionForm(request.POST, instance=action)
    if form.is_valid():
        form.save(request.user, employee)
        return HttpResponseRedirect('/action/%d' % form.instance.pk)
    # else:
    #     form = ActionForm(instance=action)
    # return TemplateResponse(
    #     request,
    #     'mus/action_edit.html',
    #     dict(
    #         form=form,
    #         edit=True
    #     )
    # )

    # return JsonResponse(status=200, data={"data": form.instance.title, "edit": True})


@login_required_403
def action_detail(request, action_id):
    """
    View for detail of action
    """
    employee = request.user.employee_user.first()
    action = Action.objects.get(pk=int(action_id))
    # if not employee.isEnsoUser() and employee.company.pk != action.employee.company.pk:
    if not employee.hasAccessTo(action.employee):
        raise PermissionDenied()

    if request.method == 'POST':
        form = ActionCommentForm(request.POST)
        if form.is_valid():
            form.save(request.user, action)
            return HttpResponseRedirect('/action/%s' % action_id)
    else:
        form = ActionCommentForm()
    return TemplateResponse(
        request,
        'mus/action_detail.html',
        dict(
            action=action,
            form=form
        )
    )


@login_required_403
def action_add(request, employee_id=None):
    """
    View for creating action
    """
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        current_employee = Employee.objects.get(user__pk=request.user.pk)
        if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
            raise PermissionDenied()
    else:
        employee = request.user.employee_user.first()
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save(request.user, employee)
            return HttpResponseRedirect('/action/%d' % form.instance.pk)
    else:
        form = ActionForm()
    return TemplateResponse(
        request,
        'mus/action_edit.html',
        dict(
            form=form
        )
    )


@login_required_403
def create_leader_model(request, company_id):
    """
    Create a leader model for employees
    """

    errors = {'noactions': []}
    company = Company.objects.get(pk=company_id)
    currentEmpl = Employee.objects.get(user__pk=request.user.pk)
    """:type : Employee """

    if not currentEmpl.isEnsoUser() and currentEmpl.company.pk != company.pk:
        raise PermissionDenied()

    if currentEmpl.isCompanySuperUserOrHigher():
        employeeQS = Employee.objects.filter(
            company__pk=company_id
        )
    else:
        employeeQS = Employee.objects.filter(
            Q(manager=currentEmpl),
            company__pk=company_id
        )

    form = MultiLeaderModelForm(request.POST or None)
    form.fields['employees'].queryset = employeeQS

    if request.method == 'POST' and form.is_valid():

        employees = form.cleaned_data['employees']
        """:type : list[Employee] """

        pdf_response = get_leader_model_pdf(currentEmpl, employees)

        if isinstance(pdf_response, HttpResponse):
            return pdf_response
        else:
            errors = pdf_response

    print(errors)

    return TemplateResponse(
        request,
        'mus/create_leader_model.html', {
            'form': form,
            'company': company,
            'errors': errors
        }
    )


def get_leader_model_pdf(currentEmpl, employees):
    """
    Create LeaderModel and send it as a PDF to the browser

    :param currentEmpl: Employee
    :param employees: list[Employee]
    :return:
    """

    lm = LeaderModel()
    employee_actions = {}
    legend = []
    colors = {}
    errors = {'noactions': []}
    # numbered_actions = {}

    for empl in employees:

        if not currentEmpl.hasAccessTo(empl):
            raise PermissionDenied()

        actions = empl.action_set.all()

        if not len(actions):
            errors['noactions'].append(empl)
            continue

        lkey = empl.user.first_name + " " + empl.user.last_name
        legend.append(lkey)

        if not lkey in employee_actions:
            employee_actions[lkey] = {}

        for action in actions:

            if not action.difficulty or not action.type:
                errors['noactions'].append(empl)
                continue

            circle_number = lm.addCircle(action)
            latest_comment = action.getLatestComment()

            employee_actions[lkey][circle_number] = {
                'name': action.title,
                'type': action.type,
                'difficulty': action.getDifficultyText(),
                'comment': latest_comment
            }

            if lkey not in colors:
                color = lm.getEmployeeColors(empl.id)
                colors[lkey] = "rgb({}, {}, {})".format(color[0], color[1], color[2])

    if len(errors['noactions']):
        return errors

    lm_filename = path.join(settings.STATIC_ROOT, "leadermodel_{}.png".format(currentEmpl.id))
    lm.writeImage(lm_filename)

    #
    # Write PDF

    pdfFilename = path.join(settings.FILES_ROOT, "leadermodel_{}.pdf".format(currentEmpl.id))
    template = get_template('mus/leader_model_pdf.html')
    context = Context({
        'site_url': settings.SITE_URL,
        'lm_filename': lm_filename,
        'employee_actions': employee_actions,
        'colors': colors,
        'legend': legend
    })

    html = template.render(context)
    # html = html.replace('<li>','<li><img class="square" src="http://test.nxtlvl.dk/static/img/square.png" />')
    result = open(pdfFilename, 'wb')
    pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), dest=result)
    result.close()

    wrapper = FileWrapper(file(pdfFilename))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename=ledermodel.pdf'
    response['Content-Length'] = os.path.getsize(pdfFilename)

    return response
    # return HttpResponseRedirect('/employee/all/%d' % int(company_id))


# @login_required_403
# # @require_http_methods(['POST'])
# @csrf_exempt
# def development_plan_answers(request, development_plan_id): #employee_id
#     """
#     Get and save answers to Development Plan questions from user
#     """
#
#
#     development_plan = DevelopmentPlan.objects.get(pk=int(development_plan_id))
#     current_employee = Employee.objects.get(user__pk=request.user.pk)
#
#     if current_employee.id in development_plan.employee_relation.all():
#         # print "OK"
#     else:
#         print "THIS EMPLOYEE ISN'T ATTACHED TO THIS PLAN"
#
#
#
#     print current_employee.id
#     print development_plan.employee_relation.all()
#
#     for emp in development_plan.employee_relation.all():
#         print emp.id






    #, employee_relation=current_employee)

    # print development_plan
    # print current_employee


    # all_employees = development_plan.employee_relation.all()
    # questions = Question.objects.filter(competence_part_id=development_plan.competence_parts.all())#, employee=current_employee)

    # for q in questions:
    #     print q
    # print "QUESTIONS", questions

# competence_parts = development_plan.competence_parts.all()



    # data = json.loads(request.body)  # SEND ACTIVE DEV_PLAN FOR USER
    # print data
    #
    # a = development_plan.competence_parts.filter(question_id = Question.objects.filter(development_plan=development_plan))
    # print "AA", a
    # if data:
    #     question["id"] = int(data['question_id'])
    #     question["id"].save()
    #     # answer = Answer.objects.filter(question__id = data['question_id'],
    #     #                                employee=current_employee).first()
    #     # answer["id"].save()
    #
    # # user = get_user_model().objects.get(pk=request.user.pk)
    # # print "MODEL", model_to_dict(user)
    #
    # # form.fields['manager'].queryset = Employee.objects.filter(is_manager=True, company=company)
    #
    # # if not form.is_valid():
    # #     return JsonResponse(status=400, data=form.errors)
    # # form.save()
    # return JsonResponse(status=201, data=data)


# all_competence_parts = current_development_plan.competence_parts.all()
#
#         competence_list = []
#         questions_list = []
#
#         if all_competence_parts:
#             for comp_part in all_competence_parts:
#
#                 comp_part_data={}
#                 competence_d={"competence_parts": []}
#
#                 comp_part_data["id"] = comp_part.id
#                 comp_part_data["title"] = comp_part.title
#                 comp_part_data["description"] = comp_part.description
#                 comp_part_data["competence_status"] = comp_part.competence_status
#
#                 all_questions = comp_part.question_set.all()
#                 print all_questions
#                 if all_questions:
#                     for question in all_questions:
#                         question_data = {}
#                         question_data["question_id"] = question.id
#                         question_data["title"] = question.title
#                         question_data["competence_part"] = question.competence_part.id
#
#                         answer = Answer.objects.filter(question__id = question.id,
#                                                        employee=current_employee).first()
#
#                         if answer:
#                             question_data["answer_id"] = answer.id






from django.forms.models import inlineformset_factory, modelformset_factory

@login_required_403
# @require_http_methods(['POST'])
@csrf_exempt
def all_competence_list(request):
    all_competences = {}
    data = []
    for competence in Competence.objects.all():
        obj = {}
        obj["id"] = competence.id
        obj["title"] = competence.title
        data.append(obj)
    all_competences["competences"] = data
    return JsonResponse(status=200, data=all_competences)


@login_required_403
@require_http_methods(['POST'])
@csrf_exempt
def create_development_plan(request, employee_id):
    """
    Add Development Plan
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    employee = Employee.objects.filter(pk=int(employee_id)).first()

    if not current_employee:
        raise PermissionDenied("You don't have any employee assigned to you.", 401)

    if not current_employee.is_manager():
        raise PermissionDenied()
    if not current_employee.pk == int(employee_id):
        if not current_employee.isCompanySuperUserOrHigher():
            return HttpResponse('unauthorized', status=401)


    data = json.loads(request.body)
    dev_plan_form = DevelopmentPlanForm(request, data)
    development_plan = None
    if dev_plan_form.is_valid():
        development_plan = dev_plan_form.save(manager=current_employee)
    competence_parts_list = data.get('competence_parts_list')
    if competence_parts_list:
        for competence_part_id in competence_parts_list:
            competence_part_related = CompetencePart.objects.get(pk=competence_part_id)
            dev_plan_form.save( dev_plan=development_plan, competence_part_object=competence_part_related)
    plan_to_employee_rel_form = DevelopmentPlanToEmployeeRelationForm(request, data)
    if plan_to_employee_rel_form.is_valid():
        for employee_id in data.get('employees_list'):
            employee = Employee.objects.get(pk=employee_id)
            plan_to_employee_rel = plan_to_employee_rel_form.save(employee, development_plan)
            dev_plan_form.save(employee=employee, dev_plan=development_plan,
                               plan_to_employee_rel=plan_to_employee_rel)

        return JsonResponse(data={"data":data}, status=200)
    else:
        return JsonResponse(data=dev_plan_form.errors, status=400)


@login_required_403
def development_plan_details(request, development_plan_id): #, employee_id ):
    """
    View for employee development plan details
    """
    # employee = Employee.objects.get(user__pk=request.user.pk)
    # employee = Employee.objects.filter(pk=int(employee_id)).first()

    development_plan = DevelopmentPlan.objects.get(pk=int(development_plan_id))
    current_employee = Employee.objects.filter(user__pk=request.user.pk).first()
    all_employees = development_plan.employee_relation.all()

    try:
        development_plan = DevelopmentPlan.objects.get(pk=int(development_plan_id))
        data={}
        development_plan_object_list=[]
        dev_plan={}
        dev_plan["id"] = development_plan.id
        dev_plan["deleted"] = development_plan.deleted
        if development_plan.type:
            dev_plan["type"] = development_plan.type.name
        # dev_plan["finished_at"] = DevelopmentPlanToEmployeeRelation.objects.get(development_plan = development_plan)\
        #                           .finished_at

        dev_plan["created_at"] = development_plan.created_at
        dev_plan["created_by"] = development_plan.created_by.username

        development_plan_object_list.append({"dev_plan_details":dev_plan})

# manager_relation
        manager_data={}
        manager_data["manager_username"] = development_plan.manager_relation.user.username
        manager_data["manager_first_name"] = development_plan.manager_relation.user.first_name
        manager_data["manager_last_name"] = development_plan.manager_relation.user.last_name
        development_plan_object_list.append({"manager_data":manager_data})

# employee_relation
        employee_data={}
        all_employees = development_plan.employee_relation.all()
        if all_employees:
            emp_list=[]
            for emp in all_employees:
                emp_data={}
                emp_data["id"] = emp.user.id
                emp_data["username"] = emp.user.username
                emp_data["first_name"] = emp.user.first_name
                emp_data["last_name"] = emp.user.last_name
                emp_data["status_questions"] = emp.status_questions

                emp_data["dev_plan_finished_at"] = DevelopmentPlanToEmployeeRelation\
                                                        .objects.get(employee=emp,
                                                                     development_plan = development_plan)\
                                                        .finished_at

                employee_role = EmployeeRole.objects.filter(employee=emp).all()
                name_role_list = []
                for obj in employee_role:
                    name_role_list.append(obj.role.name)
                emp_data["roles"] = name_role_list
                emp_list.append(emp_data)
            employee_data={"all_employees":emp_list}
        else:
            return JsonResponse(data={"details":"Any employee has Development Plan with id={}"
                                .format(development_plan.id)}, status=404)

        development_plan_object_list.append({"employee_data":employee_data})


# competence_parts
        all_competence_parts = development_plan.competence_parts.all()

        competence_list = []
        questions_list = []
        sliders_list = []

        if all_competence_parts:
            for comp_part in all_competence_parts:

                comp_part_data={}
                competence_d={"competence_parts": []}

                comp_part_data["id"] = comp_part.id
                comp_part_data["title"] = comp_part.title
                comp_part_data["description"] = comp_part.description
                comp_part_data["competence_status"] = comp_part.competence_status

                all_questions = comp_part.question_set.all()
                if all_questions:
                    for question in all_questions:
                        question_data = {}
                        question_data["question_id"] = question.id
                        question_data["title"] = question.title
                        question_data["competence_part"] = question.competence_part.id

                        answer = Answer.objects.filter(question__id = question.id).first() #employee=current_employee

                        if answer:
                            question_data["answer_id"] = answer.id
                            question_data["answer"] = answer.title

                        questions_list.append(question_data)

                    comp_part_data["questions"] = questions_list

                all_sliders = comp_part.slider_set.all()
                if all_sliders:
                    for slider in all_sliders:
                        slider_data = {}
                        slider_data["slider_id"] = slider.id
                        slider_data["scale"] = slider.scale
                        slider_data["competence_part"] = slider.competence_part.id

                        answer = Answer.objects.filter(slider__id = slider.id).first() #employee=current_employee

                        if slider:
                            slider_data["answer_id"] = answer.id
                            slider_data["answer"] = answer.slider.scale

                        sliders_list.append(slider_data)

                    comp_part_data["sliders"] = sliders_list

                comp_part_data["created_at"] = comp_part.created_at
                comp_part_data["created_by"] = comp_part.created_by.username
                comp_part_data["updated_at"] = comp_part.updated_at
                comp_part_data["updated_by"] = comp_part.updated_by.username

                competence_keys_list = ['id', 'title', 'description',
                                        'language_code', 'status']

                if not competence_list:
                    get_competence_data(competence_keys_list, comp_part.competence, competence_d,
                                        comp_part_data, competence_list)
                else:
                    competence_found = False
                    for competence_dict in competence_list:
                        if competence_dict['id'] == comp_part.competence.id:
                            competence_dict['competence_parts'].append(comp_part_data)
                            competence_found = True
                            break

                    if not competence_found:
                        get_competence_data(competence_keys_list, comp_part.competence, competence_d,
                                            comp_part_data, competence_list)

            development_plan_object_list.append({"competences":competence_list})

        else:
            return JsonResponse(data={"details":"Development Plan with id={} doesn't have any Competence Part yet"
                                    .format(development_plan.id)}, status=404)

        data = {"dev_plan:": development_plan_object_list}
        return JsonResponse(status=201, data=data)

    except DevelopmentPlan.DoesNotExist:
        return JsonResponse(data={"details":"Development Plan with this id doesn't exist"}, status=404)


def get_competence_data(competence_keys_list, competence, competence_d, comp_part_data, competence_list):
    for element in competence_keys_list:
        competence_d[element] = getattr(competence, element)
    competence_d["company_id"] = competence.company.id
    competence_d["company_name"] = competence.company.name
    competence_d["competence_parts"].append(comp_part_data)
    competence_list.append(competence_d)
    return competence_list


@login_required_403
@csrf_exempt
def get_all_user_development_plans_for_manager(request, employee_id):
    """
    View a list of user's development plans for manager
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    user_development_plans = DevelopmentPlan.objects.filter(employee_relation=current_employee).all()
    employee = Employee.objects.filter(pk=int(employee_id)).first()

    if not current_employee:
        raise PermissionDenied("You don't have any employee assigned to you.", 401)

    if not current_employee.isEnsoUser() and current_employee.is_manager:
        raise PermissionDenied()
    actions = employee.action_set.all()
    if not int(employee_id) in [obj.id for obj in Employee.objects.filter(manager=current_employee).all()]:
        raise PermissionDenied("Employee with id={} is not assigned to you.".format(employee_id), 401)

    if user_development_plans:
        data={}
        user_development_plans_list = []
        for plan in user_development_plans:

            development_plan_object_list=[]
            dev_plan = {}

            dev_plan["id"] = plan.id
            dev_plan["deleted"] = plan.deleted
            if plan.type:
                dev_plan["type"] = plan.type.name
            dev_plan["finished_at"] = DevelopmentPlanToEmployeeRelation.objects\
                                        .get(employee=current_employee, development_plan = plan).finished_at
            dev_plan["created_at"] = plan.created_at
            dev_plan["created_by"] = plan.created_by.username

            development_plan_object_list.append({"dev_plan_details":dev_plan})

            manager_data = {}
            manager_data["manager_username"] = plan.manager_relation.user.username
            manager_data["id"] = plan.manager_relation.user.id

            development_plan_object_list.append({"manager_data":manager_data})
            user_development_plans_list.append(development_plan_object_list)

    else:
        return JsonResponse(data={"details":"Employee with id={} doesn't have any Development Plan"
                            .format(request.user.pk)}, status=404)

    data = {"user_development_plans:": user_development_plans_list}
    return JsonResponse(status=201, data=data)


@login_required_403
@csrf_exempt
def get_all_development_plans_for_user(request):
    """
    View a list of development plans for active user
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    user_development_plans = DevelopmentPlan.objects.filter(employee_relation=current_employee).all()

    if not current_employee:
        raise PermissionDenied("You don't have any employee assigned to you.", 401)

    if user_development_plans:
        data={}
        user_development_plans_list = []
        for plan in user_development_plans:

            development_plan_object_list=[]
            dev_plan = {}

            dev_plan["id"] = plan.id
            dev_plan["deleted"] = plan.deleted
            if plan.type:
                dev_plan["type"] = plan.type.name
            dev_plan["finished_at"] = DevelopmentPlanToEmployeeRelation.objects\
                                        .get(employee=current_employee, development_plan = plan).finished_at
            dev_plan["created_at"] = plan.created_at
            dev_plan["created_by"] = plan.created_by.username

            development_plan_object_list.append({"dev_plan_details":dev_plan})

            manager_data = {}
            manager_data["manager_username"] = plan.manager_relation.user.username
            manager_data["id"] = plan.manager_relation.user.id

            development_plan_object_list.append({"manager_data":manager_data})
            user_development_plans_list.append(development_plan_object_list)

    else:
        return JsonResponse(data={"details":"Employee with id={} doesn't have any Development Plan"
                            .format(request.user.pk)}, status=404)

    data = {"user_development_plans:": user_development_plans_list}
    return JsonResponse(status=201, data=data)


@login_required_403
@csrf_exempt
def get_active_development_plan_for_user(request):
    """
    View active development plan for active user
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    current_development_plan = DevelopmentPlan.objects.filter(
        employee_relation=current_employee,
        employee_relation__developmentplantoemployeerelation__finished_at__isnull=True).first() # is active !!!

    if not current_employee:
        raise PermissionDenied()

    if current_development_plan:
        data={}
        development_plan_object_list=[]
        dev_plan={}
        dev_plan["id"] = current_development_plan.id
        dev_plan["deleted"] = current_development_plan.deleted
        if current_development_plan.type:
            dev_plan["type"] = current_development_plan.type.name
        dev_plan["finished_at"] = DevelopmentPlanToEmployeeRelation.objects\
                                    .get(employee=current_employee, development_plan = current_development_plan)\
                                    .finished_at

        dev_plan["created_at"] = current_development_plan.created_at
        dev_plan["created_by"] = current_development_plan.created_by.username

        development_plan_object_list.append({"dev_plan_details":dev_plan})

# manager_relation
        manager_data={}
        manager_data["manager_username"] = current_development_plan.manager_relation.user.username
        manager_data["manager_first_name"] = current_development_plan.manager_relation.user.first_name
        manager_data["manager_last_name"] = current_development_plan.manager_relation.user.last_name
        development_plan_object_list.append({"manager_data":manager_data})

# employee_relation
        employee_data={}
        all_employees = current_development_plan.employee_relation.all()
        if all_employees:
            emp_list=[]
            for emp in all_employees:
                emp_data={}
                emp_data["id"] = emp.user.id
                emp_data["username"] = emp.user.username
                emp_data["first_name"] = emp.user.first_name
                emp_data["last_name"] = emp.user.last_name
                emp_data["status_questions"] = emp.status_questions

                employee_role = EmployeeRole.objects.filter(employee=emp).all()
                name_role_list = []
                for obj in employee_role:
                    name_role_list.append(obj.role.name)
                emp_data["roles"] = name_role_list
                emp_list.append(emp_data)
            employee_data={"all_employees":emp_list}
        else:
            return JsonResponse(data={"details":"Any employee has Development Plan with id={}"
                                .format(current_development_plan.id)}, status=404)

        development_plan_object_list.append({"employee_data":employee_data})


# competence_parts
        all_competence_parts = current_development_plan.competence_parts.all()

        competence_list = []
        questions_list = []
        sliders_list = []

        if all_competence_parts:
            for comp_part in all_competence_parts:

                comp_part_data={}
                competence_d={"competence_parts": []}

                comp_part_data["id"] = comp_part.id
                comp_part_data["title"] = comp_part.title
                comp_part_data["description"] = comp_part.description
                comp_part_data["competence_status"] = comp_part.competence_status

                all_questions = comp_part.question_set.all()
                print all_questions
                if all_questions:
                    for question in all_questions:
                        question_data = {}
                        question_data["question_id"] = question.id
                        question_data["title"] = question.title
                        question_data["competence_part"] = question.competence_part.id

                        answer = Answer.objects.filter(question__id = question.id,
                                                       employee=current_employee).first()

                        if answer:
                            question_data["answer_id"] = answer.id
                            question_data["answer"] = answer.title

                        questions_list.append(question_data)

                comp_part_data["questions"] = questions_list

                all_sliders = comp_part.slider_set.all()
                if all_sliders:
                    for slider in all_sliders:
                        slider_data = {}
                        slider_data["slider_id"] = slider.id
                        slider_data["scale"] = slider.scale
                        slider_data["competence_part"] = slider.competence_part.id

                        answer = Answer.objects.filter(slider__id = slider.id,
                                                       employee=current_employee).first()

                        if slider:
                            slider_data["answer_id"] = answer.id
                            slider_data["answer"] = answer.slider.scale

                        sliders_list.append(slider_data)

                    comp_part_data["sliders"] = sliders_list

                comp_part_data["created_at"] = comp_part.created_at
                comp_part_data["created_by"] = comp_part.created_by.username
                comp_part_data["updated_at"] = comp_part.updated_at
                comp_part_data["updated_by"] = comp_part.updated_by.username

                competence_keys_list = ['id', 'title', 'description',
                                        'language_code', 'status']

                if not competence_list:
                    get_competence_data(competence_keys_list, comp_part.competence, competence_d,
                                        comp_part_data, competence_list)

                else:
                    competence_found = False
                    for competence_dict in competence_list:
                        if competence_dict['id'] == comp_part.competence.id:
                            competence_dict['competence_parts'].append(comp_part_data)
                            competence_found = True
                            break

                    if not competence_found:
                        get_competence_data(competence_keys_list, comp_part.competence, competence_d,
                                            comp_part_data, competence_list)

            development_plan_object_list.append({"competences":competence_list})

        else:
            return JsonResponse(data={"details":"Development Plan with id={} doesn't have any Competence Part yet"
                                    .format(current_development_plan.id)}, status=404)

        data = {"dev_plan:": development_plan_object_list}
        return JsonResponse(status=201, data=data)

    else:
        return JsonResponse(data={"details": "The user with id={} doesn't have an active Development Plan"
                                .format(current_employee.user.id)}, status=404)

def get_competence_data(competence_keys_list, competence, competence_d, comp_part_data, competence_list):
    for element in competence_keys_list:
        competence_d[element] = getattr(competence, element)
    competence_d["company_id"] = competence.company.id
    competence_d["company_name"] = competence.company.name
    competence_d["competence_parts"].append(comp_part_data)
    competence_list.append(competence_d)
    return competence_list


@login_required_403
@csrf_exempt
def upload_photo(request, employee_id):
    employee = Employee.objects.get(pk=int(employee_id))

    form = UploadEmployeePhotoForm(data=request.json_body)

    if not form.is_valid():
        return JsonResponse(data={"detail": json.loads(form.errors.as_json())}, status=400)

    form.save(employee)

    return JsonResponse({}, status=200)


@login_required_403
@csrf_exempt
def upload_many_employee(request, company_id=None):
    company = Company.objects.get(pk=company_id)
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    manager_list = Employee.objects.filter(manager=current_employee, is_manager=True)
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        raise PermissionDenied()
    form = UploadManyForm(current_employee, data=request.json_body)
    if not form.is_valid():
        return JsonResponse(data={"detail": json.loads(form.errors.as_json())}, status=400)

    form.save(company, request)
    data = form.cleaned_data
    return JsonResponse(data=data, status=200)


@login_required_403
@csrf_exempt
def self_goal(request):
    current_user = request.user

    fields_map = {
        'goal_answers': lambda g: [
            {
                'id': answ.id,
                'title': answ.title,
                "created_by": answ.created_by.username,
                "created_at": answ.created_at,
                "file": answ.file.url
            } for answ in g.goal_answers.all()
        ]
    }

    fields = ['title', 'goal_answers', 'id', 'is_achieved']

    if request.method == 'POST':
        f = GoalForm(data=request.json_body)

        if not f.is_valid():
            return JsonResponse(data={"detail": json.loads(f.errors.as_json())}, status=400)

        goal = f.save(current_user)

        return JsonResponse(
            data={f: fields_map[f](goal) if f in fields_map else getattr(goal, f) for f in fields}, status=200
        )
    elif request.method == 'GET':
        goals_list = Goal.objects.filter(created_by=current_user).all()

        goals = [
            {f: fields_map[f](g) if f in fields_map else getattr(g, f) for f in fields} for g in goals_list
        ]

        return JsonResponse(data={"goals": goals}, status=200)


@login_required_403
@csrf_exempt
def self_goal_by_id(request, goal_id):
    """
    Get or Update goal by id
    """
    current_user = request.user

    fields_map = {
        'goal_answers': lambda g: [
            {
                'id': answ.id,
                'title': answ.title,
                "created_by": answ.created_by.username,
                "created_at": answ.created_at,
                "file": answ.file.url
            } for answ in g.goal_answers.all()
        ]
    }

    fields = ['title', 'goal_answers', 'id', 'is_achieved']

    goal = Goal.objects.get(pk=goal_id)

    if request.method == 'POST':
        if goal.created_by != current_user:
            raise PermissionDenied("You can edit only your own goals")

        f = GoalForm(data=request.json_body)

        if not f.is_valid():
            return JsonResponse(data={"detail": json.loads(f.errors.as_json())}, status=400)

        goal = f.save(current_user, goal)

    return JsonResponse(
        data={f: fields_map[f](goal) if f in fields_map else getattr(goal, f) for f in fields}, status=200
    )


@login_required_403
@csrf_exempt
@require_http_methods(["POST"])
def add_answer(request):
    """Add goal answer"""
    current_user = request.user

    fields = ["created_by", "title", "created_at", 'id', 'file']

    fields_map = {
        "created_by": lambda a: a.created_by.username,
        "file": lambda a: a.file.url if a.file else ''
    }

    f = GoalAnswerForm(data=request.json_body)

    if not f.is_valid():
        return JsonResponse(data={"detail": json.loads(f.errors.as_json())}, status=400)

    answ = f.save(current_user)

    return JsonResponse(
        data={f: fields_map[f](answ) if f in fields_map else getattr(answ, f) for f in fields}, status=400
    )


@login_required_403
@csrf_exempt
def set_get_answer(request, answer_id):
    """
    Get or Update goal's answer by id
    """
    current_user = request.user

    fields = ["created_by", "title", "created_at", 'id', 'file']

    fields_map = {
        "created_by": lambda a: a.created_by.username,
        "file": lambda a: a.file.url if a.file else ''
    }

    answ = GoalAnswer.objects.get(pk=answer_id)

    if request.method == 'POST':
        f = GoalAnswerForm(data=request.json_body)

        if not f.is_valid():
            return JsonResponse(data={"detail": json.loads(f.errors.as_json())}, status=400)

        answ = f.save(current_user, answ)

        return JsonResponse(
            data={f: fields_map[f](answ) if f in fields_map else getattr(answ, f) for f in fields}, status=400
        )
    else:
        return JsonResponse(
            data={f: fields_map[f](answ) if f in fields_map else getattr(answ, f) for f in fields}, status=400
        )
