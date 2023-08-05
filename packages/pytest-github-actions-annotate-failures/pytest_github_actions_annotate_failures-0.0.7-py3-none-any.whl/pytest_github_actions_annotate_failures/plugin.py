from __future__ import print_function
import os

def pytest_runtest_logreport(report):
    # enable only in a workflow of GitHub Actions
    # ref: https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables#default-environment-variables
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        return

    if report.outcome != 'failed':
        return

    # collect information to be annotated
    filesystempath, lineno, _ = report.location

    # 0-index to 1-index
    lineno += 1

    longrepr = str(report.longrepr)

    print(_error_workflow_command(filesystempath, lineno, longrepr))

def _error_workflow_command(filesystempath, lineno, longrepr):
    if lineno is None:
        if longrepr is None:
            return '\n::error file={}'.format(filesystempath)
        else:
            longrepr = _escape(longrepr)
            return '\n::error file={}::{}'.format(filesystempath, longrepr)
    else:
        if longrepr is None:
            return '\n::error file={},line={}'.format(filesystempath, lineno)
        else:
            longrepr = _escape(longrepr)
            return '\n::error file={},line={}::{}'.format(filesystempath, lineno, longrepr)

def _escape(s):
    return s.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
