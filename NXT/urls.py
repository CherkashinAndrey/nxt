"""NXT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from ensomus.views import (
    add_employee, employee_detail, update_employee,
    employee_delete_file, login_user, profile_detail,
    employees_json, create_employee, edit_employee, all_employees, create_many_employees,
    get_manager_employees, employees_manager, employees_json_id,
    action_list, action_detail, action_add, action_edit, create_competence_in_db,
    dashboard, start_view, change_company, accesscode, password_reset,
    password_reset_done, logout_user, upload_photo, upload_many_employee,
    create_leader_model, employee_download_file, #development_plan_answers,
    create_development_plan, development_plan_details,
    get_all_user_development_plans_for_manager, get_active_development_plan_for_user,
    get_all_development_plans_for_user, self_goal, files, get_file, self_goal_by_id, add_answer,
    set_get_answer, all_competence_list
)


from ensomus.views import action_list, action_detail, action_add, action_edit, create_competence_in_db
from ensomus.views import dashboard, start_view, change_company, accesscode, password_reset, \
    password_reset_done, logout_user, upload_photo, upload_many_employee
from ensomus.views import create_leader_model, employee_download_file

from ensomus.views import create_development_plan, development_plan_details, \
    get_all_user_development_plans_for_manager, get_active_development_plan_for_user,\
    get_all_development_plans_for_user



urlpatterns = [
    # url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^pages/', include('django.contrib.flatpages.urls')),
    # url(r'^home/$', 'ensomeus.views.home', name='home'),
    url(r'^write_in_db/$', create_competence_in_db),

    # url(r'^clone$', clone_competencefields),
    url(r'^accesscode/(?P<code>\w+)$', accesscode),
    url(r'^employee/all/$', all_employees),
    url(r'^employee/all/(?P<company_id>\d+)$', all_employees),
    url(r'^employee/changecompany$', change_company),
    url(r'^employee/add/$', add_employee),  # *********************
    url(r'^employee/json/$', employees_json),
    url(r'^employee/json_id/(?P<employee_id>\d+)/$', employees_json_id),
    url(r'^employee/manager/$', employees_manager),
    url(r'^employee/create/(?P<company_id>\d+)$', create_employee),  # *********************
    url(r'^employee/create-many/(?P<company_id>\d+)$', create_many_employees),
    url(r'^employee/edit/(?P<employee_id>\d+)/$', edit_employee),  # *********************
    # url(r'^employee/attach/(?P<company_id>\d+)$', attach_development_plan),
    url(r'^employee/update/(?P<employee_id>\d+)/$', update_employee, name='update_employee'),  # *********************
    url(r'^employee/show/(?P<employee_id>\d+)/$', employee_detail, name='employee_detail'),
    url(r'^employees/all/$', get_manager_employees),

    url(r'^profile/show/(?P<employee_id>\d+)/$', profile_detail, name='profile_detail'), # *********************
    url(r'^employee/createleadermodel/(?P<company_id>\d+)$', create_leader_model),
    url(r'^employee/download-file/(?P<employee_id>\d+)/(?P<filename>.+)$', employee_download_file,
        name="employee_download_file"),
    url(r'^employee/delete-file/(?P<employee_id>\d+)/(?P<filename>.+)$', employee_delete_file,
        name="employee_delete_file"),
    url(r'^action/list/(?P<employee_id>\d+)$', action_list),
    url(r'^action/all$', action_list),
    url(r'^action/(?P<action_id>\d+)$', action_detail),
    url(r'^action/edit/(?P<action_id>\d+)$', action_edit),
    url(r'^action/add/(?P<employee_id>\d+)$', action_add),
    url(r'^dashboard$', dashboard),
    url(r'^files/$', files),
    url(r'^files/get/(?P<file_id>\d+)/$', get_file),
    url(r'^accounts/profile/$', start_view),
    # url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^login$', login_user, name='login'),
    url(r'^logout/$', logout_user, {'next_page': '/'}),
    url(r'^password_reset/$', password_reset),
    url(r'^password_reset_done/$', password_reset_done),

    url(r'^all_competence/$', all_competence_list),
    url(r'^development_plan/create/$', create_development_plan),
    url(r'^development_plan/(?P<development_plan_id>\d+)/$', development_plan_details),
    url(r'^employee_all_development_plans/$', get_all_development_plans_for_user),
    url(r'^employee_active_development_plan/$', get_active_development_plan_for_user),
    url(r'^all_user_development_plans_for_manager/(?P<employee_id>\d+)/', get_all_user_development_plans_for_manager), ###
    # url(r'^employee_development_plan/(?P<company_id>\d+)$', get_user_development_plan),
    url(r'^upload_photo/(?P<employee_id>\d+)/', upload_photo),
    url(r'^add_many_employee/(?P<company_id>\d+)/', upload_many_employee),
    url(r'^goal/$', self_goal),  # add goal or return all goals for current employee
    url(r'^goal/(?P<goal_id>\d+)/$', self_goal_by_id),  # update goal or get by id
    url(r'^answer/$', add_answer),  # add goal answer
    url(r'^answer/(?P<answer_id>\d+)/$', set_get_answer),  # update get goal answer by id

    # url(r'^active_development_plan_answers/(?P<development_plan_id>\d+)/$', development_plan_answers),

]
