import inspect
import subprocess

from unittest.mock import patch

from click.testing import CliRunner

from src.adbons import cli as adbons


def run_tests():
    test_command_list_devices()
    test_command_kill()
    test_command_kill_all()
    test_command_clear()
    test_command_text()


@patch.object(subprocess, "run", autospec=True)
def test_command_list_devices(mocked_run):
    runner = CliRunner()
    result = runner.invoke(adbons, ["devices"])

    assert result.exit_code == 0
    mocked_run.assert_called_with(["adb", "devices"])
    print("SUCESS: " + inspect.stack()[0][3])


@patch.object(subprocess, "run", autospec=True)
def test_command_kill(mocked_run):
    runner = CliRunner()
    result = runner.invoke(adbons, ["kill", "-a", "appId",
                                    "-d", "deviceId"])

    assert result.exit_code == 0
    mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell",
                                   "am", "force-stop", "appId"])
    print("SUCESS: " + inspect.stack()[0][3])


@patch.object(subprocess, "run", autospec=True)
def test_command_kill_all(mocked_run):
    runner = CliRunner()
    result = runner.invoke(adbons, ["kill-all", "-d", "deviceId"])

    assert result.exit_code == 0
    mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell", "am",
                                   "kill-all"])
    print("SUCESS: " + inspect.stack()[0][3])


@patch.object(subprocess, "run", autospec=True)
def test_command_clear(mocked_run):
    runner = CliRunner()
    result = runner.invoke(adbons, ["clear", "-a", "appId",
                                    "-d", "deviceId"])

    assert result.exit_code == 0
    mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell", "pm",
                                   "clear", "appId"])
    print("SUCESS: " + inspect.stack()[0][3])


@patch.object(subprocess, "run", autospec=True)
def test_command_text(mocked_run):
    runner = CliRunner()
    result = runner.invoke(adbons, ["text", "-d", "deviceId", "test-text"])

    assert result.exit_code == 0
    mocked_run.assert_called_with(["adb", "-s", "deviceId", "shell",
                                   "input", "text", "test-text"])
    print("SUCESS: " + inspect.stack()[0][3])


if __name__ == "__main__":
    run_tests()
