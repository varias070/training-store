import django_registration
from celery.app import shared_task
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.template.loader import render_to_string
from django_registration.backends.activation.views import REGISTRATION_SALT
from django_registration.exceptions import ActivationError
from django.conf import settings
from .forms import RegisterUserForm


class RegisterUser(django_registration.backends.activation.views.RegistrationView):
    form_class = RegisterUserForm
    template_name = 'django_registration/register.html'


@shared_task
def create_activation_key(user):
    return signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)


@shared_task
def send_activation_email(user, request):
    email_body_template = "django_registration/activation_email_body.txt"
    email_subject_template = "django_registration/activation_email_subject.txt"
    activation_key = create_activation_key(user)
    context = get_email_context(request, activation_key)
    context["user"] = user
    subject = render_to_string(
        context=context,
        template_name=email_subject_template,
        request=request,
    )
    subject = "".join(subject.splitlines())
    message = render_to_string(
        template_name=email_body_template,
        context=context,
        request=request,
    )
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


@shared_task
def get_email_context(request, activation_key):
    scheme = "https" if request.is_secure() else "http"
    return {
        "scheme": scheme,
        "activation_key": activation_key,
        "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
        "site": get_current_site(request),
        }


@shared_task
def activate_user(*args, **kwargs):
    username = validate_key(kwargs.get("activation_key"))
    user = get_user(username)
    user.is_active = True
    user.save()
    return user


@shared_task
def validate_key(activation_key):
    ALREADY_ACTIVATED_MESSAGE = (
        "The account you tried to activate has already been activated."
    )
    BAD_USERNAME_MESSAGE = (
        "The account you attempted to activate is invalid.")
    EXPIRED_MESSAGE =(
        "This account has expired.")
    INVALID_KEY_MESSAGE = (
        "The activation key you provided is invalid.")
    try:
        username = signing.loads(
            activation_key,
            salt=REGISTRATION_SALT,
            max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400,
        )
        return username
    except signing.SignatureExpired:
        raise ActivationError(EXPIRED_MESSAGE, code="expired")
    except signing.BadSignature:
        raise ActivationError(
            INVALID_KEY_MESSAGE,
            code="invalid_key",
            params={"activation_key": activation_key},
        )


@shared_task
def get_user(self, username):
    User = get_user_model()
    try:
        user = User.objects.get(**{User.USERNAME_FIELD: username})
        if user.is_active:
            raise ActivationError(
                self.ALREADY_ACTIVATED_MESSAGE, code="already_activated"
            )
        return user
    except User.DoesNotExist:
        raise ActivationError(self.BAD_USERNAME_MESSAGE, code="bad_username")