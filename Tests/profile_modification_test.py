import unittest

import test_helpers

import sys

sys.path.append(test_helpers.get_profile_modification_path())
sys.path.append(test_helpers.get_helpers_path())

import Config

import MDMProfileManager

TEST_FILES_DIR = "./test_files/mdm_profiles/"

V23 = "23_24_v4"
V225 = "v225"

V23_IN = "plain_" + V23 + ".txt"
V225_IN = "plain_" + V225 + ".txt"


class MdmProfileManagerTestCase(unittest.TestCase):
    def test_version_is_latest(self):
        self.assert_version_is_latest(V23_IN, True)
        self.assert_version_is_latest(V225_IN, False)

    def test_append_allowed_apps(self):
        def target(input):
            return MDMProfileManager.append_allowed_apps(
                input, test_helpers.allowed_app_bundle_ids
            )

        self.assert_output_equals("append_allowed_apps_", target)

    def test_update_restrictions(self):
        def target(input):
            return MDMProfileManager.update_restrictions(
                input, test_helpers.restriction_modifications
            )

        self.assert_output_equals("update_restrictions_", target)

    def test_update_web_filters(self):
        def target(input):
            return MDMProfileManager.update_web_filters(input)

        self.assert_output_equals("update_web_filters_", target)

    def test_remove_allowed_apps(self):
        def target(input):
            return MDMProfileManager.remove_allowed_apps(input)

        self.assert_output_equals("remove_allowed_apps_", target)

    def test_remove_restrictions(self):
        def target(input):
            return MDMProfileManager.remove_restrictions(input)

        self.assert_output_equals("remove_restrictions_", target)

    def assert_version_is_latest(self, input_path, match):
        with open(TEST_FILES_DIR + input_path, "r") as fp:
            input = fp.read()

        self.assertTrue(MDMProfileManager.version_is_latest(input) == match)

    def assert_output_equals(self, match_path, callback):
        with open(TEST_FILES_DIR + V23_IN, "r") as fp:
            input1 = fp.read()
        with open(TEST_FILES_DIR + V225_IN, "r") as fp:
            input2 = fp.read()
        with open(TEST_FILES_DIR + match_path + V23 + ".txt", "r") as fp:
            match1 = fp.read()
        with open(TEST_FILES_DIR + match_path + V225 + ".txt", "r") as fp:
            match2 = fp.read()

        self.assertTrue(callback(input1) == match1)
        self.assertTrue(callback(input2) == match2)


if __name__ == "__main__":
    unittest.main()
