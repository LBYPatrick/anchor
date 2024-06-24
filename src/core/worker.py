import asyncio
from pathlib import Path
from typing import Union, Dict, Any

import json5

from src.core.config_node import ConfigNode
from src.utils.util import Util


class Worker:

    internal_defaults = {
        "server": "0.0.0.0",
        "method": "chacha20-ietf-poly1305",
        "mode": "tcp_and_udp",
    }

    config: Dict[str, Any] = None
    root_node: ConfigNode = None

    @classmethod
    def init(cls, json_path_or_str: Union[str, Path]):
        if isinstance(json_path_or_str, Path):
            cls.config = Util.read_json(str(json_path_or_str.absolute()))
        else:
            cls.config = json5.loads(json_path_or_str)

    @classmethod
    def load_config(cls) -> ConfigNode:
        root_node = ConfigNode.empty()

        defaults = Util.read_map_value(cls.config, "global", {})

        # if the user intentionally left something important unfilled, we fill it for them
        defaults = {**cls.internal_defaults, **defaults}

        execution_args = Util.read_map_value(cls.config, "execution", {})

        root_node.name = Util.read_map_value(execution_args, "name", "anchor")
        root_node.set_params(defaults)

        groups: Dict = Util.read_map_value(cls.config, "groups", {})

        for name, group_json in groups.items():
            child = ConfigNode.from_json(group_json, name, root_node)
            root_node.children[name] = child

        cls.root_node = root_node

        return root_node

    @classmethod
    def make_ss_configs(cls) -> Dict[str, str]:

        root_node = cls.load_config()

        return {
            name: param_dict
            for name, param_dict in root_node.generate_configs().items()
        }

    @classmethod
    async def start_server(cls) -> None:

        nodes = cls.load_config().generate_configs()

        configs = [conf for _, conf in nodes.items()]

        Util.debug(configs)


if __name__ == "__main__":

    print("Here!")
    Worker.init(Path("example.json"))

    asyncio.run(Worker.start_server())

    # configs = Worker.make_ss_configs()

    # Util.verbose(configs)
