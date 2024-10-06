import os

def read_button_states(button1_var, button2_var, color_var):
    """Lit les états des boutons depuis des fichiers."""
    try:
        with open('data/button1_state.txt', 'r') as f:
            button1_var.set(f.read().strip() == 'True')
        with open('data/button2_state.txt', 'r') as f:
            button2_var.set(f.read().strip() == 'True')
        with open('data/button3_state.txt', 'r') as f:
            color_var.set(f.read().strip())
    except FileNotFoundError:
        pass  # Si les fichiers n'existent pas, on garde les valeurs par défaut

def save_button_states(button1_var, button2_var, color_var):
    """Enregistre les états des boutons dans des fichiers."""
    with open('data/button1_state.txt', 'w') as f:
        f.write(str(button1_var.get()))
    with open('data/button2_state.txt', 'w') as f:
        f.write(str(button2_var.get()))
    with open('data/button3_state.txt', 'w') as f:
        f.write(color_var.get())
