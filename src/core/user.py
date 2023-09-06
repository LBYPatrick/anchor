from typing import Dict, Any, Set, List
from src.utils.util import Util


class User:
    parent_config = None
    __ports: List[int] = None
    __pwd: str
    name: str = None

    required_keys = ["server", "server_port", "password", "method"]
    optional_keys = [
        "plugin",
        "plugin_opts",
        "redirect",
        "remarks",
        "fastopen",
        "tunnel_mode",
        "no_delay",
        "plugin_mode",
        "mode",
        "ipv6_first"
    ]

    def __init__(self, parent_config, ports: List[int], pwd: str, name: str = None):
        self.parent_config = parent_config
        self.__ports = ports
        self.__pwd = pwd
        self.name = "anonymous_user" if name is None else name

    @classmethod
    def from_json(cls, json: Dict[str, Any], name: str, parent_config=None):
        Util.ensure_valid_dict(json, "password", "ports")

        pwd = Util.read_map_value(json, "password", "")
        ports = Util.read_map_value(json, "ports", [])

        return User(parent_config, ports, pwd, name)

    def get_path(self):
        """
        Get the path of the current user.
        Returns:
        """

        parents = []
        from src.core.config_node import ConfigNode

        # Just to make IDE happy and autocomplete for me
        walk: ConfigNode = self.parent_config

        while walk is not None:
            parents.append(walk.name)
            walk = walk.parent

        parents.reverse()

        return ".".join(parents) + f".{self.name}"

    def make_config(self) -> Dict[int, Dict[str, Any]]:
        """
        Generate shadowsocks configs as Dicts (which can be EASILY converted to JSON or YAML) for the current user.
        Returns:
            Dict of Configurations, like this: {
                12345 : {
                    "server_port" : 12345,
                    "password" : "something",
                    "fastopen": ...
                    ...
                },
                56789: {
                    ...
                }

        """

        from src.core.config_node import ConfigNode

        # Just to make IDE happy and autocomplete for me
        parent_config: ConfigNode = self.parent_config
        ret = {}

        for port in self.__ports:
            # STEP 1: check and parse required keys
            conf = {}
            conf = {k: parent_config.get_param(k) for k in self.required_keys}

            conf["password"] = self.__pwd
            conf["server_port"] = port

            conf = Util.shrink_dict(conf)

            # raise Exception if required keys are missing
            Util.ensure_valid_dict(conf, *self.required_keys)

            # STEP 2: parse optional keys
            optionals = Util.shrink_dict(
                {k: parent_config.get_param(k) for k in self.optional_keys}
            )

            conf = {**conf, **optionals}

            ret[port] = conf

        return ret
