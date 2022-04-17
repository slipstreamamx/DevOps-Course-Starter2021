class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def not_started_items(self):
        return [item for item in self._items if item.status == 'Not Started']

    @property
    def In_Progress_items(self):
        return [item for item in self._items if item.status == 'In Progress']

    @property
    def Completed_items(self):
        return [ item for item in self._items if item.status == 'Completed']
    
    @property
    def should_show_all_done_items(self):
        return len(self.done_items) <= 5

    @property
    def recent_done_items(self):
        return [item for item in self.done_items if item.modified_today()]

    @property
    def older_done_items(self):
        return [item for item in self.done_items if not item.modified_today()]
