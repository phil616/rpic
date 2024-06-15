"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

from requests import post,get
from loguru import logger
from conf import BASEURL
import streamlit as st
class _HTTP:
    def __init__(self,baseurl=BASEURL):
        self.headers = {}
        self.base = baseurl
    def json_post(self,url,data):
        try:
            logger.info(f"Posting to {url} with data: {data}")
            p = post(self.base+url,json=data,headers=self.headers)
            logger.info(f"Posting to {url} with data: {data} RAW:{p.request.body}")
            logger.info(f"Posting response: {p.text}")
            return p
        except Exception as e:
            logger.error(f"Error posting to {url} with data: {data}")
            st.toast(f"Error posting to {url} with data: {data} {e}")
    def data_post(self,url,data):
        try:
            logger.info(f"Posting to {url} with data: {data}")
            p = post(self.base+url,data=data,headers=self.headers)
            logger.info(f"Posting response: {p.text}")
            return p
        except Exception as e:
            logger.error(f"Error posting to {url} with data: {data}")
            st.toast(f"Error posting to {url} with data: {data} {e}")
    def get(self,url):
        try:
            logger.info(f"Getting from {url}")
            p = get(self.base + url,headers=self.headers)
            logger.debug(f"Getting response {p.text}")
            return p
        except Exception as e:
            logger.error(f"Error getting from {url}")
            st.toast(f"Error getting from {url} {e}")
    def update_headers(self,headers:dict):
        logger.info(f"Updating headers to {headers}")
        self.headers.update(headers)

def _reverse_dict(original_dict):
    reversed_dict = {value: key for key, value in original_dict.items()}
    return reversed_dict