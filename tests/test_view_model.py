from datetime import datetime
from todo_app import view_model
from todo_app.trello_items import item
from todo_app.view_model import ViewModel

from datetime import datetime

def test_categories_are_empty_if_no_matching_items():
    items = [
        item(1, 'Task 1', datetime.now(), 'Other Status')
    ]

    view_model = view_model(items)

    assert len(view_model.not_started_items) == 0
    assert len(view_model.In_Progress_items) == 0
    assert len(view_model.Completed_items) == 0