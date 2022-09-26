from django.shortcuts import redirect

class IsAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.administrador!=1:
            return redirect("calendario")
        else:
            redirect("index")
        return super().dispatch(request, *args, **kwargs)