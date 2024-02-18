from PyATEMMax import ATEMMax, ATEMEvents
from logging import Logger
from queue import Queue
import time

class ATEMSyncHandler():

    def __init__(self, logger: Logger, queue: Queue) -> None:
        self.logger: Logger = logger
        self.queue = queue

    def atem_on_connect_attempt(self, params: dict) -> None:
        self.logger.debug(f'trying to connect to {params['switcher'].ip}')

    def atem_on_connect(self, params: dict) -> None:
        self.logger.debug(f'connected to {params['switcher'].ip}')

    def atem_on_recieve(self, params: dict) -> None:
        self.logger.debug(f'recieved from switcher: {params['cmd']}: {params['cmdName']}')

    def atem_on_disconnect(self, params: dict) -> None:
        self.logger.debug(f'DISCONNECTED from switcher at {params['switcher'].ip}')

    def start_worker(self) -> None:
        atem = ATEMMax()
        atem.connect(ip='192.168.1.1')

        atem.registerEvent(ATEMEvents.connect, self.atem_on_connect)
        atem.registerEvent(ATEMEvents.receive, self.atem_on_recieve)
        atem.registerEvent(ATEMEvents.connectAttempt, self.atem_on_connect_attempt)
        atem.registerEvent(ATEMEvents.disconnect, self.atem_on_disconnect)

        while True:
            time.sleep(0.001)