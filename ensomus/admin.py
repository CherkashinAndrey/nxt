from django.core.urlresolvers import reverse
from models import Company, Employee, EmployeeRole, Role, UserNxtlvl
from models import Competence, CompetencePart, DevelopmentPlan, DevelopmentPlanType, DevelopmentPlanToEmployeeRelation
from models import Question, Answer, Slider
from models import Action, ActionComment, ActionStatus, File, FileBytes
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin


class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 60, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        # class Media:

        # js = (
        #        '/static/js/tiny_mce/tiny_mce.js',
        #        )


class CreatedByUpdatedByModelBase(admin.ModelAdmin):
    exclude = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class CreatedByModelBase(admin.ModelAdmin):
    exclude = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


class ActionAdmin(CreatedByUpdatedByModelBase):
    pass


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'is_superuser', 'username', 'is_staff')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'first_name', 'last_name', 'is_superuser',
            'username', 'is_active', 'is_superuser', 'is_staff'
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserNxtlvlAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'id',)

    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'is_superuser', 'username', 'is_staff', 'password1', 'password2'
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ActionCommentAdmin(CreatedByUpdatedByModelBase):
    pass


class ActionStatusAdmin(CreatedByUpdatedByModelBase):
    pass


class CompanyAdmin(CreatedByUpdatedByModelBase):
    list_display = ('name', 'id')
    # pass


class EmployeeAdmin(CreatedByUpdatedByModelBase):
    list_display = ('user', 'id')
    # pass


class RoleAdmin(CreatedByUpdatedByModelBase):
    pass


class EmployeeRoleAdmin(CreatedByModelBase):
    pass


class QuestionAdmin(CreatedByUpdatedByModelBase):
    list_filter = ('competence_part',)
    list_display = ('formatted_title', 'competence_part')

    def formatted_title(self, obj):
        return format_html(obj.title)

    formatted_title.short_description = 'Title'

class SliderAdmin(CreatedByUpdatedByModelBase):
    list_filter = ('competence_part',)
    list_display = ('id', 'competence_part')


class AnswerAdmin(CreatedByUpdatedByModelBase):
    list_display = ('title', 'question', 'employee')


class CompetenceAdmin(CreatedByUpdatedByModelBase):
    list_display = (
        'title', 'language_code', #'is_manager', 'company',
        'competence_parts') # 'competence_count'

    def competence_parts(self, instance):
        return '<a href="/admin/ensomus/competencepart/?competence_id__exact=%d">%s</a>' % (instance.id, "CompetencePart")

    competence_parts.allow_tags = True


class CompetencePartAdmin(CreatedByUpdatedByModelBase):
    list_display = ('competence', 'questions',) #'question_count', '__unicode__',
    list_filter = ('competence',)
    ordering = ('id',)

    def questions(self, instance):
        return '<a href="/admin/ensomus/question/?competence_part__id__exact=%d">%s</a>' % (instance.id, "Question")

    questions.allow_tags = True


class DevelopmentPlanToEmployeeRelationInline(admin.TabularInline):
    model = DevelopmentPlanToEmployeeRelation
    extra = 3


class DevelopmentPlanTypeAdmin(CreatedByUpdatedByModelBase):
    list_display = ('name', 'company')


class DevelopmentPlanAdmin(CreatedByUpdatedByModelBase):
    list_display = ('type', 'manager_relation', "get_employee_relation")
    inlines = (DevelopmentPlanToEmployeeRelationInline,)

    def get_employee_relation(self, obj):
        return "\n".join([str(el.id) for el in obj.employee_relation.all()])

        # actions = super(FileAdmin, self).get_actions(request)
        # if 'delete_selected' in actions:
        #     del actions['delete_selected']
        # return actions




# class CompetenceAdmin(CreatedByUpdatedByModelBase):
#     list_display = ('__unicode__', 'questions') #'question_count',
#     list_filter = ('competence_part',)
#
#     def questions(self, instance):
#         return '<a href="/admin/mus/question/?competence__id__exact=%d">%s</a>' % (instance.id, "Questions")
#
#     questions.allow_tags = True


# class QuestionResponseAdmin(CreatedByUpdatedByModelBase):
#     pass


class FileAdmin(admin.ModelAdmin):
    exclude = ('file_name', 'mime_type', 'file_size', 'file', 'created_by')
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(FileAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        upload_file = request.FILES['file_path']
        file_bytes = FileBytes()
        file_bytes.set_data(upload_file.read())
        file_bytes.save()
        obj.file_name = upload_file.name
        obj.mime_type = upload_file.content_type
        obj.file_size = upload_file.size
        obj.file = file_bytes
        admin.ModelAdmin.save_model(self, request, obj, form, change)

    def delete_model(self, request, queryset):
        for obj in queryset:
            try:
                file_bytes = FileBytes.objects.get(pk=obj.file.pk)
                file_bytes.delete()
                admin.ModelAdmin.delete_model(self, request, obj)
            except FileBytes.DoesNotExist:
                pass

    delete_model.short_description = u'Slet valgte filer'


class ReminderTempateAdmin(admin.ModelAdmin):
    pass


admin.site.register(File, FileAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(get_user_model(), UserNxtlvlAdmin)
admin.site.register(ActionComment, ActionCommentAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(CompetencePart, CompetencePartAdmin)
# admin.site.register(QuestionResponse, QuestionResponseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(EmployeeRole, EmployeeRoleAdmin)
admin.site.register(ActionStatus, ActionStatusAdmin)
admin.site.register(DevelopmentPlanType, DevelopmentPlanTypeAdmin)
admin.site.register(DevelopmentPlan, DevelopmentPlanAdmin)

# admin.site.register(ReminderTemplate, ReminderTempateAdmin)