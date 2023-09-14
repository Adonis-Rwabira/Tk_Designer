import Pmw
from tkinter import*
import tkinter as Tkinter
import tkinter.ttk as Ttk
import tkinter.tix as Tix
import customtkinter as CustomTk
from os import chdir, listdir
from os.path import dirname
from tkinter.font import Font
from tkinter.ttk import Style, Notebook
from tkinter.messagebox import askyesno

class TkGuiBuilder(Tix.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tk Gui Builder")
        self.configure(bg="SystemButtonFace")
        self.maxsize(self.winfo_screenwidth()-10, self.winfo_screenheight())
        self.geometry(f"{self.winfo_screenwidth() - 10}x{self.winfo_screenheight() - 90}+0+0")

        # Definition des evenements
        self.bind("<Any-KeyPress>", self.key_combination)
        
        self.style = Style()
        self.style.theme_use("xpnative")
        #self.option_readfile(dirname(__file__)+r"\Tk_Gui.TkSS")

        self.notebook =  Notebook(self)
        self.notebook.pack(padx=2)

        # tab actuel
        self.tab = Tkinter

        # Evenement de changement de tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_Change)

        # Initialisation de la premiere fenêtre à afficher
        self.fenetre =  Toplevel(self, class_="fenetre")
        self.fenetre.title("Fenêtre")
        self.fenetre.wm_transient(self.master)

        # Lier l'événement de clic à la fonction d'ajou de widget
        self.bind_class("fenetre", "<Button-1>", self.create_widget)

        # Lier l'événement de pression de la touche "Delete" à la fonction de suppression du widget
        self.bind_class("fenetre", "<Delete>", self.delete_widget)

        # Création du dictionnaire avec les listes de widgets
        self.widgets_dict = {
            "Tkinter": [
                "Button", "Label", "Entry", "Text", "Checkbutton", "Radiobutton",  "Frame",
                "OptionMenu", "LabelFrame", "Scrollbar", "Canvas", "Menu", "Listbox",
                "Menubutton","Scale", "PanedWindow", "Message", "Spinbox"
            ],

            "Ttk": [
                "Button", "Label", "Entry", "Combobox", "Checkbutton", "Radiobutton",
                "Scrollbar", "Treeview", "Progressbar", "Notebook", "Frame","Scale",
                "LabelFrame", "Menubutton", "PanedWindow", "Separator","Sizegrip"
            ],
            
            "Tix": [
                "Balloon", "ButtonBox", "CheckList", "ComboBox", "Control", "DirList",
                "OptionMenu", "DirSelectBox", "ExFileSelectBox", "FileEntry",
                "FileSelectBox", "HList", "LabelEntry", "LabelFrame", "ListNoteBook",
                "Meter", "NoteBook", "ScrolledHList", "ScrolledListBox", "ScrolledText",
                "ScrolledTList", "Select", "TList", "Tree"
            ],

            "Pmw": [
                "AboutDialog", "Balloon", "ButtonBox", "ComboBox", "ComboBoxDialog",
                "Counter", "CounterDialog", "Dialog", "EntryField", "Group",
                "HistoryText", "LabeledWidget", "MainMenuBar", "MenuBar", "MessageBar",
                "MessageDialog", "NoteBook", "OptionMenu", "PanedWidget", "PromptDialog",
                "RadioSelect", "ScrolledCanvas", "ScrolledField", "ScrolledFrame",
                "ScrolledListBox", "ScrolledText", "SelectionDialog", "TextDialog",
                "TimeCounter"
            ],

            "CustomTk": [
                "CTkCanvas", "CTkButton", "CTkCheckBox", "CTkComboBox",
                "CTkEntry", "CTkFrame", "CTkLabel", "CTkOptionMenu", "CTkProgressBar",
                "CTkRadioButton", "CTkScrollbar", "CTkSegmentedButton", "CTkSlider",
                "CTkSwitch", "CTkTabview", "CTkTextbox", "CTkScrollableFrame", "CTkInputDialog"
            ]
        }
        
        # Initialisation de la variable pour les boutons radio
        self.selected_widget =  StringVar()
        self.selected_widget.set("")
        
        # Importation de toutes les images
        chdir(dirname(__file__)+r"\Images")
        self.images = []
        for image in listdir():
            self.images.append(PhotoImage(image[:-4], file=image))

        # Création des pages du notebook à partir du dictionnaire
        for category, widgets in self.widgets_dict.items():
            page =  Frame(self.notebook, bg="white", bd=0, relief=RIDGE)
            self.notebook.add(page, text=category)

            for widget in widgets:
                try:  
                    Radio = Radiobutton(
                    page,
                    bd = 0,
                    text = ".",
                    padx = 1,
                    pady = 2,
                    fg = "white",
                    bg = "white",
                    offrelief = FLAT,
                    value = category+" "+ widget,
                    compound = "left",
                    cursor = "hand2",
                    selectcolor = "cyan",
                    #selectimage = category+widget+"1"
                    indicatoron = False,
                    variable = self.selected_widget,
                    image = category+widget,
                    takefocus = False,
                )
                
                    Radio.pack(side=LEFT, padx=5, pady=4, anchor=CENTER)
                    Radio.bind("<Button-1>", self.select_to_create)
                except: ...
        self.last_selected = Radio
         
        self.option_Frame = Pmw.ScrolledFrame(
            self,
            borderframe = 2,
            labelpos = 'n',
            label_text = 'Widget options',
            usehullsize = 1,
            hull_width = 300,
            relief=RIDGE,
            bg="white"
        )

        self.option_Frame.pack(side=LEFT, fill=Y, anchor=NW, padx=6, pady=6)

        self.V_Splitter = PanedWindow(self, orient=HORIZONTAL)
        self.V_Splitter.pack(padx=5, pady=5)

        self.midle_Frame = PanedWindow(self)
        self.V_Splitter.add(self.midle_Frame)
        
        self.code_Frame = Frame(self.midle_Frame, relief=FLAT, bd=0)
        self.code_Frame.pack(side=TOP)

        self.code_Text = Pmw.ScrolledText(
            self.code_Frame,
            borderframe = 1,
            labelpos = 'nw',
            label_text='',
            usehullsize = 1,
            hull_width = self.winfo_screenwidth()-280,
            hull_height = self.winfo_screenheight()-80,
            text_padx = 10,
            text_pady = 10,
            text_wrap='word',
            relief=SUNKEN,
            bg="white"
        )
        self.code_Text.pack()

        self.message_Frame = Pmw.ScrolledText(
            self.midle_Frame,
            borderframe = 1,
            labelpos = 'nw',
            label_text = "Message",
            usehullsize = 1,
            hull_width = 100,
            hull_height = 250,
            text_padx = 10,
            text_pady = 10,
            text_wrap='word',
            relief=SUNKEN,
            bg="white"
        )
        self.message_Frame.place(x=0, rely=0.72, relwidth=1, relheight=0.28)

        self.separator = Ttk.Separator(
            self.midle_Frame,
            cursor="sb_v_double_arrow",
            orient=HORIZONTAL)
        
        self.separator.place(x=0, rely=0.715, relwidth=1, height=3)
        self.style.configure("TSeparator", background="blacka")
        self.separator.bind("<Button-1>", self.toggle_resizing)
        self.separator.bind("<Motion>", self.resize_message_Frame)
        self.separator.bind("<ButtonRelease>", self.toggle_resizing)
        
        # Le canvas pour afficher les éléments de rédimensionnenent
        self.canvas =  Canvas(self.fenetre, bg="white")
        
        # Dessin du cadre entourant le widget
        self.canvas.create_rectangle(0, 0, self.canvas["width"], self.canvas["height"], outline="blue", width=1, dash=1, tag="rectangle")
        
        # Afficage des points de rédimensionnenent
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_NE", "size_nw_se", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_N", "sb_v_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_NW", "size_ne_sw", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_W", "sb_h_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point5_SW", "size_nw_se", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_S", "sb_v_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_SE", "size_ne_sw", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), fill="black", tag=("point_E", "sb_h_double_arrow", "points"))

        self.canvas.tag_bind("points", "<Enter>", self.change_cursor)

        # Lier l'événement de  redimensionnement des widgets
        self.canvas.tag_bind("points", "<Motion>", self.resize_widget)
        self.canvas.tag_bind("points", "<Button-1>", self.toggle_resizing)
        self.canvas.tag_bind("points", "<ButtonRelease>", self.toggle_resizing)

        # Variable pour les widgets de la fenetre
        self.widget = None
        self.resizing = False
        self.widgets = {}
        self.options = {}

    def on_tab_Change(self, event):
        self.tab = eval(list(self.widgets_dict).__getitem__(self.notebook.tabs().index(self.notebook.select())))

    def select_to_create(self, event):
        self.last_selected.configure(font=("Segoe UI", 10))
        event.widget.configure(font=("Segoe UI", 10))
        self.last_selected = event.widget
        self.fenetre.lift()
    
    def change_cursor(self, event):
        self.canvas["cursor"] = event.widget.gettags("current")[1]

    def create_widget(self, event): # Fonction pour ajouter le widget sélectionné à l'emplacemen du clic
        widget_type = self.selected_widget.get().split(" ")[1]
        if widget_type:
            x, y = event.x, event.y

            try: widget = getattr(self.tab, widget_type)(self.fenetre, cursor="fleur")
            except (AttributeError, KeyError): ...

            if "text" in widget.keys(): widget["text"] = widget.winfo_class()
            if "takefocus" in widget.keys(): widget["takefocus"] = False
            widget.place(x=x, y=y)

            # Actualisation de l'affichage
            self.update_idletasks()
            
            # Lier l'événement de déplacement du widget
            widget.bind("<Motion>", self.move_widget)
            widget.bind("<Button-1>", lambda e: self.select_widget(widget))

            # Selectiong of the widget pour modification
            self.select_widget(widget)

            # Déselectionner le widget selectionné
            self.selected_widget.set("")
            self.last_selected.configure(font=("Segoe UI", 10))

        elif self.fenetre == event.widget: # Déselection du widget en supprimmant le rectangle te les points de redimensionnement
            self.canvas.place_forget()
            self.resizing = False

    def select_widget(self, widget):
        self.widget = widget
        
        # Récupération de la position de la souris pour le déplacement du widget
        self.start_x, self.start_y = self.winfo_pointerxy()

        x, y, width, height = self.widget.winfo_x()-10, self.widget.winfo_y()-10, self.widget.winfo_width()+20, self.widget.winfo_height()+20
        
        self.canvas.configure(bg=self.nametowidget(self.widget.winfo_parent())["bg"], width=width, height=height)
        self.canvas.place(in_=self.widget.winfo_parent(), x=x, y=y)

        # Dessin du cadre entourant le widget
        self.canvas.coords("rectangle", (5, 5, width-5, height-5))
        
        # Afficage des points de rédimensionnenent
        self.canvas.coords("point_NE", (3, 3, 7, 7))
        self.canvas.coords("point_N", ((width / 2)-2, 3, (width / 2)+2, 7))
        self.canvas.coords("point_NW", (width-3, 3, width-7, 7))
        self.canvas.coords("point_W", (width-3, (height / 2)-2, width-7, (height / 2)+2))
        self.canvas.coords("point5_SW", (width-3, height-3, width-7, height-7))
        self.canvas.coords("point_S", ((width / 2)-2, height-3, (width / 2)+2, height-7))
        self.canvas.coords("point_SE", (3, height-3, 7, height-7))
        self.canvas.coords("point_E", (3, (height / 2)-2, 7, (height / 2)+2))

        # Actualisation de l'affichage
        self.update_idletasks()

    def delete_widget(self, event):
        # Fonction pour supprimer le widget sélectionné
        if self.widget and askyesno("Suppresion", "Voulez-vous supprimez ce widget ?"):
            self.widget.destroy()
            self.widget = None

            self.canvas.place_forget()
        else: self.bell()

    def resize_widget(self, event): # Rédimensionner le widget en maintenant le clic gauche de la souris
        if self.widget and self.resizing:
            delta_x, delta_y = event.x_root - self.start_x, event.y_root - self.start_y

            #print(f"winfo_width = {self.widget.winfo_width()}, width = {self.widget['width']}")
            try:
                raise
                if delta_x // Font(font=self.widget['font']).measure('1') == self.widget["widrh"]:
                    delta_x1 = int(delta_x / Font(font=self.widget['font']).measure('1'))
                    delta_y1 = int(delta_y / Font(font=self.widget['font']).metrics("ascent"))
                    if delta_x1 == delta_y1 == 0 : return
                else: raise

            except: delta_x1, delta_y1 = delta_x,delta_y

            if "W" in event.widget.gettags(CURRENT)[0]:
                self.widget.place_configure(width=int(self.widget.winfo_width() + delta_x1))

            elif "E" in event.widget.gettags(CURRENT)[0]:
                #self.widget["width"] = int(self.widget["width"]) - delta_x1
                self.widget.place_configure(x=self.widget.winfo_x() + delta_x, width=int(self.widget.winfo_width()) - delta_x1)

            if "S" in event.widget.gettags(CURRENT)[0]:
                #self.widget["height"] = int(self.widget["height"]) + delta_y1
                self.widget.place_configure(height=int(self.widget.winfo_height() + delta_y1))

            elif "N" in event.widget.gettags(CURRENT)[0]:
                #self.widget["height"] = int(self.widget["height"]) - delta_y1
                self.widget.place_configure(y=self.widget.winfo_y() + delta_y, height=int(self.widget.winfo_height()) - delta_y1)

            # Enregistrement de la nouvelle position de la souris
            self.update_idletasks()
            self.start_x, self.start_y = self.winfo_pointerxy()

            # déplacer aussi le rectangle de rédimensionnement
            self.select_widget(self.widget)

    def resize_message_Frame(self, event):
        if self.resizing:
            delta_y = event.y_root - self.start_y
            y = int(self.message_Frame.place_info()["y"]) + delta_y
            height = self.message_Frame.winfo_height() + delta_y

            self.separator.place_configure(y=y+1)
            self.message_Frame.place_configure(height=height, y=y)

            self.start_x, self.start_y = self.winfo_pointerxy()

    def move_widget(self, event): # Fonction déplacer le widget dans la fénêtre
        if self.widget and event.state == 256:
            delta_x, delta_y = event.x_root - self.start_x, event.y_root - self.start_y
            x, y = event.widget.winfo_x() + delta_x, event.widget.winfo_y() + delta_y

            self.widget.place_configure(x=x, y=y)
            
            # déplacer aussi le rectangle de redimensionnement
            self.select_widget(self.widget)

            # Enregistrement de la nouvelle position de la souris
            self.start_x, self.start_y = self.winfo_pointerxy()
    
    def toggle_resizing(self, event): # Active | Désactive le rédimensionnement
        # Récupération de la position de la souris
        self.start_x, self.start_y = self.winfo_pointerxy()

        # Toggle resizing
        self.resizing = False if self.resizing else True

    def key_combination(self, event):
        keysym = event.keysym
        
        if keysym == "F11":
            fullscreen = bool(self.attributes()[7])
            print(fullscreen)
            self.attributes("-fullscreen", not fullscreen)

  
if __name__ == "__main__":
    TkGuiBuilder().mainloop()
