from epsilion_wars_mmorpg_automation.stats import collector


def test_get_counters_happy_path():
    collector.reset()
    collector.inc_value('first')
    collector.inc_value('second', 2)

    result = collector.get_counters()

    assert result == [
        ('second', 2),
        ('first', 1),
    ]
