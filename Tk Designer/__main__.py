try: import compile as comp
except: pass

from tkinter import font
from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter.ttk as ttk
import tkinter.tix as tix
from tkinter.tix import*
from customtkinter import*
from tkinter import*
from runpy import run_path
from json import dump, load
from py_compile import compile
from os.path import basename, dirname, exists
import idlelib.colorizer as ic
import idlelib.percolator as ip
from os import chdir, getcwd, listdir, remove
from tree import FileTreeItem, TreeNode
from xml.etree import ElementTree as Et
from tkinter.colorchooser import askcolor
from pickle import dump as dumps, load as loads
from tkinter.ttk import Style, Separator, Treeview
import sys, re, pickle, tkinter, customtkinter, Pmw
from tkinter.messagebox import askyesno, showerror, showinfo, showwarning

class Fenetre(CTkToplevel, tix.Tk):
    def __init__(self, master):
        super().__init__(master, class_="fenetre")
        self.title("Fenêtre")
        self.transient(master)

    def destroy(self): self.withdraw()

class TextIO:
    flush = lambda x: None

    def __init__(self, textbox, std, app, tags=None):
        self.std = std
        self.textbox = textbox
        self.tags = tags
        self.app = app

    def write(self, text):
        not self.std or self.std.write(text)
        self.textbox.config(state="normal")
        self.textbox.insert(END, text, self.tags)
        self.textbox.config(state="disable")

        self.textbox.yview_moveto(1)
        self.app.H_Splitter.panecget(self.app.message_Frame, "height") or self.app.H_Splitter.sash_place(0, 0, self.app.message_box_height.get())

class TkGuiBuilder(CTk):
    
    def __init__(self):
        super().__init__()

        self.title("Tk Gui Builder")
        self.configure(fg_color=("gray95", "gray15"))
        self.maxsize(self.winfo_screenwidth()-10, self.winfo_screenheight())
        self.geometry(f"{self.winfo_screenwidth() - 10}x{self.winfo_screenheight() - 100}+0+0")

        # Dark Mode
        set_appearance_mode("dark")

        # le Menu
        self.menu = Menu(
            self,
            title = "Main menu",
            font=("Arial", 12),
            tearoff=0,
            type="tearof"
        )
        
        self.configure(menu=self.menu)

        self.file_menu = Menu(
            self.menu,
            tearoff=0,
            font=("Arial", 11), 
            background=self["background"],
            foreground=self._apply_appearance_mode(("black", "white")),
            activebackground=self._apply_appearance_mode(("gray60", "gray30")),
        )

        self.file_menu.add_command(label="Nouveau", command=lambda: self.open_file(True), accelerator="Ctrl-N")
        self.file_menu.add_command(label="Ouvrir", command=self.open_file, accelerator="Ctrl-O")
        self.file_menu.add_command(label="Enregistrer", command=self.save_files, accelerator="Ctrl-S")
        self.file_menu.add_command(label="Enregistrer sous")

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Exporter vers HTML")
        self.file_menu.add_command(label="Exporter vers Figma")
        self.file_menu.add_command(label="Exporter vers Adobe XD")

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Partager")
        self.file_menu.add_command(label="Imprimer")
        self.file_menu.add_command(label="Quitter", command=self.destroy)

        self.recent_files_menu = Menu(
            self.file_menu,
            tearoff=0
        )
        
        self.open_file_menu = Menu(
            self.file_menu,
            tearoff=0, font=("Arial",11),
            background=self["background"],
            foreground=self._apply_appearance_mode(("black", "white"))
        )
        
        self.open_file_menu.add_command(label="Fichier")
        self.open_file_menu.add_command(label="Projet")
        self.open_file_menu.add_cascade(label="Fichiers récents", menu=self.recent_files_menu)

        self.debug_menu = Menu(
            self.menu,
            tearoff=0,
            font=("Arial", 11), 
            background=self["background"],
            foreground=self._apply_appearance_mode(("black", "white"))
        )

        self.debug_menu.add_command(label="Deboger", command=lambda: self.event_generate("<F5>"), accelerator="F5")

        self.menu.add_cascade(label="    Fichier  ", menu=self.file_menu)
        self.menu.add_cascade(label="  Edition  ")
        self.menu.add_cascade(label="  Affichage  ")
        self.menu.add_cascade(label="  Débogage  ", menu=self.debug_menu)
        self.menu.add_cascade(label="  Projet  ")
        self.menu.add_cascade(label="  Fénêtres  ")
        self.menu.add_cascade(label="  Options  ")
        self.menu.add_cascade(label="  Aide  ")

        # Definition des evenements
        self.bind("<Any-KeyPress>", self.key_combination)

        self.style = Style()
        self.style.theme_use("vista")

        self.tabview = CTkTabview(
            self,
            height=30,
            fg_color=("gray90", "gray15"),
            bg_color=self._fg_color,
            font=("Segoe UI", 16),
            border_width=1,
            corner_radius=5,
            corner_bt_radius=20,
            border_color=("black", "gray0"),
            text_color=("black", "white"),
            segmented_button_selected_color=("white", "gray20"),
            segmented_button_unselected_color=("gray80", "gray10"),
            segmented_button_fg_color=("gray80", "gray10"),
            segmented_button_selected_hover_color="gray20",
            segmented_button_unselected_hover_color="gray15",
            command=lambda: self.selected_widget.set("arrow"),
        )
        
        self.tabview.pack(padx=5, anchor=NW, fill=X)

        # Initialisation de la premiere fenêtre à afficher
        self.fenetre =  Fenetre(self)

        # Lier l'événement de clic à la fonction d'ajou de widget
        self.fenetre.bind("<Button-1>", self.create_widget)

        # Lier l'événement de pression de la touche "Delete" à la fonction de suppression du widget
        self.fenetre.bind("<Delete>", self.delete_widget)

        # Création du dictionnaire avec les listes de widgets
        self.widgets_dict = {
            "tkinter": [
                "Button", "Label", "Entry", "Text", "Checkbutton", "Radiobutton",  "Frame",
                "OptionMenu", "LabelFrame", "Scrollbar", "Canvas", "Menu", "Listbox",
                "Menubutton", "Scale", "PanedWindow", "Message", "Spinbox"
            ],

            "ttk": [
                "Button", "Label", "Entry", "Combobox", "Checkbutton", "Radiobutton",
                "Scrollbar", "Treeview", "Progressbar", "Notebook", "Frame","Scale",
                "LabelFrame", "Menubutton", "PanedWindow", "Separator","Sizegrip"
            ],
            
            "tix": [
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

            "customtkinter": [
                "CTkCanvas", "CTkButton", "CTkCheckBox", "CTkComboBox",
                "CTkEntry", "CTkFrame", "CTkLabel", "CTkOptionMenu", "CTkProgressBar",
                "CTkRadioButton", "CTkScrollbar", "CTkSegmentedButton", "CTkSlider",
                "CTkSwitch", "CTkTabview", "CTkTextbox", "CTkScrollableFrame", "CTkInputDialog"
            ]
        }

        self.modules_opts = {
                            "tkinter": ["from tkinter import*", 0],
                            "ttk": ["import tkinter.ttk as ttk", 0],
                            "tix": ["from tkinter.tix import*", 0],
                            "Pmw": ["import Pmw", 0],
                            "customtkinter": ["from customtkinter import*", 0]
                            }
        
        # Initialisation de la variable pour les boutons radio
        self.selected_widget =  StringVar()
        self.selected_widget.set("")
        
        # Importation de toutes les images
        chdir(dirname(__file__)+r"\Images")
        self.images = []
        for image in listdir(): self.images.append(PhotoImage(image[:-4], file=image))

        # Retour au dossier de départ
        chdir(dirname(__file__))

        # Création des pages du notebook à partir du dictionnaire
        for package, widgets in self.widgets_dict.items():
            page = self.tabview.add(package.capitalize().center(8))
            
            frame = CTkScrollableFrame(
                page,
                border_width=0,
                corner_radius=0,
                fg_color=self.tabview._fg_color,
                bg_color="transparent",
                border_color=("black", "gray0"),
                orientation="horizontal",
                height=40,
            )

            frame.pack(side=LEFT, fill=X, expand=YES, padx=[0, 10])
            frame._scrollbar.grid_forget()

            CTkButton(
                page,
                text="⬅️",
                border_width=0,
                corner_radius=0,
                fg_color="transparent",
                bg_color="transparent",
                font=("Arial", 20),
                text_color=("black", "white"),
                hover_color=("white", "gray30"),
                command=lambda frame=frame: frame._parent_canvas.xview_scroll(-100, "units"),
                width=1,
            ).pack(side=LEFT)

            CTkButton(
                page,
                text="➡️",
                border_width=0,
                corner_radius=0,
                fg_color="transparent",
                bg_color="transparent",
                font=("Arial", 20),
                text_color=("black", "white"),
                hover_color=("white", "gray30"),
                command=lambda frame=frame: frame._parent_canvas.xview_scroll(100, "units"),
                width=1,
            ).pack(side=LEFT)

            R = CTkSegmentedButton(
                frame,
                fg_color=self.tabview._fg_color,
                selected_color=("gray100", "gray30"),
                unselected_color=self.tabview._fg_color,
                border_width=0,
                corner_radius=10,
                command=lambda value: (self.fenetre.deiconify(), (not self.canvas.winfo_ismapped() or self.fenetre.event_generate("<1>")) if value != "arrow" else None),
                variable=self.selected_widget,
                selected_hover_color=("gray100", "gray30"),
                unselected_hover_color=("gray80", "gray20")
                )
            
            R.grid(sticky=NW)
            R.delete("CTkSegmentedButton")
            R.insert(0, "arrow", img="arrow")
            R.set("arrow")

            i = 1
            for widget in widgets:
                try: 
                    R.insert(i, widget, img=package.capitalize()+widget)
                    i += 1
                except: ...
         
        CTkLabel(
            self,
            font=("Calibri", 16),
            text="main.py                  Ligne:356   Colonne:10,   UTF-8   Python  3.11.1   64-bit     ",
            fg_color=("white", "gray6"),
            text_color=("black", "white"),
            corner_radius=30,
        ).pack(side=BOTTOM, fill=BOTH)

        self.panned_Window1 = PanedWindow(
            orient=VERTICAL,
            bd=5,
            width=300,
            background=self._apply_appearance_mode(self._fg_color),
            proxybackground="blue",
            handlepad=0,
            sashwidth=10
            )
        
        self.tree_frame = Frame(self.panned_Window1)
        self.panned_Window1.pack(side=LEFT, fill=Y, anchor=NW, padx=5, pady=5)

        self.Tree = Treeview(
                        self.tree_frame,
                        show = "tree",
                        )
        
        self.Tree.place(x=-1, y=-1, relwidth=1.1, relheight=1.2)
        
        self.Tree.bind("<Delete>", self.delete_widget)
        self.style.configure("Treeview", background=self._apply_appearance_mode(("gray90", "gray20")), foreground=self._apply_appearance_mode(("black", "white")), font=("Segoe UI",  10))
        
        # Les Barres de défilement
        yScroll = CTkScrollbar(self.tree_frame, orientation="vertical", bg_color=("gray90", "gray20"), width=13, command=self.Tree.yview)
        yScroll.pack(side=RIGHT, fill=Y, padx=[0, 1], pady=1)
        
        xScroll = CTkScrollbar(self.tree_frame, orientation="horizontal", bg_color=("gray90", "gray20"), height=11, command=self.Tree.xview)
        xScroll.pack(side=BOTTOM, fill=X, pady=1, padx=1)

        self.Tree.configure(xscrollcommand=xScroll.set, yscrollcommand=yScroll.set)

        for a in range(10): self.Tree.insert("", 1, a)

        self.Tree.tag_bind("master", "<ButtonRelease>", lambda e: self.create_widget(e))
        self.Tree.tag_bind("widget", "<ButtonRelease>", lambda e: self.select_widget(self.nametowidget(self.Tree.focus())))
        
        self.options_Frame = CTkScrollableFrame(
            self.panned_Window1,
            border_width=0,
            corner_radius=0,
            fg_color=("gray90", "gray12"),
            bg_color=self._fg_color,
            border_color=("gray50", "black")
            )

        self.options_Frame._parent_frame.configure(border_width=1)
        self.options_Frame._parent_canvas.grid_configure(padx=[1, 0], pady=[0, 1])
        self.options_Frame._scrollbar.grid_configure(padx=1, pady=[0, 1])
        self.options_Frame._scrollbar.configure(width=13)

        self.options_Frame.columnconfigure(0, weight=1)
        self.options_Frame.columnconfigure(1, weight=1, minsize=140)

        CTkSegmentedButton(
            self.options_Frame._parent_frame,
            border_width=1,
            corner_radius=0,
            fg_color=self.options_Frame._parent_frame._fg_color,
            unselected_color=self.options_Frame._parent_frame._fg_color,
            selected_color=self.options_Frame._parent_frame._fg_color,
            selected_hover_color=self.options_Frame._parent_frame._fg_color,
            unselected_hover_color=self.options_Frame._parent_frame._fg_color,
            font=("Arial", 14, "bold"),
            text_color=("black", "white"),
            values=["OPTIONS" , "VALEURS"],
            height=30,
        ).grid(row=0, column=0, columnspan=2, sticky=EW, padx=[1, 10], pady=1)
    
        self.panned_Window1.add(self.tree_frame, height=142)
        self.panned_Window1.add(self.options_Frame._parent_frame)

        self.V_Splitter = PanedWindow(
            self,
            orient=HORIZONTAL,
            background=self._apply_appearance_mode(self._fg_color),
            )
        
        self.V_Splitter.pack(fill=BOTH, padx=5, pady=5)

        self.H_Splitter = PanedWindow(
            self,
            orient=VERTICAL,
            height=self.winfo_screenheight(),
            background=self._apply_appearance_mode(self._fg_color),
            sashwidth=2,
            sashpad=5,
            sashrelief=GROOVE,
            )
        
        self.H_Splitter.bind("<Double-1>", lambda e: self.H_Splitter.sash_place(0, 0, self.winfo_screenheight()-370 if (self.H_Splitter.sash_coord(0)[1] > self.winfo_screenheight()-370) or (self.H_Splitter.sash_coord(0)[1] <= 80) else 50))

        self.file_list_Frame = CTkScrollableFrame(
            self.V_Splitter,
            border_width=0,
            corner_radius=0,
            fg_color=self._fg_color,
            bg_color="transparent",
            border_color=("black", "gray0"),
            height=400,
            label_text="FICHIERS",
            label_font=("Arial", 14, "bold"),
            label_fg_color="transparent",
            label_text_color=("black", "white")
            )
        
        self.file_list_Frame._scrollbar.configure(width=13)
        self.file_list_Frame._parent_canvas.grid_configure(padx=[10, 0])

        self.file_Tree = TreeNode(self.file_list_Frame._parent_canvas, None, FileTreeItem(""))
        
        self.V_Splitter.add(self.H_Splitter, minsize=300)
        self.V_Splitter.add(self.file_list_Frame.master.master, minsize=200)
        
        self.code_Frame = CTkFrame(
            self.H_Splitter,
            fg_color=self.options_Frame._parent_frame._fg_color,
            bg_color=self._fg_color,
            corner_radius=0,
            border_width=0
            )
        
        self.bar_Frame = CTkFrame(
            self.code_Frame,
            fg_color=("gray80", "gray16"),
            bg_color=self._fg_color,
            corner_radius=0,
            )
        
        self.bar_Frame.pack(side=TOP, fill=X, padx=2, pady=1)

        file_var = StringVar(value="   project.py   ")

        self.file_bar = CTkSegmentedButton(
            self.bar_Frame,
            border_width=0,
            corner_radius=0,
            fg_color=("gray90", "gray10"),
            unselected_color=self.bar_Frame._fg_color,
            selected_color=self.code_Frame._fg_color,
            selected_hover_color=self.code_Frame._fg_color,
            unselected_hover_color=("white", "gray30"),
            text_color=("black", "white"),
            font=("Calibri", 16),
            command=lambda v: ...,
            values=["   project.py   " , "    main.py   "],
            height=42,
            variable=file_var
        )

        self.file_bar.place(x=0, y=0)

        bt_var = StringVar(value=" ")
        self.code_Frame_bar = CTkSegmentedButton(
            self.bar_Frame,
            corner_radius=10,
            fg_color=("gray90", "gray15"),
            unselected_color=("gray90", "gray15"),
            selected_color=("gray90", "gray15"),
            selected_hover_color=("white", "gray30"),
            unselected_hover_color=("white", "gray30"),
            text_color=("black", "white"),
            font=("Arial", 14),
            command=lambda value: (bt_var.set(""), (exec("self.poo = not self.poo", {"self": self}), self.charge_code()) if " " in value else self.fenetre.deiconify() if value == "w" else self.event_generate("<F5>")),
            values=["⏺", "⏹", " ♻️"],
            height=20,
            variable=bt_var
        )

        self.code_Frame_bar.pack(side=RIGHT, pady=5, padx=5)
        self.code_Frame_bar.insert(value="w", img="Window")
        for i, widget in enumerate(list(self.code_Frame_bar.children.values())[1:]): widget.configure(text_color=[("black", "green2"), ("red", "red3"), ("DeepSkyBlue4", "DeepSkyBlue3"), "blue"][i])

        self.H_Splitter.add(self.code_Frame, height=self.winfo_screenheight())

        self.code_Text = CTkTextbox(
            self.code_Frame,
            width = self.winfo_screenwidth()-280,
            height=self.winfo_screenheight()-80,
            corner_radius=0,
            border_width=0,
            border_color=("black", "gray0"),
            font=("Consolas", 15),
            fg_color=self.code_Frame._fg_color,
            selectbackground=self._apply_appearance_mode(("light sky blue", "gray20")),
            selectforeground="",
            text_color=("black", "white"),
            tabs="24p",
            undo=True,
            maxundo=-1,
            wrap="word"
            )

        self.code_Text.pack(padx=[20, 5], pady=[5, 0])
        self.code_Text.tag_configure("widget")
        self.code_Text._y_scrollbar.configure(width=6)
        
        self.code_Text.bind("Control-Z", lambda e: self.code_Text.edit_undo())
        self.code_Text.bind("Control-Y", lambda e: self.code_Text.edit_redo())
        
        self.code_Text.bind("<KeyRelease-Return>", lambda e: self.code_Text.insert(INSERT, "\t\t", self.code_Text.tag_names("current")[-1]))
        
        self.cdg = ic.ColorDelegator()
        self.cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat().pattern, re.S)
        self.cdg.idprog = re.compile(r'\s+(\w+)', re.S)
        
        self.highlighted_textbox = ip.Percolator(self.code_Text._textbox)
        self.highlighted_textbox.insertfilter(self.cdg)

        self.highlighted_textbox.redir.register("insert", self.check_text_insertion)
        self.highlighted_textbox.redir.register("delete", self.check_text_delete)

        self.message_Frame = CTkFrame(
            self.H_Splitter,
            corner_radius=0,
            border_width=0,
            border_color="black",
            fg_color=self._fg_color,
            bg_color=self._fg_color
            )

        self.msg_box_bar = CTkSegmentedButton(
            self.message_Frame,
            corner_radius=10,
            fg_color=self.message_Frame._fg_color,
            unselected_color=self.message_Frame._fg_color,
            selected_color=self.message_Frame._fg_color,
            selected_hover_color=("white", "gray20"),
            unselected_hover_color=("white", "gray20"),
            text_color=("black", "white"),
            font=("Arial", 12),
            command=lambda v: (self.H_Splitter.sash_place(0, 0, self.winfo_screenheight()), bt_var.set("")) if v == "❌" else (self.message_box.config(state="normal"), self.message_box.delete(1.0, END), self.message_box.config(state="disabled"), bt_var.set("")),
            values=("♻️", "❌"),
            height=30,
            variable=bt_var
        )
        
        self.msg_box_bar.pack(side=TOP, anchor=NE)

        for i, widget in enumerate(list(self.msg_box_bar.children.values())[1:]): widget.configure(text_color=[("black", "green4"), ("red", "red3")][i], font=("Arial", [14, 12][i]),)

        self.message_box = CTkTextbox(
            self.message_Frame,
            corner_radius=0,
            border_width=0,
            width = self.winfo_screenwidth()-280,
            height=self.winfo_screenheight()-80,
            font=("Consolas", 14),
            fg_color=("gray80", "gray20"),
            selectbackground=self._apply_appearance_mode(("LightSkyBlue", "gray35")),
            state="disabled"
            )
        
        self.message_box.pack(fill=X)
        self.message_box.tag_configure("error", foreground=self._apply_appearance_mode(("red", "red1")))
        self.H_Splitter.add(self.message_Frame, minsize=0)

        separator = Separator(
            self.H_Splitter,
            orient=HORIZONTAL)

        separator.place(x=-5, y=-5, height=2)

        verify = lambda: self.after(100, verify) if self.H_Splitter.identify(self.winfo_pointerx() - self.H_Splitter.winfo_rootx(), self.winfo_pointery() - self.H_Splitter.winfo_rooty()) else (separator.place_forget(), self.message_box_height.set(self.H_Splitter.sash_coord(0)[1]))
        self.H_Splitter.bind("<Motion>", lambda e: self.H_Splitter.identify(e.x, e.y) and (separator.place(dict(zip(("x", "y", "relwidth"), list(self.H_Splitter.sash_coord(0))+[1]))), self.style.configure("TSeparator", background=self._apply_appearance_mode(("blac", "blue"))), self.after(100, verify)))

        # Le canvas pour afficher les éléments de rédimensionnenent
        self.canvas =  Canvas(self.fenetre, relief=FLAT, bd=0)
        
        # Dessin du cadre entourant le widget
        self.canvas.create_rectangle(0, 0, 0, 0, outline="blue1", width=1, dash=1, tag="rectangle")

        # Afficage des points de rédimensionnenent
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_NW", "size_nw_se", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_N", "sb_v_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_NE", "size_ne_sw", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_W", "sb_h_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_SE", "size_nw_se", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_S", "sb_v_double_arrow", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_SW", "size_ne_sw", "points"))
        self.canvas.create_rectangle((0, 0, 0, 0), tag=("point_E", "sb_h_double_arrow", "points"))

        self.canvas.tag_bind("canvas", "<1>", self.create_widget)
        self.canvas.tag_bind("points", "<Leave>", lambda e: self.canvas.configure(cursor="arrow"))
        self.canvas.tag_bind("points", "<Enter>", lambda e: self.canvas.configure(cursor=self.canvas.gettags("current")[1]))

        # Lier l'événement de  redimensionnement des widgets
        self.canvas.tag_bind("points", "<1>", lambda e: exec("self.start_x, self.start_y = self.winfo_pointerxy()", {"self": self}))
        self.canvas.tag_bind("points", "<B1-Motion>", self.resize_widget)
        self.canvas.tag_bind("points", "<ButtonRelease>", self.update_position_code)

        # Variable pour les widgets de la fenetre
        self.widget = self.fenetre
        self.deleting = True
        self.updating = False
        self.poo = True
        self.file = ""
        self.sep = ["(\n\t\t\t", ",\n\t\t\t", "\n\t\t)"]
        self.defauts = {}
        self.widgets_list = {}
        self.all_children = {self.fenetre: None}
        self.message_box_height = IntVar(value=self.winfo_screenheight()-360)

        # Construire le selecteur des couleurs
        self.build_colorchooser()
        
        # Charger le theme
        self.change_code_theme()

        # Creation des options
        self.build_Options()

        # Récupération des messgages python
        sys.stdout = TextIO(self.message_box, sys.stdout, self)
        sys.stderr = TextIO(self.message_box, sys.stderr, self, "error")

        """self.fenetre.geometry(f"{self.file_list_Frame.master.master.winfo_width()}x \
                              {int(self.file_list_Frame.master.master.winfo_height())-30}+ \
                              {self.file_list_Frame.master.master.winfo_rootx()-9}+ \
                              {self.file_list_Frame.master.master.winfo_rooty()}")"""

        self.fenetre.geometry(f"245x{int(self.winfo_screenheight())-250}+{int(self.winfo_screenwidth())-260}+135")

        self.charge_file()
        self.after(10, lambda: self.wm_state("zoomed"))
        
    def open_file(self, new=False):
        file = "nouveau.TkD" if new else askopenfilename(defaultextension="TkD", title="Sauvegarder le projet", filetypes=[("Projet Tk Designer", ["TkD"])])
        
        if file and file != self.file:
            self.file = file

            self.file_Tree.item.path = dirname(file)
            self.file_Tree.expand()

            for widget in list(self.all_children.keys())[1:]: widget.destroy()
            self.code_Text.tag_delete(self.code_Text.tag_names())
            self.Tree.delete(self.fenetre)

            self.canvas.pack_forget()
            self.widget = self.fenetre

            self.deleting = True
            self.code_Text.delete(1.0, END)
            self.deleting = False

            self.message_box._textbox.configure(state="normal")
            self.message_box.delete(1.0, END)
            self.message_box._textbox.configure(state="disable")

            try: self.charge_file()
            except: showerror("Ouvrir un fichier", "Erreur lors de l'ouverture du fichier.\n")

    def charge_file(self):
        self.defauts = {}
        self.widgets_list = {}
        self.all_children = {self.fenetre: None}

        self.fenetre.configure(fg_color="SystemButtonFace")

        items = list({key: str(self.fenetre.cget(key)) for key in set(self.fenetre.keys()).intersection(self.Options_widgets)}.items())
        items.sort(key=lambda x: x[0])

        self.defauts["tkinter.Tk"] = {key: "" for key in dict(items).keys()}
        
        try:
            with open(self.file, "rb") as Tk_file:
                data = loads(Tk_file)
                Fenetre = list(data)[0]
                self.widgets_list[self.fenetre] = data[Fenetre]
                self.all_children[self.fenetre] = self.widgets_list[self.fenetre]
                
                self.code_Text.insert(1.0, data[Fenetre]["script"], "")
                    
                for tag, indexes in data[Fenetre]["tags"].items():
                    for index1, index2 in zip(indexes[::2], indexes[1::2]):
                        self.code_Text.tag_add(tag, index1, index2)
            
        except Exception as e: #print(f"Erreur lors du chargement des fichiers: {e}", file=sys.stderr)

            self.widgets_list[self.fenetre] = {
                "nom": "Fenetre1",
                "classe": "Tk",
                "package": "tkinter",
                "titre": "Tk Gui builder",
                "geometry": self.fenetre.geometry(),
                "options": dict(items),
                "children": {}
            }

        self.all_children[self.fenetre] = self.widgets_list[self.fenetre]

        self.Tree.insert("", 0, self.fenetre, image="Window", text=f" Fenetre1", open=1, tag="master")
        
        self.charge_code()
    
    def charge_code(self):

        def create_children(parent, parent_name, children):
            for widget, values in children.copy().items():
                nom = values["nom"]
                package = values["package"]
                classe = values["classe"]
                place_info = values["position"]

                if widget == nom:
                    widget = eval(package+"."+classe)(parent)

                    self.modules_opts[package][1] += 1

                    if package+"."+classe not in self.defauts: self.defauts[package+"."+classe] = {key: widget.cget(key) for key in widget.keys()}

                    widget.config(**values["options"])

                    items = list({key: str(widget.cget(key)) for key in set(widget.keys()).intersection(self.Options_widgets)}.items())
                    items.sort(key=lambda x: x[0])
                   
                    widget.place(place_info)
                    
                    # self.Tree.insert(parent, END, widget, image=package.capitalize()+classe+"_ico", text=f" {nom}", tag=(nom, "widget"))
                    self.Tree.insert(parent, END, widget, image="Window", text=f" {nom}", tag=(nom, "widget"))

                    
                    # if "state" in widget.keys() and classe in ("Entry", "Text", "Combobox"): widget.configure(state="disabled")
                    if "disabledforeground" in widget.keys(): widget.configure(disabledforeground=widget["foreground"])
                    if "disabledbackground" in widget.keys(): widget.configure(disabledbackground= widget["background"])
                    
                    children[widget] = children[nom]
                    children[widget]["options"] = dict(items)
                    children[widget]["parent"] = parent
                    children.pop(nom)
                    
                    self.all_children[widget] = children[widget]

                    widget.bind("<B1-Motion>", self.move_widget)
                    widget.bind("<Button-1>", lambda e: self.select_widget(e.widget) if self.selected_widget.get() == "arrow" else self.create_widget(e))
                    widget.bind("<ButtonRelease>", self.update_position_code)
                    widget.bind("<Delete>", self.delete_widget)

                items = {key: value for key, value in values["options"].items() if value and value != self.defauts[package+"."+classe][key] and (str(value).isnumeric() and int(value) or not str(value).isnumeric())}
                index = self.code_Text.index(nom+".first") or self.limite[0]
                
                self.deleting = True
                self.code_Text.delete(nom+".first", nom+".last")

                text = ("\n\t\tself." if self.poo else "\n")+nom+" = "+(package+"." if package in ("ttk", "Pmw") else "")+classe+(self.sep[0] if items else "(")+parent_name+(self.sep[1] if items else "")
                text += self.sep[1].join([key+"="+str("\""+str(value)+"\"" if not (str(value).isnumeric() or str(value)[1:].isnumeric()) else value) for key, value in items.items() if value])+(self.sep[2] if items else ")")+"\n"+("\n" if items else "")

                self.highlighted_textbox.insert(index, text, tags=(nom, "widget"))
                
                text = ("\t\tself." if self.poo else "")+nom+".place("
                text += ", ".join([""+key+"="+str("\""+str(value)+"\"" if not str(value).isnumeric() else value) for key, value in place_info.items()])+")\n"

                self.highlighted_textbox.insert(nom+".last", text, tags=(nom, nom+".pos", "widget"))

                if not self.code_Text.get("import.first", "import.last").count(package):
                    self.code_Text.insert("import.last -1 c", self.modules_opts[package][0] + "\n", tags=("import", f"{package}.import", "widget"))

                self.limite = self.code_Text.index(f"{nom}.last"), nom

                create_children(widget, ("self." if self.poo else "")+values["nom"], children[widget]["children"])
        
        if ab := self.code_Text.tag_ranges("import"):
            a, b = ab
            self.deleting = True
            self.code_Text.delete(a, b)
        else: a = END
        
        self.code_Text.insert(a, "from tkinter import*", tags=("import", "widget"))
        self.code_Text.insert(self.code_Text.index("import.last"), "\n\n", tags="import")

        items = self.widgets_list[self.fenetre]["options"]

        nom = self.widgets_list[self.fenetre]["nom"]
        classe = self.widgets_list[self.fenetre]["classe"]
        package = self.widgets_list[self.fenetre]["package"]
        geometry = self.widgets_list[self.fenetre]["geometry"]
        titre = self.widgets_list[self.fenetre]["titre"]

        items = {key: value for key, value in items.items() if value and value != self.defauts[package+"."+classe][key] and (str(value).isnumeric() and int(value) or not str(value).isnumeric())}
        package = package+"." if package in ("ttk", "Pmw") else ""

        self.fenetre.title(titre)
        self.fenetre.config(items)
        self.fenetre.geometry(geometry)

        self.Tree.item(self.fenetre, text=f" {nom}")
        
        text = "  \n"+(("class "+nom+"("+package+classe+"):\n") if self.poo else (nom+" = "+package+classe+"()\n"))+ \
        ("\tdef __init__(self):\n" if self.poo else "")+ \
        ("\t\tsuper().__init__()\n\n" if self.poo else "")+ \
        ("\t\tself" if self.poo else nom)+".title(\""+titre+"\")\n"+ \
        ("\t\tself" if self.poo else nom)+".geometry(\""+geometry+"\")\n\n"+ \
        ("\t\tself" if self.poo else nom)+".configure"+self.sep[0]+ \
        self.sep[1].join([k+"="+str("\""+v+"\"" if not (v.isnumeric() or v[1:].isnumeric()) else v) for k, v in items.items() if v])+ \
        self.sep[2]+"\n"
        
        if ab := self.code_Text.tag_ranges(nom):
            a, b = ab
            self.deleting = True
            self.code_Text.delete(a, b)
        else: a = END

        self.code_Text.insert(a, text, tags=(nom, "widget"))
        
        if not self.code_Text.tag_ranges("user"): self.code_Text.insert(nom+".last", "\n\t\t\n", tags="user")

        if ab := self.code_Text.tag_ranges("run"):
            a, b = ab
            self.deleting = True
            self.code_Text.delete(a, b)
        else: a = END

        text = "\t\t\nif __name__ == \"__main__\":\n\t"+nom+("()" if self.poo else "")+".mainloop()\n\t"
        
        self.code_Text.insert(a, text, tags=("run", "widget"))
        self.code_Text.insert("run.last", "", tags="end")

        self.limite = self.code_Text.index(f"{nom}.last"), "Fenetre1"
        
        create_children(self.fenetre, "self" if self.poo else self.widgets_list[self.fenetre]["nom"], self.widgets_list[self.fenetre]["children"])
        
        self.code_Text._textbox.edit_reset()
        self.update_options_Frame()

        # Actualisation de la geometry
        self.fenetre.bind("<Configure>", lambda e: (self.update_idletasks(), self.update_Options("geometry", self.fenetre.geometry())))
     
    def save_files(self):
        self.file = self.file or asksaveasfile(confirmoverwrite=True, defaultextension="TkD", title="Sauvegarder le projet", filetypes=[("Projet Tk Designer", ["TkD"])]).name or self.file
        if not self.file or not exists(self.file): return showerror("Echec de la sauvegarde", "Le projet n'a pas pu être sauvegardé, une erreur est survenue.")
        
        file = self.file[:-4]

        try:
            def serialize(value):
                optimise = lambda v: {key: value for key, value in v["options"].items() if self.defauts[v["package"]+"."+v["classe"]][key] != value}
                return {v["nom"] if isinstance(v, dict) and "classe" in v else k : optimise(value) if k == "options" else serialize(v) for k, v in value.items() if k != "parent"} if isinstance(value, dict) else value if isinstance(value, (int, list, float, bool, None.__class__)) else int(value) if isinstance(value, str) and (value.isnumeric() or value[1:].isnumeric()) else str(value)
                
            def xmler(value, root=None, root2=None):
                for key, value in value.items():
                    if isinstance(value, dict):
                        key, att =  (value["classe"], {}) if root is None or root.tag == "children" else (key, {"total": str(len(value))})
                        root2 = Et.SubElement(root, key, att) if root is not None else Et.Element(key)
                        xmler(value, root2)
                    elif key != "classe":
                        root2 = Et.SubElement(root, key)
                        root2.text = str(value)

                if root2: Et.indent(root2, " "*4)
                return root2
                
            self.widgets_list[self.fenetre]["tags"] = {key: [float(str(val)) for val in self.code_Text.tag_ranges(key)] for key in self.code_Text.tag_names() if not key.isupper() and self.code_Text.tag_ranges(key)}
            self.widgets_list[self.fenetre]["script"] = self.code_Text.get(1.0, END)

            data = serialize(self.widgets_list)
            key = list(data)[0]
            self.widgets_list[self.fenetre].pop("script")

            with open(f"{file}.json", "w") as js_file, open(f"{file}.xml", "wb") as xml_file, \
                open(f"{file}.TkD", 'wb') as Tk_file,  open(f"{file}.py", "w") as py_file:

                    xml = xmler(data)
                    Et.ElementTree(xml).write(xml_file, encoding="utf-8", xml_declaration=True)

                    dump(data, js_file, indent=4)
                    dumps(data, Tk_file)

                    py_file.write(self.code_Text.get(1.0, END))
                    compile(self.file[:-4]+".py", self.file[-4]+".pyc")

            if not exists(dirname(file)+"\Buckup"):
                os.mkdir(os.path.dirname(file)+"\Buckup")
            
            file = dirname(file)+"\Buckup\\"+basename(file)+"_buckup"

            with open(f"{file}.json", "w") as js_file_copy, open(f"{file}.xml", "wb") as xml_file_copy, \
                open(f"{file}.Tk", 'wb') as Tk_file_copy,  open(f"{file}.py", "w") as py_file_copy:

                    Et.ElementTree(xml).write(xml_file_copy, encoding="utf-8", xml_declaration=True)
                    dump(data, js_file_copy, indent=4)
                    dumps(data, Tk_file_copy)
                    py_file_copy.write(self.code_Text.get(1.0, END))
              
        except Exception as e: print(f"Echec de la sauvegarde: {e}", file=sys.stderr)

    def build_colorchooser(self):
        with open("Colors.list", "rb") as f: colors = loads(f)

        self.colorchoser = Fenetre(self)
        self.colorchoser.geometry("405x455+0+0")
        self.colorchoser.withdraw()

        self.colorchoser.bind("<Visibility>", lambda e: (self.colorchoser.transient(self), self.colorchoser.unbind("<Visibility>")))

        cur_color = StringVar()

        F = CTkScrollableFrame(
            self.colorchoser,
            fg_color=("white", "gray70"),
            corner_radius=10,
            border_width=1,
            border_color="black",
            width=356,
            height=370,
            )
        
        F.grid(padx=10, pady=[10, 5], columnspan=3)
        
        F = F._parent_canvas
        F.create_rectangle(1, 1,36,35, fill="LightSkyblue", tag="rect")

        F.tag_bind("color", "<1>", lambda e: (F.coords("rect", [v+(3 if i>1 else -3) for i, v in enumerate(F.bbox(F.gettags("current")[1]))]), cur_color.set(F.gettags("current")[1])))
        F.tag_bind("color", "<Double-1>", lambda e: (self.colorchoser.withdraw(), self.current_var.set(F.gettags("current")[1])))
        F.tag_bind("color", "<Enter>", lambda e: F.config(cursor="hand2"))
        F.tag_bind("color", "<Leave>", lambda e: F.config(cursor="arrow"))

        i = j = 0
        for n, color in enumerate(colors):
            try:
                F.create_text(
                            i*35+5, j*34+5, text="A", fill="black", anchor=NW,
                            font=("customTkinter_shapes_font", 21), tags=("color", color))
                
                F.create_text(
                            i*35+5, j*34+5, text="A", fill=color, anchor=NW,
                            font=("customTkinter_shapes_font", 20), tags=("color", color))
                i += 1
                if i > 9:
                    j += 1
                    i = 0

            except: print("Echec de", color)
        
        CTkButton(self.colorchoser,
            text="PLUS",
            font=("Arial", 14, "bold"),
            corner_radius=15,
            text_color="white",
            fg_color="DeepSkyBlue2",
            hover_color="DeepSkyBlue3",
            image="ColorDialog",
            compound="left",
            command=lambda: (self.colorchoser.withdraw(), F.coords("rect", 1, 1, 36 ,35), self.current_var.set(askcolor()[1] or self.current_var.get())),
            width=50,
            height=35,
            ).grid(sticky=E,  column=2, padx=[0, 10], pady=[5, 0])
        
        CTkButton(self.colorchoser,
            text="OK",
            font=("Arial", 14, "bold"),
            corner_radius=15,
            text_color="white",
            fg_color="green",
            hover_color="green3",
            command=lambda: (self.colorchoser.withdraw(), self.current_var.set(cur_color.get())),
            width=80,
            height=35,
            ).grid(row=1,  column=1, pady=[5, 0])
        
        CTkButton(self.colorchoser,
            text="ANNULER",
            font=("Arial", 14, "bold"),
            corner_radius=15,
            text_color="white",
            fg_color="red",
            hover_color="red3",
            command=self.colorchoser.withdraw,
            width=50,
            height=35,
            ).grid(sticky=W, row=1, column=0, padx=[10, 0])
    
    def build_Options(self):
        self.Options_widgets = {}
        self.spin_widgets = []
        self.cur_Options_list = []

        Separator(
                self.options_Frame._parent_canvas,
                orient=HORIZONTAL,
                style="Line.TSeparator",
        ).place(x=0, y=0, relwidth=1)
        
        self.style.configure("Line.TSeparator", background=self._apply_appearance_mode(("gray90", "blac")))

        with open("Cursors.list", "rb") as f:
            cursors = loads(f)
            fonts = list(font.families())
            fonts.sort()
            cursors.sort()

        self.options_list_type = {
            "activebackground": ["colors"],
            "activeforeground": ["colors"],
            "anchor": ["comb", ["n", "s", "e", "w", "center", "ne", "nw", "se", "sw"]],
            "background": ["colors"],
            "bitmap": ["comb", ["error", "gray75", "gray50", "gray25", "gray12", "hourglass", \
                                "info", "questhead", "question", "warning"]
                        ],
            "borderwidth": ["spin"],
            "command": ["comb", ["none"]],
            "compound": ["comb", ["up", "left", "right", "bottom"]],
            "cursor": ["comb", cursors],
            "default": ["comb", ["normal", "active", "disabled", "readonly"]],
            "disabledforeground": ["colors"],
            "disabledbackground": ["colors"],
            "font": ["comb", fonts],
            "foreground": ["colors"],
            "height": ["spin"],
            "highlightbackground": ["colors"],
            "highlightcolor": ["colors"],
            "highlightthickness": ["spin"],
            "image": ["comb", ["none"]],
            "justify": ["comb", ["left", "center", "right"]],
            "overrelief": ["comb", ["flat", "solid", "ridge", "groove", "sunken"]],
            "orient": ["comb", ["horizontal", "vertical"]],
            "orientation": ["comb", ["horizontal", "vertical"]],
            "labelanchor": ["comb", ["n", "s", "e", "w", "center", "ne", "nw", "se", "sw"]],
            "padx": ["spin"],
            "pady": ["spin"],
            "relief": ["comb", ["flat", "groove", "raised", "ridge", "solid", "sunken"]],
            "repeatdelay": ["spin"],
            "repeatinterval": ["spin"],
            "show": ["text"],
            "state": ["comb", ["normal", "active", "disabled", "readonly"]],
            "takefocus": ["switch"],
            "text": ["text"],
            "textvariable": ["comb", ["none"]],
            "underline": ["spin"],
            "width": ["spin"],
            "wrap": ["comb", ["char", "word", "none"]],
            "wraplength": ["spin"]
        }
        
        # Empêche au trace_add d'actualiser la valeur pendant l'assigantion des variables
        self.updating = True
        
        for i, option in enumerate(self.options_list_type):
            var = StringVar()
            var.trace_add("write", lambda var_name, _, reason, option=option: self.updating or self.update_Options(option, self.Options_widgets[option][0].get()))

            self.Options_widgets[option] = [var]
            
            separator = Separator(
                self.options_Frame,
                orient=HORIZONTAL,
                style="Line.TSeparator",
            )
            
            separator.grid(row=i, columnspan=2, sticky=EW, pady=[0, 40])
            self.Options_widgets[option].append(separator)

            lab = CTkLabel(
                self.options_Frame,
                font=("Yu Gothic", 16),
                fg_color=self.options_Frame._parent_frame._fg_color,
                text=(option[:14].title()+"..") if len(option) > 14 else option.title(),
                text_color=("black", "white")
                )
            
            lab.grid(row=i, padx=5)
            self.Options_widgets[option].append(lab)
            
            match self.options_list_type[option][0]:
                case "text":
                    t = CTkEntry(
                        self.options_Frame,
                        border_width=0,
                        corner_radius=10,
                        text_color=("black", "black"),
                        fg_color=("white", "gray60"),
                        font=("Yu Gothic", 15, "bold"),
                        textvariable=var
                    )

                    t.grid(row=i, column=1, padx=[5, 4], pady=5, sticky=EW)

                case "colors":
                    t = CTkEntry(
                        self.options_Frame,
                        border_width=0,
                        corner_radius=10,
                        text_color=("black", "black"),
                        fg_color=("white", "gray60"),
                        font=("Yu Gothic", 14),
                        textvariable=var,
                        width=1,
                    )
                    
                    t.grid(row=i, column=1, padx=[5, 4], pady=4, sticky=EW)
                    t.bind("<FocusOut>", lambda e, option=option: self.Options_widgets[option][0].set(self.widget.cget(option)))

                    b = CTkButton(
                        self.options_Frame,
                        corner_radius=10,
                        hover_color=("white", "gray80"),
                        image="ColorDialog",
                        fg_color=("white", "gray60"),
                        background_corner_colors=(("white", "gray60"), self.options_Frame._parent_frame._fg_color, self.options_Frame._parent_frame._fg_color, ("white", "gray60")),
                        command=lambda option=option: (self.colorchoser.deiconify(), exec("self.current_var = self.Options_widgets[option][0]")),
                        text_color="white",
                        cursor="hand2",
                        width=1,
                    )
                    
                    b.grid(row=i, column=1, padx=4, sticky=E)
                    
                    self.Options_widgets[option].append(b)

                case "switch":
                    t = CTkSwitch(
                        self.options_Frame,
                        progress_color=("white", "gray80"),
                        font=("Yu Gothic", 15),
                        fg_color=("white", "gray30"),
                        button_color=("DeepSkyBlue3", "blue"),
                        button_hover_color=("DeepSkyBlue", "blue1"),
                        text_color=self.options_Frame.cget("fg_color"),
                        onvalue=True,
                        offvalue=False,
                        text="",
                        variable=var
                    )

                    t.grid(row=i, column=1, padx=5, pady=4)

                case "comb":
                    t = CTkComboBox(
                        self.options_Frame,
                        border_width=0,
                        corner_radius=10,
                        values=self.options_list_type[option][1],
                        button_color=("gray76", "gray80"),
                        button_hover_color=("DeepSkyBlue2", "gray100"),
                        text_color="black",
                        fg_color=("white", "gray60"),
                        font=("Yu Gothic", 15),
                        variable=var,
                        width=1
                    )

                    t.grid(row=i, column=1, padx=[5, 4], pady=4, sticky=EW)
                    t.bind("<FocusOut>", lambda e, option=option: self.Options_widgets[option][0].set(self.widget.cget(option)))

                case "spin":
                    t = CTkFrame(
                        self.options_Frame,
                        corner_radius=10,
                        fg_color=("white", "gray60"),
                        height=28,
                        width=1,
                    )

                    t.grid(row=i, column=1, padx=[5, 4], pady=4, sticky=EW)

                    spin = Spinbox(
                        t,
                        background=self._apply_appearance_mode(("white", "gray60")),
                        foreground=self._apply_appearance_mode(("black", "black")),
                        buttonbackground=self._apply_appearance_mode(("white", "gray80")),
                        buttondownrelief="flat",
                        buttonuprelief="flat",
                        font=("Yu Gothic", 11, "bold"),
                        from_=0,
                        to=1000,
                        relief="flat",
                        textvariable=var,
                    )

                    spin.place(relx=0.05, y=3, relwidth=0.89)
                    spin.bind("<FocusOut>", lambda e,  option=option: self.Options_widgets[option][0].set(self.widget.cget(option)))
                    
                    self.spin_widgets.append(spin)
                    
            self.Options_widgets[option].append(t)
            self.cur_Options_list.append(option)

        Separator(
            self.options_Frame._parent_frame,
            orient=VERTICAL,
            style="Line.TSeparator",
        ).place(relx=0.945, y=0, relheight=1)

        Separator(
            self.options_Frame,
            orient=VERTICAL,
            style="Line.TSeparator",
        ).grid(row=0, rowspan=i, column=0, padx=[125, 0], sticky=NS)
        
        # Redonne la liberté au trace_add car l'assignation des variables est achevée
        self.updating = False
    
    def create_widget(self, event): # Fonction pour ajouter le widget sélectionné à l'emplacemen du clic
        classe = self.selected_widget.get()
        
        if classe != "arrow" and not self.canvas.winfo_ismapped():
            package = self.tabview.get().strip() if self.tabview.get().strip() == "Pmw" else self.tabview.get().strip().lower()
            parent = event.widget.master if event.widget == self.canvas else event.widget

            x, y = event.x, event.y
            widget = eval(package+"."+classe)(parent) # = getattr(globals()[package], classe)(parent)

            if package+"."+classe not in self.defauts: self.defauts[package+"."+classe] = {key: widget.cget(key) for key in widget.keys()}
            
            nom = ("T" if package == "ttk" else "") + classe + \
                str(max([int(v["nom"][len(("T" if package == "ttk" else "") + classe):] or 0) \
                    for v in self.all_children.values() if v["classe"] == classe and v["package"] == package] or [0]) +1)
            
            self.modules_opts[package][1] += 1

            if "text" in widget.keys(): widget.configure(text=nom)
            if "background" in widget.keys() and classe in ("Label", "Checkbutton", "Radiobutton"):
                widget.configure(background=parent.cget("background"), foreground = "white" if parent.cget("background") == "black" or "gray" in parent.cget("background") else "black")
                
            widget.place(x=x, y=y)
            
            # self.Tree.insert(parent, END, widget, image=package.capitalize()+classe+"_ico", text=f" {nom}", tag=(nom, "widget"))
            self.Tree.insert(parent, END, widget, image="Window", text=f" {nom}", tag=(nom, "widget"))


            items = list({key: str(widget.cget(key)) for key in set(widget.keys()).intersection(self.Options_widgets)}.items())
            items.sort(key=lambda x: x[0])

            # if "state" in widget.keys() and classe in ("Entry", "Text", "Combobox"): widget.configure(state="disabled")
            if "disabledforeground" in widget.keys(): widget.configure(disabledforeground= widget["foreground"])
            if "disabledbackground" in widget.keys(): widget.configure(disabledbackground= widget["background"])

            self.update_idletasks()
            place_info = {key: value for key, value in widget.place_info().items() if key in "x y width height"}
            place_info.update({"width": widget.winfo_width(), "height": widget.winfo_height()})
 
            self.all_children[widget] = self.all_children[parent]["children"][widget] = {
                "nom": nom,
                "classe": classe,
                "package": package,
                "parent": parent,
                "options": dict(items),
                "children": {},
                "position": place_info
                }
            
    
            items = {key: value for key, value in items if value and value != self.defauts[package+"."+classe][key] and (str(value).isnumeric() and int(value) or not str(value).isnumeric())}.items()
            parent_name = ("self" if self.poo else self.all_children[self.fenetre]["nom"]) if parent == self.fenetre else ("self." if self.poo else "")+self.all_children[parent]["nom"]

            text = ("\n\t\tself." if self.poo else "\n")+nom+" = "+(package+"." if package in ("ttk", "Pmw") else "")+classe+(self.sep[0] if items else "(")+parent_name+(self.sep[1] if items else "")
            text += self.sep[1].join([key+"="+str("\""+str(value)+"\"" if not ((value.isnumeric() or value[1:].isnumeric()) and int(value)) else value) for key, value in items if value])+(self.sep[2] if items else ")")+"\n"+("\n" if items else "")
            
            self.highlighted_textbox.insert(self.limite[0], text, tags=(nom, "widget"))
            
            text = ("\t\tself." if self.poo else "")+nom+".place("
            text += ", ".join([key+"="+str(value) for key, value in place_info.items()])+")\n"

            self.highlighted_textbox.insert(nom+".last", text, tags=(nom, nom+".pos", "widget"))

            if not self.code_Text.get("import.first", "import.last").count(package):
                self.deleting = True
                self.code_Text.insert("import.last -1 c", self.modules_opts[package][0] + "\n", tags=("import", f"{package}.import", "widget"))

            self.limite = self.code_Text.index(f"{nom}.last"), nom

            # Actualisation de l'affichage
            self.update_idletasks()
            
            # Lier l'événement de déplacement du widget
            widget.bind("<B1-Motion>", self.move_widget)
            widget.bind("<Button-1>", lambda e: self.select_widget(e.widget) if self.selected_widget.get() == "arrow" else self.create_widget(e))
            widget.bind("<ButtonRelease>", self.update_position_code)
            widget.bind("<Delete>", self.delete_widget)

            # Selection du widget pour modification
            self.select_widget(widget)

            # Réinitialiser le sélécteur
            self.selected_widget.set("arrow")

        elif self.widget != self.fenetre and event.widget in (self.fenetre, self.canvas) and len(self.canvas.gettags("current")) <= 2: # Déselection du widget en supprimmant le rectangle te les points de redimensionnement
            self.canvas.place_forget()
            self.resizing = False

            if "cursor" in self.widget.keys(): self.widget.configure(cursor="arrow")

            #self.code_Text.tag_configure(self.widgets_list[self.fenetre]["children"][self.widget]["nom"], background="")
            #self.code_Text.tag_config(self.widgets_list[self.fenetre]["nom"], background=self.code_Text._textbox["selectbackground"])

            self.code_Text.see((self.code_Text.index(f"{self.widgets_list[self.fenetre]['nom']}.first")))
            
            self.Tree.selection_set(self.fenetre)
            
            self.widget = self.fenetre
            self.update_options_Frame()

    def select_widget(self, widget, resizing=False):
        # Récupération de la position de la souris pour le déplacement du widget
        self.start_x, self.start_y = self.winfo_pointerxy()

        if "cursor" in self.widget.keys(): widget.configure(cursor="fleur")

        x, y, width, height = widget.winfo_x()-4, widget.winfo_y()-4, widget.winfo_width()+10, widget.winfo_height()+10
        
        self.canvas.configure(bg=widget.master["bg"])
        self.canvas.place(in_=widget.master, x=-2, y=-2, relwidth=1.1, relheight=1.1)

        color = "black" if all([i >= 32896 for i in self.winfo_rgb(self.canvas["bg"])]) else "white"
        self.canvas.itemconfigure("points", fill=color, outline=color)
        
        # Dessin du cadre entourant le widget
        self.canvas.coords("rectangle", (x, y, x+width, y+height))
        
        # Afficage des points de rédimensionnenent
        self.canvas.coords("point_NW", (x-2, y-2, x+2, y+2))
        self.canvas.coords("point_N", (x+(width/2)-2, y-2, x+(width/2)+2, y+2))
        self.canvas.coords("point_NE", (x+width-2, y-2, x+width+2, y+2))
        self.canvas.coords("point_E", (x+width-2, y+(height/2)-2, x+width+2, y+(height/2)+2))
        self.canvas.coords("point_SE", (x+width-2, y+height-2, x+width+2, y+height+2))
        self.canvas.coords("point_S", (x+(width/2)-2, y+height-2, x+(width/2)+2, y+height+2))
        self.canvas.coords("point_SW", (x-2, y+height-2, x+2, y+height+2))
        self.canvas.coords("point_W", (x-2, y+(height/2)-2, x+2, y+(height/2)+2))

        self.code_Text.see(float(self.code_Text.index(f"{self.all_children[widget]['nom']}.first"))+10)
        
        if not resizing and self.widget != widget:
            self.Tree.selection_set(widget)
            self.Tree.see(widget)

            # Dans le text
            #self.code_Text.tag_configure(self.widgets_list[self.fenetre]["children"][self.widget]["nom"], background="")
            #self.code_Text.tag_configure(self.widgets_list[self.fenetre]["children"][widget]["nom"], background=self.code_Text._textbox["selectbackground"])

            self.widget = widget
            self.update_options_Frame()

    def check_text_insertion(self, pos, text, tags=""):
        if "widget" in tags or "import" in tags or "widget" not in self.code_Text.tag_names(pos):
            self.highlighted_textbox.insert(pos, text, tags or self.code_Text.tag_names(pos)[-1])

        else: self.bell()

    def check_text_delete(self, start, end=None):
        if start := self.code_Text.index(start):
            start = float(start)
            end = float(self.code_Text.index(end)) if end else None
            
            user_start = float(self.code_Text.index("user.first"))
            user_end = float(self.code_Text.index("user.last - 1c"))

            lines = [start]+(list(range(int(start), int(end)-1))+[end] if end else [])

            if start not in [user_start, user_end] and (self.deleting or all(["widget" not in self.code_Text.tag_names(index) for index in lines])):
                self.highlighted_textbox.delete(start, end)
                self.deleting = False

            else: self.bell()

    def update_options_Frame(self):
        options = self.all_children[self.widget]["options"]

        for option in set(self.cur_Options_list).difference(options):
            self.cur_Options_list.remove(option)
            for widget in self.Options_widgets[option][1:]: widget.grid_remove()
        
        for option in set(options).difference(self.cur_Options_list):
            self.cur_Options_list.append(option)
            for widget in self.Options_widgets[option][1:]: widget.grid()

        for option in self.cur_Options_list:
            self.updating = True
            self.Options_widgets[option][0].set(options[option])
            self.updating = False

        self.options_Frame._parent_canvas.yview_moveto(0)

    def update_Options(self, option, value):
        widget_opts_dict = self.all_children[self.widget]
        try:
            if self.widget == self.fenetre or option == "geometry":
                if option in self.widgets_list[self.fenetre]["options"]:
                    self.widgets_list[self.fenetre]["options"][option] = value
                else: self.widgets_list[self.fenetre][option] = value
            
                items = self.widgets_list[self.fenetre]["options"]

                nom = self.widgets_list[self.fenetre]["nom"]
                classe = self.widgets_list[self.fenetre]["classe"]
                package = self.widgets_list[self.fenetre]["package"]
                geometry = self.widgets_list[self.fenetre]["geometry"]
                titre = self.widgets_list[self.fenetre]["titre"]

                self.fenetre.config(items)
                items = {key: value for key, value in items.items() if value and value != self.defauts[package+"."+classe][key] and (str(value).isnumeric() and int(value) or not str(value).isnumeric())}

                text = "  \n"+(("class "+nom+"("+(package+"." if package in ("ttk", "Pmw") else "")+classe+"):\n") if self.poo else (nom+" = "+package+classe+"()\n"))+ \
                ("\tdef __init__(self):\n" if self.poo else "")+ \
                ("\t\tsuper().__init__()\n\n" if self.poo else "")+ \
                ("\t\tself" if self.poo else nom)+".title(\""+titre+"\")\n"+ \
                ("\t\tself" if self.poo else nom)+".geometry(\""+geometry+"\")\n\n"+ \
                ("\t\tself" if self.poo else nom)+".configure"+self.sep[0]+ \
                self.sep[1].join([k+"="+str("\""+v+"\"" if not (v.isnumeric() or v[1:].isnumeric()) else v) for k, v in items.items() if v])+ \
                self.sep[2]+"\n"
                
                a, b = self.code_Text.tag_ranges(nom)
                self.deleting = True
                self.code_Text.delete(a, b)

                self.code_Text.insert(a, text, tags=(nom, "widget"))
                return
            
            try:
                if self.widget.cget("state") in "disabled":
                    if option == "foreground": self.widget.configure(disabledforeground=value)
                    elif option == "background" and "disabledbackground" in widget_opts_dict["options"]: self.widget.configure(disabledbackground=value)
            except: pass

            if option not in ("disabledforeground", "disabledbackground") and ((option == "state" and value in "disabledactive") or option != "state"):
                self.widget.configure({option: value})

            widget_opts_dict["options"][option] = str(value)

            self.update_idletasks()
            self.select_widget(self.widget, True)

            a, b = self.code_Text.tag_ranges(widget_opts_dict["nom"])
            self.deleting = True
            self.code_Text.delete(a, b)

            parent = widget_opts_dict["parent"]
            parent_name = parent = ("self" if self.poo else self.all_children[self.fenetre]["nom"]) if parent == self.fenetre else ("self." if self.poo else "")+self.all_children[parent]["nom"]

            items = {key: value for key, value in widget_opts_dict["options"].items() if value and value != self.defauts[widget_opts_dict["package"]+"."+widget_opts_dict["classe"]][key] and (str(value).isnumeric() and int(value) or not str(value).isnumeric())}

            text = ("\n\t\tself." if self.poo else "\n")+widget_opts_dict["nom"]+" = "+(widget_opts_dict["package"]+"." if widget_opts_dict["package"] in ("ttk", "Pmw") else "")+widget_opts_dict["classe"]+(self.sep[0] if items else "")+parent_name+(self.sep[1] if items else "")
            text += self.sep[1].join([key+"="+("\""+str(value)+"\"" if not ((value.isnumeric() or value[1:].isnumeric()) and int(value)) else value) for key, value in items.items() if value])+(self.sep[2] if items else ")")+"\n"+("\n" if items else "")
            
            self.highlighted_textbox.insert(a, text, tags=("widget", widget_opts_dict["nom"]))

            self.limite = self.code_Text.index(f"{widget_opts_dict['nom']}.last"), widget_opts_dict["nom"]

        except Exception as e: print(option, "x :-->", value, "\n", e, file=sys.stderr)
    
    def delete_widget(self, event): # Fonction pour supprimer le widget sélectionné
        if self.widget != self.fenetre:
            if askyesno("Suppresion", f"Voulez-vous supprimez {self.all_children[self.widget]['nom']} ?"):
                # Suppression du texte correspondant
                widget_opts_dict = self.all_children[self.widget]
                package = widget_opts_dict["package"]
                
                self.modules_opts[package][1] -= 1

                if package != "tkinter":
                    if not self.modules_opts[package][1]:
                        self.deleting = True
                        self.code_Text.delete(f"{package}.import.first", f"{package}.import.last")

                a, b = self.code_Text.tag_ranges(widget_opts_dict["nom"])
                self.deleting = True
                self.code_Text.delete(a, b)

                if widget_opts_dict["nom"] == self.limite[1]:
                    self.limite = a, widget_opts_dict["nom"]
                    self.code_Text.tag_delete(self.limite[1])

                self.Tree.delete(self.widget)

                # TO DO: Recursion delete
                for widget in widget_opts_dict["children"]: widget.destroy()
                
                self.all_children[widget_opts_dict["parent"]]["children"].pop(self.widget)
                self.all_children.pop(self.widget)
                self.widget.destroy()

                self.canvas.place_forget()
                self.resizing = False
            
                self.widget = self.fenetre
                self.update_options_Frame()

        else: self.bell()

    def resize_widget(self, event): # Rédimensionner le widget en maintenant le clic gauche de la souris
        if self.widget != self.fenetre:
            delta_x, delta_y = event.x_root - self.start_x, event.y_root - self.start_y

            if abs(delta_x) >= 5 or abs(delta_y) >= 5:

                if "E" in event.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(width=int(self.widget.winfo_width() + delta_x))

                elif "W" in event.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(x=self.widget.winfo_x() + delta_x, width=int(self.widget.winfo_width()) - delta_x)

                if "S" in event.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(height=int(self.widget.winfo_height() + delta_y))

                elif "N" in event.widget.gettags(CURRENT)[0]:
                    self.widget.place_configure(y=self.widget.winfo_y() + delta_y, height=int(self.widget.winfo_height()) - delta_y)

                # Enregistrement de la nouvelle position de la souris
                self.start_x, self.start_y = self.winfo_pointerxy()

                # déplacer aussi le rectangle de rédimensionnement
                self.update_idletasks()
                self.select_widget(self.widget, True)
                self.update_position_code(event)
   
    def move_widget(self, event): # Fonction déplacer le widget dans la fénêtre
        if self.widget != self.fenetre:
            delta_x, delta_y = event.x_root - self.start_x, event.y_root - self.start_y

            if abs(delta_x) >= 5 or abs(delta_y) >= 5:
                x, y = int(self.widget.place_info()["x"]) + delta_x, int(self.widget.place_info()["y"]) + delta_y
                self.widget.place_configure(x=x, y=y)

                # déplacer aussi le rectangle de redimensionnement
                self.update_idletasks()
                self.select_widget(self.widget, True)

                # Enregistrement de la nouvelle position de la souris
                self.start_x, self.start_y = self.winfo_pointerxy()

    def update_position_code(self, e):
        try:
            widget_opts_dict = self.all_children[self.widget]

            place_info = {key: value for key, value in self.widget.place_info().items() if key in widget_opts_dict["position"].keys() and value}
            place_info.update({"width": self.widget.winfo_width(), "height":self.widget.winfo_height()})

            a, b = self.code_Text.index(widget_opts_dict["nom"]+".pos.first"), self.code_Text.index(widget_opts_dict["nom"]+".pos.last")
            self.deleting = True
            self.code_Text.delete(a, b)

            text = ("\t\tself." if self.poo else "")+widget_opts_dict["nom"]+".place("
            text += ", ".join([""+key+"="+str("\""+str(value)+"\"" if not str(value).isnumeric() else value) for key, value in place_info.items()])+")\n"

            self.highlighted_textbox.insert(a, text, tags=("widget", widget_opts_dict["nom"], widget_opts_dict["nom"]+".pos"))
                    
            widget_opts_dict["position"] = place_info
            self.limite = self.code_Text.index(f"{widget_opts_dict['nom']}.last"), widget_opts_dict["nom"] 

        except Exception as e: print(e, file=sys.stderr); self.charge_code()

    def key_combination(self, e):
        #print(f"{e.keysym = }, {e.state = }")
        if e.state == 4 and e.keysym == "s":  self.save_files()

        if e.state == 4 and e.keysym == "o":  self.open_file()

        elif e.keysym == "F11": self.attributes("-fullscreen", not bool(self.attributes()[7]))

        elif e.keysym == "F5":
            if self.file: self.save_files(); run_path(self.file[:-4]+".py", run_name="__main__")
            else:
                try: exec(self.code_Text.get(1.0, END))
                except: self.charge_code(); exec(self.code_Text.get(1.0, END))

        elif e.keysym == "F10":
            set_appearance_mode("dark" if self._get_appearance_mode() == "light" else "light")
            self.change_code_theme()

            self.file_menu.configure(
                background=self["background"],
                foreground=self._apply_appearance_mode(("black", "white")),
                activebackground=self._apply_appearance_mode(("gray60", "gray30")),
            )

            self.style.configure("Line.TSeparator", background=self._apply_appearance_mode(("gray90", "blac")))
            self.code_Text._textbox.configure(selectbackground=self._apply_appearance_mode(("LightSkyBlue", "gray20")))

            self.V_Splitter["background"] = self._apply_appearance_mode(self._fg_color)
            self.H_Splitter["background"] = self._apply_appearance_mode(self._fg_color)
            self.panned_Window1["background"] = self._apply_appearance_mode(self._fg_color)

            color = "black" if all([i >= 32896 for i in self.winfo_rgb(self.canvas["bg"])]) else "white"
            self.canvas.itemconfigure("points", fill=color, outline=color)
            self.canvas.configure(bg=self.canvas.master.cget("bg"))

            self.style.configure("Treeview", background=self._apply_appearance_mode(("gray90", "gray20")), foreground=self._apply_appearance_mode(("black", "white")))

            # self.code_Text.config(selectbackground=self._apply_appearance_mode(("LightSkyBlue", "gray40")))
            # self.code_Text.tag_configure(self.widgets_list[self.fenetre]["children"][self.widget]["nom"], background=self.code_Text._textbox["selectbackground"])

            for widget in self.spin_widgets:
                widget.configure(
                    background=self._apply_appearance_mode(("white", "gray60")),
                    foreground=self._apply_appearance_mode(("black", "black")),
                    buttonbackground=self._apply_appearance_mode(("white", "gray80"))
                    )

    def change_code_theme(self):
        self.cdg.tagdefs['MYGROUP'] = {'foreground': self._apply_appearance_mode(('#7F7F7F', "gray60"))}

        # These five lines are optional. If omitted, default colours are used.
        self.cdg.tagdefs['COMMENT'] = {'foreground': self._apply_appearance_mode(('#dd0000', "#dd0000")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['KEYWORD'] = {'foreground': self._apply_appearance_mode(('#ff7700', "#ff8000")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['BUILTIN'] = {'foreground': self._apply_appearance_mode(('#900090', "#ff00ff")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['STRING'] = {'foreground': self._apply_appearance_mode(('#00aa00', "#02ff02")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}
        self.cdg.tagdefs['DEFINITION'] = {'foreground': self._apply_appearance_mode(('#0000ff', "#5e5eff")), "background": self._apply_appearance_mode(self.code_Text._fg_color)}

        self.cdg.config_colors()

    def destroy(self):
        if not self.code_Text.edit_modified():
            answer = showwarning(title="Fermerture", message="Voulez-vous sauvegarder avant de quiter ?", type="yesnocancel", icon="question")
            if answer == "no" or answer == "yes" and self.Savefile(): return super().destroy()

        elif askyesno(title="Fermerture", message="Voulez-vous vraiment quiter ?"): return super().destroy()

if __name__ == "__main__":
    TkGuiBuilder().mainloop()
