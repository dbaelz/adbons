import subprocess
import yaml

from unittest import TestCase
from unittest.mock import patch
from unittest import mock

from click.testing import CliRunner

from src.adbons import cli as adbons


class TestAdbons(TestCase):
    @patch.object(subprocess, "run", autospec=True)
    def test_command_list_devices(self, mocked_run):
        runner = CliRunner()
        result = runner.invoke(adbons, ["devices"])

        assert result.exit_code == 0
        mocked_run.assert_called_with(["adb", "devices"])

    @patch.object(subprocess, "run", autospec=True)
    def test_command_kill(self, mocked_run):
        runner = CliRunner()
        result = runner.invoke(adbons, ["kill", "-a", "appId",
                                        "-d", "deviceId"])

        assert result.exit_code == 0
        mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell",
                                       "am", "force-stop", "appId"])

    @patch.object(subprocess, "run", autospec=True)
    def test_command_kill_all(self, mocked_run):
        runner = CliRunner()
        result = runner.invoke(adbons, ["kill-all", "-d", "deviceId"])

        assert result.exit_code == 0
        mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell", "am",
                                       "kill-all"])

    @patch.object(subprocess, "run", autospec=True)
    def test_command_clear(self, mocked_run):
        runner = CliRunner()
        result = runner.invoke(adbons, ["clear", "-a", "appId",
                                        "-d", "deviceId"])

        assert result.exit_code == 0
        mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell", "pm",
                                       "clear", "appId"])

    @patch.object(subprocess, "run", autospec=True)
    def test_command_text(self, mocked_run):
        runner = CliRunner()
        result = runner.invoke(adbons, ["text", "-d", "deviceId", "test-text"])

        assert result.exit_code == 0
        mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell",
                                       "input", "text", "test-text"])

    @patch.object(subprocess, "run", autospec=True)
    def test_command_screencap(self, mocked_run):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(adbons, ["screencap", "-d", "deviceId",
                                            "test-output"])

            assert result.exit_code == 0
            mocked_run.assert_called_with(["adb", "-s", "deviceId",
                                           "exec-out", "screencap",
                                           "-p"], stdout=mock.ANY)

    def test_command_config_set_ids(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(adbons, ["config", "-a", "appId",
                                            "-d", "deviceId"])

            with open(".adbons.yml", 'r') as config_file:
                assert result.exit_code == 0
                config = yaml.safe_load(config_file)
                assert config is not None
                assert config["app"]["default"] == "appId"
                assert config["device"]["default"] == "deviceId"

    def test_command_config_clear(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(".adbons.yml", 'w') as config_file:
                config = {'device': {'default': 'deviceId'},
                          'app': {'default': 'appId'}}
                yaml.dump(config, config_file, default_flow_style=False)

            # Clear the device id
            result = runner.invoke(adbons, ["config", "-c", "device"])
            with open(".adbons.yml", 'r') as config_file:
                assert result.exit_code == 0
                config = yaml.safe_load(config_file)
                assert config is not None
                assert config["app"]["default"] == "appId"
                assert config["device"] == {}

            # Clear the app id, too
            result = runner.invoke(adbons, ["config", "-c", "app"])
            with open(".adbons.yml", 'r') as config_file:
                assert result.exit_code == 0
                config = yaml.safe_load(config_file)
                assert config is not None
                assert config["app"] == {}
                assert config["device"] == {}

    def test_command_config_show_ids(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(".adbons.yml", 'w') as config_file:
                config = {'device': {'default': 'deviceId'},
                          'app': {'default': 'appId'}}
                yaml.dump(config, config_file, default_flow_style=False)

            result = runner.invoke(adbons, ["config", "-s"])
            with open(".adbons.yml", 'r') as config_file:
                assert result.exit_code == 0
                config = yaml.safe_load(config_file)
                assert config is not None
                assert config["app"]["default"] == "appId"
                assert config["device"]["default"] == "deviceId"
