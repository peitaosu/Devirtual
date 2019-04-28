Devirtual
=========

De-virtual virtual file system and registry to actual system.

## Config Sample
```
{
    "VFS": {
        "ProgramFilesX64": "C:\\Program Files",
        "ProgramFilesX86": "C:\\Program Files (x86)",
        "AppData": "%AppData%",
        "LocalAppData": "%LocalAppData%",
        "CommonAppData": "C:\\ProgramData"
    },
    "VREG": {
        "Registry.dat": {
            "REGISTRY\\MACHINE": "HKEY_LOCAL_MACHINE"        
        },
        "User.dat": {
            "REGISTRY\\USER": "HKEY_CURRENT_USER"  
        },
        "Classes.dat": {
            "REGISTRY\\CLASSES": "HKEY_CLASSES_ROOT"  
        }
    },
    "STORE": "."
}
```