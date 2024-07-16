from xmrsigner.helpers import wallet as wallet_controller
wallet_controller.WALLET_DAEMON_PATH = '/home/thor/monero-gui-v0.18.3.3/extras/monero-wallet-rpc'
wallet_controller.PIDFILE_BASE_PATH = '/tmp/monero-wallet-rpc'

from xmrsigner.models.settings import Settings
from xmrsigner.models.settings_definition import SettingsConstants, SettingsDefinition

settings = Settings.get_instance()
settings.set_value(SettingsConstants.SETTING__CAMERA_ROTATION, SettingsConstants.CAMERA_ROTATION__270)  # fix camera rotation for emulator


from xmrsigner.controller import Controller
# Get the one and only Controller instance and start our main loop
Controller.get_instance().start()
