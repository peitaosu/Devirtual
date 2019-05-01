import os, json, re, shutil, uuid, platform

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

    def _devirtual_from_vreg_file(self, vreg_mapping, vreg_file_path, vreg_file_type="dat"):
        from Reg_Hive.reg import Registry
        reg = Registry()
        if vreg_file_type == "dat":
            if len(vreg_mapping.keys()) > 1:
                print("CURRENT NOT SUPPORT MULTIPLE MAPPINGS.")
                return
            hive_replace_path = vreg_mapping.keys()[0]
            hive_load_path = vreg_mapping[hive_replace_path]
            reg.read_from_dat(vreg_file_path, hive_replace_path, hive_load_path)
            reg.dump_to_reg()
        elif vreg_file_type == "reg":
            reg.read_from_reg(vreg_file_path)
            reg.dump_to_reg()
        else:
            reg.read_from_dat(vreg_file_path)
            for hive_key, real_key in vreg_mapping.items():
                reg.dump_to_reg()
                reg.reg_str = "\n".join(reg.reg_str).replace(hive_key, real_key).split("\n")
        uuid_str = str(uuid.uuid4())
        temp_reg = uuid_str + ".reg"
        reg.dump_to_reg(temp_reg)
        if platform.system() == "Windows":
            os.system("reg import " + temp_reg)
        else:
            print("Only Windows supports registry, your OS is {}".format(platform.system()))
        os.remove(temp_reg)

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
        store_path = self.config["STORE"]
        vreg_path = os.path.join(store_path, "VREG")
        for vreg_file in self.config["VREG"].keys():
            vreg_file_path = os.path.join(vreg_path, vreg_file)
            if not os.path.isfile(vreg_file_path):
                continue
            vreg_mapping = self.config["VREG"][vreg_file]
            self._devirtual_from_vreg_file(vreg_mapping, vreg_file_path, vreg_file.split(".")[-1])

    def go(self):
        if not self.config:
            self.load_config()
        self._devirtual_vfs()
        self._devirtual_vreg()
    
if __name__=="__main__":
    dev = Devirtual()
    dev.go()
