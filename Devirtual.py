import json

class Devirtual():
    def __init__(self):
        self.config_path = "config.json"
        self.config = None

    def get_config(self, config=None):
        if config:
            self.config_path = config
        with open(self.config_path) as in_file:
            self.config = json.load(in_file)
    
    def _devirtual_vfs(self):
        pass
        #TODO impl

    def _devirtual_vreg(self):
        pass
        #TODO impl
    
    def go(self):
        if not self.config:
            self.get_config()
        self._devirtual_vfs()
        self._devirtual_vreg()
    
