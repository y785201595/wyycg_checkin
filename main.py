# -*- coding: utf-8 -*-
import os
import time
import requests
import json


def signin(url, cookie):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
        'Authorization': str(cookie),
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'n.cg.163.com',
        'Origin': 'https://cg.163.com',
        'Referer': 'https://cg.163.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Platform': '0'
    }

    result = requests.post(url = url, headers = header)
    return result


def getme(url, cookie):
    header = {
        'Host': 'n.cg.163.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Platform': '0',
        'Authorization': str(cookie),
        'Origin': 'https://cg.163.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cg.163.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5'
    }
    result = requests.get(url = url, headers = header)
    return result


def do_sign(i, cookie):
    sign_url = 'https://n.cg.163.com/api/v2/sign-today'
    current = 'https://n.cg.163.com/api/v2/client-settings/@current'
    autherror = False
    signerror = False
    sign_return = None
    me = None
    try:
        me = getme(current, cookie)
    except:
        message = f'第{i + 1}个账号验证失败！请检查Cookie是否过期！'
        autherror = True
        return message, autherror

    if me.status_code != 200 and not autherror:
        message = f'第{i + 1}个账号验证失败！请检查Cookie是否过期！'
        return message, True

    try:
        sign_return = signin(sign_url, cookie)
    except:
        message = f'第{i + 1}个账号签到失败，回显状态码为{sign_return.status_code}，具体错误信息如下：{sign_return.text}'
        signerror = True
        return message, signerror

    if sign_return.status_code == 200:
        message = f'第{i + 1}个账号签到成功！'
    elif not signerror:
        message = f'第{i + 1}个账号签到失败，回显状态码为{sign_return.status_code}，具体错误信息如下：{sign_return.text}'
        signerror = True

    return message, autherror or signerror


def main():
    if os.path.exists('config.json'):
        config = open('config.json').read()
    else:
        config = os.environ["CONFIG"]
    config = json.loads(config)

    success = []
    failure = []
    msg = ''
    cookies = [item['cookie'] for item in config]
    for i, cookie in enumerate(cookies):
        message, error = do_sign(i, cookie)
        if error:
            failure.append(cookie)
        else:
            success.append(cookie)
        msg += message + '\n'
        if i < len(config) - 1:
            sleep_time = 10
            print('睡眠 %d s' % sleep_time)
            time.sleep(sleep_time)
    infomsg = '''
今日签到结果如下：
成功数量：{0}/{2}
失败数量：{1}/{2}
具体情况如下：
{3}
网易云游戏自动签到脚本: https://github.com/shenmishajing-script/wyycg_checkin
    '''.format(len(success), len(failure), len(cookies), msg)

    print(infomsg)


if __name__ == "__main__":
    main()
