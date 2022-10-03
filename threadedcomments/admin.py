
from threadedcomments.models import ThreadedComment
from django.utils.translation import gettext_lazy as _

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
        'flags',
    )
    
# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(CommentAdmin)
