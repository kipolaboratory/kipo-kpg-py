import time
import json
import requests
import webbrowser


class KipoKPG:
    merchant_key = ''

    __shopping_key = ''
    __referent_code = ''

    """
        Default headers
        don't change default values
        
        :var array
    """
    __headers = {
        "Accept": "application/json",
        "IP": "127.0.0.1",
        "OS": "web",
        "SC": "false",
        "SK": "'.'",
        "Content-Type": "application/json",
        "User-Agent": "kipopay-kpg-agent"
    }

    """
        Default post data parameters and keys

        :var array
    """
    __post_data = {
        "Command": {
            "Sign": ''
        },
        "OrderAt": '',
        "OrderID": "100000",
        "Profile": {
            "HID": "+989901001001",
            "SID": "00000000-0000-0000-0000-000000000000"
        },
        "Session": {
            '': ''
        },
        "Version": {
            "AID": "kipo1-alpha"
        },
        "RawData": {
        }
    }

    """
        Contain error code explanation

        :var array
    """
    ERROR_MESSAGE = {
        -1: "خطایی در داده‌های ارسالی وجود دارد،‌ لطفا اطلاعات را بررسی کنید و دوباره ارسال نمایید. (درخواست پرداخت)",
        -2: "امکان برقراری ارتباط با سرور کیپو میسر نمی‌باشد.",
        -3: "امکان برقراری ارتباط با سرور کیپو میسر نمی‌باشد.",
        -4: "خطایی در داده‌های ارسالی وجود دارد،"
            "‌ لطفا اطلاعات را بررسی کنید و دوباره ارسال نمایید. (بررسی تایید پرداخت)",
        -5: "پرداخت توسط کاربر لغو شده یا با مشکل مواجه شده است"
    }

    """
        Kipo server application url

        :var array
    """
    request_url = "https://backend.kipopay.com/V1.0/processors/json/"
    request_url_test = "https://kpg.kipopay.com:8091/V1.0/processors/json/"

    kipo_webgate_url = "http://webgate.kipopay.com/"

    def __init__(self, merchant_key):
        if merchant_key:
            self.merchant_key = merchant_key

    """
        Get two parameter for amount and call back url and send data
        to kipo server, retrieve shopping key to start payment, after
        shopping key received, render form must be called or create form
        manually
        
        :param amount
        :param callback_url
        :return dict
    """
    def kpg_initiate(self, amount, callback_url):
        post_data = self.__post_data
        post_data["Command"]["Sign"] = "KPG@KPG/Initiate"
        post_data["OrderAt"] = time.strftime("%Y%m%d%H%M%S")
        post_data['RawData'] = {
            "MerchantKy": self.merchant_key,
            "Amount": amount,
            "BackwardUrl": callback_url
        }

        s = requests.Session()
        req = requests.Request('POST', self.request_url, data=json.dumps(post_data), headers=self.__headers)
        prepped = req.prepare()

        try:
            resp = s.send(prepped,
                          verify=False,
                          cert=False,
                          timeout=10000,
                          )
        except:
            return {
                "status": False,
                "message": -3
            }

        response = json.loads(resp.text)

        if response['Outcome'] == "0000":
            shopping_key = response['RawData']['ShoppingKy']
            self.__shopping_key = shopping_key

            return {
                "status": True,
                "shopping_key": shopping_key
            }

        else:
            return {
                "status": False,
                "message": -1
            }

    """
        Send inquery request to kipo server and retrieve
        payment status, if response contain ReferingID, that
        payment was successfully
        
        :param shopping_key
        :return dict
    """
    def kpg_inquery(self, shopping_key):
        post_data = self.__post_data
        post_data["Command"]["Sign"] = "KPG@KPG/Initiate"
        post_data["OrderAt"] = time.strftime("%Y%m%d%H%M%S")
        post_data['RawData'] = {
            "ShoppingKy": shopping_key
        }

        s = requests.Session()
        req = requests.Request('POST', self.request_url, data=json.dumps(post_data), headers=self.__headers)
        prepped = req.prepare()

        try:
            resp = s.send(prepped,
                          verify=False,
                          cert=False,
                          timeout=10000,
                          )
        except:
            return {
                "status": False,
                "message": -3
            }

        response = json.loads(resp.text)

        if response['Outcome'] == "0000":
            self.__referent_code = response['RawData']['ReferingID']

            if self.__referent_code is not None:
                return {
                    "status": True,
                    "referent_code": self.__referent_code
                }

            return {
                "status": False,
                "message": -5
            }

        else:
            return {
                "status": False,
                "message": -4
            }

    """
        This function render a simple form to
        redirect user to kipo webgate with shopping key
        
        :param shopping_key
    """
    def render_form(self, shopping_key):
        f = open('form.html', 'w')
        html_form = """
            <form id="kipopay-gateway" method="post" action="{url}" style="display: none;">
                <input type="hidden" id="sk" name="sk" value="{shopping_key}"/>
            </form>
        <script language="javascript">document.forms['kipopay-gateway'].submit();</script>
        """.format(url=self.kipo_webgate_url, shopping_key=shopping_key)

        f.write(html_form)
        f.close()

        webbrowser.open_new_tab("form.html")

    """
        Retrieve to user shopping key property
        
        :return str
    """
    def get_shopping_key(self):
        return self.__shopping_key

    """
        Retrieve to user shopping key property
        
        :return str
    """
    def get_referent_code(self):
        return self.__referent_code

    """
        Retrieve error message
        
        :param error_code
        :return mixed|None
    """
    def get_error_message(self, error_code):
        return_error = None

        if isinstance(error_code, int):
            return_error = self.ERROR_MESSAGE[error_code]

        return return_error
