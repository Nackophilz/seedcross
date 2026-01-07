from email.policy import default
from django import forms
from .models import CLIENT_TYPES, INDEXER_TYPES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML, Div
from crispy_forms.bootstrap import PrependedText
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import pytz

class ParamSettingForm(forms.Form):
    client_type = forms.ChoiceField(label=_('Type'), choices=CLIENT_TYPES)
    client_host = forms.GenericIPAddressField(label=_('Host'))
    client_port = forms.IntegerField(label=_('Port'))
    client_username = forms.CharField(label=_('Username'), required=False)
    client_password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(render_value=True), required=False)
    include_cjk = forms.BooleanField(label=_('Search CJK title'),  required=False)
    category_indexers = forms.BooleanField(label=_('Category indexers'),  required=False)
    indexer_movie = forms.CharField(label=_('Movie/TV indexers'),  required=False)
    indexer_tv = forms.CharField(label=_('Movie/TV indexers'),  required=False)
    indexer_music = forms.CharField(label=_('Music indexers'),  required=False)
    indexer_ebook = forms.CharField(label=_('eBook indexers'),  required=False)
    indexer_audio = forms.CharField(label=_('Audio indexers'),  required=False)
    indexer_other = forms.CharField(label=_('Other(Unknown) indexers'),  required=False)
    jackett_prowlarr = forms.ChoiceField(label=_('Jackett or Prowlarr'), choices=INDEXER_TYPES)
    jackett_url = forms.URLField(label=_('Jackett/Prowlarr Url'))
    jackett_api_key = forms.CharField(label=_('Jackett/Prowlarr Api key'))
    jackett_trackers = forms.CharField(label=_('Tracker / Indexer'),  required=False)
    fc_count = forms.IntegerField(label=_('Flow control: Count limit'))
    fc_interval = forms.IntegerField(label=_('Flow control: Interval'))
    cyclic_reload = forms.BooleanField(label=_('Cycle run'),  required=False)
    reload_interval_min = forms.IntegerField(label=_('Cycle run interval (minutes)'), required=False)
    max_size_difference = forms.IntegerField(label=_('Max size difference (bytes) when compare torrents.'), required=False)
    map_from_path = forms.CharField(label=_('Map From: Download client(QB/Tr/De) path'), required=False)
    map_to_path = forms.CharField(label=_('Map to: seedcross path'), required=False)
    language = forms.ChoiceField(label=_('Language'), choices=settings.LANGUAGES, required=False)
    timezone = forms.ChoiceField(label=_('Timezone'), choices=[(tz, tz) for tz in pytz.common_timezones], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            HTML("""
            <p><strong>{}</strong></p>
            """.format(_("General Setting"))),
            Field('language'),
            Field('timezone'),
            HTML("""
            <p><strong>{}</strong></p>
            """.format(_("Download Client Setting"))),
            Field('client_type'), 
            Row(
                Column(Field('client_host',
                             placeholder='only IP addr'),
                       css_class='form-group col-md-8 mb-0'
                       ),
                Column(PrependedText('client_port', ':', placeholder="Port"),
                       css_class='form-group col-md-4 mb-0'
                       ),
                # Column('client_port', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(Column('client_username',
                       css_class='form-group col-md-6 mb-0'
                       ),
                Column('client_password',
                       css_class='form-group col-md-6 mb-0'
                       ),
                css_class='form-row'),

            HTML("""
            <p><strong>{}</strong></p>
            """.format(_("Jackett/Prowlarr Setting"))),
            Field('jackett_prowlarr',
                  placeholder=_('Jackett or Prowlarr')),
            Field('jackett_url',
                  placeholder=_('ex. http://jackett/prowlarr.server.ip:9117/')),
            Field('jackett_api_key',
                  placeholder=_('copy from jackett/prowlarr web ui')),
            Field('jackett_trackers',
                  placeholder=_('leave blank to search all configured indexers')),
            HTML("""
            <p><strong>{}</strong></p>
            """.format(_("Search options"))),
            # TODO: shoud this be configurable
            Field('max_size_difference', placeholder=_("max size difference (in bytes)")),
            Field('include_cjk'),
            Field('category_indexers', id='check_id'),
            Div(
                Field('indexer_movie'),
                Field('indexer_tv'),
                Field('indexer_music'),
                Field('indexer_ebook'),
                Field('indexer_audio'),
                Field('indexer_other'),
                css_id='CategoryIndexers', 
            ), 
            HTML("""
            <p><strong>{}</strong></p>
            """.format(_("Flow Control Setting"))),
            Row(Column(Field('fc_count'),
                       css_class='form-group col-md-6 mb-0'),
                Column(Field('fc_interval'),
                       css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            HTML("""
            <p><strong>{}</strong></p>
            """.format(_("Cycle run options"))),
            Field('cyclic_reload'),
            Field('reload_interval_min'),
            HTML("""
            <p><strong>{}</strong> {}</p>
            """.format(_("Fix options"), _("(required: your download client is running on the same machine as seedcross)"))),
            Row(Column(Field('map_from_path'),
                       css_class='form-group col-md-6 mb-0'),
                Column(Field('map_to_path'),
                       css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
        )
        self.helper.add_input(
            Submit('submit', _('Save Settings'), css_class='btn-primary'))
        self.helper.form_method = 'POST'
