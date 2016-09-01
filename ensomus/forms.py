"""
Forms for NXT LVL
"""
from django import forms
# from django_mailer_plus import send_mail
from django.core.mail import send_mail
from tasks import send_emails
from models import (
    Employee, Competence, CompetencePart, Action, ActionComment, Company,
    UserNxtlvl, Role, EmployeeRole, DevelopmentPlanType, DevelopmentPlan,
    DevelopmentPlanToEmployeeRelation, Question, Answer, Goal, GoalAnswer
)
# from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.template import loader, Context
from django.forms.formsets import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db.models import Q
import widgets
from django.utils.html import strip_tags
from common.util import my_encrypt, generate_password, logUnauthorizedAccess
import os
from django.utils.timezone import now, utc
from datetime import date, datetime, time
import logging
import common.util as util
from threadlocals.threadlocals import get_current_request
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from models import STATUS, POTENCIALE
import tempfile
from django.core.files import File
import base64
import StringIO
import csv
from django.core.validators import validate_email

from django.forms.models import model_to_dict


logger = logging.getLogger(__name__)


class PasswordResetForm(forms.Form):
    """
    Form to reset password and send the new password by mail
    """
    email = forms.EmailField(label=_("Email"))

    def save(self):
        employee = Employee.objects.get(user__email__exact=self.cleaned_data['email'])
        # mail_from = 'kharenko.send.mail@gmail.com'
        # subject = _("NXT LVL: new password")
        password = generate_password(8)
        print password
        employee.user.set_password(password)
        employee.user.save()
        email_subject = 'Next level'
        email_body = 'NXT LVL: new password: {}'.format(password)
        sender = settings.DEFAULT_FROM_EMAIL
        recipients = ['{}'.format(employee.user.email)]
        send_emails.delay(recipients, email_subject, email_body, sender)


        # send_mail('Next level', 'NXT LVL: new password: {}'.format(password),
        #           'kharenko.send.mail@gmail.com', ['{}'.format(employee.user.email)], fail_silently=True)

        # template = loader.get_template('mus/emails/reset_password_%s.html' % employee.language_code)
        # htmlbody = template.render(
        #     Context({
        #         'user': employee.user,
        #         'access_code': employee.getAccessCode(),
        #         'newpassword': password
        #     })
        # )
        # try:
        #     send_mail(
        #         subject,
        #         # strip_tags(htmlbody),
        #         "new password {}".format(password),
        #         mail_from,
        #         'kharenko.send.mail@gmail.com',
        #         (employee.user.email,),
        #         # html_message=htmlbody,
        #         html_message="new password {}".format(password)
        #     )
        # except Exception, ex:
        #     print ex

    def clean(self):
        super(PasswordResetForm, self).clean()
        print "EMAIL:", self.cleaned_data
        if not 'email' in self.cleaned_data or not get_user_model().objects.filter(
                email__exact=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('Unknown email'))
        return self.cleaned_data


class EmployeeForm(forms.Form):
    """
    Create employee form
    """
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=True, widget=forms.HiddenInput())
    first_name = forms.CharField(label=_(u'First name'), max_length=100,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(label=_(u'Last name'), max_length=100,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label=_(u'Email'), widget=forms.TextInput(attrs={'class': "form-control"}))
    language_code = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES,
                                      widget=forms.Select(attrs={'class': "form-control"}))
    manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True),
                                     empty_label=_("choose manager"), required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))
    is_manager = forms.BooleanField(required=False, label=_('Create as manager'))
    title = forms.CharField(label=_(u'Title'), max_length=4000,
                            widget=forms.TextInput(attrs={'class': "form-control"}), required=False)

    def __init__(self, request, *args, **kwargs):
        import json
        self.request = request
        self.user = get_user_model().objects.get(pk=request.user.pk)
        # self.data = json.loads(self.request.body)

        super(EmployeeForm, self).__init__(*args, **kwargs)

    def save(self):
        """
        Save form and send welcome mail (currently disabled)
        """

        employee = Employee.objects.get(user__pk=self.user.pk)  ###!!!!!!!!!!
        data = self.data
        employee_manager = Employee.objects.get(pk=data['manager'])
        man_list = []
        from views import found_all_managers
        manager_list = list(Employee.objects.filter(manager=employee, is_manager=True))
        if employee.is_manager == True:
            manager_list.append(employee)
        if len(manager_list) > 0:
            result_list = manager_list
            all_managers_list = found_all_managers(manager_list, result_list)
        else:
            raise forms.ValidationError(_('"error": "this employee have not any manager"'))
        employees = list()
        for manager in all_managers_list:
            manager_dict = model_to_dict(manager)

            for k in ['first_name', 'last_name', 'email']:
                manager_dict[k] = getattr(manager.user, k)

            manager_dict['photo'] = manager.photo.url if manager.photo else ''
            employees.append(manager_dict)
        for i in employees:
            man_list.append(i['email'])
        man_list.append(employee.user.email)
        if employee_manager.user.email not in man_list:
            raise forms.ValidationError(_('you can not given manager with id={}, changed manager'
                                          .format(data['manager'])))

        # if not employee.isEnsoUser():
        #     if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
        #         logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 1", self.request)
        #         raise PermissionDenied()
        #     if self.cleaned_data.get('is_manager') and not employee.isCompanySuperUserOrHigher()\
        #             and not employee.id == employee_parent.manager_id:
        #         logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 2", self.request)
        #         raise PermissionDenied()
            # if self.cleaned_data.get('company') != employee.company:
            #     logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 3", self.request)
            #     raise PermissionDenied()

        password = generate_password(8)
        user_model = get_user_model()
        users = user_model.objects.filter(email=data.get('email')).all()
        if users:
            raise SuspiciousOperation("A user with the given username/email already exists", 400)
        user = user_model.objects.create_user(
            # username=self.cleaned_data.get('user_name'),
            username=data.get('email'),
            email=data.get('email'),
            password=password
        )
        # user.username = self.cleaned_data.get('first_name')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.save()
        id = int(data.get('manager'))
        manager = Employee.objects.get(id=id)

        Employee.objects.create(
            user=user,
            manager=manager,
            is_manager=data.get('is_manager'),
            company=manager.company,
            created_by=self.user,
            updated_by=self.user,
            # development_plan_type=self.cleaned_data.get('development_plan_type'),
            language_code=data.get('language_code'),
            # plaintext_password=my_encrypt(password)
            title=data.get('title'),
        )
        email_subject = 'Next level'
        email_body = 'Created a new user: {}, your email: {}, your password: {}.' \
                     'To register please go to http://nxtlvl-dev.chisw.us/login'\
            .format(user.username, user.email, password)
        sender = settings.DEFAULT_FROM_EMAIL
        recipients = ['{}'.format(user.email)]
        send_emails.delay(recipients, email_subject, email_body, sender)


    def _sendWelcomeMail(self, user, password):
        """
        Send welcome mail to user
        """
        template = loader.get_template('create_user_mail.tpl')
        send_mail(
            settings.WELCOME_MAIL_SUBJECT,
            template.render(
                Context({
                    'user': user,
                    'password': password,
                    'url': self.request.build_absolute_uri('/login/'),
                    'sender': self.user
                })
            ),
            self.user.email,
            [user.email]
        )


    def clean(self):
        """
        Do validation
        """
        super(EmployeeForm, self).clean()

        username = self.cleaned_data.get('first_name')

        if username:

            if not Employee.isValidUsername(username):
                raise forms.ValidationError(_(
                    'Invalid username format. Accepted characters are A-Z,a-z,0-9,_-,.'
                ))

            if get_user_model().objects.filter(username__exact=username).exists():
                raise forms.ValidationError(_('A user with the given username already exists'))

        email = self.cleaned_data.get('email')
        # confirm_email = self.cleaned_data.get('confirm_email')
        # if not email == confirm_email:
        #     raise forms.ValidationError(_('The emails are not equal'))
        if UserNxtlvl.objects.filter(email__exact=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError(_('A user with the given email already exists'))
        return self.cleaned_data


class EditEmployeeForm(forms.Form):
    """
    Edit employee form
    """
    first_name = forms.CharField(label=_(u'First name'), max_length=100,
                                 widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(label=_(u'Last name'), max_length=100,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label=_(u'Email'), widget=forms.TextInput(attrs={'class': "form-control"}))
    language_code = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES,
                                      widget=forms.Select(attrs={'class': "form-control"}), required=False)
    # development_plan_type = forms.ModelChoiceField(label=_('Type'), queryset=DevelopmentPlanType.objects.all(),
    #                                                empty_label=_('choose type'),
    #                                                widget=forms.Select(attrs={'class': "form-control"}))
    old_password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': "form-control"}),
                                   required=False)
    password = forms.CharField(label=_('New password'), widget=forms.PasswordInput(attrs={'class': "form-control"}),
                               required=False)
    confirm_password = forms.CharField(label=_('Repeat password'),
                                       widget=forms.PasswordInput(attrs={'class': "form-control"}), required=False)
    manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True),
                                     empty_label=_("choose manager"), required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))
    is_manager = forms.BooleanField(required=False, label='Leder')
    roles = forms.ModelMultipleChoiceField(label=_('Roles'), queryset=Role.objects.all(),
                                     required=False, widget=forms.SelectMultiple(attrs={'class': "form-control"}))
    status_questions = forms.ChoiceField(label=_('Manager'), choices=STATUS, required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))
    phone = forms.CharField(label=_(u'Phone'), max_length=40,
                                 widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    potenciale = forms.ChoiceField(label=_('Potenciale'), choices=POTENCIALE, required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))
    notes = forms.CharField(label=_(u'Notes'), max_length=4000,
                                 widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    company = forms.ModelChoiceField(label=_('Company'), queryset=Company.objects.all(), required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))
    title = forms.CharField(label=_(u'Title'), max_length=4000,
                            widget=forms.TextInput(attrs={'class': "form-control"}), required=False)

    def __init__(self, user, employee, *args, **kwargs):
        self.user = user
        self.employee = employee
        self.current_employee = Employee.objects.get(user__pk=self.user.pk)
        super(EditEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['manager'].initial = self.employee.manager
        if not self.current_employee.isCompanySuperUserOrHigher():
            # del self.fields['is_manager']
            del self.fields['manager']
            # del self.fields['development_plan_type']

    def save(self):
        """
        Save form
        """
        if not self.current_employee.isCompanySuperUserOrHigher() and not self.user.pk == self.employee.user.pk \
                and not self.user.pk == self.employee.manager.user.pk \
                and not self.user.pk == self.employee.created_by_id:
            raise PermissionDenied()
        self.employee.user.first_name = self.cleaned_data.get('first_name')
        self.employee.user.last_name = self.cleaned_data.get('last_name')
        self.employee.user.email = self.cleaned_data.get('email')
        if not self.cleaned_data.get('password') is None and len(self.cleaned_data.get('password')) > 5:
            self.employee.user.set_password(self.cleaned_data.get('password'))
            self.employee.plaintext_password = my_encrypt(self.cleaned_data.get('password'))
        if self.current_employee.isCompanySuperUserOrHigher():
            # self.employee.development_plan_type = self.cleaned_data.get('development_plan_type')
            if not self.cleaned_data.get('manager') is None:
                manager = self.cleaned_data.get('manager')

                self.employee.manager = manager

            self.employee.is_manager = self.cleaned_data.get('is_manager')
        self.employee.language_code = self.cleaned_data.get('language_code')

        self.employee.roles.clear()
        for role in self.cleaned_data.get('roles', []):
            EmployeeRole.objects.create(
                employee=self.employee,
                role=role,
                created_by=self.user
            )
        # self.employee.roles.name = self.cleaned_data.get('roles')
        self.employee.potenciale = self.cleaned_data.get('potenciale')
        self.employee.phone = self.cleaned_data.get('phone')
        self.employee.status_questions = self.cleaned_data.get('status_questions')
        self.employee.notes = self.cleaned_data.get('notes')
        self.employee.title = self.cleaned_data.get('title')
        self.employee.company = self.cleaned_data.get('company')
        self.employee.is_manager = self.cleaned_data.get('is_manager')
        self.employee.user.save()
        self.employee.save()


    def clean(self):
        """
        Validate
        """
        print self.cleaned_data
        password = self.cleaned_data.get('password', None)
        confirm_password = self.cleaned_data.get('confirm_password', None)
        if not password == confirm_password:
            raise forms.ValidationError(_(u'The passwords are not equal'))
        old_password = self.cleaned_data.get('old_password', None)
        if not len(password) == 0 and not self.user.check_password(old_password):
            raise forms.ValidationError(_('Wrong password given'))
        if not len(old_password) == 0 and not len(password) > 5:
            raise forms.ValidationError(_(u'The password need to have be at least 6 characters'))
        if UserNxtlvl.objects.filter(email__exact=self.cleaned_data.get('email')).exclude(pk=self.employee.user.pk).exists():
            raise forms.ValidationError(_(u'A user with the given email already exists'))
        return self.cleaned_data


# class AttachMUSForm(forms.Form):
#     """
#     Form to attach development plan to employees
#     """
#     email_text = forms.CharField(required=False,
#                                  widget=forms.Textarea(attrs={'placeholder': _("Add a personal message (optional)")}))
#     template = forms.ChoiceField(label=_("Template"), choices=settings.LANGUAGES,
#                                  widget=forms.Select(attrs={'class': "form-control"}))
#     employees = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=Employee.objects.all())
#     competence_parts = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,
#                                                        queryset=CompetenceField.objects.filter(is_system=False,
#                                                                                                parent=None))


class ActionForm(forms.ModelForm):
    """
    Model form for action
    """


    # difficulty = forms.ChoiceField(label=_("Difficulty"), choices=Action.difficulty(),
    #                                widget=forms.Select(attrs={'class': "form-control"}))
    # type = forms.ChoiceField(label=_("Type"), choices=Action.type(),
    #                          widget=forms.Select(attrs={'class': "form-control"}))

    class Meta:
        model = Action
        fields = ['title', 'description', 'difficulty', 'type']

    def save(self, current_user, employee, *args, **kwargs):
        """
        Save form
        """
        self.instance.sort_order = 1
        if not self.instance.pk:
            self.instance.created_by = current_user
            self.instance.employee = employee
        self.instance.updated_by = current_user
        action = super(ActionForm, self).save(*args, **kwargs)
        action.save()
        action.send_approval_notification()


DATE_INPUT_FORMATS = ['%Y-%m-%d',  # '2006-10-25'
                      '%m/%d/%Y',  # '10/25/2006'
                      '%d-%m-%Y',  # '10/25/2006'
                      '%m/%d/%y']  # '10/25/06'


class ActionCommentForm(forms.ModelForm):
    """
    Form for action comment
    """
    follow_up_at = forms.DateField(required=False, input_formats=DATE_INPUT_FORMATS,
                                   widget=forms.DateInput(attrs={'class': 'form-control'}))
    # reminder_at = forms.DateField(required=False, input_formats=DATE_INPUT_FORMATS,
    #                               widget=forms.DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ActionComment
        fields = ['status', 'text', 'follow_up_at'] #, 'reminder_at'
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, current_user, action, *args, **kwargs):
        """
        Save form
        """
        if not self.instance.pk:
            self.instance.created_by = current_user
        self.instance.updated_by = current_user
        self.instance.action = action
        action.follow_up_at = self.instance.follow_up_at
        if self.instance.status:
            action.status = self.instance.status
        action.save()
        action_comment = super(ActionCommentForm, self).save(*args, **kwargs)
        action_comment.save()

        if action.employee.user == current_user:
            self.instance.sendCommentNotification(1, action.employee.manager.user, current_user)
        else:
            self.instance.sendCommentNotification(2, action.employee.user, current_user)

        # if self.cleaned_data['reminder_at']:
        #
        #     at = time(0, 0, 0, 0, tzinfo=utc)
        #     follow_up_at = None
        #
        #     if 'follow_up_at' in self.cleaned_data:
        #         follow_up_at = datetime.combine(self.cleaned_data['follow_up_at'], at)
        #
        #     Reminder.create(
        #         ReminderTemplate.ID_CONTRIBUTION_KEY,
        #         send_date=datetime.combine(self.cleaned_data['reminder_at'], at),
        #         date=follow_up_at,
        #         comment=self.cleaned_data['text'],
        #         created_by=current_user
        #     )


class UploadEmployeesForm(forms.Form):
    """
    Form for uploading csv file to create manye employee
    """
    file = forms.FileField()

    def clean(self):

        if not 'file' in self.cleaned_data:
            raise forms.ValidationError("Missing file")

        filename = self.cleaned_data['file'].name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in ['.csv']:
            raise forms.ValidationError("Not allowed filetype!")


def validate_uniqueemail(value):
    """
    Make sure email doesn't already exist
    """
    if UserNxtlvl.objects.filter(email__exact=value).exists():
        raise forms.ValidationError(_(u'An user with the given email already exists'))


def validate_uniqueusername(value):
    """
    Make sure username doesn't already exist
    """
    if UserNxtlvl.objects.filter(username__exact=value).exists():
        raise forms.ValidationError(_(u'An user with the given username already exists'))


class EmployeeRowForm(forms.Form):
    """
    Form for each line in create many employees
    """
    first_name = forms.CharField(label=_(u'First name'))
    last_name = forms.CharField(label=_(u'Last name'))
    username = forms.CharField(label=_(u'Username'), validators=[validate_uniqueusername])
    email = forms.EmailField(label=_(u'Email'), validators=[validate_uniqueemail])
    language_code = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES,
                                      widget=forms.Select(attrs={'class': "form-control"}))
    # development_plan_type = forms.ModelChoiceField(label=_('Type'), initial=1,
    #                                                queryset=DevelopmentPlanType.objects.all(),
    #                                                empty_label=_('choose type'),
    #                                                widget=forms.Select(attrs={'class': "form-control"}))
    is_manager = forms.BooleanField(label=_(u'Is manager'), initial=False, required=False)

    def save(self, current_user, company):
        """
        Save form
        """
        employee = current_user.employee_user.first()
        if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
            raise PermissionDenied()
        if company != employee.company and not employee.isEnsoUser():
            raise PermissionDenied()
        password = generate_password(8)
        user = UserNxtlvl.objects.create_user(
            username=self.cleaned_data.get('username').strip(),
            email=self.cleaned_data.get('email'),
            password=password
        )
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return Employee.objects.create(
            user=user,
            manager=None,
            is_manager=self.cleaned_data.get('is_manager'),
            company=company,
            created_by=current_user,
            updated_by=current_user,
            # development_plan_type=self.cleaned_data.get('development_plan_type'),
            language_code=self.cleaned_data.get('language_code'),
            plaintext_password=my_encrypt(password)
        )

    def clean(self):
        if any(self.errors):
            return

        username = self.cleaned_data['username'].strip()

        if username:

            if not Employee.isValidUsername(username):
                raise forms.ValidationError(_(
                    'Invalid username format. Accepted characters are A-Z,a-z,0-9,_-,.'
                ))

            if get_user_model().objects.filter(username__exact=username).exists():
                raise forms.ValidationError(_('A user with the given username already exists'))

        return self.cleaned_data


class EmployeeManagerRowForm(forms.Form):
    """
    Form for setting manager for each employee in create many employees
    """
    employee = forms.ModelChoiceField(label=_('Employee'), queryset=Employee.objects.filter(), required=True,
                                      widget=widgets.PlainTextWidget(model=Employee))
    manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True),
                                     empty_label=_("choose manager"), required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))

    def save(self, current_user):
        """
        Save form
        """
        employee = current_user.employee_user.first()
        if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
            raise PermissionDenied()
        employee = self.cleaned_data.get('employee')
        employee.manager = self.cleaned_data.get('manager')
        employee.save()


EmployeeManagerRowFormSet = formset_factory(EmployeeManagerRowForm, extra=0)


class BaseEmployeeRowFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseEmployeeRowFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        if any(self.errors):
            return
        return self.cleaned_data


EmployeeRowFormSet = formset_factory(EmployeeRowForm, extra=0, formset=BaseEmployeeRowFormSet)


class ChangeCompanyForm(forms.Form):
    """
    Form to change company
    """
    company = forms.ModelChoiceField(label=_('company'), queryset=Company.objects.all(), required=True,
                                     widget=forms.Select(attrs={'class': "form-control"}))


class EmployeeNoteForm(forms.ModelForm):
    """
    Model form for EmployeeNoteForm
    """

    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'col-md-10'}),
        label=_(u'Notes')
    )

    class Meta:
        model = Employee
        fields = ['notes']

    def save(self, current_user, employee, *args, **kwargs):
        """
        Save form
        """

        empl = super(EmployeeNoteForm, self).save(*args, **kwargs)
        empl.save()


class MultiLeaderModelForm(forms.Form):
    """
    Form to create a leader model for multiple employees
    """
    employees = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple, queryset=Employee.objects.all()
    )


class UploadFileToEmployeyForm(forms.Form):
    """
    Form for uploading files to an employee
    """
    file = forms.FileField()

    def __init__(self, post=None, files=None):
        forms.Form.__init__(self, post, files)
        self.upload_status = 'OK' if 'upload_status' in get_current_request().GET else ''

    def clean_file(self):

        filename = self.cleaned_data.get('file').name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in ['.png', '.jpg', '.doc', '.pdf']:
            raise forms.ValidationError("Not an allowed filetype!")

    def handle_upload(self, employee_id, f):

        user_dir = util.get_user_files_dir(employee_id)

        with open(os.path.join(user_dir, f.name), 'wb+') as dst:
            for chunk in f.chunks():
                dst.write(chunk)


IMG_EXT_CHOICES = (
    ('jpg', 'jpg format'),
    ('png', 'png format'),
    ('jpeg', 'jpeg format')
)


class UploadEmployeePhotoForm(forms.Form):
    photo = forms.CharField()
    extension = forms.ChoiceField(choices=IMG_EXT_CHOICES)

    def save(self, employee_obj):
        self.cleaned_data['photo'] = base64.b64decode(self.cleaned_data['photo'])

        with tempfile.NamedTemporaryFile(mode='wrb') as f:
            f.write(self.cleaned_data['photo'])
            file_to_save = File(f)

            employee_obj.photo.save(
                '.'.join(['logo', self.cleaned_data['extension']]), file_to_save, save=True
            )


class DevelopmentPlanToEmployeeRelationForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)
    development_plan = forms.ModelChoiceField(queryset=DevelopmentPlan.objects.all(), required=False)
    finished_at = forms.DateTimeField(label="Finished at", widget=forms.DateInput(),
                input_formats = ('%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%Y-%m-%d'),
                required=False)
    is_private = forms.BooleanField(required=False, label=_(u"is private"))

    class Meta:
        model = DevelopmentPlanToEmployeeRelation
        fields = ['finished_at', 'is_private', 'employee', 'development_plan',]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(DevelopmentPlanToEmployeeRelationForm, self).__init__(*args, **kwargs)


    def save(self, current_user, development_plan):
        data = self.data
        finished_at = data.get("finished_at")
        is_private = data.get("is_private")
        user_nxtlvl = get_user_model().objects.get(pk=self.request.user.pk)
        return DevelopmentPlanToEmployeeRelation.objects.create(employee=current_user,    #!!!!!!!!!!!!!!!!!!!!!!!!!
                                              development_plan=development_plan,
                                              finished_at=finished_at,
                                              is_private=is_private,
                                              created_by=user_nxtlvl,)


class DevelopmentPlanForm(forms.Form):
    """
    Create Development Plan form
    """
    type = forms.ModelChoiceField(queryset=DevelopmentPlanType.objects.all(), required=True,
                                  widget=forms.HiddenInput())
    language_code = forms.ChoiceField(label=_("Language"), choices=settings.LANGUAGES,
                                  widget=forms.Select(attrs={'class': "form-control"}))
    # manager_relation = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.all(),  ### ???????????
    #                               empty_label=_("choose manager"), required=True,
    #                               widget=forms.HiddenInput())
    # employee_relation =
    # competence_parts =
    deleted = forms.BooleanField(required=False, label=_('Deleted'))
    last_name = forms.CharField(label=_(u'Last name'), max_length=100,
                                widget=forms.TextInput(attrs={'class': "form-control"}))
    manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True),
                                     empty_label=_("choose manager"), required=False,
                                     widget=forms.Select(attrs={'class': "form-control"}))

    class Meta:
        model = DevelopmentPlan
        exclude = ('competence_parts',) #'employee_relation',


    def __init__(self, request, *args, **kwargs):
        import json
        self.request = request
    #     # self.data = json.loads(self.request)
    #     self.data = self.request
        super(DevelopmentPlanForm, self).__init__(*args, **kwargs)


    def save(self, employee=None, manager=None,  dev_plan=None,
             plan_to_employee_rel=None, competence_part_object=None):
        data = self.data
        language_code = data.get('language_code')
        user_nxtlvl = get_user_model().objects.get(pk=self.request.user.pk)
        if not dev_plan:
            return DevelopmentPlan.objects.create(manager_relation=manager,
                                                  language_code=language_code,
                                                  created_by=user_nxtlvl,)

        if dev_plan and competence_part_object:
            return dev_plan.competence_parts.add(competence_part_object)

        if dev_plan and plan_to_employee_rel:
            dev_plan.employee_relation.employee = employee
            return dev_plan.save()
        # email_subject = 'Next level'
        # email_body = 'Created a new Development Plan: {}'.format(dev_plan.)
        # sender = settings.DEFAULT_FROM_EMAIL
        # recipients = ['{}'.format(user.email)]
        # send_emails.delay(recipients, email_subject, email_body, sender)


        # if dev_plan and plan_to_competence_parts:
        #     dev_plan.plan_to_competence_parts = competence_part
        #     return dev_plan.save()




    # def save(self):
    #     """
    #     Save form and send welcome mail (currently disabled)
    #     """
    #     employee = Employee.objects.get(user__pk=self.user.pk)  ###!!!!!!!!!!
    #     # import json
    #     data = self.data
    #
    #     if not employee.isEnsoUser():
    #         if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
    #             logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 1", self.request)
    #             raise PermissionDenied()
    #         if self.cleaned_data.get('is_manager') and not employee.isCompanySuperUserOrHigher():
    #             logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 2", self.request)
    #             raise PermissionDenied()
    #         # if self.cleaned_data.get('company') != employee.company:
    #         #     logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 3", self.request)
    #         #     raise PermissionDenied()
    #
    #     password = generate_password(8)
    #     user_model = get_user_model()
    #     users = user_model.objects.filter(email=data.get('email')).all()
    #     if users:
    #         raise SuspiciousOperation("A user with the given username/email already exists", 400)
    #     user = user_model.objects.create_user(
    #         # username=self.cleaned_data.get('user_name'),
    #         username=data.get('email'),
    #         email=data.get('email'),
    #         password=password
    #     )
    #     # user.username = self.cleaned_data.get('first_name')
    #     user.first_name = data.get('first_name')
    #     user.last_name = data.get('last_name')
    #     user.save()
    #     id = int(data.get('manager'))
    #     manager = Employee.objects.get(id=id)
    #     Employee.objects.create(
    #         user=user,
    #         manager=manager,
    #         is_manager=data.get('is_manager'),
    #         company=manager.company,
    #         created_by=self.user,
    #         updated_by=self.user,
    #         # development_plan_type=self.cleaned_data.get('development_plan_type'),
    #         language_code=data.get('language_code')
    #         # plaintext_password=my_encrypt(password)
    #     )
    #     aaa = self.cleaned_data.get('password')
    #     from django.core.mail import send_mail
    #     send_mail('Next level', 'Created a new user: {}, your email: {}, your password: {}.'
    #                             'To register please go to http://nxtlvl-dev.chisw.us/login'
    #               .format(user.username, user.email, password),
    #               'kharenko.send.mail@gmail.com', ['{}'.format(user.email)], fail_silently=True)
    #     print(aaa)
    #     # self._sendWelcomeMail(user, self.cleaned_data.get('password'))
    #
    # def _sendWelcomeMail(self, user, password):
    #     """
    #     Send welcome mail to user
    #     """
    #     template = loader.get_template('create_user_mail.tpl')
    #     send_mail(
    #         settings.WELCOME_MAIL_SUBJECT,
    #         template.render(
    #             Context({
    #                 'user': user,
    #                 'password': password,
    #                 'url': self.request.build_absolute_uri('/login/'),
    #                 'sender': self.user
    #             })
    #         ),
    #         self.user.email,
    #         [user.email]
    #     )
    #
    #
    # def clean(self):
    #     """
    #     Do validation
    #     """
    #     super(EmployeeForm, self).clean()
    #
    #     username = self.cleaned_data.get('first_name')
    #
    #     if username:
    #
    #         if not Employee.isValidUsername(username):
    #             raise forms.ValidationError(_(
    #                 'Invalid username format. Accepted characters are A-Z,a-z,0-9,_-,.'
    #             ))
    #
    #         if get_user_model().objects.filter(username__exact=username).exists():
    #             raise forms.ValidationError(_('A user with the given username already exists'))
    #
    #     email = self.cleaned_data.get('email')
    #     # confirm_email = self.cleaned_data.get('confirm_email')
    #     # if not email == confirm_email:
    #     #     raise forms.ValidationError(_('The emails are not equal'))
    #     if UserNxtlvl.objects.filter(email__exact=self.cleaned_data.get('email')).exists():
    #         raise forms.ValidationError(_('A user with the given email already exists'))
    #     return self.cleaned_data

class UploadManyForm(forms.Form):
    employee_file = forms.CharField()

    def __init__(self, employee, *args, **kwargs):
        self.employee = employee
        # self.manager_employee = Employee.objects.filter(manager=self.employee.pk).all()

        super(UploadManyForm, self).__init__(*args, **kwargs)


    def save(self, company, request):
        """
        Save form
        """
        for data in self.cleaned_data['employee_file']:
            manager_email = Employee.objects.get(user__email=data.get('manager')).id
            manager = Employee.objects.get(pk=manager_email)
            if not self.employee.isEnsoUser():
                if not self.employee.is_manager and not self.employee.isCompanySuperUserOrHigher():
                    logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 1", self.request)
                    raise PermissionDenied()
                if self.cleaned_data.get('is_manager') and not self.employee.isCompanySuperUserOrHigher():
                    logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 2", self.request)
                    raise PermissionDenied()
            current_user = get_user_model().objects.get(pk=request.user.pk)
            password = generate_password(8)
            user_model = get_user_model()
            users = user_model.objects.filter(email=data.get('email')).all()
            # if users:
            #     raise SuspiciousOperation("A user with the given username/email already exists", 400)
            user = user_model.objects.create_user(
                username=data.get('email'),
                email=data.get('email'),
                password=password
            )
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.save()
            Employee.objects.create(
                user=user,
                manager=manager,
                is_manager=False if data.get('is_manager') == 'false' else True,
                company=self.employee.company,
                created_by=current_user,
                updated_by=current_user,
                # development_plan_type=self.cleaned_data.get('development_plan_type'),
                language_code=data.get('language_code')
                # plaintext_password=my_encrypt(password)
            )
            email_subject = 'Next level'
            email_body = 'Created a new user: {}, your email: {}, your password: {}.' \
                         'To register please go to http://nxtlvl-dev.chisw.us/login' \
                .format(user.username, user.email, password)
            sender = settings.DEFAULT_FROM_EMAIL
            recipients = ['{}'.format(user.email)]
            send_emails.delay(recipients, email_subject, email_body, sender)

    def clean_employee_file(self):
        data = base64.b64decode(self.cleaned_data['employee_file'])
        output = StringIO.StringIO()
        output.write(data)
        output.seek(0)
        fieldnames = ['first_name', 'last_name', 'is_manager', 'email', 'manager', 'language_code']
        reader = csv.DictReader(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
        employee_list = []
        unique = {}
        man_list = []
        from views import found_all_managers

        for row in reader:
            # from ensomus.views import found_all_managers
            manager_list = Employee.objects.filter(manager=self.employee, is_manager=True)
            if len(manager_list) > 0:
                result_list = list(manager_list)
                all_managers_list = found_all_managers(manager_list, result_list)
            else:
                raise forms.ValidationError(_('"error": "this employee have not any manager"'))
            employees = list()
            for manager in all_managers_list:
                manager_dict = model_to_dict(manager)

                for k in ['first_name', 'last_name', 'email']:
                    manager_dict[k] = getattr(manager.user, k)

                manager_dict['photo'] = manager.photo.url if manager.photo else ''
                employees.append(manager_dict)
            for i in employees:
                man_list.append(i['email'])
            man_list.append(self.employee.user.email)
            if row.get('manager') not in man_list:
                raise forms.ValidationError(_('you can not given manager with email={}, changed manager'.format(row.get('manager'))))
            employee_list.append(row)
            if row['email'] in unique:
                raise forms.ValidationError(_('email this record already exists '))
            if validate_email(row.get("email"))==False:
                raise forms.ValidationError(_('email not validate'))
            if get_user_model().objects.filter(email=row.get('email')).exists():
                raise forms.ValidationError(_('A user with the given email already exists'))
        return employee_list


class GoalForm(forms.Form):
    title = forms.CharField(required=False)
    is_achieved = forms.BooleanField(required=False)

    def save(self, current_user, goal=None):
        if goal:
            goal.updated_by = current_user

            for f in ['is_achieved', 'title']:
                if self.cleaned_data.get(f) is not None:
                    setattr(goal, f, self.cleaned_data[f])

            goal.updated_at = datetime.utcnow()
            goal.updated_by = current_user
        else:
            goal = Goal(
                title=self.cleaned_data.get("title", ""),
                created_by=current_user,
                updated_by=current_user,
                is_achieved=self.cleaned_data.get("is_achieved", False)
            )

        goal.save()

        return goal


class GoalAnswerForm(forms.Form):
    file = forms.CharField(required=False)
    file_name = forms.CharField(required=False)
    title = forms.CharField(required=False, min_length=1)
    goal = forms.IntegerField(min_value=1, required=False)

    def clean(self):
        cleaned_data = super(GoalAnswerForm, self).clean()

        file = cleaned_data.get("file")
        file_name = cleaned_data.get("file_name")

        print "FILE:", file
        print "FILE NAME:", file_name
        if file and not file_name:
            raise forms.ValidationError("Field 'file' have to be used together with 'file_name'.")

        if file:
            cleaned_data['file'] = base64.b64decode(cleaned_data['file'])

    def save(self, current_user, answ=None):
        if answ:
            if self.cleaned_data.get("title") is not None:
                answ.title = self.cleaned_data["title"]
            answ.updated_by = current_user
            answ.updated_at = datetime.utcnow()
        else:
            if not self.cleaned_data.get("goal"):
                raise forms.ValidationError("Field 'goal' is required.")

            goal = Goal.objects.get(pk=self.cleaned_data.get("goal"))

            answ = GoalAnswer(
                title=self.cleaned_data.get("title"),
                created_by=current_user,
                updated_by=current_user,
                updated_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
                goal=goal
            )

        answ.save()

        if self.cleaned_data.get("file"):
            with tempfile.TemporaryFile() as f:
                f.write(self.cleaned_data['file'])
                file_to_save = File(f)

                answ.file.save(self.cleaned_data.get("file_name"), file_to_save, save=True)

        return answ
