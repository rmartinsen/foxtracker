from unittest.mock import patch

from game_summary import main


@patch('game_summary.publish')
def test_main(publish):
    summary = main(anchor_date='20181121')
    assert 'Fox' in summary
