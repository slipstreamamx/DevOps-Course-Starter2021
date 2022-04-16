from datetime import datetime
class Item:

    def __init__(self, id, short_id, name, desc, due, status = 'Not Started'):
        self.id = id
        self.short_id = short_id
        self.name = name
        self.desc = desc
        self.due = due
        self.status = status

    @classmethod
    def fromTrelloCard(cls, card, list):
        due_string = ''
        if card['due'] is not None:
            # format here should match the Trello datetimes
            trello_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            # use strptime to convert the string to a datetime
            due_datetime = datetime.strptime(card['due'], trello_date_format)
           # convert to just the date, and then take the string
            due_string = str(due_datetime.date())
      
        return cls(card['id'],card['idShort'], card['name'], card['desc'], due_string, list['name'])