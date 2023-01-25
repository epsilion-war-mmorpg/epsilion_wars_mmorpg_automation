from epsilion_wars_mmorpg_automation.stats import collector, show_stats


async def test_show_stats_happy_path():
    collector.inc_value('test')
    collector.inc_value('best', 22)

    result = await show_stats()

    assert result is None
