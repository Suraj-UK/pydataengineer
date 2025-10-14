from typing import NoReturn
import os
import re
import subprocess
import pytest


def test_java_home_is_set() -> None:
    java_home = os.environ.get("JAVA_HOME")
    assert java_home is not None, \
        "Environment variable 'JAVA_HOME' is not set but is required by pySpark to work."


def test_java_version_minimum_requirement(expected_major_version: int = 11) -> None:
    version_line = __extract_version_line(__java_version_output())
    major_version = __parse_major_version(version_line)
    assert major_version >= expected_major_version, (
        f"Major version {major_version} is not recent enough, "
        f"we need at least version {expected_major_version}.")


def __java_version_output() -> str:
    java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode(
        "utf-8")
    print(f"\n`java -version` returned\n{java_version}")
    return java_version


def _fail(msg: str) -> NoReturn:
    pytest.fail(msg)                 # test-friendly failure
    raise AssertionError(msg)        # satisfy mypy: function never returns


def __extract_version_line(java_version_output: str) -> str:
    for line in java_version_output.splitlines():
        if "version" in line:
            return line
    _fail("Couldn't find version information in `java -version` output.")
    raise AssertionError("unreachable")  # appease mypy


def __parse_major_version(version_line: str) -> int:
    version_regex = re.compile(r'version "(?P<major>\d+)\.(?P<minor>\d+)\.\w+"')
    match = version_regex.search(version_line)
    if match is not None:
        major_version = int(match.group("major"))
        if major_version == 1:
            major_version = int(match.group("minor"))
        return major_version
    _fail(f"Couldn't parse Java version from {version_line}.")
    raise AssertionError("unreachable")  # appease mypy
