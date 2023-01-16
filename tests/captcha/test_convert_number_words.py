import pytest

from epsilion_wars_mmorpg_automation.captcha.symbol_traps_utils import convert_number_words


@pytest.mark.parametrize('payload, expected', [
    ('', ''),
    ('жили были семь козлят и один волк', 'жили были 7 козлят и 1 волк')
])
def test_convert_number_words(payload: str, expected: str):
    result = convert_number_words(payload)

    assert result == expected
    assert payload == payload
