from datetime import datetime
from freezegun import freeze_time
from todo_app.data.trello_items import Item
from todo_app.view_model import ViewModel

def test_workflows_should_be_empty_if_there_are_no_matching_items():
    items = [
        Item(1, 'Do something', 'workflow does not exists',datetime.now(), datetime.now(), 'Some other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.not_started_items) == 0
    assert len(view_model.in_progress_items) == 0
    assert len(view_model.completed_items) == 0

@freeze_time()
def test_items_are_grouped_into_workflows():
    items = [
        Item(1, 'Do something', 'workflow does not exists', datetime.now(), datetime.now(), 'Some other Status'),
        Item(2, 'Task 2', 'Task 2 not started', datetime.now(), datetime.now(), 'Not Started'),
        Item(3, 'Task 3', 'Task 3 in progress', datetime.now(), datetime.now(), 'In Progress'),
        Item(4, 'Task 4', 'Task 4 completed', datetime.now(), datetime.now(), 'Completed'),
        Item(5, 'Task 5', 'Task 5 not started', datetime.now(), datetime.now(), 'Not Started'),
        Item(6, 'Task 6', 'Task 6 completed', datetime.now(), datetime.now(), 'Completed'),
    ]

    view_model = ViewModel(items)
    assert view_model.not_started_items == [
        Item(2, 'Task 2', 'Task 2 not started', datetime.now(), datetime.now(), 'Not Started'),
        Item(5, 'Task 5', 'Task 5 not started', datetime.now(), datetime.now(), 'Not Started'),
    ]
    assert view_model.in_progress_items == [
        Item(3, 'Task 3', 'Task 3 in progress', datetime.now(), datetime.now(), 'In Progress'),
    ]
    assert view_model.completed_items == [
        Item(4, 'Task 4', 'Task 4 completed', datetime.now(), datetime.now(), 'Completed'),
        Item(6, 'Task 6', 'Task 6 completed', datetime.now(), datetime.now(), 'Completed'),
    ]

def test_all_completed_items_are_shown_if_there_are_five_or_fewer():
    items = [
        Item(2, 'Task 2', 'Task 2 not started', datetime.now(), datetime.now(), 'Completed'),
        Item(3, 'Task 3', 'Task 3 in progress', datetime.now(), datetime.now(), 'Completed'),
        Item(4, 'Task 4', 'Task 4 completed', datetime.now(), datetime.now(), 'Completed'),
        Item(5, 'Task 5', 'Task 5 not started', datetime.now(), datetime.now(), 'Completed'),
        Item(6, 'Task 6', 'Task 6 completed', datetime.now(), datetime.now(), 'Completed'),
    ]

    view_model = ViewModel(items)

    assert view_model.should_show_all_completed_items is True

@freeze_time("2022-04-18")
def test_recent_items_shows_only_items_last_modified_today():
    items = [
        Item(2, 'Task 2', 'Task 2 completed', datetime.now(), datetime(2022, 4, 18), 'Completed'),
        Item(4, 'Task 4', 'Task 4 Completed', datetime.now(), datetime(2022, 4, 18), 'Completed'),
        Item(5, 'Task 5', 'Task 5 not in progress', datetime.now(), datetime(2022, 4, 18), 'In Progress'),
        Item(6, 'Task 6', 'Task 6 not started', datetime.now(), datetime(2022, 4, 18), 'Not Started'),
    ]

    view_model = ViewModel(items)

    assert view_model.recent_completed_items == [
        Item(2, 'Task 2', 'Task 2 completed', datetime.now(), datetime(2022, 4, 18), 'Completed'),
        Item(4, 'Task 4', 'Task 4 Completed', datetime.now(), datetime(2022, 4, 18), 'Completed'),
    ]
    
@freeze_time("2022-04-18")
def test_older_items_contain_only_items_last_modified_before_today():
    items = [
        Item(2, 'Task 2', 'Task 2 completed yesterday', datetime.now(), datetime(2022, 4, 17), 'Completed'),
        Item(3, 'Task 3', 'Task 2 completed today', datetime.now(), datetime(2022, 4, 18), 'Completed'),
        Item(4, 'Task 4', 'Task 4 not started', datetime.now(), datetime(2022, 4, 18), 'Not Started'),
        Item(5, 'Task 5', 'Task 5 not in progress', datetime.now(), datetime(2022, 4, 18), 'In Progress'),
        Item(2, 'Task 6', 'Task 6 completed', datetime.now(), datetime(2022, 4, 18), 'In Progress'),
    ]

    view_model = ViewModel(items)

    assert view_model.older_completed_items == [
        Item(2, 'Task 2', 'Task 2 completed yesterday', datetime.now(), datetime(2022, 4, 17), 'Completed'),
    ]


