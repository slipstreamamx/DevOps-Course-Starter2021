
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
        due_date_string = str(card['due'])
        due = due_date_string[0:10]
      
        return cls(card['id'],card['idShort'], card['name'], card['desc'], due, list['name'])

    def start(self):
        self.status='In Progress'

    def complete(self):
        self.status='Completed'

    def reset(self):
        self.status= 'Not Started'