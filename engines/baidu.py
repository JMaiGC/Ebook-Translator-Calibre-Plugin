import re
import json
import random
import hashlib

from .. import _z
from ..exceptions.engine import IncorrectApiKeyFormat
from .base import Base, load_lang_codes
from .languages import baidu


load_translations()

lang_codes = load_lang_codes(baidu)


class BaiduTranslate(Base):
    name = 'Baidu'
    alias = _z('Baidu')
    lang_codes = lang_codes
    endpoint = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    api_key_hint = 'appid|appkey'
    api_key_rule = r'^[^\s:\|]+?[:\|][^\s:\|]+$'
    api_key_errors = ['54004']

    def translate(self, text):
        try:
            app_id, app_key = re.split(r'[:\|]', self.api_key)
        except Exception:
            raise IncorrectApiKeyFormat(self.api_key_error_message())

        salt = random.randint(32768, 65536)
        sign_str = app_id + text + str(salt) + app_key
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {
            'appid': app_id,
            'q': text,
            'from': self._get_source_code(),
            'to': self._get_target_code(),
            'salt': salt,
            'sign': sign
        }

        return self.get_result(self.endpoint, data, headers, method='POST')

    def parse(self, response):
        return json.loads(response)['trans_result'][0]['dst']
