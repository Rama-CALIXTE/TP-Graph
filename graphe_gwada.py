import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk


class InterfaceUtilisateur(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)

        self.get_themes()                 # Returns a list of all themes that can be set
        self.set_theme("radiance")        # Sets an available theme

        self.title("Interface Utilisateur Graphe")

        self.guadeloupe = Graphe("Guadeloupe")

        # Créer un conteneur pour les onglets
        self.onglets = ttk.Notebook(self)
        self.onglets.pack(expand=1, fill="both")

        # Onglet 1 : Remplir le graphe depuis un fichier Excel
        self.onglet_remplir_graphe = ttk.Frame(self.onglets)
        self.onglets.add(self.onglet_remplir_graphe, text="Remplir Graphe")

        self.bouton_choisir_fichier = ttk.Button(self.onglet_remplir_graphe, text="Choisir un fichier Excel",
                                                 command=self.choisir_fichier)
        self.bouton_choisir_fichier.pack(pady=10)

        # Onglet 2 : Visualiser le graphe
        self.onglet_visualiser_graphe = ttk.Frame(self.onglets)
        self.onglets.add(self.onglet_visualiser_graphe, text="Visualiser Graphe")

        self.canevas_graphe = tk.Canvas(self.onglet_visualiser_graphe, width=350, height=350, bg='white')
        self.canevas_graphe.pack(pady=10)

        self.bouton_visualiser_graphe = ttk.Button(self.onglet_visualiser_graphe, text="Visualiser Graphe",
                                                    command=self.visualiser_graphe)
        self.bouton_visualiser_graphe.pack(pady=10)

        # Ajoutez des champs de saisie pour les valeurs spécifiées
        self.label_saisie_ville = ttk.Label(self.onglet_visualiser_graphe, text="Saisir une ville:")
        self.label_saisie_ville.pack(pady=5)

        self.entry_ville = ttk.Entry(self.onglet_visualiser_graphe)
        self.entry_ville.pack(pady=10)

        self.bouton_obtenir_voisins = ttk.Button(self.onglet_visualiser_graphe, text="Obtenir Voisins",
                                                 command=self.obtenir_voisins_interface)
        self.bouton_obtenir_voisins.pack(pady=10)

        self.label_ville_source = ttk.Label(self.onglet_visualiser_graphe, text="Ville Source:")
        self.label_ville_source.pack(pady=5)

        self.entry_ville_source = ttk.Entry(self.onglet_visualiser_graphe)
        self.entry_ville_source.pack(pady=10)

        self.label_ville_destination = ttk.Label(self.onglet_visualiser_graphe, text="Ville Destination:")
        self.label_ville_destination.pack(pady=5)

        self.entry_ville_destination = ttk.Entry(self.onglet_visualiser_graphe)
        self.entry_ville_destination.pack(pady=10)

        self.bouton_chemin_optimal = ttk.Button(self.onglet_visualiser_graphe, text="Chemin Optimal",
                                                command=self.chemin_optimum_interface)
        self.bouton_chemin_optimal.pack(pady=10)

        self.label_villes_cycle = ttk.Label(self.onglet_visualiser_graphe, text="Liste de villes (séparées par des virgules):")
        self.label_villes_cycle.pack(pady=5)

        self.entry_villes_cycle = ttk.Entry(self.onglet_visualiser_graphe)
        self.entry_villes_cycle.pack(pady=10)

        self.bouton_cycle_optimal = ttk.Button(self.onglet_visualiser_graphe, text="Cycle Optimal",
                                               command=self.cycle_optimal_interface)
        self.bouton_cycle_optimal.pack(pady=10)

    def obtenir_voisins_interface(self):
        # Récupère la valeur saisie dans le champ de saisie pour la ville
        ville_saisie = self.entry_ville.get()

        # Appelle la fonction obtenir_voisins du graphe avec la ville saisie et affiche le résultat
        voisins = self.guadeloupe.obtenir_voisins(ville_saisie)
        print(f"Voisins de {ville_saisie}: {voisins}")

    def chemin_optimum_interface(self):
        # Récupère les valeurs saisies dans les champs de saisie pour les villes source et destination
        ville_source = self.entry_ville_source.get()
        ville_destination = self.entry_ville_destination.get()

        # Appelle la fonction chemin_optimum du graphe avec les villes source et destination saisies et affiche le résultat
        chemin_optimal, distance_optimale = self.guadeloupe.chemin_optimum(ville_source, ville_destination)
        print(f"Chemin optimal de {ville_source} à {ville_destination}: {chemin_optimal}, Distance optimale: {distance_optimale}")

    def cycle_optimal_interface(self):
        # Récupère la liste de villes saisie dans le champ de saisie
        villes_cycle_saisies = self.entry_villes_cycle.get().split(',')

        # Appelle la fonction cycle_optimal du graphe avec la liste de villes saisies et affiche le résultat
        cycle_optimal, distance_optimale = self.guadeloupe.cycle_optimal(villes_cycle_saisies)
        print(f"Cycle optimal pour les villes {villes_cycle_saisies}: {cycle_optimal}, Distance optimale: {distance_optimale}")

    def choisir_fichier(self):
        fichier_path = filedialog.askopenfilename(filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")])
        if fichier_path:
            self.guadeloupe.remplir_graphe_depuis_excel(fichier_path)
            print(f"Graphe rempli depuis le fichier : {fichier_path}")

    def visualiser_graphe(self):
        self.canevas_graphe.delete("all")  # Efface le canevas avant de redessiner
        self.dessiner_graphe(self.guadeloupe.graph)

    def dessiner_graphe(self, graph):
        # Dessine le graphe sur le canevas
        fig, ax = plt.subplots()
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=ax)

        # Utilise FigureCanvasTkAgg pour afficher la figure dans le canevas Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.onglet_visualiser_graphe)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def matplotlib_to_tk_photo(self, figure):
        # Convertit une figure Matplotlib en image Tkinter
        canvas = FigureCanvasTkAgg(figure, master=self.onglet_visualiser_graphe)
        canvas.draw()
        return self._tkinter_photoimage(canvas)

    def _tkinter_photoimage(self, canvas):
        # Convertit la figure Matplotlib en image Tkinter
        return ImageTk.PhotoImage(canvas.get_tk_widget().photo)


class Graphe:
    def __init__(self, nom):
        # Initialisation d'un nouveau graphe dirigé (DiGraph) avec un nom spécifié.
        self.nom = nom
        self.graph = nx.DiGraph()

    def ajouter_ville(self, nom_ville):
        # Ajoute une ville (ajout d'un sommet au graphe)
        self.graph.add_node(nom_ville)

    def ajouter_chemin(self, ville_source, ville_destination, distance):
        # Ajoute un arc (chemin) du sommet source au sommet destination avec une distance spécifiée.
        self.graph.add_edge(ville_source, ville_destination, distance=distance)

    def remplir_graphe_depuis_excel(self, excel_filename):
        try:
            # Lecture des données du fichier Excel
            data = pd.read_excel(excel_filename, index_col=0)

            # Ajout des communes comme nœuds dans le graphe
            for commune in data.index:
                self.ajouter_ville(commune)

            # Ajout des distances entre les communes comme arcs dans le graphe dirigé
            for ville_source in data.index:
                for ville_destination in data.columns:
                    distance = data.loc[ville_source, ville_destination]
                    if pd.notna(distance):  # Assurez-vous que la distance n'est pas NaN
                        self.ajouter_chemin(ville_source, ville_destination, distance)

        except FileNotFoundError:
            print(f"Le fichier {excel_filename} n'a pas été trouvé.")

    def obtenir_voisins(self, sommet):
        # Retourne la liste des voisins (successors) d'un sommet dans le graphe dirigé.
        return list(self.graph.successors(sommet))

    def chemin_optimum(self, ville_source, ville_destination):
        try:
            # Utilise l'algorithme de Dijkstra pour trouver le chemin et la distance optimaux.
            chemin_optimal = nx.shortest_path(self.graph, ville_source, ville_destination, weight='distance')
            distance_optimale = nx.shortest_path_length(self.graph, ville_source, ville_destination, weight='distance')
            return chemin_optimal, distance_optimale
        except nx.NetworkXNoPath:
            return None, None

    def cycle_optimal(self, villes):
        try:
            # Utilise l'approximation de l'algorithme du voyageur de commerce pour trouver le cycle optimal
            cycle_optimal = nx.approximation.traveling_salesman_problem(self.graph.subgraph(villes), weight='distance', cycle=True)
            distance_optimale = sum(self.graph[villes[i]][villes[i + 1]]['distance'] for i in range(len(villes) - 1))

            # Ajoute le dernier arc pour fermer le cycle
            cycle_optimal.append(cycle_optimal[0])

            return cycle_optimal, distance_optimale
        except nx.NetworkXNoPath:
            return None, None

    def __str__(self):
        # Représentation sous forme de chaîne du graphe, montrant les nœuds et les arcs.
        return f"Graphe: {self.nom}, Noeuds: {list(self.graph.nodes)}, Arcs: {list(self.graph.edges)}"


# Exécutez l'application
if __name__ == "__main__":
    app = InterfaceUtilisateur()
    app.mainloop()