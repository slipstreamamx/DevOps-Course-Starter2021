from datetime import date, datetime
class Item:

    def __init__(self, id, name, desc, due, last_modified, status = 'Not Started'):
        self.id = id
        self.name = name
        self.desc = desc
        self.due = due
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def fromCard(cls, card):      
        return cls(
            card['_id'],
            card['name'], 
            card['desc'], 
            card['due'],
            card['list']
            )
    
    def modified_today(self):
        today = date.today()
        return self.last_modified.date() == today.strftime("%Y-%m-%d")
    
    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, desc: {self.desc}, due: {self.due}, status: {self.status}, last_modified: {self.last_modified}"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False

        return self.id == other.id \
            and self.name == other.name \
            and self.status == other.status \
            and self.last_modified == other.last_modified