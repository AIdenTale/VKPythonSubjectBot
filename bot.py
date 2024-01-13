import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.vk_api import VkApiMethod
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
class VKBot:

    commands_handlers = {}

    def __init__(self, token=None, id=None):
        self._vk_token = token
        self._admin = id
        self.vk = None
        self.api: VkApiMethod

    def handle_func(self, command: str, func) -> None:
        self.commands_handlers[command] = func

    def set_vk_token(self, token: str) -> None:
        self._vk_token = token

    def set_admin(self, id: str) -> None:
        self._admin = id

    def send_msg(self, user_id, message, keyboard_buttons):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.getrandbits(64), "buttons": keyboard_buttons})

    def start_pooling(self):
        self.vk = vk_api.VkApi(token=self._vk_token)
        self.api = self.vk.get_api()
        longpoll = VkLongPoll(self.vk)
        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:

                    command = event.text
                    if self.commands_handlers.get(command, None) is None:
                        keyboard = VkKeyboard(**dict(one_time=False))
                        keyboard.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY,payload={"type": "show_snackbar","text": "Это исчезающее сообщение"})
                        self.api.messages.send(user_id=event.user_id, message='Ваш текст',random_id=random.getrandbits(64), keyboard=keyboard.get_keyboard())
                        # self.send_msg(event.user_id, "Неверная команда")
                        continue

                    self.commands_handlers[command](self, event)
