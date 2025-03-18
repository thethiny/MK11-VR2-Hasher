import pytest
from yaml import full_load

@pytest.fixture()
def vr2_env():
    with open("env.yaml", encoding="utf-8") as f:
        return full_load(f)
