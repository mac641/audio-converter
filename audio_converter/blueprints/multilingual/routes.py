import os

from flask import redirect, render_template, request, Blueprint, g, abort, url_for
from flask_babelex import gettext
from flask_login import current_user
from flask_security import unauth_csrf, auth_required

from audio_converter import app, db
from audio_converter.blueprints.multilingual import utils, user_management
from audio_converter.blueprints.multilingual.convert_feature.convert import process
from audio_converter.blueprints.multilingual.convert_feature.download import zip_converted_files, zip_list, \
    send_archive
from audio_converter.blueprints.multilingual.convert_feature.upload import upload
from audio_converter.models import Track, User

multilingual = Blueprint('multilingual', __name__, template_folder='templates', url_prefix='/<lang_code>')

upload_path = app.config['UPLOAD_PATH']
download_path = app.config['DOWNLOAD_PATH']


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


@multilingual.after_request
def after_request(response):
    # Reduce browser caching
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@multilingual.route('/change_password', methods=['GET', 'POST'])
@auth_required()
def change_password():
    return user_management.change_password(request)


@multilingual.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email(token=None):
    return user_management.confirm_email(request, token)


@multilingual.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return user_management.forgot_password(request)


@multilingual.route('/login', methods=['GET', 'POST'])
def login():
    return user_management.login(request)


@multilingual.route('/logout')
@auth_required()
def logout():
    return user_management.logout()


@multilingual.route('/register', methods=['GET', 'POST'])
def register():
    return user_management.register(request)


@multilingual.route('/reset_password', methods=['GET', 'POST'])
def reset_password(token=None):
    return user_management.reset_password(request, token)


@multilingual.route('/send_login', methods=['GET', 'POST'])
@unauth_csrf(fall_through=True)
def send_login():
    return user_management.send_login(request)


@multilingual.route('/')
def index():
    app.logger.info('Redirecting to index route...')
    return render_template('multilingual/index.html', title='Audio-Converter', lang=g.lang_code)


@multilingual.route('/convert')
def convert():
    app.logger.info('Redirecting to convert route...')
    return render_template('multilingual/convert.html', title='Audio-Converter - ' + gettext('Convert'),
                           lang=g.lang_code,
                           allowed_audio_file_types=app.config['ALLOWED_AUDIO_FILE_TYPES'])


@multilingual.route('/convert_upload', methods=['GET', 'POST'])
def convert_upload():
    app.logger.info('Processing uploads and returning status codes...')
    return upload(request)


@multilingual.route('/convert_process', methods=['GET', 'POST'])
def convert_process():
    process_return_value = process(request)
    app.logger.info('Processed audio file template: ' + ', '.join(map(str, process_return_value)))
    if process_return_value[1] == 301:
        return redirect(url_for('multilingual.convert_done'), 301)
    else:
        abort(process_return_value[1])


@multilingual.route('/convert_done')
def convert_done():
    app.logger.info('Redirecting to download route and display conversion results...')
    return render_template('multilingual/download.html',
                           title='Audio Converter - ' + gettext('Conversion Results'),
                           lang=g.lang_code)


@multilingual.route('/convert_download')
def convert_download():
    zip_archive = zip_converted_files()
    app.logger.info('Received zip compression status: ' + ', '.join(map(str, zip_archive)))
    return send_archive(zip_archive)


@multilingual.route('/settings')
@auth_required()
def settings():
    if not current_user.is_authenticated:
        app.logger.info('Settings attempted access to settings route, detour to login.')
        return redirect(url_for('multilingual.login'))

    app.logger.info('Redirecting to settings route...')
    return render_template('multilingual/settings.html', title='Audio-Converter - ' + gettext('Settings'),
                           lang=g.lang_code)


@multilingual.route('/clear_cache', methods=['GET', 'POST'])
@auth_required()
def clear_cache():
    if not current_user.is_authenticated:
        app.logger.info('Clear_cache attempted to access settings route, redirect to login.')
        return redirect(url_for('multilingual.login'))

    if request.method == 'POST':
        reply_form = request.form.get('reply')
        if reply_form == "yes":
            utils.delete_path(upload_path)
            utils.delete_path(download_path)
            utils.create_path(download_path)
            app.logger.info('Cache cleared...')
            return redirect(url_for('multilingual.index'))
        else:
            return redirect(url_for('multilingual.settings'))
    else:
        return render_template('multilingual/clear_cache.html',
                               title='Audio-Converter - ' + gettext('Clear cache'),
                               lang=g.lang_code)


@multilingual.route('/delete_history', methods=['GET', 'POST'])
@auth_required()
def delete_history():
    if not current_user.is_authenticated:
        app.logger.info('Delete_history attempted access to settings route, detour to login.')
        return redirect(url_for('multilingual.login'))

    if request.method == 'POST':
        reply_form = request.form.get('reply')
        if reply_form == "yes":
            g.user = current_user.get_id()
            # delete audio files
            conversion_path = app.config['CONVERSION_PATH']
            path = os.path.join(conversion_path, g.user)
            utils.delete_path(path)
            # delete db entries
            Track.query.filter_by(user=g.user).delete()
            # reset convert count
            user = User.query.filter_by(fs_uniquifier=g.user).first()
            user.convert = 0
            db.session.commit()
            app.logger.info('Deleted history...')

            return redirect(url_for('multilingual.index'))
        else:
            return redirect(url_for('multilingual.settings'))
    else:
        return render_template('multilingual/delete_history.html',
                               title='Audio-Converter - ' + gettext('Delete history'),
                               lang=g.lang_code)


@multilingual.route('/history')
@auth_required()
def history():
    if not current_user.is_authenticated:
        return redirect(url_for('multilingual.login'))

    g.user = current_user.get_id()
    track_list = Track.query.filter_by(user=g.user).all()
    tracks = []
    for track in track_list:
        # TODO: compare duplicates with mime types instead of file names / endings
        is_duplicate = False
        for t in tracks:
            if t.trackname == track.trackname and t.format == track.format:
                is_duplicate = True
        if not is_duplicate:
            track.timestamp = track.timestamp.date()
            tracks.append(track)

    return render_template('multilingual/history.html', title='Audio-Converter - ' + gettext('History'),
                           lang=g.lang_code, tracks=tracks)


@multilingual.route('/history_download', methods=['GET', 'POST'])
def history_download():
    if not current_user.is_authenticated:
        return redirect(url_for('multilingual.login'))

    if request.method == 'POST':
        tracks_form = request.form.getlist('download-tracks')
        links = []
        for i in tracks_form:
            track = Track.query.filter_by(id=i).first()
            links.insert(-1, os.path.join(track.path, track.trackname + track.format))

        zip_archive = zip_list(links)
        app.logger.info('Received status for zipping selected files: ' + ', '.join(map(str, zip_archive)))
        return send_archive(zip_archive)


@multilingual.route('/imprint')
def imprint():
    app.logger.info('Redirecting to imprint route...')
    return render_template('multilingual/imprint.html', title='Audio-Converter - ' + gettext('Imprint'),
                           lang=g.lang_code)


@multilingual.route('/privacy')
def privacy():
    app.logger.info('Redirecting to privacy route...')
    return render_template('multilingual/privacy.html', title='Audio-Converter - ' + gettext('Privacy'),
                           lang=g.lang_code)


# TODO: Add translations to error pages
@multilingual.app_errorhandler(403)
def error_403(error):
    app.logger.error('Error_403 attempted access to a forbidden page.')
    return render_template('multilingual/error.html',
                           title='Audio-Converter - Error_403',
                           errortitle="You don't have permission to do that. (403)",
                           msg='Please check your account and try again.'), 403


@multilingual.app_errorhandler(404)
def error_404(error):
    app.logger.error('Error_403 attempted access to a non-existent page.')
    return render_template('multilingual/error.html',
                           title='Audio-Converter - Error 404',
                           errortitle='Oops. Page Not Found. (404)',
                           msg='That page does not exist. Please try a different location.'), 404


@multilingual.app_errorhandler(500)
def error_500(error):
    app.logger.error('Error_500 Internal error.')
    return render_template('multilingual/error.html',
                           title='Audio-Converter - Error_500',
                           errortitle='Something went wrong. (500)',
                           msg="We're experiencing some trouble on our end. Please try again in the near future."), 500


# Help methods - no direct endpoints
def token_login(token=None):
    return user_management.token_login(request, token)
