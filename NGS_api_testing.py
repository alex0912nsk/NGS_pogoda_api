import requests
import unittest
from dataprovider import data_provider


class TestServerFunctionality(unittest.TestCase):
    def url_with_parametrs(self, url, param, value):
        if url.find('?') != -1:
            url = url + '&' + param + '=' + str(value)
        else:
            url = url + '?' + param + '=' + str(value)
        return url

    parametrs = lambda: (
        ('http://pogoda.ngs.ru/api/v1/cities', 200, 'get'),
        ('http://pogoda.ngs.ru/api/v1/cities/novosibirsk', 200, 'get'),
        ('http://pogoda.ngs.ru/api/v1/cities/novosibirsk', 404, 'delete'),
        ('http://pogoda.ngs.ru/api/v1/forecasts/current', 400, 'get'))

    @data_provider(parametrs)
    def test_response_code(self, url, code, metod):
        if metod == 'get':
            r = requests.get(url)
        elif metod == 'post':
            r = requests.delete(url)
        elif metod == 'put':
            r = requests.delete(url)
        elif metod == 'delete':
            r = requests.delete(url)
        else:
            print('rewrite metod')
            return
        self.assertEqual(code, r.status_code)

    def test_limit(self):
        limit = 10
        url = 'http://pogoda.ngs.ru/api/v1/cities'

        limit_url = self.url_with_parametrs(url, 'limit', limit)
        r = requests.get(limit_url)

        r.json()['cities'][limit - 1]
        with self.assertRaises(IndexError):
            r.json()['cities'][limit]

    def test_offset(self):
        url = 'http://pogoda.ngs.ru/api/v1/cities'
        offset = 50

        count = requests.get(url).json()['metadata']['resultset']['count']
        offset_url = self.url_with_parametrs(url, 'offset', offset)

        self.assertEqual(requests.get(url).json()['cities'][offset]['id'],
                         requests.get(offset_url).json()['cities'][0]['id'])
        with self.assertRaises(IndexError):
            requests.get(offset_url).json()['cities'][count - offset]['id']
        self.assertEqual(requests.get(self.url_with_parametrs(url, 'offset', count)).json()['errors']['message'],
                         "города не найдены")

    parametrs = lambda: (
        ('id', 'int', 3, 3, ''),
        ('alias', 'str', 3, 19, ''),
        ('region', 'int', 1, 4, ''),
        ('title', 'str', 2, 24, ''),
        ('title_dative', 'str', 2, 26, ''),
        ('name', 'str', 3, 23, ''),
        ('title_prepositional', 'str', 2, 26, ''),
        ('timezone', 'str', 3, 20, ''),
        ('url', 'str', 19, 47, 'http://pogoda.'),
        ('mobile_url', 'str', 14, 42, 'm.pogoda.'))

    @data_provider(parametrs)
    def test_parapetr_cities(self, parametr, value, lengthmin, lengthmax, startstr):
        global parametrval, i
        url = 'http://pogoda.ngs.ru/api/v1/cities'
        count = requests.get(url).json()['metadata']['resultset']['count']
        try:
            for i in range(0, count):
                parametrval = requests.get(url).json()['cities'][i][parametr]
                if value == 'int':
                    self.assertTrue(str(parametrval).isdigit)
                elif value == 'str':
                    self.assertTrue(parametr.isalpha)
                self.assertGreaterEqual(len(str(parametrval)), lengthmin)
                self.assertLessEqual(len(str(parametrval)), lengthmax)
                self.assertTrue(str(parametrval).startswith(startstr))
        except:
            print('№' + str(i) + '(' + requests.get(url).json()['cities'][i]['title'] + ' - ' + parametr + ':' + str(
                parametrval) + ')')
            self.fail('test_parametr_cities is failed')


if __name__ == '__main__':
    unittest.main()
