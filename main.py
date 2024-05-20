import base64
import json
import logging
import random
import string
import sys
import threading
import time

import loguru#type: ignore
import random_strings #type: ignore
import tls_client
import re as uwu
import fingerprint_gen

from kopeechka import MailActivations #type: ignore

logging.disable(sys.maxsize)

_hcop_api = 'hcopapi'
kopeechka = "kopeechka api"


class Solver:
    def __init__(self, _proxy_: str) -> None:
        self.session =tls_client.Session(client_identifier="chrome120")
        self._proxy_ = _proxy_
    def solve(self, site_key: str, captcha_rqdata: str) -> tuple:

        createTask_payload = {
            "task_type": "hcaptchaEnterprise",
            "api_key": _hcop_api,
            "data": {
                "sitekey": site_key,
                "url": "https://www.epicgames.com",
                "proxy": self._proxy_,
                "rqdata": captcha_rqdata,
            }
        }

        createTask = self.session.post("https://api.hcoptcha.online/api/createTask", json=createTask_payload)
        try:
            createTask_ = createTask.json()
            if createTask.status_code == 200:
                taskId = createTask_['task_id']
                loguru.logger.info("Task created", taskId)
            else:
                return None
        except Exception as e:
            print("Error, while creating task: ", e)

        while True:
            try:
                getTask_payload = {
                    "api_key": _hcop_api,
                    "task_id": str(taskId)
                }
                response = self.session.post("https://api.hcoptcha.online/api/getTaskData", json=getTask_payload)
                response_json = response.json()
                if response_json['task']['state'] == 'completed':
                    # loguru.logger.info(f"Task completed")
                    captcha_key = response_json['task']['captcha_key']
                    captcha_data_key = response_json['task']['captcha_data_key']
                    loguru.logger.info(f'Captcha solved {captcha_key[:50]}xxxx')
                    return captcha_key, captcha_data_key

                elif response_json['task']['state'] == 'processing':
                    pass
                elif response_json['task']['error']:
                    if 'Failed to solve' in response_json['task']['error']:
                        continue
                    else:
                        return None


            except Exception as e:
                #loguru.logger.info("Error, while getting task result: ", e)
                break


class EpicGenerator:
    def __init__(self) -> None:
        self.session = tls_client.Session(client_identifier="chrome_120",random_tls_extension_order=True)

        self.session.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US',
            'content-type': 'application/json',
            'origin': 'https://www.epicgames.com',
            'priority': 'u=1, i',
            'referer': 'https://www.epicgames.com/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="120", "Not-A.Brand";v="99"' #ok yoabi nigga u are the best coder in the world,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
        self.proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
        self.session.proxies = {'http': 'http://' + self.proxy.strip(), 'https': 'http://' + self.proxy.strip()}
        self.mailapi = MailActivations(api_token=kopeechka)

        maildata = self.mailapi.mailbox_get_email("epicgames.com", "hotmail.com")

        self.email = maildata.mail
        self.emailid = maildata.id
        self.password = random.choice(string.ascii_uppercase)+random.choice(string.ascii_lowercase)+random.choice(string.digits)+random_strings.random_string(5)



    def solve_hcaptcha(self, captcha_data: dict) -> tuple:
        solver = Solver(self.proxy)

        while True:
            try:
                captcha_key, captcha_data_key = solver.solve(captcha_data["site_key"], captcha_data["rqdata"]) # create task
                break
            except Exception as e:
                loguru.logger.info("Error, while solving captcha, retrying: ", e)
                continue

        return captcha_key, captcha_data_key

    def get_epic_session(self) -> dict: # returns epic games session data
        while True:
            try:
                response = self.session.get('https://www.epicgames.com/id/register')
                break
            except Exception as e:
                loguru.logger.info("Error, while getting session: ", e)
                continue

        self.session.headers['accept'] = 'application/json, text/plain, */*' # change headers for json

        json_data = {
            'eventType': 'APP_INIT',
        }

        while True:
            try:
                response = self.session.post('https://www.epicgames.com/id/api/analytics',
                                 json=json_data) #for getting x-xsrf-token
                break
            except Exception as e:
                loguru.logger.info("Error, while getting x-xsrf-token: ", e)
                continue

        self.session.headers['x-xsrf-token'] = self.session.cookies['XSRF-TOKEN']

        json_data = {
            'flow_id': 'email_exists_prod',
        }

        while True:
            try:
                response = self.session.post(
            'https://talon-service-prod.ecosec.on.epicgames.com/v1/init',
            json=json_data,
        ) # get session info
                break
            except Exception as e:
                loguru.logger.info("Error, while getting session info: ", e)
                continue

        return response.json()
    def get_hcaptcha_rqdata(self, response: dict) -> dict: # response is hcaptcha rqdata
        json_data = {
            'session': {
                'session': {
                    'version': response['session']['version'],
                    'id': response['session']['id'],
                    'flow_id': response['session']['flow_id'],
                    'ip_address': response['session']['ip_address'],
                    'timestamp': response['session']['timestamp'],
                    'plan': {
                        'mode': response['session']['plan']['mode'],
                        'h_captcha': {
                            'plan_name': response['session']['plan']['h_captcha']['plan_name'],
                            'site_key': response['session']['plan']['h_captcha']['site_key'],
                        },
                    },
                    'config': {
                        'h_captcha_config': {
                            'sdk_base_url': response['session']['config']['h_captcha_config']['sdk_base_url'],
                        },
                    },
                },
                'signature': response['signature'],
            },
            'v': 1,
            'xal': fingerprint_gen.create_fingerprint(), #create fingerprint
            'ewa': 'b', # always same
            'kid': 'aRAejw' # always same
        }

        while True:
            try:
                resp = self.session.post(
            'https://talon-service-prod.ecosec.on.epicgames.com/v1/init/execute',
            json=json_data,
        ) # get hcaptcha rqdata
                break
            except Exception as e:
                loguru.logger.info("Error, while getting hcaptcha rqdata: ", e)
                continue

        loguru.logger.info(f"Got hcaptcha rqdata: {resp.json()['h_captcha']['data'][:50]}..")
        return {"rqdata":resp.json()["h_captcha"]["data"] ,"site_key":response['session']['plan']['h_captcha']['site_key']}
    def enter_mail(self, captcha_token: str, captcha_data_key: str, response: dict) ->bool: # email is email, captcha_solution is hcaptcha solution
        captcha_to_send = {
           "session_wrapper":{
              "session":{
                 "version":1,
                 "id":response['session']['id'],
                 "flow_id":"email_exists_prod",
                 "ip_address":response['session']['ip_address'],
                 'timestamp': response['session']['timestamp'],
                 "plan":{
                    "mode":"h_captcha",
                    "h_captcha":{
                       "plan_name":response['session']['plan']['h_captcha']['plan_name'],
                       "site_key":response['session']['plan']['h_captcha']['site_key']
                    }
                 },
                 "config":{
                    "h_captcha_config":{
                       "sdk_base_url":"https://js.hcaptcha.com"
                    }
                 }
              },
              "signature":response['signature']
           },
           "plan_results":{
              "h_captcha":{
                 "value":captcha_token,
                 "resp_key":captcha_data_key
              }
           },
           "v":1,
           "xal":fingerprint_gen.create_fingerprint(),
           "ewa":"b",
           "kid":"aRAejw"
        }

        data = base64.b64encode(json.dumps(captcha_to_send).encode()).decode()



        json_data = {
            'email': self.email,
            'captcha': data,
        }
        while True:
            try:
                response = self.session.post('https://www.epicgames.com/id/api/email/exists',
                                 json=json_data)
                break
            except Exception as e:
                loguru.logger.info("Error, while entering email: ", e)
                continue

        if response.status_code == 204:
            loguru.logger.info(f"Entered email: {self.email}, response of request: {response.status_code}, {response.text}")
            return True
        else:
            loguru.logger.error(
                f"Entered email: {self.email}, response of request: {response.status_code}, {response.text}")
            return False

    def complete_register(self):
        json_data = {
            'flow_id': 'registration_prod',
        }

        while True:
            try:
                response = self.session.post(
            'https://talon-service-prod.ecosec.on.epicgames.com/v1/init',
            json=json_data,
        ).json()
                break
            except Exception as e:
                loguru.logger.info("Error, while getting session info: ", e)
                continue


        rqdata = self.get_hcaptcha_rqdata(response)
        captcha_token, captcha_data_key = self.solve_hcaptcha(rqdata)

        captcha_to_send = {
            "session_wrapper": {
                "session": {
                    "version": 1,
                    "id": response['session']['id'],
                    "flow_id": "registration_prod",
                    "ip_address": response['session']['ip_address'],
                    'timestamp': response['session']['timestamp'],
                    "plan": {
                        "mode": "h_captcha",
                        "h_captcha": {
                            "plan_name": response['session']['plan']['h_captcha']['plan_name'],
                            "site_key": response['session']['plan']['h_captcha']['site_key']
                        }
                    },
                    "config": {
                        "h_captcha_config": {
                            "sdk_base_url": "https://js.hcaptcha.com"
                        }
                    }
                },
                "signature": response['signature']
            },
            "plan_results": {
                "h_captcha": {
                    "value": captcha_token,
                    "resp_key": captcha_data_key
                }
            },
            "v": 1,
            "xal": fingerprint_gen.create_fingerprint(),
            "ewa": "b",
            "kid": "aRAejw"
        }

        data = base64.b64encode(json.dumps(captcha_to_send).encode()).decode()

        register_json_data = {
            'country': 'TR',
            'name': random_strings.random_string(6),
            'lastName': random_strings.random_string(6),
            'displayName': random_strings.random_string(15),
            'email': self.email,
            'password': self.password,
            'captcha': data,
            'createdForClientId': '875a3b57d3a640a6b7f9b4e883463ab4',
            'dateOfBirth': f'{random.randint(1990,2000)}-0{random.randint(1,8)}-{random.randint(10,20)}',
        }
        while True:
            try:
                response = self.session.post('https://www.epicgames.com/id/api/account',
                                 json=register_json_data)
                break
            except Exception as e:
                loguru.logger.info("Error, while registering: ", e)
                continue


        loguru.logger.info(f"[{self.email}] sent mail code")

        while True:

            try:
                code= self.mailapi.mailbox_get_message(self.emailid, 1).fullmessage.split('letter-spacing: 10px !important;border-radius: 4px;">')[1].split('<br>')[0].strip()
                
                loguru.logger.success(f"Got mail code: {code}")
                break
            except Exception as E:

                time.sleep(1)
        json_data = {
            'verificationCode': code,
        }
        while True:
            try:
                response = self.session.post('https://www.epicgames.com/id/api/email/verify',
                                 json=json_data)
                break
            except Exception as e:
                loguru.logger.info("Error, while verifying email: ", e)
                continue

        loguru.logger.info(f"[{response.status_code}] - {self.email} - mail verified")

        register_json_data["optInChecked"] = True


        while True:
            try:
                response = self.session.post('https://www.epicgames.com/id/api/account',json=register_json_data)
                break
            except Exception as e:
                loguru.logger.info("Error, while completing registration: ", e)
                continue


        params = {
            'redirectUrl': 'https://store.epicgames.com/en-US/',
            'clientId': '875a3b57d3a640a6b7f9b4e883463ab4',
        }

        while True:
            try:
                response = self.session.get('https://www.epicgames.com/id/api/redirect', params=params, allow_redirects=True)
                break
            except Exception as e:
                loguru.logger.info("Error, while redirecting: ", e)
                continue

        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=0, i',
            'referer': 'https://www.epicgames.com/id/register/epic?lang=tr&redirect_uri=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F&client_id=875a3b57d3a640a6b7f9b4e883463ab4',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        params = {
            'sid': response.json()["sid"],
        }

        while True:
            try:
                response = self.session.get('https://www.epicgames.com/id/api/sso', params=params, allow_redirects=True)

                break
            except Exception as e:
                loguru.logger.info("Error, while getting sso: ", e)
                continue


    def get_that_code_nigga(self):

        while True:
            try:
                response = self.session.get('https://store.epicgames.com/en-US/p/discord--discord-nitro')
                break
            except Exception as e:
                loguru.logger.info("Error, while getting nitro code : ", e)
                continue

        accountId = response.text.split('["identityId","')[1].split('"')[0]

        self.session.headers['accept'] = 'application/json, text/plain, */*'

        json_data = {
            'query': 'mutation acceptEulaMutation($eulaId: String!, $accountId: String!, $version: Int!, $locale: String!) {\n  Eula {\n    acceptEula(\n      id: $eulaId\n      accountId: $accountId\n      locale: $locale\n      version: $version\n    ) {\n      key\n      accepted\n    }\n  }\n}\n',
            'variables': {
                'eulaId': 'egstore',
                'locale': 'en',
                'version': 4,
                'accountId': accountId,
            },
        }

        while True:
            try:
                response = self.session.post('https://store.epicgames.com/graphql',
                                 json=json_data)
                break
            except Exception as e:
                loguru.logger.info("Error, while accepting eula: ", e)
                continue


        self.session.headers['accept'] =  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'

        params = {
            'highlightColor': '0078f2',
            'offers': '1-5f3c898b2a3244af99e9900e015717f8-55ba24c34b87463a966d186f26835665-',
            'showNavigation': 'true',
        }

        while True:
            try:

                response = self.session.get('https://store.epicgames.com/purchase', params=params)
                break
            except Exception as e:
                loguru.logger.info("Error, while purchasing nitro: ", e)
                continue


        order_id = response.text.split('"orderId":"')[1].split('"')[0]
        loguru.logger.success(f"Purchased nitro, order id: {order_id}")


        resp = self.mailapi.mailbox_reorder("epicgames.com", self.email)
        emailid = resp.id
        loguru.logger.warning(f"[{self.email}] waiting for nitro gift code")
        while True:

            try:
                code= self.mailapi.mailbox_get_message(emailid, 1).fullmessage.split('<p style="text-align:center;"> <a href="')[1].split('"')[0]
                loguru.logger.success(f"Got nitro code: {code}")
                open("nitro.txt", "a").write(f"{code}\n")

                break
            except Exception as E:

                time.sleep(1)

def handle_threads():
    gen = EpicGenerator()
    response = gen.get_epic_session()
    rqdata = gen.get_hcaptcha_rqdata(response)
    captcha_token, captcha_data_key = gen.solve_hcaptcha(rqdata)


    x = gen.enter_mail(captcha_token, captcha_data_key, response)
    if x:

        gen.complete_register()
        gen.get_that_code_nigga()

def loop():
    #keep creating accs
    while True:
        try:
            handle_threads()
        except Exception as e:
            loguru.logger.exception(e)


threads = input("thread count >")
for i in range(int(threads)):
    t = threading.Thread(target=loop).start()
