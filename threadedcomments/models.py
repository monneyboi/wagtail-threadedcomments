from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django_comments.managers import CommentManager
from django_comments.models import Comment
from wagtail.admin.panels import MultiFieldPanel, FieldRowPanel, FieldPanel, HelpPanel

PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)


class ThreadedComment(Comment):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='children', verbose_name=_('Parent'))
    last_child = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Last child'))
    tree_path = models.CharField(_('Tree path'), max_length=500, editable=False)
    newest_activity = models.DateTimeField(null=True)

    objects = CommentManager()

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('user'),
                FieldPanel('parent'),
            ]),
            FieldPanel('comment'),
        ], heading=_("Info")),
        MultiFieldPanel([
            HelpPanel(template="help_panel.html", heading=_("Content object")),
            FieldRowPanel([
                FieldPanel('submit_date'),
                FieldPanel('ip_address'),
            ])
        ], heading=_("Metadata")),
        FieldRowPanel([
            FieldPanel('is_public'),
            FieldPanel('is_removed'),
        ], heading=_("Visibility")),
    ]

    @property
    def depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))

    @property
    def root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])

    @property
    def root_path(self):
        return ThreadedComment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])

    @transaction.atomic
    def save(self, *args, **kwargs):
        skip_tree_path = kwargs.pop('skip_tree_path', False)
        super().save(*args, **kwargs)
        if skip_tree_path:
            return None

        tree_path = str(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=self.id)
            ThreadedComment.objects.filter(pk=self.parent_id).update(newest_activity=self.submit_date)
            ThreadedComment.objects.filter(parent_id=self.parent_id).update(newest_activity=self.submit_date)

        self.tree_path = tree_path
        ThreadedComment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)
        ThreadedComment.objects.filter(pk=self.pk).update(newest_activity=self.submit_date)

    def delete(self, *args, **kwargs):
        # Fix last child on deletion.
        if self.parent_id:
            try:
                prev_child = ThreadedComment.objects \
                    .filter(parent=self.parent_id) \
                    .exclude(pk=self.pk) \
                    .order_by('-submit_date')[0]
            except IndexError:
                prev_child = None
            if prev_child:
                ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=prev_child)
                ThreadedComment.objects.filter(pk=self.parent_id).update(newest_activity=prev_child.submit_date)
                ThreadedComment.objects.filter(parent_id=self.parent_id).update(newest_activity=prev_child.submit_date)
            else:
                ThreadedComment.objects.filter(pk=self.parent_id).update(last_child=None)
                ThreadedComment.objects.filter(pk=self.parent_id).update(newest_activity=self.parent.submit_date)

        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('tree_path',)
        db_table = 'threadedcomments_comment'
        verbose_name = _('Threaded comment')
        verbose_name_plural = _('Threaded comments')
