from flask import redirect, render_template, request, Blueprint, g, abort, after_this_request, url_for
from flask_babelex import _
from flask_login import current_user
from flask_security import RegisterForm, ConfirmRegisterForm, views
from flask_security.recoverable import send_reset_password_instructions, reset_password_token_status, update_password
from flask_security.registerable import register_user
from flask_security.twofactor import tf_login, tf_verify_validility_token, is_tf_setup
from flask_security.utils import suppress_form_csrf, config_value, view_commit, login_user, get_post_register_redirect, \
    base_render_json, json_error_response, get_message, get_url, get_post_login_redirect, do_flash
from flask_security.views import _ctx, _security
from werkzeug.datastructures import MultiDict

from audio_converter import app
from audio_converter.blueprints.multilingual.convert.upload import upload

multilingual = Blueprint('multilingual', __name__, template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.before_request
def before_request():
    if g.lang_code not in app.config['LANGUAGES']:
        abort(404)
        # TODO: create error page as HTML


@multilingual.route('/')
def index():
    return render_template('multilingual/index.html', title='Audio-Converter', lang=g.lang_code)


@multilingual.route('/login', methods=['GET', 'POST'])
def login():
    # NOTE: Source code copied from flask_security/views.py - login() method
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
        return _security.render_template(
            config_value("LOGIN_USER_TEMPLATE"),
            login_user_form=form,
            **_ctx("login"),
            title='Audio-Converter - ' + _('Sign In'),
            lang=g.lang_code
        )


@multilingual.route('/logout')
def logout():
    return views.logout()


@multilingual.route('/register', methods=['GET', 'POST'])
def register():
    # NOTE: Source code copied from flask_security/views.py - register() method
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

    return render_template(
        config_value('REGISTER_USER_TEMPLATE'),
        register_user_form=form,
        **_ctx('register'),
        title='Audio-Converter - ' + _('Register'),
        lang=g.lang_code
    )


@multilingual.route('confirm_email', methods=['GET', 'POST'])
def confirm_email(token=None):
    if token is None:
        token = request.args.get('token')
    return views.confirm_email(token)


# FIXME: Reset password token generation and routing when clicking on link in email
@multilingual.route('/reset_password', methods=['GET', 'POST'])
def reset_password(token):
    # NOTE: Source code copied from flask_security/views.py - reset_password() method
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
        return _security.render_template(
            config_value("RESET_PASSWORD_TEMPLATE"),
            reset_password_form=form,
            reset_password_token=token,
            **_ctx("reset_password"),
            title='Audio-Converter - ' + _('Reset Password'),
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

    if _security._want_json(request):
        return base_render_json(form)
    return _security.render_template(
        config_value("RESET_PASSWORD_TEMPLATE"),
        reset_password_form=form,
        reset_password_token=token,
        **_ctx("reset_password"),
        title='Audio-Converter - ' + _('Reset Password'),
        lang=g.lang_code,
    )


@multilingual.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    # NOTE: Source code copied from flask_security/views.py - forgot_password() method
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

    return _security.render_template(
        config_value("FORGOT_PASSWORD_TEMPLATE"),
        forgot_password_form=form,
        **_ctx("forgot_password"),
        title='Audio-Converter - ' + _('Forgot Password'),
        lang=g.lang_code
    )


@multilingual.route('/convert', methods=['POST', 'GET'])
def convert():
    return render_template('multilingual/convert.html', title='Audio-Converter - ' + _('Convert'), lang=g.lang_code,
                           allowed_audio_file_types=app.config['ALLOWED_AUDIO_FILE_TYPES'])


@multilingual.route('/convert_upload', methods=['POST', 'GET'])
def convert_upload():
    return upload(request)


@multilingual.route('/imprint')
def imprint():
    return render_template('multilingual/imprint.html', title='Audio-Converter - ' + _('Imprint'), lang=g.lang_code)


@multilingual.route('/privacy')
def privacy():
    return render_template('multilingual/privacy.html', title='Audio-Converter - ' + _('Privacy'), lang=g.lang_code)
