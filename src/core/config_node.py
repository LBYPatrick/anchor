import copy
import functools
from typing import Dict, Any, List, Optional

from src.core.user import User
from src.utils.util import Util


class ConfigNode:
    __params: Dict[str, Any] = None
    users: Dict[str, User] = None
    children: Dict[str, Any] = {}
    parent = None
    name: str = None

    def __init__(
        self,
        name: str,
        parent,
        params: Dict[str, Any],
        users: Dict[str : Dict[int, str]],
    ):
        self.name = "anonymous_config_node" if name is None else name
        self.parent = parent
        self.__params = params if params is not None else {}
        self.children = {}
        self.users = {} if users is None else users

    @classmethod
    def empty(cls):
        return ConfigNode(None, None, None, None)

    @property
    def params(self):
        return {} if self.__params is None else copy.deepcopy(self.__params)

    def get_param(self, key: str = None) -> Optional[Any]:
        if key is None:
            return None

        walk = self

        while walk is not None:
            if key in walk.params:
                return walk.params[key]

            walk = walk.parent

        return None

    @classmethod
    def from_json(
        cls, json: Dict[str, Any], name: Optional[str] = None, parent_config=None
    ):
        params: Dict[str, Any] = Util.read_map_value(json, "params", {})
        users: Dict[str, Any] = Util.read_map_value(json, "users", {})
        children: Dict[str, Any] = Util.read_map_value(json, "children", {})

        ret = ConfigNode.empty()
        ret.__params = params
        ret.parent = parent_config
        ret.name = name

        for user_name, user_json in users.items():
            parsed_user: User = User.from_json(user_json, user_name, ret)

            ret.users[user_name] = parsed_user

        for config_name, child_config_json in children.items():
            parsed_node = ConfigNode.from_json(
                child_config_json, config_name, ret
            )

            ret.children[config_name] = parsed_node

        return ret

    def generate_configs(self) -> List[Dict[str, Any]]:
        # TODO: Finish this
        pass
