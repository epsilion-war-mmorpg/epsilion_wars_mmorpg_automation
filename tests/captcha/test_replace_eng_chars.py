import pytest

from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import replace_eng_chars


@pytest.mark.parametrize('payload, expected', [
    ('a b c e k m n o p r u y x',
     'а ь с е к т п о р г и у х')
])
def test_replace_eng_chars(payload: str, expected: str):
    result = replace_eng_chars(payload)

    assert result == expected
    assert payload == payload
