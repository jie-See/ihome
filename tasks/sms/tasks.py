from tasks.main import celery_app
from libs.yuntongxun.SendTemplateSMS import CCP


@celery_app.task(name='ihome.tasks.sms.tasks.send_sms')
def send_sms(to, datas, temp_id):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)
