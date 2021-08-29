# Generated by Django 3.2.6 on 2021-08-27 12:41

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Опрос', help_text='название опроса', max_length=512, verbose_name='Название')),
                ('start', models.DateField(default=django.utils.timezone.now, editable=False, help_text='дата старта, после сохранения не редактируется', verbose_name='Дата старта')),
                ('end', models.DateField(default=django.utils.timezone.now, help_text='дата окончания опроса', verbose_name='Дата окончания')),
                ('description', models.TextField(default='Описание опроса', max_length=2048, verbose_name='Описание')),
            ],
            managers=[
                ('polls', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='Вопрос', help_text='вопрос по опросу', max_length=1024, verbose_name='Вопрос')),
                ('type', models.CharField(choices=[('M', 'Multi'), ('S', 'Single'), ('T', 'Free text')], default='T', max_length=10, verbose_name='Тип вопроса')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='Ответ', max_length=1024, verbose_name='Вариант ответа')),
            ],
        ),
        migrations.CreateModel(
            name='PollSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(help_text='в ТЗ указано так,             будто пользователь может приходить из левой системы            , поэтому числовой ID, а не FK на base_user_model', null=True, verbose_name='Числовой идентификатор пользователя сессии опроса')),
                ('finished', models.BooleanField(db_index=True, default=False, verbose_name='Окончена ли сессия опроса')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polls.poll', verbose_name='Опрос сессии')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll_session', models.ForeignKey(help_text='Сессия, в которой был дан ответ на вопрос', on_delete=django.db.models.deletion.DO_NOTHING, to='polls.pollsession', verbose_name='Сессия опроса')),
                ('question', models.ForeignKey(help_text='Вопрос, на который был дан ответ', on_delete=django.db.models.deletion.DO_NOTHING, to='polls.question', verbose_name='Вопрос')),
            ],
        ),
    ]