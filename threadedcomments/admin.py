
from threadedcomments.models import ThreadedComment
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

class CommentAdmin(ModelAdmin):
    model = ThreadedComment
    menu_label = _("Comments")
    menu_icon = "comment"  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = (
        'comment',
        'content_object',
        'user',
        'flags_count',
        'submit_date',
    )
    list_filter = (
        'is_public',
        'is_removed',
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'comment'
    )

    def flags_count(self, inst):
        return inst.flags_count
    flags_count.admin_order_field = 'flags_count'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(flags_count=Count('flags'))


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(CommentAdmin)
