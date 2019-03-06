from common.redis import rds
from common.captcha.captcha import captcha

def get_image_code(image_code_id):
    """
    获取图片验证码
    :return: 验证码图片
    """
    name, text, image_data = captcha.generate_captcha()
    try:
        rds.setex("image_code_%s" % image_code_id, 180, text)
    except Exception as e:
        print(e)
    # print(name, text, image_data)
    return name, text, image_data






if __name__ == "__main__":
    get_image_code(2)