from datetime import datetime
from freezegun import freeze_time
from todo_app.data.trello_items import Item
from todo_app.view_model import ViewModel

def test_workflows_should_be_empty_if_there_are_no_matching_items():
    items = [
        Item('61fbc', 1, 'Do something', 'workflow does not exists', datetime.now(), 'Some other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.not_started_items) == 0
    assert len(view_model.in_Progress_items) == 0
    assert len(view_model.completed_items) == 0

@freeze_time()
def test_items_are_grouped_into_workflows():
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
        Item('k3d3', 5, 'Task 5', 'Task 5 not started', datetime.now(), 'Not Started'),
    ]
    assert view_model.in_Progress_items == [
        Item('43d8', 3, 'Task 3', 'Task 3 in progress', datetime.now(), 'In Progress'),
    ]
    assert view_model.completed_items == [
        Item('g3d9', 4, 'Task 4', 'Task 4 completed', datetime.now(), 'Completed'),
        Item('53x9', 6, 'Task 6', 'Task 6 completed', datetime.now(), 'Completed'),
    ]

def test_all_completed_items_are_shown_if_there_are_five_or_fewer():
    items = [
        Item('43d8', 2, 'Task 2', 'Task 2 not started', datetime.now(), 'Completed'),
        Item('43d8', 3, 'Task 3', 'Task 3 in progress', datetime.now(), 'Completed'),
        Item('g3d9', 4, 'Task 4', 'Task 4 completed', datetime.now(), 'Completed'),
        Item('k3d3', 5, 'Task 5', 'Task 5 not started', datetime.now(), 'Completed'),
        Item('53x9', 6, 'Task 6', 'Task 6 completed', datetime.now(), 'Completed'),
    ]

    view_model = ViewModel(items)

    assert view_model.should_show_all_completed_items is True

@freeze_time("2022-04-18 10:45:00")
def test_recent_items_shows_only_items_last_modified_today():
    items = [
        Item('43d8', 2, 'Task 2', 'Task 2 not started', datetime.now(2022, 4, 17, 20, 50, 15), 'Completed'),
        Item('43d8', 3, 'Task 3', 'Task 3 in progress', datetime.now(2022, 4, 18, 9, 34, 10), 'Completed'),
        Item('g3d9', 4, 'Task 4', 'Task 4 completed', datetime.now(2022, 4, 18, 20, 50, 15), 'Not Started'),
        Item('k3d3', 5, 'Task 5', 'Task 5 not started', datetime.now(2022, 4, 18, 23, 10, 15), 'In Progress'),
    ]

    view_model = ViewModel(items)

    assert view_model.recent_completed_items == [
        Item('43d8', 3, 'Task 3', 'Task 3 in progress', datetime.now(2022, 4, 18, 9, 34, 10), 'Completed'),
    ]

@freeze_time("2022-04-18 10:45:00")
def test_older_items_contain_only_items_last_modified_before_today():
    items = [
        Item('43d8', 2, 'Task 2', 'Task 2 completed yesterday', datetime.now(2022, 4, 17, 20, 50, 15), 'Completed'),
        Item('43d8', 3, 'Task 3', 'Task 3 completed today', datetime.now(2022, 4, 18, 9, 34, 10), 'Completed'),
        Item('g3d9', 4, 'Task 4', 'Task 4 not started', datetime.now(2022, 4, 18, 20, 50, 15), 'Not Started'),
        Item('k3d3', 5, 'Task 5', 'Task 5 not in progress', datetime.now(2022, 4, 18, 23, 10, 15), 'In Progress'),
    ]

    view_model = ViewModel(items)

    assert view_model.older_completed_items == [
        Item('43d8', 2, 'Task 2', 'Task 2 completed yesterday', datetime.now(2022, 4, 17, 20, 50, 15), 'Completed'),
    ]