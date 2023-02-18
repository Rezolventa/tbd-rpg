from player import ActionManager, Player
from sprites import ScreenManager

from game_client.network import NetworkManager


class GameController:
    """Контроллер, управляющий основными процессами игры."""

    def __init__(self):
        self.net_man = NetworkManager()
        self.screen_man = ScreenManager()
        self.player = Player()
        self.action_man = ActionManager(self)
