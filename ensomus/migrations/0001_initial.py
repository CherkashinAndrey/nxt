# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ensomus.models
import django.utils.timezone
import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNxtlvl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.TextField(verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('type', models.CharField(max_length=1, null=True, choices=[(b'A', b'TYPE_A'), (b'B', b'TYPE_B'), (b'C', b'TYPE_C')])),
                ('difficulty', models.IntegerField(null=True, choices=[(1, b'DIFFICULTY_LOW'), (2, b'DIFFICULTY_MEDIUM'), (3, b'DIFFICULTY_HIGH')])),
                ('created_by', models.ForeignKey(related_name='action_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'action',
                'verbose_name_plural': 'actions',
            },
        ),
        migrations.CreateModel(
            name='ActionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('text', models.TextField(verbose_name='text')),
                ('follow_up_at', models.DateField(default=None, null=True, verbose_name='follow up at', blank=True)),
                ('action', models.ForeignKey(related_name='comments', verbose_name='action', blank=True, to='ensomus.Action', null=True)),
                ('created_by', models.ForeignKey(related_name='actioncomment_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'action comment',
                'verbose_name_plural': 'action comments',
            },
        ),
        migrations.CreateModel(
            name='ActionStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_da', models.CharField(max_length=30, verbose_name='name_da')),
                ('name_en', models.CharField(max_length=30, verbose_name='name_en')),
            ],
            options={
                'verbose_name': 'action status',
                'verbose_name_plural': 'action statuses',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.TextField(null=True, verbose_name='text')),
                ('created_by', models.ForeignKey(related_name='answer_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('created_by', models.ForeignKey(related_name='company_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='company_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.CharField(max_length=400, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('status', models.BooleanField(default=False, verbose_name='status')),
                ('language_code', models.CharField(default=b'da', max_length=15, verbose_name='language', choices=[(b'da', 'Danish'), (b'en', 'English')])),
                ('is_manager', models.BooleanField(default=False, verbose_name='for manager')),
                ('company', models.ForeignKey(default=None, blank=True, to='ensomus.Company', null=True, verbose_name='company')),
                ('created_by', models.ForeignKey(related_name='competence_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='competence_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'competence',
                'verbose_name_plural': 'competences',
            },
        ),
        migrations.CreateModel(
            name='CompetencePart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.CharField(max_length=400, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('competence_status', models.BooleanField(default=False)),
                ('competence', models.ForeignKey(related_name='competence_part', verbose_name='competence', to='ensomus.Competence')),
                ('created_by', models.ForeignKey(related_name='competencepart_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='competencepart_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'competence_part',
                'verbose_name_plural': 'competence_parts',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('language_code', models.CharField(default=b'da', max_length=15, verbose_name='language', choices=[(b'da', 'Danish'), (b'en', 'English')])),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('competence_parts', models.ManyToManyField(related_name='development_plan_competence_parts', verbose_name='competence parts', to='ensomus.CompetencePart')),
                ('created_by', models.ForeignKey(related_name='developmentplan_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'development plan',
                'verbose_name_plural': 'development plans',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlanToEmployeeRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('finished_at', models.DateTimeField(default=None, null=True, verbose_name='finished at', blank=True)),
                ('is_private', models.BooleanField(default=True, verbose_name='is private')),
                ('created_by', models.ForeignKey(related_name='developmentplantoemployeerelation_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('development_plan', models.ForeignKey(verbose_name='development_plan', to='ensomus.DevelopmentPlan')),
            ],
            options={
                'verbose_name': 'development plan to user relation',
                'verbose_name_plural': 'development plan to user relations',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlanType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(verbose_name='company', blank=True, to='ensomus.Company', null=True)),
            ],
            options={
                'verbose_name': 'development plan type',
                'verbose_name_plural': 'development plan types',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.CharField(max_length=4000, verbose_name='title')),
                ('phone', models.CharField(default=b'', max_length=40, verbose_name='phone')),
                ('potenciale', models.CharField(blank=True, max_length=15, null=True, verbose_name='potenciale', choices=[(b'POTENCIALE_YES', b'YES'), (b'POTENCIALE_NO', b'NO')])),
                ('is_manager', models.BooleanField(default=False, verbose_name='is manager')),
                ('language_code', models.CharField(default=b'da', max_length=15, verbose_name='language', choices=[(b'da', 'Danish'), (b'en', 'English')])),
                ('notes', models.TextField(null=True, blank=True)),
                ('status_questions', models.CharField(default=b'STATUS_MISSING', max_length=15, verbose_name='status_questions', choices=[(b'STATUS_MISSING', b'MISSING'), (b'STATUS_IN_PROGRESS', b'IN_PROGRESS'), (b'STATUS_SHOW', b'SHOW')])),
                ('date_of_birth', models.DateTimeField(default=None, null=True, verbose_name='date of birth', blank=True)),
                ('photo', models.ImageField(storage=ensomus.models.OverwriteStorage(), upload_to=ensomus.models.user_photo_directory_path, blank=True)),
                ('company', models.ForeignKey(verbose_name='company', to='ensomus.Company')),
                ('created_by', models.ForeignKey(related_name='employee_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('development_plan_type', models.ForeignKey(verbose_name='development plan type', blank=True, to='ensomus.DevelopmentPlanType', null=True)),
                ('manager', models.ForeignKey(verbose_name='manager', blank=True, to='ensomus.Employee', null=True)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
        migrations.CreateModel(
            name='EmployeeRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('created_by', models.ForeignKey(related_name='employeerole_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('employee', models.ForeignKey(verbose_name='employee', to='ensomus.Employee')),
            ],
            options={
                'verbose_name': 'employee role',
                'verbose_name_plural': 'employee roles',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('file_name', models.CharField(max_length=255)),
                ('mime_type', models.CharField(max_length=100)),
                ('file_size', models.BigIntegerField()),
                ('file_path', models.FileField(upload_to=b'temp')),
                ('company', models.ForeignKey(related_name='files', to='ensomus.Company')),
                ('created_by', models.ForeignKey(related_name='file_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Fil',
                'verbose_name_plural': 'Filer',
            },
        ),
        migrations.CreateModel(
            name='FileBytes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_data', models.TextField(db_column=b'data', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('title', models.TextField(null=True, verbose_name='text')),
                ('scale', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('competence_part', models.ForeignKey(verbose_name='competence_part', blank=True, to='ensomus.CompetencePart', null=True)),
                ('created_by', models.ForeignKey(related_name='question_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='question_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('created_by', models.ForeignKey(related_name='role_created_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('updated_by', models.ForeignKey(related_name='role_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.ForeignKey(default=None, blank=True, to='ensomus.FileBytes', null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='role',
            field=models.ForeignKey(related_name='files', default=None, blank=True, to='ensomus.Role', null=True),
        ),
        migrations.AddField(
            model_name='employeerole',
            name='role',
            field=models.ForeignKey(verbose_name='role', to='ensomus.Role'),
        ),
        migrations.AddField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(to='ensomus.Role', through='ensomus.EmployeeRole'),
        ),
        migrations.AddField(
            model_name='employee',
            name='updated_by',
            field=models.ForeignKey(related_name='employee_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(related_name='employee_user', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='developmentplantoemployeerelation',
            name='employee',
            field=models.ForeignKey(verbose_name='employee', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='employee_relation',
            field=models.ManyToManyField(related_name='development_plan_employee', verbose_name='employee relation', through='ensomus.DevelopmentPlanToEmployeeRelation', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='manager_relation',
            field=models.ForeignKey(related_name='development_plan_manager', verbose_name='manager relation', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='developmentplan',
            name='type',
            field=models.ForeignKey(verbose_name='type', blank=True, to='ensomus.DevelopmentPlanType', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='employee',
            field=models.ForeignKey(verbose_name='employee', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(verbose_name='question', to='ensomus.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='updated_by',
            field=models.ForeignKey(related_name='answer_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='actioncomment',
            name='status',
            field=models.ForeignKey(verbose_name='status', blank=True, to='ensomus.ActionStatus', null=True),
        ),
        migrations.AddField(
            model_name='actioncomment',
            name='updated_by',
            field=models.ForeignKey(related_name='actioncomment_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='employee',
            field=models.ForeignKey(verbose_name='employee', to='ensomus.Employee'),
        ),
        migrations.AddField(
            model_name='action',
            name='status',
            field=models.ForeignKey(default=5, blank=True, to='ensomus.ActionStatus', null=True, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='action',
            name='updated_by',
            field=models.ForeignKey(related_name='action_updated_by', on_delete=django.db.models.deletion.SET_NULL, verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
