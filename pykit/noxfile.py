
import os
import nox


DEFAULT_PYTHON_VERSIONS = ["3.8"]
PYTHON_VERSIONS = os.environ.get(
    "NOX_PYTHON_VERSIONS", ",".join(DEFAULT_PYTHON_VERSIONS)
).split(",")

SILENT = False


def deps(session, editable_install=False):
    session.install("--upgrade", "setuptools", "pip", silent=SILENT)
    session.run("pip", "install", "-r", "requirements/dev.txt", silent=SILENT)
    session.run("pip", "install", "-r",
                "requirements/requirements.txt", silent=SILENT)


@nox.session(python=PYTHON_VERSIONS)
def pykit(session):
    deps(session)
