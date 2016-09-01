"""
This module contains the models for NXT LVL
"""
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import base64
import re
import os
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from common.util import safeHtmlString
from django.utils.translation import ugettext_lazy as _, get_language, activate
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from NXT.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse


STATUS = (
    ('STATUS_MISSING', 'MISSING'),
    ('STATUS_IN_PROGRESS', 'IN_PROGRESS'),
    ('STATUS_SHOW', 'SHOW')
)

POTENCIALE = (
    ('YES', 'YES'),
    ('NO', 'NO')
)


class UserNxtlvl(AbstractUser):

    def save(self, *args, **kwargs):
        if self.email and self.id is None:
            if get_user_model().objects.filter(email=self.email).count() > 0:
                raise FieldError('User %s already exists' % self.email)
        if self.email and self.id is not None:
            if get_user_model().objects.filter(email=self.email).exclude(id=self.id):
                raise FieldError('User email %s already exists' % self.email)
        return super(UserNxtlvl, self).save(*args, **kwargs)


class CreatedAbstract(models.Model):
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"),
                                   related_name='%(class)s_created_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class UpdatedAbstract(models.Model):
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"),
                                   related_name='%(class)s_updated_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Role(CreatedAbstract, UpdatedAbstract):
    """
    Roles for employee
    """
    name = models.CharField(verbose_name=_(u"name"), max_length=255)
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='role_created_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='role_updated_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')

    def __unicode__(self):
        return self.name[:50]


class EmployeeRole(CreatedAbstract):
    """
    Employee/Role relation
    """
    employee = models.ForeignKey('Employee', verbose_name=_(u"employee"))
    role = models.ForeignKey('Role', verbose_name=_(u"role"))
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='employee_role_created_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'employee role')
        verbose_name_plural = _(u'employee roles')

    def __unicode__(self):
        return u'%s - (%s)' % (self.employee.user.get_full_name(), self.role.name)


class DevelopmentPlanType(models.Model):
    """
    Types of development plan
    """
    name = models.CharField(max_length=255)
    company = models.ForeignKey('Company', verbose_name=_(u'company'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'development plan type')
        verbose_name_plural = _(u'development plan types')


def user_photo_directory_path(object, filename):
    filename = 'logo.{0}'.format(filename.split('.')[-1]) if '.' in filename else 'logo'

    return 'user_{0}/{1}'.format(object.id, filename)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Employee(CreatedAbstract, UpdatedAbstract):
    """
    Employee in a company
    """
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='employee_user', verbose_name=_("user"))
    development_plan_type = models.ForeignKey(DevelopmentPlanType, verbose_name=_("development plan type"), null=True,
                                              blank=True)
    title = models.CharField(verbose_name=_(u"title"), max_length=4000)
    phone = models.CharField(verbose_name=_(u"phone"), max_length=40, default='')
    potenciale = models.CharField(max_length=15, verbose_name=_(u'potenciale'), choices=POTENCIALE, null=True, blank=True)
    manager = models.ForeignKey('self', verbose_name=_(u"manager"), null=True, blank=True)
    is_manager = models.BooleanField(verbose_name=_(u"is manager"), default=False)
    company = models.ForeignKey('Company', verbose_name=_(u"company"))
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='employee_created_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='employee_updated_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    language_code = models.CharField(max_length=15, verbose_name=_(u'language'), choices=settings.LANGUAGES,
                                     default=settings.LANGUAGE_CODE)
    roles = models.ManyToManyField(
        Role,
        through=EmployeeRole)
    notes = models.TextField(null=True, blank=True)
    status_questions = models.CharField(max_length=15, verbose_name=_(u'status_questions'), choices=STATUS,
                                     default='STATUS_MISSING')
    date_of_birth = models.DateTimeField(verbose_name=_(u"date of birth"), blank=True, null=True, default=None)
    photo = models.ImageField(upload_to=user_photo_directory_path, blank=True, storage=OverwriteStorage())

    class Meta:
        verbose_name = _(u'employee')
        verbose_name_plural = _(u'employees')

    def __unicode__(self):
        try:
            username = self.user.username if self.user else ''
        except Exception as e:
            print self.__dict__
            raise
        return username


    def getMyEmployees(self, manager=None):
        """
        Get list of employees with given manager or self as manager
        """
        if manager is None:
            manager = self
        employees = list()
        for employee in self.getMyEmployeesQueryset(manager):
            employees.append(employee)
        return employees

    def getMyEmployeesQueryset(self, manager=None):
        """
        Get queryset of employe with given manager or self as manager
        """
        if manager is None:
            manager = self
        return Employee.objects.filter(manager__pk=manager.pk, company__pk=self.company.pk).order_by('-is_manager',
                                                                                                     'user__last_name',
                                                                                                     'user__first_name')

    def isCompanySuperUserOrHigher(self):
        """
        Is self company super user or higher privileges
        """
        return self.roles.count() > 0

    def isEnsoUser(self):
        """
        Is self enso user
        """
        return self.roles.count() > 0 and self.roles.filter(name=u'Enso-bruger').exists()

    @staticmethod
    def isValidUsername(username):
        """
        Checks the username against nxtlvl rules

        :param username: str
        :return: bool
        """
        r = re.compile('^[a-z0-9_\-\.]+$', re.I)

        return True if r.match(username) else False


class Company(CreatedAbstract, UpdatedAbstract):
    """
    A company (client of NXT LVL)
    """
    name = models.CharField(verbose_name=_(u"name"), max_length=255)
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='company_created_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='company_updated_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'company')
        verbose_name_plural = _(u'companies')

    def __unicode__(self):
        return self.name

    """
        Convert to json serializable dict
        """

    def to_json(self):
        return dict(
            id=self.pk,
            name=self.name
        )

    def getTopManagers(self):
        """
        Get top managers in the company of self
        """
        return Employee.objects.filter(company__pk=self.pk, manager_id=None)

    def toString(self):
        return self.__unicode__()


class Competence(CreatedAbstract, UpdatedAbstract):
    """
    A competence part is a part of the competence
    """
    title = models.CharField(verbose_name=_(u"title"), max_length=400)
    description = models.TextField(verbose_name=_(u"description"))
    # company = models.ForeignKey(Company, verbose_name=_(u"company"), null=True, blank=True, default=None)
    status = models.BooleanField(verbose_name=_(u"status"), default=False)
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='competence_field_created_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='competence_field_updated_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    # development_plan_type = models.ForeignKey(DevelopmentPlanType, verbose_name=_(u'development plan type'))
    language_code = models.CharField(max_length=15, verbose_name=_(u'language'), choices=settings.LANGUAGES,
                                     default=settings.LANGUAGE_CODE)

    # is_manager = models.BooleanField(default=False, verbose_name=_(u'for manager'))  #???????????

    class Meta:
        verbose_name = _(u'competence')
        verbose_name_plural = _(u'competences')


class DevelopmentPlanToEmployeeRelation(CreatedAbstract):
    """
    Relation between user(employee/manager) and development plan
    """
    employee = models.ForeignKey(Employee, verbose_name=_(u"employee"))
    development_plan = models.ForeignKey("DevelopmentPlan", verbose_name=_(u"development_plan"))
    finished_at = models.DateTimeField(verbose_name=_(u"finished at"), null=True, default=None, blank=True)
    is_private = models.BooleanField(verbose_name=_(u"is private"), default=True)
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='development_plan_user_created_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'development plan to user relation')
        verbose_name_plural = _(u'development plan to user relations')


class CompetencePart(CreatedAbstract, UpdatedAbstract):
    """
    A competence part is a subpart of a competence
    """
    title = models.CharField(verbose_name=_(u"title"), max_length=400)
    description = models.TextField(verbose_name=_(u"description"))
    competence = models.ForeignKey(Competence, verbose_name=_(u"competence"),
                                   related_name='competence_part')
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='competence_created_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='competence_updated_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    competence_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'competence_part')
        verbose_name_plural = _(u'competence_parts')


class DevelopmentPlan(CreatedAbstract):
    """
    An employee can only have one active development plan, and several completed
    """
    # owner = models.ForeignKey(Employee, verbose_name=_(u"owner"))
    type = models.ForeignKey(DevelopmentPlanType, verbose_name=_(u'type'), null=True, blank=True)
    language_code = models.CharField(max_length=15, verbose_name=_(u'language'), choices=settings.LANGUAGES,
                                     default=settings.LANGUAGE_CODE)
    manager_relation = models.ForeignKey(
        Employee,
        verbose_name=_(u"manager relation"),
        related_name='development_plan_manager'
    )
    employee_relation = models.ManyToManyField(
        Employee,
        through=DevelopmentPlanToEmployeeRelation,
        verbose_name=_(u"employee relation"),
        related_name='development_plan_employee'
    )
    competence_parts = models.ManyToManyField(
        CompetencePart,
        verbose_name=_(u"competence parts"),
        related_name='development_plan_competence_parts'
    )
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='development_plan_created_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(verbose_name=_('deleted'), default=False)

    class Meta:
        verbose_name = _(u'development plan')
        verbose_name_plural = _(u'development plans')


class ActionStatus(models.Model):
    """
    Possible statuses for an action
    """
    name_da = models.CharField(verbose_name=_(u'name_da'), max_length=30)
    name_en = models.CharField(verbose_name=_(u'name_en'), max_length=30)

    class Meta:
        verbose_name = _(u'action status')
        verbose_name_plural = _(u'action statuses')

    def __unicode__(self):
        if get_language() == 'da':
            return u'%s' % safeHtmlString(self.name_da, 100)
        else:
            return u'%s' % safeHtmlString(self.name_en, 100)

    def __str__(self):
        return self.__unicode__()


TYPE = (
    ('A', 'TYPE_A'),
    ('B', 'TYPE_B'),
    ('C', 'TYPE_C')
)

DIFFICULTY = (
    (1, 'DIFFICULTY_LOW'),
    (2, 'DIFFICULTY_MEDIUM'),
    (3, 'DIFFICULTY_HIGH')
)


class Action(CreatedAbstract, UpdatedAbstract):
    """
    Each employee has a number of action representing their goals
    """
    title = models.TextField(verbose_name=_(u"title"))
    description = models.TextField(verbose_name=_(u"description"), null=True, blank=True)
    status = models.ForeignKey(ActionStatus, verbose_name=_(u"status"), null=True, blank=True, default=5)
    employee = models.ForeignKey(Employee, verbose_name=_(u"employee"))
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='action_created_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='action_updated_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=1, null=True, choices=TYPE)
    difficulty = models.IntegerField(null=True, choices=DIFFICULTY)

    class Meta:
        verbose_name = _(u'action')
        verbose_name_plural = _(u'actions')


class ActionComment(CreatedAbstract, UpdatedAbstract):
    """
    Actions can have comments
    """
    action = models.ForeignKey(Action, verbose_name=_(u'action'), null=True, blank=True, related_name='comments')
    text = models.TextField(verbose_name=_(u"text"))
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='action_comment_created_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='action_comment_updated_by',
    #                                blank=True, null=True, on_delete=models.SET_NULL)
    follow_up_at = models.DateField(verbose_name=_(u"follow up at"), null=True, blank=True, default=None)
    status = models.ForeignKey(ActionStatus, verbose_name=_(u"status"), null=True, blank=True)

    class Meta:
        verbose_name = _(u'action comment')
        verbose_name_plural = _(u'action comments')


class Question(CreatedAbstract, UpdatedAbstract):
    """
    A competence has questions
    """
    title = models.TextField(verbose_name=_(u"text"), null=True)
    # scale = models.PositiveIntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    competence_part = models.ForeignKey('CompetencePart', verbose_name=_(u"competence_part"), blank=True,
                                        null=True)
    # is_achieved = models.BooleanField(default=False)
    # created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"created by"), related_name='question_created_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)
    # updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    # updated_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_(u"updated by"), related_name='question_updated_by', blank=True,
    #                                null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')


class Slider(CreatedAbstract, UpdatedAbstract):
    """
    A competence has slider
    """
    competence_part = models.ForeignKey('CompetencePart', verbose_name=_(u"competence part"),
                                        blank=True, null=True)
    scale = models.PositiveIntegerField(null=True, default=0, validators=[MinValueValidator(0),
                                                                          MaxValueValidator(100)])

    class Meta:
        verbose_name = _(u'slider')
        verbose_name_plural = _(u'sliders')



# class QuestionResponse(models.Model):
#     """
#     A response for a question in chat
#     """
#     employee = models.ForeignKey('Employee', verbose_name=_(u"employee"))
#     question = models.ForeignKey('Question', verbose_name=_(u"question"))
#     created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
#     created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='question_response_created_by',
#                                    blank=True, null=True, on_delete=models.SET_NULL)
#     updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
#     updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='question_response_updated_by',
#                                    blank=True, null=True, on_delete=models.SET_NULL)
#
#     class Meta:
#         verbose_name = _(u'response')
#         verbose_name_plural = _(u'responses')
#
#     def __unicode__(self):
#         return u'%s' % safeHtmlString(self.text, 100)


class FileBytes(models.Model):
    _data = models.TextField(db_column='data', blank=True)

    def set_data(self, data):
        self._data = base64.encodestring(data)

    def get_data(self):
        return base64.decodestring(self._data)

    data = property(get_data, set_data)


class File(CreatedAbstract):
    file_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    file_path = models.FileField(upload_to='temp')
    file = models.ForeignKey(FileBytes, null=True, default=None, blank=True)
    company = models.ForeignKey(Company, related_name='files')
    role = models.ForeignKey(Role, related_name='files', null=True,
                             default=None, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='file_created_by',
    #                                blank=True, null=True,
    #                                on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Fil'
        verbose_name_plural = u'Filer'

    def __unicode__(self):
        return u'%s' % safeHtmlString(self.file_name, 255)

    @staticmethod
    def getMyfiles(user):
        employee = Employee.objects.get(user=user)
        role_ids = employee.roles.values_list('employeerole__role__pk')
        return File.objects.filter(Q(role__pk__in=role_ids) | Q(role__pk=None))

    def canDownload(self, current_user):
        employee = Employee.objects.get(user=current_user)
        role_ids = employee.roles.values_list('employeerole__role__pk', flat=True)
        correct_company = employee.company == self.company
        has_needed_role = self.role is None
        if not has_needed_role:
            for role_id in role_ids:
                has_needed_role = has_needed_role or role_id == self.role.pk
        return correct_company and has_needed_role


def answer_file_dir_path(object, filename):
    return u'goal_answer_{0}/{1}'.format(object.id, filename)


class Answer(CreatedAbstract, UpdatedAbstract):
    """
    A answer for a question in chat
    """
    question = models.ForeignKey('Question', verbose_name=_(u"question"), related_name='answers')
    slider = models.ForeignKey('Slider', verbose_name=_(u"slider"), related_name='sliders')
    employee = models.ForeignKey('Employee', verbose_name=_(u"employee"))
    title = models.TextField(verbose_name=_(u"text"), null=True)

    class Meta:
        verbose_name = _(u'answer')
        verbose_name_plural = _(u'answers')


class Goal(CreatedAbstract, UpdatedAbstract):
    """
    Goal for yourself
    """
    title = models.TextField(verbose_name=_(u"text"), null=True)
    is_achieved = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'goal')
        verbose_name_plural = _(u'goals')


class GoalAnswer(CreatedAbstract, UpdatedAbstract):
    """
    A answer for a goal
    """
    goal = models.ForeignKey(Goal, verbose_name=_(u"goal"), related_name='goal_answers')
    title = models.TextField(verbose_name=_(u"text"), null=True)
    file = models.FileField(
        verbose_name=_(u"answer_file"), upload_to=answer_file_dir_path, blank=True, storage=OverwriteStorage()
    )

    class Meta:
        verbose_name = _(u'goal answer')
        verbose_name_plural = _(u'goal answers')


# class Chat(models.Model):
#     """
#     A answer for a question in chat line
#     """
#     answer = models.ForeignKey('Answer', verbose_name=_(u"answer"))
#     question = models.ForeignKey('QuestionResponse', verbose_name=_(u"question response"))
#
#     class Meta:
#         verbose_name = _(u'chat')
#         verbose_name_plural = _(u'chats')
#

# class Chat(models.Model):
#     """
#     A chat line for a competence in chat
#     """
#     chat_line = models.ForeignKey('ChatLine', verbose_name=_(u"chat line"))
#
#     class Meta:
#         verbose_name = _(u'chat')
#         verbose_name_plural = _(u'chats')