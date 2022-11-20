import logging
import psutil
import schedule
import time

from elastic import ElasticClient

class Monitoring:

    def __init__(self) -> None:
        self.elastic = ElasticClient()
        self.disk_info = {}
        self.memory_info = {}
        self.battery_info = {}

    def get_disk_info(self):
        disk_info = psutil.disk_usage('/')
        data = {
            'total': disk_info[0] / (2**30),
            'used': disk_info[1] / (2**30),
            'free': disk_info[2] / (2**30),
            'percent': disk_info[3]
        }
        return data

    def get_memory_info(self):
        mem_info = psutil.virtual_memory()
        data = {
            'total': mem_info[0] / (1024 ** 3),
            'available': mem_info[1] / (1024 ** 3),
            'percent': mem_info[2] / (1024 ** 3),
            'used': mem_info[3] / (1024 ** 3),
            'free': mem_info[4] / (1024 ** 3),
            'active': mem_info[5] / (1024 ** 3),
            'inactive': mem_info[6] / (1024 ** 3),
            'buffers': mem_info[7] / (1024 ** 3),
            'cached': mem_info[8] / (1024 ** 3),
            'shared': mem_info[9] / (1024 ** 3)
        }
        return data

    def get_battery_info(self):
        battery_info = psutil.sensors_battery()
        data = {
            'percent': battery_info[0],
            'secsleft': battery_info[1],
            'power_plugged': battery_info[2]
        }
        return data

    def run(self):
        self.disk_info = self.get_disk_info()
        self.memory_info = self.get_memory_info()
        self.battery_info = self.get_battery_info()
        self.elastic.create_machine_info(disk_info=self.disk_info,
                                         mem_info=self.memory_info,
                                         battery_info=self.battery_info)


if __name__ == '__main__':
    monitoring = Monitoring()
    schedule.every(1).minutes.do(monitoring.run)
    while True:
        schedule.run_pending()
        time.sleep(1)
