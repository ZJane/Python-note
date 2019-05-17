import requests
import time
import json
import numpy
import math
import hashlib
class Lianjia():
    def __init__(self, city):
        self.city_dict = {
            '上海': {'city_id': '310000', 'max_lat': '31.36552', 'min_lat': '31.106158', 'max_lng': '121.600985',
                   'min_lng': '121.360095'},
            '北京': {'city_id': '110000', 'max_lat': '40.074766', 'min_lat': '39.609408', 'max_lng': '116.796856',
                   'min_lng': '115.980476'},
            '广州': {'city_id': '440100', 'max_lat': '23.296086', 'min_lat': '22.737277', 'max_lng': '113.773905',
                   'min_lng': '113.038013'},
            '深圳': {'city_id': '440300', 'max_lat': '22.935891', 'min_lat': '22.375581', 'max_lng': '114.533683',
                   'min_lng': '113.797791'},
            '长沙': {'city_id': '430100', 'max_lat': '28.368467', 'min_lat': '28.101143', 'max_lng': '113.155889',
                   'min_lng': '112.735051'},
            '烟台': {'city_id': '370600', 'max_lat': '37.590234', 'min_lat': '37.349651', 'max_lng': '121.698469',
                   'min_lng': '121.210365'},
            '厦门': {'city_id': '350200', 'max_lat': '24.794145', 'min_lat': '24.241819', 'max_lng': '118.533083',
                   'min_lng': '117.892627'}
        }
        self.city_id = self.city_dict[city]['city_id']
        self.city = city
        self.url_fang = 'https://ajax.lianjia.com/map/resblock/ershoufanglist/?callback=jQuery11110617424919783834_1541868368031' \
                        '&id=%s' \
                        '&order=0' \
                        '&page=%d' \
                        '&filters=%s' \
                        '&request_ts=%d' \
                        '&source=ljpc' \
                        '&authorization=%s' \
                        '&_=%d'
        self.url = 'https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery1111012389114747347363_1534230881479' \
                   '&city_id=%s' \
                   '&group_type=%s' \
                   '&max_lat=%s' \
                   '&min_lat=%s' \
                   '&max_lng=%s' \
                   '&min_lng=%s' \
                   '&filters=%s' \
                   '&request_ts=%d' \
                   '&source=ljpc' \
                   '&authorization=%s' \
                   '&_=%d'
        self.cookies = {'lianjia_uuid': '9bdccc1a-7584-4639-ba95-b42cf21bbbc7',
                        'jzqa': '1.3180246719396510700.1534145942.1534145942.1534145942.1',
                        'jzqckmp': '1',
                        'ga': 'GA1.2.964691746.1534145946',
                        'gid': 'GA1.2.826685830.1534145946',
                        'UM_distinctid': '165327625186a-029cf60b1994ee-3461790f-fa000-165327625199d3',
                        'select_city': '310000',
                        'lianjia_ssid': '34fc4efa-7fcc-4f3f-82ae-010401f27aa8',
                        '_smt_uid': '5b72c5f7.5815bcdf',
                        'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1537530243',
                        'select_city': '110000',
                        '_jzqc': '1',
                        '_gid': 'GA1.2.178601063.1541866763',
                        '_jzqb': '1.2.10.1541866760.1'

                        }
        self.headers = {
            'Host': 'ajax.lianjia.com',
            'Referer': 'https://sh.lianjia.com/ditu/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
    def GetMD5(self, string_):
        m = hashlib.md5()
        m.update(string_.encode('utf-8'))
        return m.hexdigest()
    def GetAuthorization(self, dict_) -> str:
        datastr = "vfkpbin1ix2rb88gfjebs0f60cbvhedlcity_id={city_id}group_type={group_type}max_lat={max_lat}" \
                  "max_lng={max_lng}min_lat={min_lat}min_lng={min_lng}request_ts={request_ts}".format(
            city_id=dict_["city_id"],
            group_type=dict_["group_type"],
            max_lat=dict_["max_lat"],
            max_lng=dict_["max_lng"],
            min_lat=dict_["min_lat"],
            min_lng=dict_["min_lng"],
            request_ts=dict_["request_ts"])
        authorization = self.GetMD5(datastr)
        return authorization
    def GetDistrictInfo(self) -> list:
        time_13 = int(round(time.time() * 1000))
        authorization = Lianjia(self.city).GetAuthorization(
            {'group_type': 'district', 'city_id': self.city_id, 'max_lat': self.city_dict[self.city]['max_lat'],
             'min_lat': self.city_dict[self.city]['min_lat'],
             'max_lng': self.city_dict[self.city]['max_lng'], 'min_lng': self.city_dict[self.city]['min_lng'],
             'request_ts': time_13})

        url = self.url % (
            self.city_id, 'district', self.city_dict[self.city]['max_lat'], self.city_dict[self.city]['min_lat'],
            self.city_dict[self.city]['max_lng'], self.city_dict[self.city]['min_lng'], '%7B%7D', time_13,
            authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

            house_json = json.loads(ret.text[43:-1])

            if house_json['errno'] == 0:

                return house_json['data']['list'].values()

            else:
                return None
    def GetCommunityInfo(self, max_lat, min_lat, max_lng, min_lng) -> list:
        time_13 = int(round(time.time() * 1000))
        authorization = Lianjia(self.city).GetAuthorization(
            {'group_type': 'community', 'city_id': self.city_id, 'max_lat': max_lat, 'min_lat': min_lat,
             'max_lng': max_lng, 'min_lng': min_lng, 'request_ts': time_13})

        url = self.url % (
            self.city_id, 'community', max_lat, min_lat, max_lng, min_lng, '%7B%7D', time_13, authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)
            house_json = json.loads(ret.text[43:-1])

            if house_json['errno'] == 0:
                data_list = []
                if type(house_json['data']['list']) is dict:
                    for x in house_json['data']['list']:
                        data_list.append(house_json['data']['list'][x])
                    return data_list
                else:
                    return house_json['data']['list']

            else:
                return None
    def GetHousingInfo(self, id, count) -> list:

        ll = []
        for page in range(1, math.ceil(count / 10) + 1):
            time_13 = int(round(time.time() * 1000))
            authorization = self.GetMD5(
                "vfkpbin1ix2rb88gfjebs0f60cbvhedlid={id}order={order}page={page}request_ts={request_ts}".format(
                    id=id, order=0, page=1, request_ts=time_13))
            # e = {id: "1111027380242", order: 0, page: 1, filters: "{}", request_ts: 1541871468249} 1b9f64bd353667b4e44ed593eca6451d
            ###############-----拼接请求url-----#################
            url = self.url_fang % (id, page, '%7B%7D', time_13, authorization, time_13)
            with requests.Session() as sess:
                ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

                house_json = json.loads(ret.text[41:-1])

                try:
                    for x in house_json['data']['ershoufang_info']['list']:
                        ll.append(house_json['data']['ershoufang_info']['list'][x])
                except:
                    print(house_json)

        return ll
