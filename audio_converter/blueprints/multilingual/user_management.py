from flask import after_this_request, g, render_template, url_for
from flask_babelex import gettext
from flask_login import current_user
from flask_security import RegisterForm, ConfirmRegisterForm, views
from flask_security.changeable import change_user_password
from flask_security.passwordless import send_login_instructions
from flask_security.recoverable import reset_password_token_status, send_reset_password_instructions, \
    update_password
from flask_security.registerable import register_user
from flask_security.twofactor import tf_verify_validility_token, is_tf_setup, tf_login
from flask_security.utils import json_error_response, get_message, get_url, suppress_form_csrf, config_value, \
    login_user, view_commit, base_render_json, get_post_login_redirect, do_flash, get_post_register_redirect, \
    get_token_status
from flask_security.views import _ctx, _security
from werkzeug.datastructures import MultiDict
from werkzeug.utils import redirect

from audio_converter import app


def change_password(request):
    """View function which handles a change password request."""
    # Source code copied from flask_security/views.py - change_password() method
    # Only minor import and template variable adjustments
    form_class = _security.change_password_form

    if request.is_json:
        form = form_class(MultiDict(request.get_json()), meta=suppress_form_csrf())
    else:
        form = form_class(meta=suppress_form_csrf())

    if form.validate_on_submit():
        after_this_request(view_commit)
        change_user_password(current_user._get_current_object(), form.new_password.data)
        if _security._want_json(request):
            form.user = current_user
            return base_render_json(form, include_auth_token=True)

        do_flash(*get_message("PASSWORD_CHANGE"))
        return redirect(
            get_url(_security.post_change_view) or get_url(_security.post_login_view)
        )

    if _security._want_json(request):
        form.user = current_user
        return base_render_json(form)

    app.logger.info('Redirecting to change password route...')
    return _security.render_template(
        config_value("CHANGE_PASSWORD_TEMPLATE"),
        change_password_form=form,
        **_ctx("change_password"),
        title='Audio-Converter - ' + gettext('Change password'),
        lang=g.lang_code,
    )


# FIXME: Set token not on None and delete "if token is None:" statement.
def confirm_email(request, token):
    if token is None:
        token = request.args.get('token')
    app.logger.info('Confirm Email')
    return views.confirm_email(token)


def forgot_password(request):
    # Source code copied from flask_security/views.py - forgot_password() method
    # Only minor import and template variable adjustments
    form_class = _security.forgot_password_form

    if request.is_json:
        form = form_class(MultiDict(request.get_json()), meta=suppress_form_csrf())
    else:
        form = form_class(meta=suppress_form_csrf())

    if form.validate_on_submit():
        send_reset_password_instructions(form.user)
        if not _security._want_json(request):
            do_flash(*get_message("PASSWORD_RESET_REQUEST", email=form.user.email))

    if _security._want_json(request):
        return base_render_json(form, include_user=False)

    if form.requires_confirmation and _security.requires_confirmation_error_view:
        do_flash(*get_message("CONFIRMATION_REQUIRED"))
        return redirect(
            get_url(
                _security.requires_confirmation_error_view,
                qparams={"email": form.email.data},
            )
        )

    app.logger.info('"Forgot password" link will be sent...')
    return _security.render_template(
        config_value("FORGOT_PASSWORD_TEMPLATE"),
        forgot_password_form=form,
        **_ctx("forgot_password"),
        title='Audio-Converter - ' + gettext('Forgot Password'),
        lang=g.lang_code
    )


def login(request):
    # Source code copied from flask_security/views.py - login() method
    # Only minor import and template variable adjustments
    if current_user.is_authenticated and request.method == "POST":
        if _security._want_json(request):
            payload = json_error_response(
                errors=get_message("ANONYMOUS_USER_REQUIRED")[0]
            )
            return _security._render_json(payload, 400, None, None)
        else:
            return redirect(get_url(_security.post_login_view))

    form_class = _security.login_form

    if request.is_json:
        if request.content_length:
            form = form_class(MultiDict(request.get_json()), meta=suppress_form_csrf())
        else:
            form = form_class(MultiDict([]), meta=suppress_form_csrf())
    else:
        form = form_class(request.form, meta=suppress_form_csrf())

    if form.validate_on_submit():
        remember_me = form.remember.data if "remember" in form else None
        if config_value("TWO_FACTOR"):
            if request.is_json and request.content_length:
                tf_validity_token = request.get_json().get("tf_validity_token", None)
            else:
                tf_validity_token = request.cookies.get("tf_validity", default=None)

            tf_validity_token_is_valid = tf_verify_validility_token(
                tf_validity_token, form.user.fs_uniquifier
            )

            if config_value("TWO_FACTOR_REQUIRED") or (is_tf_setup(form.user)):
                if config_value("TWO_FACTOR_ALWAYS_VALIDATE") or (
                        not tf_validity_token_is_valid
                ):
                    return tf_login(
                        form.user, remember=remember_me, primary_authn_via="password"
                    )

        login_user(form.user, remember=remember_me, authn_via=["password"])
        after_this_request(view_commit)

        if _security._want_json(request):
            return base_render_json(form, include_auth_token=True)
        return redirect(get_post_login_redirect())

    if _security._want_json(request):
        if current_user.is_authenticated:
            form.user = current_user
        return base_render_json(form)

    if current_user.is_authenticated:
        return redirect(get_url(_security.post_login_view))
    else:
        if form.requires_confirmation and _security.requires_confirmation_error_view:
            do_flash(*get_message("CONFIRMATION_REQUIRED"))
            return redirect(
                get_url(
                    _security.requires_confirmation_error_view,
                    qparams={"email": form.email.data},
                )
            )
        app.logger.info('Redirecting to login route...')
        return _security.render_template(
            config_value("LOGIN_USER_TEMPLATE"),
            login_user_form=form,
            **_ctx("login"),
            title='Audio-Converter - ' + gettext('Sign In'),
            lang=g.lang_code
        )


def logout():
    app.logger.info('Logout')
    return views.logout()


def register(request):
    # Source code copied from flask_security/views.py - register() method
    # Only minor import and template variable adjustments
    if _security.confirmable or request.is_json:
        form_class = ConfirmRegisterForm
    else:
        form_class = RegisterForm

    if request.is_json:
        form_data = MultiDict(request.get_json())
    else:
        form_data = request.form

    form = form_class(form_data, meta=suppress_form_csrf())
    if form.validate_on_submit():
        did_login = False
        user = register_user(form)
        form.user = user

        if not _security.confirmable or _security.login_without_confirmation:
            if config_value('TWO_FACTOR') and config_value('TWO_FACTOR_REQUIRED'):
                return tf_login(user, primary_authn_via='register')
            after_this_request(view_commit)
            login_user(user, authn_via=['register'])
            did_login = True

        if not _security._want_json(request):
            return redirect(get_post_register_redirect())

        return base_render_json(form, include_auth_token=did_login)
    if _security._want_json(request):
        return base_render_json(form)

    app.logger.info('Redirecting to register route...')
    return render_template(
        config_value('REGISTER_USER_TEMPLATE'),
        register_user_form=form,
        **_ctx('register'),
        title='Audio-Converter - ' + gettext('Register'),
        lang=g.lang_code
    )


# FIXME: Set token not on None and delete "if token is None:" statement.
def reset_password(request, token):
    if token is None:
        token = request.args.get('token')
    # Source code copied from flask_security/views.py - reset_password() method
    # Only minor import and template variable adjustments
    expired, invalid, user = reset_password_token_status(token)
    form_class = _security.reset_password_form
    if request.is_json:
        form = form_class(MultiDict(request.get_json()), meta=suppress_form_csrf())
    else:
        form = form_class(meta=suppress_form_csrf())
    form.user = user

    if request.method == "GET":
        if not user or invalid:
            m, c = get_message("INVALID_RESET_PASSWORD_TOKEN")
            if _security.redirect_behavior == "spa":
                return redirect(get_url(_security.reset_error_view, qparams={c: m}))
            do_flash(m, c)
            return redirect(url_for("multilingual.forgot_password"))
        if expired:
            send_reset_password_instructions(user)
            m, c = get_message(
                "PASSWORD_RESET_EXPIRED",
                email=user.email,
                within=_security.reset_password_within,
            )
            if _security.redirect_behavior == "spa":
                return redirect(
                    get_url(
                        _security.reset_error_view,
                        qparams=user.get_redirect_qparams({c: m}),
                    )
                )
            do_flash(m, c)
            return redirect(url_for("multilingual.forgot_password"))

        # All good - for SPA - redirect to the ``reset_view``
        if _security.redirect_behavior == "spa":
            return redirect(
                get_url(
                    _security.reset_view,
                    qparams=user.get_redirect_qparams({"token": token}),
                )
            )
        app.logger.info('Resetting your password!')
        return _security.render_template(
            config_value("RESET_PASSWORD_TEMPLATE"),
            reset_password_form=form,
            reset_password_token=token,
            **_ctx("reset_password"),
            title='Audio-Converter - ' + gettext('Reset Password'),
            lang=g.lang_code,
        )

    # This is the POST case.
    m = None
    if not user or invalid:
        invalid = True
        m, c = get_message("INVALID_RESET_PASSWORD_TOKEN")
        if not _security._want_json(request):
            do_flash(m, c)

    if expired:
        send_reset_password_instructions(user)
        m, c = get_message(
            "PASSWORD_RESET_EXPIRED",
            email=user.email,
            within=_security.reset_password_within,
        )
        if not _security._want_json(request):
            do_flash(m, c)

    if invalid or expired:
        if _security._want_json(request):
            return _security._render_json(json_error_response(m), 400, None, None)
        else:
            return redirect(url_for("multilingual.forgot_password"))

    if form.validate_on_submit():
        after_this_request(view_commit)
        update_password(user, form.password.data)
        if config_value("TWO_FACTOR") and (
                config_value("TWO_FACTOR_REQUIRED")
                or (form.user.tf_totp_secret and form.user.tf_primary_method)
        ):
            return tf_login(user, primary_authn_via="reset")
        login_user(user, authn_via=["reset"])
        if _security._want_json(request):
            login_form = _security.login_form()
            login_form.user = user
            return base_render_json(login_form, include_auth_token=True)
        else:
            do_flash(*get_message("PASSWORD_RESET"))
            return redirect(
                get_url(_security.post_reset_view) or get_url(_security.post_login_view)
            )

    app.logger.info('Resetting your password!')
    if _security._want_json(request):
        return base_render_json(form)
    app.logger.info('Reset Password')
    return _security.render_template(
        config_value("RESET_PASSWORD_TEMPLATE"),
        reset_password_form=form,
        reset_password_token=token,
        **_ctx("reset_password"),
        title='Audio-Converter - ' + gettext('Reset Password'),
        lang=g.lang_code,
    )


def send_login(request):
    """View function that sends login instructions for password less login"""
    # Source code copied from flask_security/views.py - send_login() method
    # Only minor import and template variable adjustments

    form_class = _security.passwordless_login_form

    if request.is_json:
        form = form_class(MultiDict(request.get_json()), meta=suppress_form_csrf())
    else:
        form = form_class(meta=suppress_form_csrf())

    if form.validate_on_submit():
        send_login_instructions(form.user)
        if not _security._want_json(request):
            do_flash(*get_message("LOGIN_EMAIL_SENT", email=form.user.email))

    if _security._want_json(request):
        return base_render_json(form)

    app.logger.info('Instructions for password less login link will be sent...')
    return _security.render_template(
        config_value("SEND_LOGIN_TEMPLATE"),
        send_login_form=form,
        **_ctx("send_login"),
        title='Audio-Converter - ' + gettext('Send Login'),
        lang=g.lang_code
    )


# TODO: Make function private if no longer needed
# FIXME: Set token not on None and delete "if token is None:" statement.
def token_login(request, token):
    """A view function that handles logins without the need of passwords, similar to reset_password and
    confirm.
    This is usually a GET request sent via email. The request puts us in no position to differentiate
    between form based apps and those who are not.
    """
    if token is None:
        token = request.args.get('token')
    expired, invalid, user = _login_token_status(token)
    # Source code copied from flask_security/views.py - token_login() method
    # Only minor import and template variable adjustments

    if not user or invalid:
        m, c = get_message("INVALID_LOGIN_TOKEN")
        if _security.redirect_behavior == "spa":
            return redirect(get_url(_security.login_error_view, qparams={c: m}))
        do_flash(m, c)
        return redirect(url_for("login"))
    if expired:
        send_login_instructions(user)
        m, c = get_message(
            "LOGIN_EXPIRED", email=user.email, within=_security.login_within
        )
        if _security.redirect_behavior == "spa":
            return redirect(
                get_url(
                    _security.login_error_view,
                    qparams=user.get_redirect_qparams({c: m}),
                )
            )
        do_flash(m, c)
        return redirect(url_for("login"))

    login_user(user, authn_via=["token"])
    after_this_request(view_commit)
    if _security.redirect_behavior == "spa":
        return redirect(
            get_url(_security.post_login_view, qparams=user.get_redirect_qparams())
        )

    do_flash(*get_message("PASSWORDLESS_LOGIN_SUCCESSFUL"))

    return redirect(get_post_login_redirect())


def _login_token_status(token):
    # Source code copied from flask_security/views.py - login_token_status() method
    """Returns the expired status, invalid status, and user of a login token.
    For example::

        expired, invalid, user = login_token_status('...')

    :param token: The login token
    """
    app.logger.info('Retrieve login token status...')
    return get_token_status(token, "login", "LOGIN")
