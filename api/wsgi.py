import os

from main import api as application

if __name__ == "__main__":
    """
    NOTE - These should default to None unless we're
    running in  a dev environment
    """

    host_ = os.environ.get("DEV__HOST", "0.0.0.0")
    port_ = os.environ.get("DEV__PORT", 80)

    application.run(host=host_, port=port_)
