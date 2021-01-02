# import time
#
# from synchronization.fetcher.device_status_fetcher_factory import DeviceStatusFetcherFactory
#
# fetcher = DeviceStatusFetcherFactory(None, None, "test").create_fetcher()
#
# fetcher.start()
#
# while True:
#     iterator = fetcher.get_updated()
#     while iterator.has_next():
#         msg = iterator.next()
#         print(msg)
#     time.sleep(10)
from synchronization.home_pi_status_manager import HomePiStatusManager

manager = HomePiStatusManager(None, None, "test")

manager.start_synchronizing()