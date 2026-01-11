import requests
import json
import hashlib
import time
def get_zty_sign_url(base_url,method,payload):
    timestamp = str(int(time.time() * 1000))
    SIGNATURE_KEY = "eptim]q34imt5b]-q04i5q=fdkfjfsadlkjfasdfrt573df4pltoy]-pn965498d"
    sign_raw_string = f"{method}{base_url}{timestamp}{SIGNATURE_KEY}{payload}"
    sign = hashlib.md5(sign_raw_string.encode('utf-8')).hexdigest()
    final_url = f"{base_url}?sign={sign}&t={timestamp}"
    return final_url

def patch_brush_code(code, device_id):

    base_url = "https://ztp.yunzuoye.net/api/v2/pub/platform/brushCode"

    user_agent = f"com.xuehai.launcher/v1.21.06.20251212hwS (SM-P200; android; 9; {device_id})"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": user_agent
    }

    payload_dict = {
        "code": code,
        "deviceId": device_id
    }
    payload_data = json.dumps(payload_dict, separators=(',', ':'))
    
    method="PATCH"
    final_url=get_zty_sign_url(base_url,method,payload_data)
 
    try:
        response = requests.patch(final_url, headers=headers, data=payload_data)

        if response.status_code!=200 and response.status_code!=400:
            print("请求发生错误！")
            print(response.text)

        if response.status_code!=400:
            response.raise_for_status() 
        
        #print("响应内容:", response.text)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"{e}")
        return None

if __name__=="__main__":
    try_code = "100000"
    device_id = "Your own device id here."
    for i in range(100000,999999):
        try_code=str(i)
        result = patch_brush_code(try_code, device_id)
        if result['code']!=400:
            print(f'OK!!!!!!!!!{i}')
            break
        print(f'Tried.{i}')