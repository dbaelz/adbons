import subprocess

from unittest import TestCase
from unittest.mock import patch

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
