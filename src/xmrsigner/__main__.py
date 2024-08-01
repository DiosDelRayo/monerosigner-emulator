from xmrsigner.helpers import wallet as wallet_controller
import xmrsigner.emulator.desktopDisplay as desktopDisplay
from os import path
from random import randint
import sys


WALLET_RPC_EXECUTABLE = 'monero-wallet-rpc'


def is_executable() -> bool:
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_path() -> str:
    if is_executable():
        return path.dirname(path.abspath(__file__))  # same path as the extracted script
    return path.dirname(path.dirname(path.abspath(__package__)))  # on directory up of the module

def get_file_path(file: str) -> str:
    return path.join(get_path(), file)

def get_executable_file_path() -> str:
    if is_executable():
        return path.dirname(path.abspath(sys.executable))  # same path as the extracted script
    return path.dirname(path.dirname(path.abspath(__package__)))  # on directory up of the module

wallet_controller.WALLET_DAEMON_PATH = get_file_path(WALLET_RPC_EXECUTABLE)
wallet_controller.PIDFILE_BASE_PATH = f'/tmp/{WALLET_RPC_EXECUTABLE}'
wallet_controller.WALLET_RPC_PORT_OFFSET = 100 + randint(0, 99)
desktopDisplay.CONFIG_FILE = path.join(get_executable_file_path(), 'xmrsigner-emulator.yml')
desktopDisplay.SCREENSHOT_PATH = get_executable_file_path()

print(f"wallet rpc: {wallet_controller.WALLET_DAEMON_PATH}: {'found' if path.exists(wallet_controller.WALLET_DAEMON_PATH) else 'not found'}")
print(f'temp dir: {wallet_controller.PIDFILE_BASE_PATH}')

from xmrsigner.models.settings import Settings
from xmrsigner.models.settings_definition import SettingsConstants, SettingsDefinition

settings = Settings.get_instance()
settings.set_value(SettingsConstants.SETTING__CAMERA_ROTATION, SettingsConstants.CAMERA_ROTATION__270)  # fix camera rotation for emulator


from xmrsigner.controller import Controller
Controller.IS_EMULATOR = True
# Get the one and only Controller instance and start our main loop
Controller.get_instance().start()
