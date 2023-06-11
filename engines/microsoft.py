import json
import base64
from datetime import datetime

from .languages import microsoft
from .base import load_lang_codes, Base


try:
    from urllib.parse import urlencode
except ImportError:
     from urllib import urlencode

load_translations()

lang_codes = load_lang_codes(microsoft)


class MicrosoftEdgeTranslate(Base):
    name = 'MicrosoftEdge(Free))'
    alias = 'Microsoft Edge (Free)'
    lang_codes = lang_codes
    endpoint = 'https://api-edge.cognitive.microsofttranslator.com/translate'
    need_api_key = False
    access_info = None

    def normalized_endpoint(self):
        query = {
            'to': self._get_target_code(),
            'api-version': '3.0',
            'includeSentenceLength': True,
        }
        if not self._is_auto_lang():
            query['from'] = self._get_source_code()
        return '%s?%s' % (self.endpoint, urlencode(query))

    def parse_jwt(self, token):
        parts = token.split(".")
        if len(parts) <= 1:
            raise Exception(_('Failed get APP key due to an invalid Token.'))
        base64_url = parts[1]
        if not base64_url:
            raise Exception(
                _('Failed get APP key due to and invalid Base64 URL.'))
        base64_url = base64_url.replace('-', '+').replace('_', '/')
        json_payload = base64.b64decode(base64_url + '===').decode('utf-8')
        parsed = json.loads(json_payload)
        expired_date = datetime.fromtimestamp(parsed['exp'])
        return {'Token': token, 'Expire': expired_date}

    def get_app_key(self):
        if not self.access_info or datetime.now() > self.access_info['Expire']:
            auth_url = 'https://edge.microsoft.com/translate/auth'
            app_key = self.get_result(
                auth_url, callback=lambda result: result, method='GET')
            self.access_info = self.parse_jwt(app_key)
        else:
            app_key = self.access_info['Token']
        return app_key

    def translate(self, text):
        headers = {
            'Content-Type': 'application/json',
            'authorization': 'Bearer %s' % self.get_app_key()
        }

        data = json.dumps([{'text': text}])

        return self.get_result(
            self.normalized_endpoint(), data, headers, method='POST')

    def parse(self, response):
        return json.loads(response)[0]['translations'][0]['text']
