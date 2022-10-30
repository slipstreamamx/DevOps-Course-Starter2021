from datetime import date, datetime
class Item:

    def __init__(self, id, short_id, name, desc, due, last_modified, status = 'Not Started'):
        self.id = id
        self.short_id = short_id
        self.name = name
        self.desc = desc
        self.due = due
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def fromCard(cls, card):
        due_string = ''
        if card['due'] is not None:
            # format here should match the Trello datetimes
            trello_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            # use strptime to convert the string to a datetime
            due_datetime = datetime.strptime(card['due'], trello_date_format)
           # convert to just the date, and then take the string
            due_string = str(due_datetime.date())
      
        return cls(
            card['_id'],
            card['idShort'], 
            card['name'], 
            card['desc'], 
            due_string,
            datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            card['list']
            )
    
    def modified_today(self):
        return self.last_modified.date() == date.today()
    
    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, desc: {self.desc}, due: {self.due}, status: {self.status}, last_modified: {self.last_modified}"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False

        return self.id == other.id \
            and self.name == other.name \
            and self.status == other.status \
            and self.last_modified == other.last_modified