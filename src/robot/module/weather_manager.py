# -*- coding:utf8 -*-
__author__ = 'changyuf'

import requests
import xml.etree.ElementTree as ET
from robot.utility.utilities import to_str


class WeatherManager:
    def __init__(self):
        pass

    @staticmethod
    def get_weather_message():
        #response = requests.get("http://api.k780.com:88/?app=weather.today&weaid=101010100&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json")
        #response = requests.get("http://apistore.baidu.com/microservice/weather?cityid=101010100")
        response = requests.get("http://wthrcdn.etouch.cn/WeatherApi?citykey=101010100")
        #response = requests.get("http://wthrcdn.etouch.cn/weather_mini?citykey=101010100")
        #response = requests.get("http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101010100")
        #print response.content
        message = ""
        root = ET.fromstring(response.content)
        city = root.find("city").text
        message += "城市：%s\\n" % to_str(city)
        current_temp = root.find("wendu").text
        message += "当前温度：%s\\n" % current_temp
        wind_force = root.find("fengli").text
        message += "风力: %s\\n" % to_str(wind_force)
        wind_direction = root.find("fengxiang").text
        message += "风向: %s\\n" % to_str(wind_direction)
        humidity = root.find("shidu").text
        message += "湿度：%s\\n" % to_str(humidity)

        forecast = root.find("forecast")
        today = forecast[0]
        temp_high = today.find("high").text
        temp_low = today.find("low").text
        message += "气温：%s, %s\\n" % (to_str(temp_low), to_str(temp_high))
        #message += "最高气温：%s\n" % to_str(temp_high)
        day_type = today.find("day").find("type").text
        night_type = today.find("night").find("type").text
        message += "白天：%s, 晚间：%s\\n" % (to_str(day_type), to_str(night_type))

        environment = root.find("environment")
        aqi = environment.find("aqi").text
        pm25 = environment.find("pm25").text
        quality = environment.find("quality").text

        message += "空气指数：%s, PM2.5:%s\\n空气质量：%s\\n" % (to_str(aqi), to_str(pm25), to_str(quality))

        updatetime = root.find("updatetime").text
        message += "更新时间：%s\\n" % updatetime

        return message


if __name__ == "__main__":
    WeatherManager.get_weather_message()


