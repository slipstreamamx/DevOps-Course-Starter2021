from datetime import datetime
from freezegun import freeze_time
from todo_app.data.trello_items import Item
from todo_app.view_model import ViewModel

def test_workflows_are_empty_if_no_matching_items():
    items = [
        Item('61fbc', 1, 'Do something', 'workflow does not exists', datetime.now(), 'Some other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.not_started_items) == 0
    assert len(view_model.In_Progress_items) == 0
    assert len(view_model.Completed_items) == 0

@freeze_time()
def test_items_are_split_into_workflows():
    items = [
        Item('f4cc', 1, 'Do something', 'workflow does not exists', datetime.now(), 'Some other Status'),
        Item('43d8', 2, 'Task 2', 'Task 2 not started', datetime.now(), 'Not Started'),
        Item('43d8', 3, 'Task 3', 'Task 3 in progress', datetime.now(), 'In Progress'),
        Item('g3d9', 4, 'Task 4', 'Task 4 completed', datetime.now(), 'Completed'),
        Item('k3d3', 5, 'Task 5', 'Task 5 not started', datetime.now(), 'Not Started'),
        Item('53x9', 6, 'Task 6', 'Task 6 completed', datetime.now(), 'Completed'),
    ]

    view_model = ViewModel(items)
    assert view_model.not_started_items == [
        Item('43d8', 2, 'Task 2', 'Task 2 not started', datetime.now(), 'Not Started'),
        Item('k3d3', 5, 'Task 5', 'Task 5 not started', datetime.now(), 'Not Started')
    ]
    assert view_model.In_Progress_items == [
        Item('43d8', 3, 'Task 3', 'Task 3 in progress', datetime.now(), 'In Progress')
    ]
    assert view_model.Completed_items == [
        Item('g3d9', 4, 'Task 4', 'Task 4 completed', datetime.now(), 'Completed'),
        Item('53x9', 6, 'Task 6', 'Task 6 completed', datetime.now(), 'Completed')
    ]