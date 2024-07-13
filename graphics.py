from tkinter import Tk, BOTH, Canvas, Button, Label, Entry
from tkinter import messagebox


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self._buttons = {}
        self._entries = {}
        self._formatting()

    ################ UTILS #################################
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def clear_canvas(self):
        self.__canvas.delete("all")

    def wait_for_close(self):
        self.__running = True

        while self.__running:
            self.redraw()
        if not self.__running:
            self.__root.destroy()

            print("window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def create_mb(self, title, message):
        messagebox.showinfo(title=title, message=message)

    def close(self):
        self.__running = False

    def _formatting(self):
        self.create_button("Quit", self.close, "right", "ne")
        self.create_button("Reset", self.clear_canvas, "right", "ne")

        self.create_label("Rows:", "left", "nw")
        self.create_entry("Rows", "left", "nw")
        self.create_label("Columns:", "left", "nw")
        self.create_entry("Columns", "left", "nw")

    def create_button(self, text, command, side, anchhor):
        button = Button(self.__root, text=text, command=command)
        button.pack(side=side, anchor=anchhor)
        self._buttons[text] = button

    def create_entry(self, name, side, anchor):
        entry = Entry(self.__root)
        entry.pack(side=side, anchor=anchor)
        self._entries[name] = entry

    def get_entry_value(self, name):
        return self._entries[name].get()

    def create_label(self, text, side, anchor):
        label = Label(self.__root, text=text)
        label.pack(side=side, anchor=anchor)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# takes two points
class Line:
    def __init__(
        self,
        p1,
        p2,
    ):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
