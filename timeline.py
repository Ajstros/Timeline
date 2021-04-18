from datetime import date
import csv
from enum import Enum

# Class for the Timeline itself. Contains a list of events, 
# the orientation of the timeline (1:vertical, 0:horizontal), 
# and order of events (1:forward in time, -1:backward in time). 
# Timeline can be saved to files in CSV format and opened from
# those same files.
class Timeline:
    def __init__(self, title, events, orientation, order):
        self.title = title
        self.events = events
        self.orientation = orientation # 1:vertical, 0:horizontal
        self.order = order # 1:forward, -1:backward, order is used for displaying the timeline, the events list is always stored forward in time

    # Class method for creating an empty timeline with a new title.
    # Defaults to vertical orientation and forward order in time.
    @classmethod
    def new_empty_timeline(cls, title):
        return cls(title, [], Orientation.VERTICAL, Order.FORWARD)

    # Class method for opening a saved timeline from a text file.
    @classmethod
    def from_csv(cls, file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            timeline_data = reader[0]
            try:
                events_data = reader[1:] # If there are no events, our event_data is an empty list
            except IndexError:
                events_data = []
                
        title = timeline_data[0]
        events = []
        orientation = timeline_data[1]
        order = timeline_data[2]

        for data in events_data:
            # Ex. Mission Report,1991-12-16,CE
            event_title = data[0]
            event_date = date.fromisoformat(data[1])
            event_era = data[2]
            # Don't have to sort here because the data will have been saved in order
            events.append(TimelineEvent(event_title, event_date, event_era))
        
        return cls(title, events, orientation, order)


    # Method to add a new event to the list of events. 
    # The new event is placed in its correct position for forward in time order.
    def add_event(self, new_event):
        # BC or BCE before AD or CE
        for index in range(len(self.events)):
            event = self.events[index]
            if new_event.get_era() < event.get_era:
                self.events.insert(new_event, index) # If BC or BCE compared to AD or CE, insert
            elif new_event.get_era() > event.get_era:
                continue
            else: # Same era
                if new_event.get_date < event.get_date: # If date is before, insert. This means for equal dates, the new date will go after the current one
                    self.events.insert(new_event, index)
                else:
                    continue
        return
        
    # Method to remove an event from the list of events by its index.
    def remove_event(self, event_index):
        self.events.remove(event_index)
        return

    # Method to save the timeline in CSV format to a file named file_name.
    def save(self, file_name):
        with open(file_name, 'w') as file:
            writer = csv.writer(file)
            # Ex. Flashpoint,1,1 is a timeline titled Flashpoint, oriented vertically, ordered forward in time
            writer.writerow(self.title+','+self.orientation+','+self.order)
            for event in self.events:
                # Ex. Mission Report,1991-12-16,CE
                writer.writerow(str(event))


# Class to represent an Event in time. Contains the Event's title, 
# date as a datetime.date object, and era (BC, AD, BCE, CE).
class TimelineEvent:
    def __init__(self, title, date, era):
        self.title = title
        self.date = date
        self.era = era

    # Method to get the string representation of the event, which is used in writing the event to CSV file
    def __str__(self):
        # Ex. Mission Report,1991-12-16,CE
        return self.title+','+str(self.date)+','+self.era

    def get_title(self):
        return self.title
        
    def get_date(self):
        return self.date

    def get_era(self):
        return self.era


# Enum for the orientation of the Timeline
class Orientation(Enum):
    VERTICAL = 1
    HORIZONTAL = 0


# Enum for the order of the Timeline
class Order(Enum):
    FORWARD = 1
    BACKWARD = -1


# Enum for the era of the Events
class Era(Enum):
    BC = 1
    BCE = 1
    AD = 2
    CE = 2
