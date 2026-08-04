class ServiceRegistry:
    """
    Central registry for every engine/module
    used inside Ancestor.
    """

    def __init__(self):

        self._services = {}

    def register(self, name, service):

        self._services[name] = service

    def get(self, name):

        if name not in self._services:

            raise KeyError(
                f"Service '{name}' not registered."
            )

        return self._services[name]

    def exists(self, name):

        return name in self._services

    def remove(self, name):

        if self.exists(name):

            del self._services[name]

    def clear(self):

        self._services.clear()

    def all(self):

        return self._services

    def list_services(self):

        return list(self._services.keys())