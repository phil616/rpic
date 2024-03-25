from core.logcontroller import logger
from core.utils import get_ip,ipv4_to_hex,port_to_hex
from conf import config
import etcd3
import asyncio
import ujson as json
etcd = etcd3.client(host=config.ETCD_HOST,port=config.ETCD_PORT)


service_id = f"{config.SUBAPP_NAME}{ipv4_to_hex(get_ip())}{port_to_hex(config.DEPLOY_PORT)}"

SERVICE_KEY = f"services/app/{service_id}"
SERVICE_VALUE = {
    "port":config.DEPLOY_PORT,
    "host":get_ip()
}


def discover_service()->list:
    services = {}
    for value, meta in etcd.get_prefix("services/app/"):
        # logger.debug(f"{value},{meta}")
        services[meta.key.decode("utf-8").split('/')[-1]] = value.decode("utf-8")
    return services

lease = etcd.lease(10)
etcd.put(SERVICE_KEY, json.dumps(SERVICE_VALUE), lease=lease)

async def register_app(state):
    while True:
        lease.refresh()
        await asyncio.sleep(9)
        logger.debug("flush app to etcd success")
        allservices = discover_service()
        logger.debug(allservices)
