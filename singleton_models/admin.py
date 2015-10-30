from __future__ import absolute_import, print_function, unicode_literals

from functools import wraps

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.http import HttpResponseRedirect


def singleton_view(fn_name):
    def view(self, request, object_id, extra_context=None):
        object_id = '1'
        self.model.objects.get_or_create(pk=1)

        super_view = getattr(super(SingletonModelAdmin, self), fn_name)
        return super_view(request, object_id, extra_context=extra_context)

    view.__name__ = str(fn_name)
    return view


class SingletonModelAdmin(admin.ModelAdmin):
    change_form_template = "admin/singleton_models/change_form.html"
    object_history_template = "admin/singleton_models/object_history.html"

    def has_add_permission(self, request):
        """ Singleton pattern: prevent addition of new objects """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Singleton pattern: prevent deletion of THE object """
        return False

    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            @wraps(view)
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return wrapper

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = patterns(
            '',
            url(r'^history/$',
                wrap(self.history_view),
                {'object_id': 1},
                name='%s_%s_history' % info),
            url(r'^$',
                wrap(self.change_view),
                {'object_id': 1},
                name='%s_%s_change' % info),
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
        )

        return urlpatterns

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta

        msg = _('%(obj)s was changed successfully.') % {'obj': force_text(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect("../")

    change_view = singleton_view('change_view')
    history_view = singleton_view('history_view')
