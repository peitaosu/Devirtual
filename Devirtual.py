import os, json, re, shutil

class Devirtual():
    def __init__(self):
        self.config_path = "config.json"
        self.config = None

    def load_config(self, config=None):
        if config:
            self.config_path = config
        with open(self.config_path) as in_file:
            self.config = json.load(in_file)
    
    def _parse_real_path(self, real_path):
        envvar_regex = r"(%(\w+)%)"
        matches = re.findall(envvar_regex, real_path)
        for group_env, group_var in matches:
            real_path = real_path.replace(group_env, os.environ[group_var])
        return real_path

    def _copy_file(self, src, dest):
        if not os.path.isdir(dest):
            os.mkdir(dest)
        for item in os.listdir(src):
            source = os.path.join(src, item)
            destination = os.path.join(dest, item)
            if os.path.isdir(source):
                self._copy_file(source, destination)
            else:
                shutil.copy(source, destination)

    def _devirtual_vfs(self):
        store_path = self.config["STORE"]
        vfs_path = os.path.join(store_path, "VFS")
        vfs_mapping = {}
        for sub_path, real_path in self.config["VFS"].items():
            vfs_mapping[os.path.join(vfs_path, sub_path)] = self._parse_real_path(real_path)
        for sub_path, real_path in vfs_mapping.items():
            if not os.path.isdir(sub_path):
                continue
            if not os.path.isdir(real_path):
                os.makedirs(real_path)
            self._copy_file(sub_path, real_path)

    def _devirtual_vreg(self):
        pass
        #TODO impl
    
    def go(self):
        if not self.config:
            self.load_config()
        self._devirtual_vfs()
        self._devirtual_vreg()
    
if __name__=="__main__":
    dev = Devirtual()
    dev.go()