__author__ = 'Gabriel Salgado and Milo Utsch'
__version__ = '0.1.2'

from take_satisfaction.utils import load_params


def test_load_params():
    params = load_params()
    assert isinstance(params, dict)
    assert 'bot_events_answer_column' in params
    assert 'bot_events_quantities_column' in params
    assert 'bot_satisfaction_level_column' in params
    assert 'bot_satisfaction_quantity_column' in params
    assert 'databricks_query' in params
    assert 'scale_manual' in params
    assert 'scale_translations' in params

