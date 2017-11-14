#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : YuLuo

# 发送邮件工具类
import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
from Constants import from_email ,email_password ,to_email ,smtp_server
from Utils.Logger import Logger
logger = Logger('scheduler').getLog()
def sendEmail(sendContent):
    ret = True
    try:
        msg = MIMEText(sendContent, 'plain', 'utf-8')
        msg['From'] = formataddr(["", from_email])
        msg['To'] = formataddr(["", to_email])
        msg['Subject'] = "ip代理池"

        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_email, email_password )
        server.sendmail(from_email, [to_email, ], msg.as_string())
        server.quit()
    except Exception:
        ret = False

    if ret:
        logger.info('email send success !')
    else:
        logger.error('email send fail !')
