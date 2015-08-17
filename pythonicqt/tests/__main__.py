"""This file runs all the tests of pythonicqt.
It is intended to run as the main entry point of tests.

You can run this file by writing "python -m pythonicqt.tests"
"""

def check_if_all_tests_pass(option='-x'):
    """Runs all of the tests and only returns True if all tests pass.
       The -x option is the default, and -x will tell pytest to exit on the first encountered failure.
       The -s option prints out stdout from the tests (normally hidden.)"""
    import pytest
    options = [option]
    arguments = options
    exitcode = pytest.main(arguments)
    all_passed = exitcode == 0
    if not all_passed:
        raw_input()
    return all_passed

if __name__ == "__main__":
    if check_if_all_tests_pass():
        raw_input()

