from pathlib import Path
from typing import Union, Dict, Any

import json5

from src.core.config_node import ConfigNode
from src.utils.util import Util


class Worker:
    config: Dict[str, Any] = None
    root_node: ConfigNode = None

    @classmethod
    def init(cls, json_path_or_str: Union[str, Path]):
        if isinstance(json_path_or_str, Path):
            cls.config = Util.read_json(str(json_path_or_str.absolute()))

        else:
            cls.config = json5.loads(json_path_or_str)

    @classmethod
    def load_config(cls):

        root_node = ConfigNode.empty()

        defaults = Util.read_map_value(cls.config, "globals", {})
        execution_args = Util.read_map_value(cls.config, "execution", {})

        root_node.name = Util.read_map_value(execution_args, "name", "anchor")
        root_node.params = defaults

        groups: Dict = Util.read_map_value(cls.config, "groups", {})

        for name, group_json in groups.items():
            child = ConfigNode.from_json(group_json, name, root_node)
            root_node.children[name] = child

        cls.config = root_node

        return root_node
