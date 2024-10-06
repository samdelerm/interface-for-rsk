import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser
from src.drawing import *
from src.state_manager import read_button_states, save_button_states
from src.geometry_utils import calculate_line_equation


class SoccerFieldSimulator(tk.Tk):
    def __init__(self, client):
        super().__init__()
        self.title("Soccer Field Simulator")
        self.geometry("1200x600")
        self.configure(bg="black")
        
        self.client = client  # Instance du client rsk


        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Canvas pour le terrain de football
        self.canvas = tk.Canvas(self, bg="green")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Frame de contrôle (boutons et sélecteur de couleur)
        self.control_frame = tk.Frame(self, bg="#36013f", padx=10, pady=10)
        self.control_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        self.button1_var = tk.BooleanVar(value=True)
        self.button2_var = tk.BooleanVar(value=True)
        self.color_var = tk.StringVar(value="green")

        # Widgets de contrôle
        self.button1 = ttk.Checkbutton(self.control_frame, text="Direction of robot", variable=self.button1_var)
        self.button2 = ttk.Checkbutton(self.control_frame, text="Axe of goal", variable=self.button2_var)
        self.color_selector = ttk.Combobox(self.control_frame, textvariable=self.color_var, values=["green", "blue"])

        self.button1.grid(row=0, column=0, sticky="ew", pady=5)
        self.button2.grid(row=1, column=0, sticky="ew", pady=5)
        self.color_selector.grid(row=2, column=0, sticky="ew", pady=5)

        # Ajouter le bouton de redirection web
        self.create_web_button("https://robot-soccer-kit.github.io/", "documentation", t=3)
        self.create_web_button("les-amicales.fr", "les amicales", t=4)
        self.create_web_button("python.org", "python", t=5)

        # Ajouter l'espace d'écriture
        self.create_text_area()


        # Frame pour afficher les coordonnées
        self.coord_frame = tk.Frame(self, bg="#36013f", padx=10, pady=10)
        self.coord_frame.grid(row=0, column=2, sticky="ns", padx=10, pady=10)
        self.coord_label = tk.Label(self.coord_frame, text="Coordinates:\n", bg="#36013f", fg="white", font=("Arial", 12))
        self.coord_label.grid(row=0, column=0, sticky="nsw")

        # Lecture des états des boutons
        read_button_states(self.button1_var, self.button2_var, self.color_var)

        # Liaison d'événements
        self.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.teleport_ball)
        self.canvas.bind("<Button-3>", self.client.teleport_ball(0,0))

        # Lancement de la mise à jour
        self.after(10, self.update_field)

    def create_web_button(self, url, button_text="Visit Website", t=int()):
        """Crée un bouton qui redirige vers un site web spécifié."""
        def open_web():
            webbrowser.open(url)
        
        button = tk.Button(self.control_frame, text=button_text, command=open_web)
        button.grid(row=t, column=0, sticky="ew", pady=5)

    def create_text_area(self):
        """Crée un espace d'écriture et un bouton pour enregistrer le contenu."""
        self.text_area = tk.Text(self.control_frame, height=10, width=30)
        self.text_area.grid(row=6, column=0, sticky="ew", pady=5)

        save_button = tk.Button(self.control_frame, text="Save Text", command=self.save_text)
        save_button.grid(row=7, column=0, sticky="ew", pady=5)

    def save_text(self):
        """Enregistre le contenu de l'espace d'écriture dans un fichier."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

    def on_resize(self, event):
        """Met à jour les éléments statiques lors du redimensionnement."""
        draw_static_elements(self.canvas)

    def teleport_ball(self, event):
        """Téléporte la balle à la position cliquée sur le terrain."""
        field_x, field_y = self.convert_coords(event.x, event.y, to_canvas=False)
        self.client.teleport_ball(field_x, field_y)

    def calculate_half_line_equation(self, green1_position, ball_position):
        """
        Retourne l'équation de la demi-droite qui a pour origine green1 et passe par la balle.
        Retourne (a, b) où 'a' est la pente et 'b' est l'ordonnée à l'origine.
        Si la demi-droite est verticale, retourne None.
        """
        return calculate_line_equation(green1_position, ball_position)

    def update_coordinates_display(self, ball_pos, robot1_pos, robot2_pos, robot3_pos, robot4_pos, score1, score2):
        """Update the coordinates display in the UI."""
        display_text = (
            f"Ball Position: ({ball_pos[0]:.2f}, {ball_pos[1]:.2f})\n"
            f"Robot green1: ({robot1_pos[0]:.2f}, {robot1_pos[1]:.2f})\n"
            f"Robot green2: ({robot2_pos[0]:.2f}, {robot2_pos[1]:.2f})\n"
            f"Robot blue1: ({robot3_pos[0]:.2f}, {robot3_pos[1]:.2f})\n"
            f"Robot blue2: ({robot4_pos[0]:.2f}, {robot4_pos[1]:.2f})\n"
            f"Half Line Equation of green 1: {self.calculate_half_line_equation(robot1_pos, ball_pos)}\n"
            f"Score: {score1} - {score2}\n"
        )
        self.coord_label.config(text=display_text, font=("Arial", 12))

    def update_field(self):
        self.update_coordinates_display(self.client.ball, self.client.green1.position, self.client.green2.position, self.client.blue1.position, self.client.blue2.position, self.client.referee['teams']['green']['score'], self.client.referee['teams']['blue']['score'])
        draw_dynamic_elements(self.canvas, self.client, self.button1_var, self.button2_var, self.color_var)
        self.after(100, self.update_field)  # Répète la mise à jour toutes les 100ms


    def convert_coords(self, x, y, to_canvas=False):
        """Convertit les coordonnées du terrain à celles du canvas, et inversement."""
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if to_canvas:
            return (x * self.scale_factor() + width / 2, y * -self.scale_factor() + height / 2)
        else:
            return (x - width / 2) / self.scale_factor(), (height / 2 - y) / self.scale_factor()

    def scale_factor(self):
        """Calcule le facteur d'échelle en fonction de la taille du canvas."""
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        return min(width, height) / 2

