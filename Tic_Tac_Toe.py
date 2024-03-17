import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random, win32api

# Получаем размер экрана
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Вычисляем размеры окна
window_width = int(screen_width * 0.13)
window_height = int(screen_height * 0.55)

# Вычисляем координаты центра экрана
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)

buttons = {}

def tic_tac_toe(window, window_game_menu):
    global player1_marker, player2_marker, computer_marker, board, game_mode, winning_combinations, winning_color, window_tic_tac_toe
    
    font = ctk.CTkFont(family='Arial', size=20)
    font_2 = ctk.CTkFont(family='Arial', size=18)
    
    def on_game_window_close():
        try:
            window_game_menu.deiconify()
            game_window.destroy()
        except NameError:
            window.deiconify()
            game_window.destroy()
        except AttributeError:
            window.deiconify()
            game_window.destroy()

    try:
        window_game_menu.withdraw()
    except NameError:
        window.withdraw()
    except AttributeError:
        window.withdraw()

    player1_marker = ""
    player2_marker = ""
    computer_marker = ""
    board = [" "] * 10
    game_mode = ""
    winning_combinations = [
        (7, 8, 9), (4, 5, 6), (1, 2, 3),  # горизонтальные линии
        (7, 4, 1), (8, 5, 2), (9, 6, 3),  # вертикальные линии
        (7, 5, 3), (9, 5, 1)  # диагональные линии
    ]
    winning_color = "green"

    def place_marker(position):
        buttons[position].configure(state=tk.DISABLED)
        if game_mode == "player_vs_player":
            if turn_label.cget("text") == "Ход игрока 1":
                board[position] = player1_marker
                buttons[position].configure(text=player1_marker)
                if check_win(player1_marker):
                    result_label.configure(text="Игрок 1 выиграл!", font=font)
                    disable_buttons()
                elif " " not in board[1:]:
                    result_label.configure(text="Ничья!", font=font)
                    disable_buttons()
                else:
                    turn_label.configure(text="Ход игрока 2", font=font)
            else:
                board[position] = player2_marker
                buttons[position].configure(text=player2_marker)
                if check_win(player2_marker):
                    result_label.configure(text="Игрок 2 выиграл!", font=font)
                    disable_buttons()
                elif " " not in board[1:]:
                    result_label.configure(text="Ничья!", font=font)
                    disable_buttons()
                else:
                    turn_label.configure(text="Ход игрока 1", font=font)
        elif game_mode == "player_vs_computer":
            if check_free_space(position):
                board[position] = player1_marker
                buttons[position].configure(text=player1_marker)
                if check_win(player1_marker):
                    result_label.configure(text="Вы выиграли! Поздравляю!", font=font)
                    disable_buttons()
                elif " " not in board[1:]:
                    result_label.configure(text="Ничья!", font=font)
                    disable_buttons()
                else:
                    computer_move()

    def check_win(marker):
        for combination in winning_combinations:
            if all(board[pos] == marker for pos in combination):
                for pos in combination:
                    buttons[pos].configure(fg_color="green", text_color='white')
                return True
        return False

    def check_free_space(position):
        return board[position] == " "

    def disable_buttons():
        for i in range(1, 10):
            buttons[i].configure(state=tk.DISABLED)

    def reset_board_color():
        for i in range(1, 10):
            buttons[i].configure(fg_color="#1f6aa5", text_color='white')

    def create_game_window():
        global buttons, result_label, turn_label, game_window

        instruction_label.pack_forget()
        player_vs_player_button.pack_forget()
        player_vs_computer_button.pack_forget()
        x_button.pack_forget()
        o_button.pack_forget()

        try:
            window_tic_tac_toe.destroy()
        except NameError:
            pass

        game_window = ctk.CTkToplevel(window)
        game_window.title("Крестики-нолики")
        game_window.protocol("WM_DELETE_WINDOW", on_game_window_close)
        game_window.geometry(f"{center_x - int(window_width / 1.2)}+{center_y - int(window_height / 2.5)}")

        for i in range(1, 10):
            buttons[i] = ctk.CTkButton(game_window, text=" ", width=10, height=5, command=lambda position=i: place_marker(position), font=font)
            buttons[i].grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)
            buttons[i].configure(width=100, height=100, text_color='white')

        result_label = ctk.CTkLabel(game_window, text="", font=font)
        result_label.grid(row=3, column=0, columnspan=3, pady=10)

        turn_label = ctk.CTkLabel(game_window, text="Ход игрока 1", font=font)
        turn_label.grid(row=4, column=0, columnspan=3)

        new_game_button = ctk.CTkButton(game_window, text="Новая игра", command=start_new_game, font=font)
        new_game_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        separator = ttk.Separator(game_window, orient=tk.HORIZONTAL)
        separator.grid(row=3, column=0, columnspan=3, pady=10)

    def start_new_game():
        global board, player1_marker, player2_marker
        reset_board_color()
        board = [" "] * 10
        for i in range(1, 10):
            buttons[i].configure(state=tk.NORMAL, text=" ")
        result_label.configure(text="")

    def choose_marker(marker):
        global player1_marker, player2_marker, game_mode, computer_marker
        player1_marker = marker
        player2_marker = "O" if player1_marker == "X" else "X"
        computer_marker = player2_marker
        instruction_label.configure(text="Игрок 1 выбрал маркер '{}'.\nИгрок 2 - маркер '{}'".format(player1_marker, player2_marker))
        if game_mode == "player_vs_computer":
            create_game_window()
            if player1_marker == "X":
                computer_move()
        else:
            game_mode = "player_vs_player"
            create_game_window()

    def choose_game_mode(mode):
        global game_mode
        game_mode = mode
        instruction_label.configure(text="Выберите маркер 'X' или 'O' для Игрока 1")
        x_button.configure(state=tk.NORMAL)
        o_button.configure(state=tk.NORMAL)

    def computer_move():
        try:
            for i in range(1, 10):
                if check_free_space(i):
                    copy = board.copy()
                    copy[i] = computer_marker
                    if check_win(computer_marker):
                        place_marker(i)
                        return

            for i in range(1, 10):
                if check_free_space(i):
                    copy = board.copy()
                    copy[i] = player1_marker
                    if check_win(player1_marker):
                        place_marker(i)
                        return

            free_positions = [i for i in range(1, 10) if check_free_space(i)]
            if free_positions:
                position = random.choice(free_positions)
                if position in buttons:
                    buttons[position].configure(state=tk.DISABLED)
                    board[position] = computer_marker
                    buttons[position].configure(text=computer_marker)
                    if check_win(computer_marker):
                        result_label.configure(text="Компьютер выиграл!")
                        disable_buttons()
                    elif " " not in board[1:]:
                        result_label.configure(text="Ничья!")
                        disable_buttons()
        except tk.TclError:
            game_window.quit()
            window_tic_tac_toe.quit()

    def window_tic_tac_toe_close():
        try:
            window_game_menu.deiconify()
            window_tic_tac_toe.destroy()
        except NameError:
            window.deiconify()
            window_tic_tac_toe.destroy()

    window_tic_tac_toe = ctk.CTkToplevel(window)
    window_tic_tac_toe.title("Меню крестики-нолики")
    window_tic_tac_toe.protocol('WM_DELETE_WINDOW', window_tic_tac_toe_close)
    window_tic_tac_toe.geometry(f"{center_x - int(window_width / 0.55)}+{center_y - int(window_height / 4)}")

    instruction_label = ctk.CTkLabel(window_tic_tac_toe, text="Выберите режим игры", font=font)
    instruction_label.pack(pady=10)

    player_vs_player_button = ctk.CTkButton(window_tic_tac_toe, text="Игрок против игрока", command=lambda: choose_game_mode("player_vs_player"), font=font)
    player_vs_computer_button = ctk.CTkButton(window_tic_tac_toe, text="Игрок против компьютера", command=lambda: choose_game_mode("player_vs_computer"), font=font)
    player_vs_player_button.pack(side=tk.LEFT, padx=10)
    player_vs_computer_button.pack(side=tk.LEFT, padx=10)

    x_button = ctk.CTkButton(window_tic_tac_toe, text="X", state=tk.DISABLED, command=lambda: choose_marker("X"), font=font)
    o_button = ctk.CTkButton(window_tic_tac_toe, text="O", state=tk.DISABLED, command=lambda: choose_marker("O"), font=font)
    x_button.pack(side=tk.LEFT, padx=10)
    o_button.pack(side=tk.LEFT, padx=10)

    window_tic_tac_toe.configure(bg="white")