from datetime import timedelta

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer

from doctor.user.forms import ForgotPasswordForm
from doctor.user.models import ForgotPassword
from doctor.user.validators import Validations


class ForgotPasswordTemplateView(FormView):
    """
        A user can reset their password by opening the one-time reset link sent to their email
    """
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    form_class = ForgotPasswordForm
    template_name = 'forgot_password.html'

    def get(self, request, *args, **kwargs):
        forgot_password = ForgotPassword.objects.filter(
            token=self.kwargs.get('token'),
            created_at__gte=timezone.now() - timedelta(days=1)
        )
        if not forgot_password.exists():
            return render(request, 'forgot_password_expired.html')
        return super(ForgotPasswordTemplateView, self).get(request,
                                                           *args,
                                                           **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            token = self.kwargs.get('token')
            password = self.request.POST.get('password1')
            forgot_password = ForgotPassword.objects.filter(token=token).first()
            user = forgot_password.user
            try:
                Validations.validate_password(password)
            except Exception as error:
                form.add_error(
                    "password",
                    error.args[0]
                )
                return self.form_invalid(form)
            user.set_password(password)
            user.save()
            forgot_password.delete()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('doctor.user:forgot_password_success')


class ForgotPasswordSuccessTemplateView(TemplateView):
    template_name = 'forgot_password_success.html'
