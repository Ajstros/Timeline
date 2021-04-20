# Program for the GUI for the Timeline. Users can add or remove events to the timeline,
# save or open a timeline, change the orientation, and change the order.

from timeline import *
from tkinter import *

class GUI:
    def __init__(self):
        self.create_new()
        self.root = Tk()
        self.root.title("Timeline")
        self.root.geometry('600x600')

        self.menu = Menu(self.root)

        self.item = Menu(self.menu)
        self.item.add_command(label='New', command=self.create_new)
        self.item.add_command(label='Open', command=self.open)
        self.item.add_command(label='Save', command=self.save)
        self.menu.add_cascade(label='File', menu=self.item)

        self.root.config(menu=self.menu)

        self.canvas = Canvas(self.root, bg='White', height=600, width=300)
        self.canvas.grid(column=3, row=0, rowspan=600)

        self.draw_btn = Button(self.root, text='Draw', command=self.draw)
        self.draw_btn.grid(column=1, row=11)

        self.event_titles_label = Label(self.root, text='Title')
        self.event_titles_label.grid(column=1, row=0)
        self.event_titles = []
        for i in range(10):
            self.event_titles.append(Entry(self.root, width=10))
            self.event_titles[i].grid(column=1, row=i+1)

        self.event_dates_label = Label(self.root, text='Date')
        self.event_dates_label.grid(column=2, row=0)
        self.event_dates = []
        for i in range(10):
            self.event_dates.append(Entry(self.root, width=10))
            self.event_dates[i].grid(column=2, row=i+1)

        self.root.mainloop()

    # Function to create a new Timeline in the GUI
    def create_new(self):
        self.timeline = Timeline.new_empty_timeline('Timeline')
        return

    # Function to open a saved Timeline CSV file in the GUI
    def open(self):
        # self.timeline = Timeline.from_csv()
        return

    # Function to save the current Timeline in a CSV file
    def save(self):
        return

    def draw(self):
        self.canvas.delete('all')
        self.canvas.create_line(150, 0, 150, 600)
        self.timeline.clear_events()

        for i in range(10):
            try:
                new_event = TimelineEvent(self.event_titles[i].get(), date.fromisoformat(self.event_dates[i].get()), Era.CE)
            except ValueError:
                print('ValueError at '+str(i))
                continue
            self.timeline.add_event(new_event)
        
        print([x.date for x in self.timeline.get_events()])

        ordered_labels = []
        side = 0
        try:
            time_span_days = (self.timeline.get_events()[-1].date - self.timeline.get_events()[0].date).days
        except IndexError:
            return
        if time_span_days == 0:
            day_distance = 1
        else:
            day_distance = 570/time_span_days
        first_date = self.timeline.get_events()[0].date

        for event in self.timeline.get_events():
            height = (event.date - first_date).days * day_distance + 10
            self.canvas.create_window(
                100+100*side, height, window=Label(self.canvas, text=event.title))
            self.canvas.create_line(150, height, 100+100*side, height)
            if side:
                side = 0
            else:
                side = 1
        
        return

gui = GUI()
