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