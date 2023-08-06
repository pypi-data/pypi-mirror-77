from datetime import datetime, timedelta

from flask import Blueprint, request
from jinja2 import TemplateNotFound
from pytz import timezone, utc as UTC

from cornerstone.db.models import LiveStream, Page, Sermon
from cornerstone.email import send_email
from cornerstone.settings import get_setting
from cornerstone.theming import render

CONTACT_MESSAGE = """New contact form submission:

Name: {name}
E-mail: {email}
Subject: {subject}
Message:

{message}
"""

home = Blueprint('home', __name__)


def _get_datetime(isostring):
    if not isostring:
        return None
    tzinfo = timezone(get_setting('localization-timezone'))
    return datetime.fromisoformat(isostring).astimezone(tzinfo).replace(tzinfo=None)


@home.route('/', methods=['GET'])
def index():
    context = {
        'page': Page.query.filter_by(slug='home').first()
    }
    if get_setting('sermons-on-home-page', False):
        limit = get_setting('sermons-home-page-count', 10)
        context.update({
            'sermons': Sermon.query.order_by(Sermon.date.desc()).limit(limit).all()
        })
    try:
        return render('home.html', **context)
    except TemplateNotFound:
        return render('page.html', **context)


@home.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    message = None
    if request.method == 'POST' and not request.form.get('sweet-nectar'):
        body = CONTACT_MESSAGE.format(name=request.form['name'], email=request.form['email'],
                                      subject=request.form['subject'], message=request.form['message'])
        if send_email([get_setting('contact-form-email')], '[Contact Form] {}'.format(request.form['subject']), body):
            message = ('Thank you for your e-mail!', 'success')
        else:
            message = ('Unable to send your e-mail, please try again later', 'error')
    return render('contact-us.html', message=message)


@home.route('/live-stream', methods=['GET'])
def live_stream():
    tzinfo = timezone(get_setting('localization-timezone'))
    now = datetime.utcnow().replace(tzinfo=UTC).astimezone(tzinfo)
    tomorrow = (now + timedelta(days=1)).replace(tzinfo=None)
    yesterday = (now - timedelta(days=1)).replace(tzinfo=None)
    prev_streams = LiveStream.query.filter(LiveStream.scheduled_time <= yesterday).all()
    current_stream = LiveStream.query.filter(LiveStream.scheduled_time > yesterday)\
        .filter(LiveStream.scheduled_time < tomorrow).first()
    next_stream = LiveStream.query.filter(LiveStream.scheduled_time > tomorrow).first()
    context = {
        'stream_general': get_setting('live-stream-general'),
        'stream_before': get_setting('live-stream-before'),
        'stream_after': get_setting('live-stream-after'),
        'stream_start': _get_datetime(get_setting('live-stream-start')),
        'time_now': datetime.utcnow(),
        'prev_streams': prev_streams,
        'current_stream': current_stream,
        'next_stream': next_stream
    }
    return render('live-stream.html', **context)
