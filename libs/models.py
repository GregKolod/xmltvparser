class Channel():

    def __init__(self, id, name, icon):
        self.id = id
        self.name = name
        self.icon = icon

class BroadCast():

    def __init__(self, id, channel, title, start_time, end_time, blurb):
        self.id = id
        self.channel = channel
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.blurb = blurb
