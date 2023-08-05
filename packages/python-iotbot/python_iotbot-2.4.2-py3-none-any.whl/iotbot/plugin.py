import importlib
import os
import re
from pathlib import Path
from types import ModuleType
from typing import Dict
from typing import List

from prettytable import PrettyTable

from .typing import EventMsgReceiver
from .typing import FriendMsgReceiver
from .typing import GroupMsgReceiver


class Plugin:
    def __init__(self, module: ModuleType):
        self.module = module
        self.name = Path(module.__file__).stem[4:]
        self.receive_group_msg: GroupMsgReceiver = module.__dict__.get('receive_group_msg')
        self.receive_friend_msg: FriendMsgReceiver = module.__dict__.get('receive_friend_msg')
        self.receive_events: EventMsgReceiver = module.__dict__.get('receive_events')


class PluginManager:
    def __init__(self, plugin_dir: str = 'plugins'):
        self.plugin_dir = plugin_dir
        self._plugins: Dict[str, Plugin] = dict()
        self._removed_plugins: Dict[str, Plugin] = dict()

    def load_plugins(self, plugin_dir: str = None) -> None:
        if plugin_dir is None:
            plugin_dir = self.plugin_dir
        plugin_files = (i for i in os.listdir(plugin_dir) if re.search(r'^bot_\w+\.py$', i))
        for plugin_file in plugin_files:
            module = importlib.import_module(
                '{}.{}'.format(plugin_dir.replace('/', '.'), plugin_file.split('.')[0]))
            plugin = Plugin(module)
            if plugin.name not in self._removed_plugins:
                self._plugins[plugin.name] = plugin

    def refresh(self, plugin_dir: str = None) -> None:
        '''reload all plugins'''
        self._plugins.clear()
        self.load_plugins(plugin_dir)
        self.reload_plugins(plugin_dir)

    def reload_plugins(self, plugin_dir: str = None) -> None:
        '''reload old, load new.'''
        # reload old
        old_plugins = self._plugins.copy()
        for old_plugin in old_plugins.values():
            old_plugins[old_plugin.name].module = importlib.reload(old_plugin.module)
        # load new
        self.load_plugins(plugin_dir)
        # tidy
        self._plugins.update(old_plugins)

    def reload_plugin(self, plugin_name: str) -> None:
        '''reload one plugin according to plugin name
        whether the plugin exists or not, it will always keep quiet.
        '''
        if plugin_name in self._plugins:
            self._plugins[plugin_name].module = importlib.reload(self._plugins[plugin_name].module)

    def remove_plugin(self, plugin_name: str) -> None:
        '''remove not delete.'''
        try:
            if plugin_name in self._plugins:
                self._removed_plugins[plugin_name] = self._plugins.pop(plugin_name)
        except KeyError:
            pass

    def recover_plugin(self, plugin_name: str) -> None:
        '''recover plugin if it's in the removed plugins list.'''
        try:
            if plugin_name in self._removed_plugins:
                self._plugins[plugin_name] = self._removed_plugins.pop(plugin_name)
        except KeyError:
            pass

    @property
    def plugins(self) -> List[str]:
        '''return a list of plugin name'''
        return [i for i in self._plugins]

    @property
    def removed_plugins(self) -> List[str]:
        '''return a list of removed plugin name'''
        return [i for i in self._removed_plugins]

    @property
    def friend_msg_receivers(self) -> List[FriendMsgReceiver]:
        '''funcs to handle (friend msg)context'''
        return [plugin.receive_friend_msg for plugin in self._plugins.values()
                if plugin.receive_friend_msg]

    @property
    def group_msg_receivers(self) -> List[GroupMsgReceiver]:
        '''funcs to handle (group msg)context'''
        return [plugin.receive_group_msg for plugin in self._plugins.values()
                if plugin.receive_group_msg]

    @property
    def event_receivers(self) -> List[EventMsgReceiver]:
        '''funcs to handle (event msg)context'''
        return [plugin.receive_events for plugin in self._plugins.values()
                if plugin.receive_events]

    @property
    def info_table(self) -> str:
        table = PrettyTable(['Receiver', 'Count', 'Info'])
        table.add_row([
            'Friend Msg Receiver',
            len(self.friend_msg_receivers),
            ' '.join([f'<{p.name}>' for p in self._plugins.values() if p.receive_friend_msg])
        ])
        table.add_row([
            'Group  Msg Receiver',
            len(self.group_msg_receivers),
            ' '.join([f'<{p.name}>' for p in self._plugins.values() if p.receive_group_msg])
        ])
        table.add_row([
            'Event      Receiver',
            len(self.event_receivers),
            ' '.join([f'<{p.name}>' for p in self._plugins.values() if p.receive_events])
        ])
        return str(table)
