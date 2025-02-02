from django.conf import settings
from django.db import models, migrations, connection
import django.db.models.deletion

if 'django.contrib.comments' in settings.INSTALLED_APPS:
    BASE_APP = 'comments'
else:
    BASE_APP = 'django_comments'


class Migration(migrations.Migration):

    dependencies = [
        (BASE_APP, '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=BASE_APP + '.Comment', on_delete=models.CASCADE)),
                ('tree_path', models.CharField(verbose_name='Tree path', max_length=500, editable=False, db_index=True)),
                ('last_child', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Last child', blank=True, to='threadedcomments.ThreadedComment', null=True)),
                ('parent', models.ForeignKey(related_name='children', default=None, blank=True, to='threadedcomments.ThreadedComment', null=True, verbose_name='Parent', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('tree_path',),
                'db_table': 'threadedcomments_comment',
                'verbose_name': 'Threaded comment',
                'verbose_name_plural': 'Threaded comments',
            },
            bases=(f'{BASE_APP}.comment',),
        )
    ]
