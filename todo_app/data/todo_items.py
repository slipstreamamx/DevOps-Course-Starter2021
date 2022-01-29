class Item:

    def __init__(self, id, short_id, name, status = 'Not Started'):
        self.id = id
        self.short_id = short_id
        self.name = name
        self.status = status

    @classmethod
    def fromTrelloCard(cls, card, list):
        return cls(card['id'],card['idShort'], card['name'],list['name'])

    def start(self):
        self.status='In Progress'

    def complete(self):
        self.status='Completed'

    def reset(self):
        self.status= 'Not Started'