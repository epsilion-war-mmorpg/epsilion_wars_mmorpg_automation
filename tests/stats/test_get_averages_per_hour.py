from epsilion_wars_mmorpg_automation.stats import collector


def test_get_averages_per_hour_happy_path(mocker):
    collector.reset()
    mocker.patch(
        'epsilion_wars_mmorpg_automation.stats.collector._collecting_time',
        return_value=15 * 60,
    )
    collector.inc_value('first', 1)
    collector.inc_value('second', 20)
    collector.inc_value('rand', 1)
    collector.inc_value('rand', 2)
    collector.inc_value('rand', 3)

    result = collector.get_averages_per_hour()

    assert result == [
        ('first', 4),
        ('second', 80),
        ('rand', 24),
    ]
