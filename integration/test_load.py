from subprocess import CalledProcessError, check_output  # noqa

import pytest


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """test command load"""
    out = (
        check_output(["dundie", "load", "assets/people.csv"])
        .decode("utf-8")
        .split("\n")
    )
    assert len(out) == 2


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize(
    "wrong_command", ["loady", "carregar", "start", "comando"]
)
def test_load_negative_call_load_command_with_wrong_params(wrong_command):
    """test command load"""
    with pytest.raises(CalledProcessError) as error:
        check_output(
            ["dundie", wrong_command, "tests/assets/people.csv"]
        ).decode("utf-8").split("\n")

    assert "status 2" in str(error.getrepr())
