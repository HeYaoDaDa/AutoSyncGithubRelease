import os
import sys
github_token = {
    "Authorization": os.environ["SYNC_GITHUB_TOKEN"]
}
download_dir = os.path.join(os.path.dirname(
    os.path.realpath(sys.argv[0])), "releases")
