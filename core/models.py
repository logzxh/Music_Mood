import mongoengine as me

class UserProfile(me.Document):
    username = me.StringField(required=True, unique=True)
    mood_history = me.ListField(me.DictField())  # stores list of dicts
    preferences = me.DictField(default=dict)

    def __str__(self):
        return self.username

    meta = {
        'collection': 'user_profiles'
    }

class Recipe(me.Document):
    name = me.StringField(required=True)
    ingredients = me.ListField(me.DictField())
    taste = me.StringField()
    budget = me.StringField(choices=["low", "medium", "high"])

    def __str__(self):
        return self.name

    meta = {
        'collection': 'recipes'
    }