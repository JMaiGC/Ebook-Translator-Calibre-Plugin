import json
import random
import hashlib

from calibre_plugins.ebook_translator.engines.base import Base


load_translations()


class BaiduTranslate(Base):
    name = 'Baidu'
    support_lang = 'baidu.json'
    endpoint = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    api_key_hint = 'appid:appkey'
    api_key_validate = r'^\d+:[a-zA-Z\d]+$'

    @Base._translate
    def translate(self, text):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            app_id, app_key = self.api_key.split(':')
        except Exception:
            raise Exception(_('Incorrect format of APP id and key.'))

        salt = random.randint(32768, 65536)
        sign_str = app_id + text + str(salt) + app_key
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

        data = {
            'appid': app_id,
            'q': text,
            'from': self._get_source_lang_code(),
            'to': self._get_target_lang_code(),
            'salt': salt,
            'sign': sign
        }

        return self.request(data, method='POST', headers=headers)

    def parse(self, response):
        return json.loads(response)['trans_result'][0]['dst']