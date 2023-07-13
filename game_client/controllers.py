from game_client.actions import ActionManager
from game_client.network import NetworkManager
from game_client.sprites import ScreenManager


class GameController:
    """Контроллер, управляющий основными процессами игры."""

    def __init__(self):
        self.net_man = NetworkManager()
        self.screen_man = ScreenManager()
        # self.player = PlayerManager()
        self.action_man = ActionManager(self)
