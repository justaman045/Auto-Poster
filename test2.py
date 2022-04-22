try:
    import tkinter as tk
except:
    import Tkinter as tk


def on_every_keyboard_input(event):
    update_char_length(text, label)


def update_char_length(text_widget, display_widget):
    string_in_text = text_widget.get('1.0', 'end-1c')
    string_length = len(string_in_text)
    display_widget['text'] = string_length


if __name__ == '__main__':
    root = tk.Tk()
    text = tk.Text(root)
    label = tk.Label(root, text=0, justify='center')

    text.bind('<KeyPress>', on_every_keyboard_input)
    text.bind('<KeyRelease>', on_every_keyboard_input)

    label.pack()
    text.pack()
    root.mainloop()
