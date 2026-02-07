import winreg
import json
import os

def get_ue_installs():
    installs = {}

    # 1. Check Registry (HKLM & HKCU)
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\EpicGames\Unreal Engine"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Epic Games\Unreal Engine\Builds"),
    ]

    for root, path in reg_paths:
        try:
            with winreg.OpenKey(root, path) as key:
                num_subkeys, num_values, _ = winreg.QueryInfoKey(key)
                
                # Check Subkeys (Version names like 5.3, 5.6)
                for i in range(num_subkeys):
                    try:
                        ver_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, ver_name) as subkey:
                            # Usually "InstalledDirectory"
                            loc, _ = winreg.QueryValueEx(subkey, "InstalledDirectory")
                            installs[ver_name] = loc
                    except Exception:
                        continue
                
                # Check Values (Direct mapping in builds key)
                for i in range(num_values):
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if os.path.isdir(str(value)):
                            installs[name] = value
                    except Exception:
                        continue
        except FileNotFoundError:
            continue

    # 2. Check Epic Launcher Manifests (The most reliable for 5.3.2)
    # This file tracks exactly where the launcher put the engines.
    manifest_path = os.path.join(os.environ.get("ALLUSERSPROFILE", ""), 
                                 r"Epic\UnrealEngineLauncher\LauncherInstalled.dat")
    
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get("InstallationList", []):
                    app_name = item.get("AppName", "")
                    if "UE_" in app_name:
                        ver = app_name.replace("UE_", "")
                        installs[ver] = item.get("InstallLocation")
        except Exception as e:
            print(f"Error reading manifest: {e}")

    return installs

if __name__ == "__main__":
    print("Searching for Unreal Engine installations...")
    print("="*40)
    found_installs = get_ue_installs()
    
    if found_installs:
        for version, path in found_installs.items():
            print(f"Version: {version}")
            print(f"Path:    {path}")
            print("-"*40)
    else:
        print("No Unreal Engine installations found.")