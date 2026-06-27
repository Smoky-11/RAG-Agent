import os
import time
import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from utils.logger_handler import logger
import random
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

PRIVATE_KEY_PEM=os.getenv("PRIVATE_KEY_PEM","").encode()
KID=os.getenv("KID","")
SUB=os.getenv("SUB","")
API_HOST=os.getenv("API_HOST","")

IP_API_URL="http://ip-api.com/json/"


def generate_jwt():
    """生成长效JWT (例如有效期10分钟，最高24小时)"""
    # 加载PEM格式的私钥
    private_key = serialization.load_pem_private_key(PRIVATE_KEY_PEM, password=None)
    if not isinstance(private_key, Ed25519PrivateKey):
        raise TypeError("私钥必须为Ed25519格式")

    # 设置JWT的payload (有效期最长24小时)
    now = int(time.time())
    payload = {
        "sub": SUB,
        "iat": now - 30,        # 签发时间，可略早于当前时间
        "exp": now + 600        # 过期时间，600秒 = 10分钟
    }
    headers = {"alg": "EdDSA", "kid": KID}
    
    # 生成并返回JWT字符串
    return jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)


def get_location_by_ip():
    try:
        response = requests.get(IP_API_URL, timeout=5)
        data = response.json()
        
        if data.get("status") == "success":
            city = data.get("city", "")
            # 处理直辖市后缀（如 "北京市" -> "北京"）
            city = city.replace("市", "")
            logger.info(f"IP定位成功: {city}")
            return city
        else:
            logger.warning(f"IP定位失败: {data.get('message', '未知错误')}")
            return random.choice(["广州", "北京", "上海"])  # 降级使用随机城市
    except Exception as e:
        logger.error(f"IP定位异常: {e}")
        return random.choice(["广州", "北京", "上海"])


def get_weather_now(city_name: str) -> str:
    """自动生成JWT并查询实时天气"""
    try:
        # 1. 在函数调用时自动生成一个新的JWT
        jwt_token = generate_jwt()
        
        # 2. 使用这个新生成的Token调用API
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept-Encoding": "gzip"
        }
        
        # 第一步：城市查询
        geo_url = f"https://{API_HOST}/geo/v2/city/lookup"
        geo_params = {"location": city_name}
        geo_response = requests.get(geo_url, headers=headers, params=geo_params)
        geo_response = requests.get(geo_url, headers=headers, params=geo_params)
        
        # 打印调试信息，查看实际返回状态和内容
        print(f"GeoAPI Status: {geo_response.status_code}")
        #print(f"GeoAPI Response Text: {geo_response.text}")
            
        if geo_response.status_code != 200:
            return logger.error(f"城市查询接口请求失败，HTTP状态码: {geo_response.status_code}")
                
        geo_data = geo_response.json()
            
        if geo_data.get("code") != "200":
            return logger.error(f"查询城市失败：{geo_data.get('message', '未知错误')}")
            
        if not geo_data.get("location"):
            return logger.error(f"未找到城市: {city_name}")
            
        # 获取第一个匹配城市的ID
        city_info = geo_data["location"][0]
        city_id = city_info["id"]
        city_full_name = f"{city_info.get('country', '')} {city_info.get('adm1', '')} {city_info.get('name', '')}".strip()
            
        # 第二步：根据城市ID查询实时天气 (使用修正后的路径)
        weather_url = f"https://{API_HOST}/v7/weather/now"
        weather_params = {"location": city_id}
        weather_response = requests.get(weather_url, headers=headers, params=weather_params)
        weather_data = weather_response.json()
        
        if weather_data.get("code") != "200":
            return logger.error(f"查询天气失败：{weather_data.get('message', '未知错误')}")
        
        # 提取关键天气信息
        now = weather_data["now"]
        result = f"""
        🌤️ {city_full_name} 实时天气
        温度：{now['temp']}°C       体感温度：{now['feelsLike']}°C
        天气状况：{now['text']}      湿度：{now['humidity']}%
        风向：{now['windDir']} {now['windScale']}级      
        更新时间：{weather_data.get('updateTime', 'N/A')}
        """
        logger.info(f"Token生成成功，已调用API查询{city_name}天气。\nJWT: {jwt_token[:50]}...")
        return result.strip()
    

    except requests.exceptions.RequestException as e:
        return logger.error(f"网络请求出错：{str(e)}")
    except ValueError as e:
        # 捕获JSON解析错误，并打印原始响应内容
        return logger.error(f"解析返回数据失败，请检查API认证是否有效。错误：{str(e)}")
    except Exception as e:
        return logger.error(f"调用天气API出错：{str(e)}")
    

if __name__ == "__main__":
    print(get_location_by_ip())