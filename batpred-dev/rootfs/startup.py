import os
import sys
import urllib.request
import shutil
import time
print("Bootstrap Predbat")

root = "/config"
batpred_repository = "Scholdan/batpred"
batpred_branch = "main"


def copy_tree_contents(source, target, skip_files=None, skip_dirs=None):
    skip_files = skip_files or []
    skip_dirs = skip_dirs or []
    for name in os.listdir(source):
        if name in skip_files or name in skip_dirs:
            continue
        source_path = os.path.join(source, name)
        target_path = os.path.join(target, name)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, target_path)

# Check if config exists, if not run locally
if not os.path.exists(root):
    root = "./"

# Download BatPred from the dev fork. This fork currently has no releases, so
# bootstrap from the main branch archive instead of the GitHub releases API.
apps_yaml_exists = os.path.exists(root + "/apps.yaml")
download_url = "https://github.com/{}/archive/refs/heads/{}.zip".format(batpred_repository, batpred_branch)
save_path = root + "/batpred_{}.zip".format(batpred_branch)
print("Downloading Predbat {}".format(download_url))

try:
    urllib.request.urlretrieve(download_url, save_path)
    print("Predbat downloaded successfully")
except Exception as e:
    print("Error: Unable to download Predbat - {}".format(str(e)))
    sys.exit(1)

print("Unzipping Predbat")
unzip_root = root + "/unzip"
if os.path.exists(unzip_root):
    shutil.rmtree(unzip_root)
os.makedirs(unzip_root)
shutil.unpack_archive(save_path, unzip_root)
unzip_path = unzip_root + "/batpred-" + batpred_branch
predbat_path = unzip_path + "/apps/predbat"
copy_tree_contents(predbat_path, root, skip_dirs=["config"])
copy_tree_contents(predbat_path + "/config", root, skip_files=["apps.yaml"] if apps_yaml_exists else [])
shutil.rmtree(unzip_root)


print("Startup")
os.system("cd " + root + "; python3 hass.py")

print("Shutdown, sleeping 20 seconds before restarting")
time.sleep(20)
