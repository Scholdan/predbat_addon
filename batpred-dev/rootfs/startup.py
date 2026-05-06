import os
import sys
import urllib.request
import shutil
import time
print("Bootstrap Predbat")

root = "/config"
batpred_repository = "Scholdan/batpred"
batpred_branch = "main"

# Check if config exists, if not run locally
if not os.path.exists(root):
    root = "./"

# Download BatPred from the dev fork. This fork currently has no releases, so
# bootstrap from the main branch archive instead of the GitHub releases API.
if not os.path.exists(root + "/apps.yaml"):
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
    unzip_path = root + "/unzip"
    if os.path.exists(unzip_path):
        shutil.rmtree(unzip_path)
    os.makedirs(unzip_path)
    shutil.unpack_archive(save_path, unzip_path)
    unzip_path = unzip_path + "/batpred-" + batpred_branch
    os.system("cp {}/apps/predbat/* {}".format(unzip_path, root))
    os.system("cp {}/apps/predbat/config/* {}".format(unzip_path, root))
    os.system("rm -rf {}".format(unzip_path))


print("Startup")
os.system("cd " + root + "; python3 hass.py")

print("Shutdown, sleeping 20 seconds before restarting")
time.sleep(20)
