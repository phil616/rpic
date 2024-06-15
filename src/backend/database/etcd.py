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



from core.logcontroller import logger
from core.utils import get_ip,ipv4_to_hex,port_to_hex
from conf import config
import etcd3
import asyncio
import ujson as json
from core.runtime import get_global_state
etcd = etcd3.client(host=config.ETCD_HOST,port=config.ETCD_PORT)

service_id = f"{config.SUBAPP_NAME}{ipv4_to_hex(get_ip())}{port_to_hex(config.DEPLOY_PORT)}"


SERVICE_KEY = f"services/app/{service_id}"
## PAYLOADS of ETC
SERVICE_VALUE = {
    "type":"Command Pod",
    "port":config.DEPLOY_PORT,
    "host":get_ip(),
    "jwt":config.JWT_SECRET_KEY,
    "jwt_algo":config.JWT_ALGORITHM
}


def discover_service()->list:
    services = {}
    for value, meta in etcd.get_prefix("services/app/"):
        # logger.debug(f"{value},{meta}")
        services[meta.key.decode("utf-8").split('/')[-1]] = value.decode("utf-8")
    return services

lease = etcd.lease(10)
etcd.put(SERVICE_KEY, json.dumps(SERVICE_VALUE), lease=lease)

async def flush_command_pod_info(services:dict):
    state = get_global_state()
    service_pods = []
    for k,v in services.items():
        if str(k).startswith("SP"):
            v = json.loads(v)
            service_pods.append(v)
    
    state.runtime.set("sp",service_pods.copy())
    logger.debug(f"Current Online Services:{[service for service in services]}")

async def etcd_loop():
    while True:
        lease.refresh()
        await asyncio.sleep(9)
        allservices = discover_service()
        await flush_command_pod_info(allservices)
