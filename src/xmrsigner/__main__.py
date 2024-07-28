from xmrsigner.helpers import wallet as wallet_controller
from os import path

wallet_controller.WALLET_DAEMON_PATH = \
        path.join(path.dirname(path.abspath(__file__)), 'monero-wallet-rpc') \
        if path.basename(path.dirname(path.abspath(__package__))) != 'emulator' else \
        path.join(path.dirname(path.dirname(path.abspath(__package__))), 'monero-wallet-rpc')
wallet_controller.PIDFILE_BASE_PATH = '/tmp/monero-wallet-rpc'
wallet_controller.WALLET_RPC_PORT_OFFSET = 100

from xmrsigner.models.settings import Settings
from xmrsigner.models.settings_definition import SettingsConstants, SettingsDefinition

settings = Settings.get_instance()
settings.set_value(SettingsConstants.SETTING__CAMERA_ROTATION, SettingsConstants.CAMERA_ROTATION__270)  # fix camera rotation for emulator


from xmrsigner.controller import Controller
Controller.IS_EMULATOR = True
# Get the one and only Controller instance and start our main loop
Controller.get_instance().start()
