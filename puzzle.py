from tkinter import Frame, Label, CENTER, Button, EW, PhotoImage, Spinbox, StringVar
import random
import logic
import constants as c
from RV.RVRNN import Reconocedor
from RV.conversor.convertidor import crear_data_set

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        crear_data_set()
        self.__rec = Reconocedor()

        self.grid()
        self.master.title('2048')
        self.microphone_icon = PhotoImage(file = "resources/mic.png")

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE)
        background.grid()


        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

        i = c.GRID_LEN #Last row = 4
        
        # Adding input recognition text
        self.input_msg = Label(
            master=background,
            text="Presionar botón",
            bg="white",
            justify="left",
            font=c.FONT,

            )
        self.input_msg.grid(
            row=i,
            column=0,
            columnspan=3,
            sticky=EW,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING,
        )

        # Adding microphone
        self.mic_btn = Button(
            background,
            text="Microfono",
            bg="green",
            image=self.microphone_icon,
            width=c.SIZE / c.GRID_LEN,
            height=c.SIZE / c.GRID_LEN,
            command=self.btn_event
        )
        self.mic_btn.grid(
            row=i,
            column=i-1,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING,
            sticky=EW
        )
        # error label
        self.error_label = Label(
            master=background,
            text="",
            bg=c.BACKGROUND_COLOR_GAME,
            foreground="red",
            justify="left",
            font=("Verdana", 20, "bold"),
            wraplength=500
        )
        self.error_label.grid(
            row=i + 1,
            column=0,
            columnspan=3,
            sticky=EW,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING
        )
        # Adding spinner 
        my_var= StringVar(background)
        my_var.set("22")
        self.sensibility = Spinbox(background, from_=16, to=30, textvariable=my_var, font=c.FONT, width=3)
        self.sensibility.grid(
            row=i+1,
            column=i-1,
            padx=c.GRID_PADDING,
            pady=c.GRID_PADDING
        )

        
    def btn_event(self):
        input1 = ""
        self.mic_btn.configure(state="disabled")
        self.input_msg.configure(text="esperando...", background="#33b5e5")
        #########################
        error = ""
        try:
            input1 = self.__rec.reconocer_voz(int(self.sensibility.get()))
            self.execute_voice_command(input1)
            self.input_msg.configure(text=input1)
        except IndexError as e:
            self.error_label.configure(text=e)
            self.input_msg.configure(text="Comando Invalido")
        self.mic_btn.configure(state="normal", bg="green")
        #########################



    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def execute_voice_command(self, voice_command):
        tokens = voice_command
        if len(tokens) <= 2:
            first_command = tokens[0]
            if first_command in c.VOICE_END:
                exit()
            elif first_command in c.VOICE_BACK:
                if len(self.history_matrixs) > 1:
                    self.matrix = self.history_matrixs.pop()
                    self.update_grid_cells()
                    print('back on step total step:', len(self.history_matrixs))
                else:
                    self.input_msg.configure(background="#FFBC11")
            elif first_command in c.VOICE_ACTION:
                if len(tokens) == 2:
                    second_command = tokens[1]
                    if second_command in c.VOICE_UP:
                        self.execute_movement(logic.up)
                    elif second_command in c.VOICE_DOWN:
                        self.execute_movement(logic.down)
                    elif second_command in c.VOICE_RIGHT:
                        self.execute_movement(logic.right)
                    elif second_command in c.VOICE_LEFT:
                        self.execute_movement(logic.left)
                    else:
                        self.input_msg.configure(background="#C91432")
            else:
                self.input_msg.configure(background="#C91432")
        else:
            self.input_msg.configure(background="#C91432")
        

    def execute_movement(self, action_movement):
        self.matrix, done = action_movement(self.matrix)
        if done:
            self.input_msg.configure(background="#138636")
            self.matrix = logic.add_two(self.matrix)
            # record last move
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()
            if logic.game_state(self.matrix) == 'win':
                self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            if logic.game_state(self.matrix) == 'lose':
                self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        else:
            self.input_msg.configure(background="#FFBC11")

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2
