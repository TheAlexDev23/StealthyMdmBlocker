import test_helpers

import sys
import subprocess

sys.path.append(test_helpers.get_profile_modification_path())
sys.path.append(test_helpers.get_helpers_path())

import MDMProfileManager
import Config

# If you're not using unix then get fucked
subprocess.call("cp ./test_files/mdm_profiles/plain_* ./test_files/", shell=True)
subprocess.call("rm -rf ./test_files/mdm_profiles/*", shell=True)
subprocess.call("mv ./test_files/plain_* ./test_files/mdm_profiles/", shell=True)

with open("./test_files/mdm_profiles/plain_23_24_v4.txt", "r") as fp:
    result = MDMProfileManager.remove_allowed_apps(fp.read())
    with open(
        "./test_files/mdm_profiles/remove_allowed_apps_23_24_v4.txt", "w"
    ) as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_23_24_v4.txt", "r") as fp:
    result = MDMProfileManager.append_allowed_apps(
        fp.read(), test_helpers.allowed_app_bundle_ids
    )
    with open(
        "./test_files/mdm_profiles/append_allowed_apps_23_24_v4.txt", "w"
    ) as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_23_24_v4.txt", "r") as fp:
    result = MDMProfileManager.remove_restrictions(fp.read())

    with open(
        "./test_files/mdm_profiles/remove_restrictions_23_24_v4.txt", "w"
    ) as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_23_24_v4.txt", "r") as fp:
    result = MDMProfileManager.update_restrictions(
        fp.read(), test_helpers.restriction_modifications
    )

    with open(
        "./test_files/mdm_profiles/update_restrictions_23_24_v4.txt", "w"
    ) as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_23_24_v4.txt", "r") as fp:
    result = MDMProfileManager.update_web_filters(fp.read())

    with open("./test_files/mdm_profiles/update_web_filters_23_24_v4.txt", "w") as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_v225.txt", "r") as fp:
    result = MDMProfileManager.remove_allowed_apps(fp.read())
    with open("./test_files/mdm_profiles/remove_allowed_apps_v225.txt", "w") as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_v225.txt", "r") as fp:
    result = MDMProfileManager.append_allowed_apps(
        fp.read(), test_helpers.allowed_app_bundle_ids
    )
    with open("./test_files/mdm_profiles/append_allowed_apps_v225.txt", "w") as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_v225.txt", "r") as fp:
    result = MDMProfileManager.remove_restrictions(fp.read())

    with open("./test_files/mdm_profiles/remove_restrictions_v225.txt", "w") as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_v225.txt", "r") as fp:
    result = MDMProfileManager.update_restrictions(
        fp.read(), test_helpers.restriction_modifications
    )

    with open("./test_files/mdm_profiles/update_restrictions_v225.txt", "w") as save:
        save.write(result)

with open("./test_files/mdm_profiles/plain_v225.txt", "r") as fp:
    result = MDMProfileManager.update_web_filters(fp.read())

    with open("./test_files/mdm_profiles/update_web_filters_v225.txt", "w") as save:
        save.write(result)
