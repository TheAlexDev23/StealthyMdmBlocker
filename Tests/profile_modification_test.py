import test_helpers

import sys

sys.path.append(test_helpers.get_profile_modification_path())
# MDMProfileManager imports XMLHelpers and other helpers
sys.path.append(test_helpers.get_helpers_path())

import MDMProfileManager  # noqa: E402 needs path to be imported

TEST_FILES_DIR = "./test_files/mdm_profiles/"

V23 = "23_24_v4"
V225 = "v225"

V23_IN = "plain_" + V23 + ".txt"
V225_IN = "plain_" + V225 + ".txt"


def test_version_is_latest():
    assert_version_is_latest(V23_IN, True)
    assert_version_is_latest(V225_IN, False)


def test_append_allowed_apps():
    def target(input):
        return MDMProfileManager.append_allowed_apps(
            input, test_helpers.allowed_app_bundle_ids
        )

    assert_output_equals("append_allowed_apps_", target)


def test_update_restrictions():
    def target(input):
        return MDMProfileManager.update_restrictions(
            input, test_helpers.restriction_modifications
        )

    assert_output_equals("update_restrictions_", target)


def test_update_web_filters():
    def target(input):
        return MDMProfileManager.update_web_filters(input)

    assert_output_equals("update_web_filters_", target)


def test_remove_allowed_apps():
    def target(input):
        return MDMProfileManager.remove_allowed_apps(input)

    assert_output_equals("remove_allowed_apps_", target)


def test_remove_restrictions():
    def target(input):
        return MDMProfileManager.remove_restrictions(input)

    assert_output_equals("remove_restrictions_", target)


def assert_version_is_latest(input_path, match):
    with open(TEST_FILES_DIR + input_path, "r") as fp:
        input = fp.read()

    assert MDMProfileManager.version_is_latest(input) == match


def assert_output_equals(match_path, callback):
    with open(TEST_FILES_DIR + V23_IN, "r") as fp:
        input1 = fp.read()
    with open(TEST_FILES_DIR + V225_IN, "r") as fp:
        input2 = fp.read()
    with open(TEST_FILES_DIR + match_path + V23 + ".txt", "r") as fp:
        match1 = fp.read()
    with open(TEST_FILES_DIR + match_path + V225 + ".txt", "r") as fp:
        match2 = fp.read()

    assert callback(input1) == match1
    assert callback(input2) == match2
