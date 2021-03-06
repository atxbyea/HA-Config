from .yaml_const import (CONFIG_TYPE)
from .yaml_const import (CONFIG_DEVICE_CONNECTION_PARAMS)
   
CLIMATE_IP_CONNECTIONS = []

def register_connection(conn):
    """Decorate a function to register a propery."""
    CLIMATE_IP_CONNECTIONS.append(conn)
    return conn

class Connection:
    def __init__(self, logger):
        self._params = {}
        self._logger = logger

    @property
    def logger(self):
        return self._logger

    def load_from_yaml(self, node, connection_base):
        """Load configuration from yaml node dictionary. Use connection base as base but DO NOT modify it.
        Return True if successful False otherwise."""
        return False

    def execute(self, template, value):
        """execute connection and return JSON object as result or None if unsuccesful."""
        return None

    def create_updated(self, yaml_node):
        """Create a copy of connection object and update this object from YAML configuration node"""
        return None

def create_connection(node, logger) -> Connection:
    for conn in CLIMATE_IP_CONNECTIONS:
        if CONFIG_TYPE in node:
            if conn.match_type(node[CONFIG_TYPE]):
                c = conn(logger)
                if c.load_from_yaml(node, None):
                    return c
    return None
