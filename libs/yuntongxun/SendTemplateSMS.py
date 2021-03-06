#coding=utf-8


from libs.yuntongxun.CCPRestSDK import REST
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
import configparser

#主帐号
accountSid= '8a216da8653147e60165409ffcbd08ad';

#主帐号Token
accountToken= 'f0da165d19e349deaeee5fda3867cec7';

#应用Id
appId='8a216da8653147e60165409ffd0708b3';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id


class CCP(object):
    # 用来保存对象的类属性
    instance = None
    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存，如果有，则将保存的对象直接返回
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            cls.instance = obj

            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
        return cls.instance



    def send_template_sms(self, to, datas, temp_id):
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        for k, v in result.items():

            if k == 'templateSMS':
                for k, s in v.items():
                    print('%s:%s' % (k, s))
            else:
                print('%s:%s' % (k, v))
        if result.get('statusCode') == '000000':
            return 0
        else:
            return -1

    

    

    
if __name__ == "__main__":
    ccp = CCP()
    ret = ccp.send_template_sms('13168277007',['12','34'],1)
    print(ret)