import os


def get_required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise Exception(f"{var_name} environment variable is required.")
    return value
