# advanced_gui.py - SEVİYE 3 ESTETİK UPGRADE
"""
🎨 LEVEL 3 AESTHETIC UPGRADE - KAPSAMLI MAKEOVER
- Glassmorphism Effects
- 3D Card Animations  
- Particle Backgrounds
- Cinematic Transitions
- Modern UI Components
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from datetime import datetime
import time
import math
import random
import threading
from typing import List, Dict, Any, Optional

class Level3EnterpriseGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎭 Enterprise ERP v5.0 - Level 3 Aesthetic")
        self.root.geometry("1600x900")
        self.root.state('zoomed')
        
        # ✨ LEVEL 3 AESTHETIC VARIABLES
        self.particles = []
        self.animation_running = True
        self.hover_effects = {}
        self.transition_state = "idle"
        self.glassmorphism_alpha = 0.85
        
        # Veri depolama (orijinal)
        self.main_data = []
        self.current_records = []
        self.processing_files = []
        
        # Modal referansları (orijinal)
        self.data_entry_window = None
        self.confirmation_dialog = None
        
        # 🎨 LEVEL 3 SETUP
        self.setup_level3_base()
        self.setup_glassmorphism_styles()
        self.setup_3d_effects()
        self.create_particle_system()
        self.create_level3_interface()
        self.start_aesthetic_animations()
        
        # GUI'yi öne getir (orijinal)
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

    def setup_level3_base(self):
        """🎨 Level 3 temel ayarlar"""
        # Modern dark background with gradient feel
        self.root.configure(bg='#0d1117')
        
        # Smooth cursor and modern feel
        self.root.configure(cursor='arrow')
        
        # Disable window resize animations (smoother)
        self.root.resizable(True, True)
        
    def setup_glassmorphism_styles(self):
        """🪟 Glassmorphism efektleri"""
        style = ttk.Style()
        style.theme_use('clam')

        # 🪟 GLASSMORPHISM NOTEBOOK - Transparan sekme efekti
        style.configure('Glassmorphism.TNotebook',
                       tabposition='n',
                       background='#1e1e2e',  # Originally rgba(30,30,46,0.7)
                       borderwidth=0,
                       relief='flat')
        
        style.configure('Glassmorphism.TNotebook.Tab',
                       padding=[25, 15],
                       background='#313244',  # Originally rgba(49,50,68,0.6)
                       foreground='#cdd6f4',
                       focuscolor='none',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=1,
                       relief='solid')
        
        # ✨ HOVER GLOW EFFECT
        style.map('Glassmorphism.TNotebook.Tab',
                  background=[('selected', '#89b4fa'),
                            ('active', '#89b4fa')],
                  foreground=[('selected', '#1e1e2e'),
                            ('active', '#1e1e2e')])

        # 🎴 3D CARD FRAMES - Depth effect
        style.configure('Glass3D.TLabelframe',
                       background='#313244',  # Originally rgba(49,50,68,0.8)
                       foreground='#cdd6f4',
                       borderwidth=2,
                       relief='raised',  # 3D effect
                       )
        
        style.configure('Glass3D.TLabelframe.Label',
                       background='#313244',  # Originally rgba(49,50,68,0.9)
                       foreground='#89b4fa',
                       font=('Segoe UI', 12, 'bold'))

        # 🔥 GLOWING BUTTONS - Neon effect
        style.configure('NeonPrimary.TButton',
                       background='#89b4fa',
                       foreground='#1e1e2e',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        
        style.map('NeonPrimary.TButton',
                  background=[('active', '#74c0fc'),
                            ('pressed', '#4dabf7')])

        style.configure('NeonSuccess.TButton',
                       background='#a6e3a1',
                       foreground='#1e1e2e',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        
        style.map('NeonSuccess.TButton',
                  background=[('active', '#8cf98c'),
                            ('pressed', '#69db69')])

        style.configure('NeonDanger.TButton',
                       background='#f38ba8',
                       foreground='#1e1e2e',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')

        # 🌊 GRADIENT TOOLBARS
        style.configure('GradientToolbar.TFrame',
                       background='linear-gradient(90deg, #181825, #313244)',
                       relief='flat',
                       borderwidth=0)

    def setup_3d_effects(self):
        """🎴 3D efektleri ve shadow sistemleri"""
        # 3D Transform matrisleri için hazırlık
        self.shadow_offset = 5
        self.perspective_depth = 10
        self.hover_scale = 1.05
        
    def create_particle_system(self):
        """✨ Particle background sistemi"""
        # Canvas for particles
        self.particle_canvas = tk.Canvas(
            self.root, 
            highlightthickness=0,
            background='#0d1117'
        )
        self.particle_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Send to back
        # Canvas.lower expects an item ID, so explicitly call the widget
        # method to move the entire canvas behind other widgets
        tk.Widget.lower(self.particle_canvas)
        
        # Generate initial particles
        self.generate_particles()
        
    def generate_particles(self):
        """✨ Parçacık üretimi"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Create 50 floating particles
        for _ in range(50):
            particle = {
                'x': random.randint(0, screen_width),
                'y': random.randint(0, screen_height),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(2, 6),
                'color': random.choice(['#89b4fa', '#a6e3a1', '#f9e2af', '#f38ba8', '#cdd6f4']),
                'alpha': random.uniform(0.3, 0.8),
                'pulse': random.uniform(0, 2 * math.pi)
            }
            self.particles.append(particle)

    def animate_particles(self):
        """✨ Parçacık animasyonu"""
        if not self.animation_running:
            return
            
        try:
            # Clear canvas
            self.particle_canvas.delete("particle")
            
            screen_width = self.root.winfo_width()
            screen_height = self.root.winfo_height()
            
            for particle in self.particles:
                # Update position
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                
                # Wrap around screen
                if particle['x'] < 0:
                    particle['x'] = screen_width
                elif particle['x'] > screen_width:
                    particle['x'] = 0
                    
                if particle['y'] < 0:
                    particle['y'] = screen_height
                elif particle['y'] > screen_height:
                    particle['y'] = 0
                
                # Pulse effect
                particle['pulse'] += 0.05
                pulse_alpha = particle['alpha'] + 0.2 * math.sin(particle['pulse'])
                pulse_size = particle['size'] + 1 * math.sin(particle['pulse'] * 2)
                
                # Draw particle with glow effect
                self.draw_glowing_particle(
                    particle['x'], particle['y'], 
                    pulse_size, particle['color'], pulse_alpha
                )
                
        except tk.TclError:
            # Widget destroyed
            self.animation_running = False
            return
            
        # Schedule next frame
        self.root.after(50, self.animate_particles)

    def draw_glowing_particle(self, x, y, size, color, alpha):
        """✨ Işıldayan parçacık çizimi"""
        try:
            # Outer glow
            glow_size = size * 2
            self.particle_canvas.create_oval(
                x - glow_size, y - glow_size,
                x + glow_size, y + glow_size,
                fill=color, outline="",
                stipple="gray25",
                tags="particle"
            )
            
            # Inner particle
            self.particle_canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=color, outline="",
                tags="particle"
            )
        except tk.TclError:
            pass

    def start_aesthetic_animations(self):
        """🎬 Estetik animasyonları başlat"""
        # Particle animation
        self.animate_particles()
        
        # Breathing effect for main elements
        self.start_breathing_effect()
        
        # Floating effect for cards
        self.start_floating_effect()

    def start_breathing_effect(self):
        """🫁 Nefes alma efekti"""
        def breathe():
            if not self.animation_running:
                return
                
            try:
                # Subtle alpha breathing for glassmorphism
                breath_cycle = time.time() * 0.5
                alpha_variation = 0.05 * math.sin(breath_cycle)
                self.glassmorphism_alpha = 0.85 + alpha_variation
                
            except:
                pass
                
            self.root.after(100, breathe)
            
        breathe()

    def start_floating_effect(self):
        """🎈 Yüzen eleman efekti"""
        def float_elements():
            if not self.animation_running:
                return
                
            try:
                # Subtle floating motion for stats cards
                float_cycle = time.time() * 0.3
                float_offset = 2 * math.sin(float_cycle)
                
                # Apply to stats cards if they exist
                if hasattr(self, 'stats_cards'):
                    for card in self.stats_cards:
                        try:
                            current_y = card.winfo_y()
                            card.place(y=current_y + float_offset)
                        except:
                            pass
                            
            except:
                pass
                
            self.root.after(150, float_elements)
            
        float_elements()

    def create_level3_interface(self):
        """🎨 Level 3 arayüz - Tüm efektlerle"""
        # Ana menü sistemi (orijinal fonksiyonellik korunuyor)
        self.create_comprehensive_menu()
        
        # 🌊 GRADIENT TOOLBAR
        self.create_gradient_toolbar()
        
        # 🪟 GLASSMORPHISM TABS
        self.create_glassmorphism_tabs()
        
        # 🎴 3D CONTENT MODULES
        self.create_3d_module_contents()
        
        # ✨ GLOWING STATUS BAR
        self.create_glowing_status_bar()

    def create_gradient_toolbar(self):
        """🌊 Gradient toolbar"""
        # Create gradient effect using multiple frames
        toolbar_height = 70
        
        # Base toolbar frame
        toolbar_frame = tk.Frame(
            self.root, 
            height=toolbar_height,
            bg='#181825'
        )
        toolbar_frame.pack(fill='x')
        toolbar_frame.pack_propagate(False)
        
        # Gradient overlay using Canvas
        gradient_canvas = tk.Canvas(
            toolbar_frame,
            height=toolbar_height,
            highlightthickness=0
        )
        gradient_canvas.pack(fill='both', expand=True)
        
        # Create gradient effect
        self.create_gradient_background(gradient_canvas, '#181825', '#313244')
        
        # Sol taraf - 🔥 GLOWING QUICK ACCESS
        self.create_glowing_quick_buttons(gradient_canvas)
        
        # Orta - ✨ ANIMATED TITLE
        self.create_animated_title(gradient_canvas)
        
        # Sağ taraf - 🎯 STATUS INDICATORS
        self.create_status_indicators(gradient_canvas)

    def create_gradient_background(self, canvas, color1, color2):
        """🌊 Canvas'ta gradient arka plan"""
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb)
        
        try:
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)
            
            width = canvas.winfo_reqwidth() or 1600
            height = canvas.winfo_reqheight() or 70
            
            # Create gradient strips
            for i in range(height):
                ratio = i / height
                r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
                g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
                b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
                
                color = rgb_to_hex((r, g, b))
                canvas.create_line(0, i, width, i, fill=color, width=1, tags="gradient")
                
        except Exception as e:
            # Fallback to solid color
            canvas.configure(bg=color1)

    def create_glowing_quick_buttons(self, parent_canvas):
        """🔥 Işıldayan hızlı erişim butonları"""
        # Buton frame'i canvas üzerine
        button_frame = tk.Frame(parent_canvas, bg='#181825')
        parent_canvas.create_window(20, 35, window=button_frame, anchor='w')
        
        quick_buttons = [
            ("🏠", "Ana Sayfa", self.go_home, "#89b4fa"),
            ("📊", "Dashboard", self.open_dashboard, "#a6e3a1"),
            ("💾", "Kaydet", self.quick_save, "#f9e2af"),
            ("🔍", "Ara", self.quick_search, "#f38ba8"),
            ("🖨️", "Yazdır", self.quick_print, "#cdd6f4")
        ]
        
        self.glow_buttons = []
        for i, (icon, tooltip, command, glow_color) in enumerate(quick_buttons):
            btn = self.create_glow_button(
                button_frame, icon, tooltip, command, glow_color
            )
            btn.pack(side='left', padx=8, pady=15)
            self.glow_buttons.append(btn)

    def create_glow_button(self, parent, icon, tooltip, command, glow_color):
        """🔥 Tek işıldayan buton oluşturma"""
        # Button frame for glow effect
        btn_frame = tk.Frame(parent, bg='#181825')
        
        # Main button
        btn = tk.Button(
            btn_frame,
            text=icon,
            font=('Segoe UI Emoji', 16),
            bg='#313244',
            fg='#cdd6f4',
            relief='flat',
            borderwidth=0,
            width=3,
            height=1,
            cursor='hand2',
            command=command
        )
        btn.pack()
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=glow_color, fg='#1e1e2e')
            self.create_hover_glow(btn, glow_color)
            
        def on_leave(e):
            btn.configure(bg='#313244', fg='#cdd6f4')
            self.remove_hover_glow(btn)
            
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn_frame

    def create_hover_glow(self, widget, color):
        """✨ Hover glow efekti"""
        # Bu advanced bir efekt - basit versiyonu
        try:
            widget.configure(relief='raised', borderwidth=2)
        except:
            pass

    def remove_hover_glow(self, widget):
        """✨ Hover glow efektini kaldır"""
        try:
            widget.configure(relief='flat', borderwidth=0)
        except:
            pass

    def create_animated_title(self, parent_canvas):
        """✨ Animasyonlu başlık"""
        title_text = "🎭 Enterprise ERP v5.0 - Level 3 Aesthetic"
        
        # Ana başlık
        title_id = parent_canvas.create_text(
            800, 35,  # Orta
            text=title_text,
            fill='#89b4fa',
            font=('Segoe UI', 16, 'bold'),
            anchor='center',
            tags="title"
        )
        
        # Alt ışık efekti
        glow_id = parent_canvas.create_text(
            800, 37,  # Hafif offset
            text=title_text,
            fill='#4dabf7',
            font=('Segoe UI', 16, 'bold'),
            anchor='center',
            tags="title_glow"
        )
        
        # Başlığı öne getir
        parent_canvas.tag_lower(glow_id)
        parent_canvas.tag_raise(title_id)

    def create_status_indicators(self, parent_canvas):
        """🎯 Status göstergeleri"""
        status_frame = tk.Frame(parent_canvas, bg='#181825')
        parent_canvas.create_window(1580, 35, window=status_frame, anchor='e')
        
        # Real-time clock
        self.clock_label = tk.Label(
            status_frame,
            text=datetime.now().strftime('%H:%M:%S'),
            font=('Segoe UI', 11, 'bold'),
            bg='#181825',
            fg='#a6e3a1'
        )
        self.clock_label.pack(side='right', padx=10)
        
        # User indicator
        user_label = tk.Label(
            status_frame,
            text="👤 Admin",
            font=('Segoe UI', 11),
            bg='#181825',
            fg='#cdd6f4'
        )
        user_label.pack(side='right', padx=10)
        
        # Start clock update
        self.update_clock()

    def update_clock(self):
        """⏰ Saati güncelle"""
        if hasattr(self, 'clock_label'):
            try:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.clock_label.configure(text=current_time)
            except:
                pass
        
        self.root.after(1000, self.update_clock)

    def create_glassmorphism_tabs(self):
        """🪟 Glassmorphism sekme sistemi"""
        # Ana container
        main_frame = tk.Frame(self.root, bg='#0d1117')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 🪟 GLASSMORPHISM NOTEBOOK
        self.notebook = ttk.Notebook(main_frame, style='Glassmorphism.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # 6 ana modül sekmesi (orijinal fonksiyonellik korunuyor)
        self.tabs = {}
        tab_configs = [
            ("📊 Dashboard", "dashboard"),
            ("📚 Muhasebe", "accounting"), 
            ("💰 Finans-Tahsilat", "finance"),
            ("📦 Stok", "inventory"),
            ("📈 Raporlar", "reports"),
            ("⚙️ Sistem", "system")
        ]
        
        for tab_name, tab_key in tab_configs:
            # Glassmorphism frame
            frame = tk.Frame(self.notebook, bg='#0d1117')  # Originally rgba(13,17,23,0.9)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_key] = frame
            
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed_with_effects)

    def on_tab_changed_with_effects(self, event):
        """🎬 Sekme değişiminde cinematic efektler"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        
        # Transition effect
        self.create_tab_transition_effect()
        
        # Update status with glow
        self.update_status_with_glow(f"Aktif modül: {selected_tab}")
        
        # Original functionality
        self.tab_changed(event)

    def create_tab_transition_effect(self):
        """🎬 Sekme geçiş efekti"""
        # Subtle flash effect
        if hasattr(self, 'notebook'):
            try:
                # Store original style
                original_bg = self.notebook.cget('background')
                
                # Flash effect
                self.notebook.configure(background='#89b4fa')
                self.root.after(100, lambda: self.notebook.configure(background=original_bg))
            except:
                pass

    def create_3d_module_contents(self):
        """🎴 3D modül içerikleri"""
        # Dashboard modülü (3D upgrade)
        self.create_3d_dashboard_module()
        
        # Finans-Tahsilat modülü (3D upgrade)
        self.create_3d_finance_module()
        
        # Diğer modüller (3D basit içerik)
        for module in ["accounting", "inventory", "reports", "system"]:
            self.create_3d_simple_module(module)

    def create_3d_dashboard_module(self):
        """📊 3D Dashboard modülü"""
        frame = self.tabs["dashboard"]
        frame.configure(bg='#0d1117')
        
        # 🎨 GRADIENT HEADER
        header_canvas = tk.Canvas(frame, height=80, highlightthickness=0, bg='#0d1117')
        header_canvas.pack(fill='x', pady=10, padx=20)
        
        self.create_gradient_background(header_canvas, '#1e1e2e', '#313244')
        
        # Animated title
        header_canvas.create_text(
            80, 40,
            text="📊 Enterprise Dashboard - Level 3",
            fill='#89b4fa',
            font=('Segoe UI', 18, 'bold'),
            anchor='w',
            tags="dashboard_title"
        )
        
        # 🎴 3D STATS CARDS
        self.create_3d_stats_cards(frame)
        
        # 🌊 FLOWING DATA TABLE
        self.create_flowing_data_table(frame)

    def create_3d_stats_cards(self, parent):
        """🎴 3D istatistik kartları"""
        stats_frame = tk.Frame(parent, bg='#0d1117')
        stats_frame.pack(fill='x', pady=20, padx=20)
        
        stats = [
            ("Toplam İşlem", "0", "#a6e3a1", "📊"),
            ("Bugünkü İşlem", "0", "#89b4fa", "📈"),
            ("Aktif Dosya", "0", "#f9e2af", "📁"),
            ("Başarı Oranı", "%0", "#f38ba8", "🎯")
        ]
        
        self.stats_cards = []
        for i, (title, value, color, icon) in enumerate(stats):
            card = self.create_floating_3d_card(
                stats_frame, title, value, color, icon, i
            )
            card.pack(side='left', fill='both', expand=True, padx=10)
            self.stats_cards.append(card)

    def create_floating_3d_card(self, parent, title, value, color, icon, index):
        """🎴 Tek yüzen 3D kart"""
        # Card container with 3D effect
        card_frame = tk.Frame(parent, bg='#0d1117')
        
        # 3D Card with glassmorphism
        card = ttk.LabelFrame(
            card_frame,
            text=f"{icon} {title}",
            padding=20,
            style='Glass3D.TLabelframe'
        )
        card.pack(fill='both', expand=True)
        
        # Value with glow effect
        value_frame = tk.Frame(card, bg='#313244')  # Originally rgba(49,50,68,0.8)
        value_frame.pack(fill='both', expand=True)
        
        value_label = tk.Label(
            value_frame,
            text=value,
            font=('Segoe UI', 28, 'bold'),
            fg=color,
            bg='#313244'
        )
        value_label.pack(pady=10)
        
        # Store reference for updates
        if index == 0:
            self.total_transactions_label = value_label
        elif index == 1:
            self.today_transactions_label = value_label
        
        # Hover effects
        def on_card_hover(e):
            card.configure(relief='raised')
            value_label.configure(fg='#ffffff')
            
        def on_card_leave(e):
            card.configure(relief='solid')
            value_label.configure(fg=color)
            
        card.bind('<Enter>', on_card_hover)
        card.bind('<Leave>', on_card_leave)
        value_label.bind('<Enter>', on_card_hover)
        value_label.bind('<Leave>', on_card_leave)
        
        return card_frame

    def create_flowing_data_table(self, parent):
        """🌊 Akan veri tablosu"""
        table_frame = tk.Frame(parent, bg='#0d1117')
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Glassmorphism table container
        glass_container = ttk.LabelFrame(
            table_frame,
            text="🌊 İşlem Kayıtları - Canlı Akış",
            padding=15,
            style='Glass3D.TLabelframe'
        )
        glass_container.pack(fill='both', expand=True)
        
        # Treeview with custom styling
        columns = ['ID', 'Tarih', 'Dosya', 'Açıklama', 'Tutar', 'Durum', 'Zaman']
        self.main_tree = ttk.Treeview(
            glass_container,
            columns=columns,
            show='headings',
            height=12
        )
        
        # Style the treeview
        widths = [50, 100, 150, 300, 120, 100, 120]
        for col, width in zip(columns, widths):
            self.main_tree.heading(col, text=f"✨ {col}")
            self.main_tree.column(
                col,
                width=width,
                anchor='center' if col in ['ID', 'Tarih', 'Tutar', 'Durum', 'Zaman'] else 'w'
            )
        
        # Scrollbar with style
        scrollbar = ttk.Scrollbar(
            glass_container,
            orient='vertical',
            command=self.main_tree.yview
        )
        self.main_tree.configure(yscrollcommand=scrollbar.set)
        
        self.main_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def create_3d_finance_module(self):
        """💰 3D Finans modülü"""
        frame = self.tabs["finance"]
        frame.configure(bg='#0d1117')
        
        # 🌊 GRADIENT HEADER
        header_canvas = tk.Canvas(frame, height=80, highlightthickness=0, bg='#0d1117')
        header_canvas.pack(fill='x', pady=10, padx=20)
        
        self.create_gradient_background(header_canvas, '#1e1e2e', '#313244')
        
        header_canvas.create_text(
            80, 40,
            text="💰 Finans - Tahsilat İşlemleri - Level 3",
            fill='#a6e3a1',
            font=('Segoe UI', 16, 'bold'),
            anchor='w'
        )
        
        # 🪟 GLASSMORPHISM SUB-TABS
        sub_notebook = ttk.Notebook(frame, style='Glassmorphism.TNotebook')
        sub_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Alt sekmeler (orijinal fonksiyonellik korunuyor)
        sub_tabs = [
            ("💳 Tahsilat", "collections"),
            ("🏦 Banka İşlemleri", "banking"),
            ("📊 Veri İşlemleri", "data_ops"),  # ANA ALT SEKME
            ("📈 Raporlar", "finance_reports")
        ]
        
        self.sub_tabs = {}
        for tab_name, tab_key in sub_tabs:
            sub_frame = tk.Frame(sub_notebook, bg='#0d1117')
            sub_notebook.add(sub_frame, text=tab_name)
            self.sub_tabs[tab_key] = sub_frame
            
        # 🎯 3D DATA OPERATIONS CONTENT
        self.create_3d_data_operations_content()
        
        # Diğer alt sekmeler için glassmorphism içerik
        for key in ["collections", "banking", "finance_reports"]:
            self.create_3d_placeholder_content(self.sub_tabs[key], key)

    def create_3d_data_operations_content(self):
        """🎯 3D Veri İşlemleri içeriği - 6 ADIMLI SÜREÇ"""
        frame = self.sub_tabs["data_ops"]
        frame.configure(bg='#0d1117')
        
        # 🌊 PROCESS STEPS TOOLBAR - Glassmorphism
        process_canvas = tk.Canvas(frame, height=100, highlightthickness=0, bg='#0d1117')
        process_canvas.pack(fill='x', padx=15, pady=15)
        
        self.create_gradient_background(process_canvas, '#181825', '#313244')
        
        # 🎯 3D PROCESS STEPS
        self.create_3d_process_steps(process_canvas)
        
        # 🎴 3D OPERATIONS CENTER
        self.create_3d_operations_center(frame)

    def create_3d_process_steps(self, canvas):
        """🎯 3D süreç adımları"""
        steps = [
            ("1️⃣", "Hazırlık", "#89b4fa"),
            ("2️⃣", "Doğrulama", "#a6e3a1"), 
            ("3️⃣", "Veri Seçimi", "#f9e2af"),
            ("4️⃣", "İşlem Türü", "#f38ba8"),
            ("5️⃣", "Veri Giriş", "#cba6f7"),  # ANA ADIM
            ("6️⃣", "Onay & Kayıt", "#94e2d5")
        ]
        
        step_width = 200
        start_x = 100
        
        for i, (icon, name, color) in enumerate(steps):
            x = start_x + (i * step_width)
            y = 50
            
            # 3D Step circle with glow
            self.create_3d_step_circle(canvas, x, y, icon, name, color, i == 4)  # Highlight step 5

    def create_3d_step_circle(self, canvas, x, y, icon, name, color, is_active=False):
        """🎯 3D adım dairesi"""
        # Outer glow
        glow_radius = 35 if is_active else 25
        canvas.create_oval(
            x - glow_radius, y - glow_radius,
            x + glow_radius, y + glow_radius,
            fill=color, outline="", stipple="gray25",
            tags="step_glow"
        )
        
        # Main circle
        radius = 25 if is_active else 20
        circle = canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline="#ffffff", width=2 if is_active else 1,
            tags="step_circle"
        )
        
        # Icon
        canvas.create_text(
            x, y - 5,
            text=icon,
            fill="#1e1e2e",
            font=('Segoe UI Emoji', 14 if is_active else 12, 'bold'),
            tags="step_icon"
        )
        
        # Label
        canvas.create_text(
            x, y + 35,
            text=name,
            fill="#cdd6f4",
            font=('Segoe UI', 9 if is_active else 8, 'bold'),
            tags="step_label"
        )

    def create_3d_operations_center(self, parent):
        """🎴 3D İşlem merkezi"""
        # Glassmorphism container
        operations_frame = ttk.LabelFrame(
            parent,
            text="🎯 Veri İşlem Merkezi - Level 3",
            padding=25,
            style='Glass3D.TLabelframe'
        )
        operations_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # 🔥 GLOWING OPERATION BUTTONS
        self.create_glowing_operation_buttons(operations_frame)
        
        # 🌊 FLOWING STATUS DISPLAY
        self.create_flowing_status_display(operations_frame)

    def create_glowing_operation_buttons(self, parent):
        """🔥 Işıldayan işlem butonları"""
        # İşlem butonları - KARMAŞIK HIYERARŞI (orijinal fonksiyonellik korunuyor)
        button_configs = [
            # 1. Seviye butonları
            [
                ("📂 Veri Kaynağı Seç", self.step1_select_source, "#89b4fa"),
                ("🔍 Kayıt Filtrele", self.step2_filter_records, "#a6e3a1"),
                ("📊 Veri Önizleme", self.step3_preview_data, "#f9e2af")
            ],
            # 2. Seviye butonları  
            [
                ("⚙️ İşlem Parametreleri", self.step4_set_parameters, "#f38ba8"),
                ("📝 Veri Giriş Başlat", self.step5_start_data_entry, "#cba6f7"),  # ANA BUTON
                ("✅ Toplu Onay", self.step6_batch_confirm, "#94e2d5")
            ]
        ]
        
        for i, button_row in enumerate(button_configs):
            row_frame = tk.Frame(parent, bg='#313244')
            row_frame.pack(fill='x', pady=15)
            
            for text, command, glow_color in button_row:
                btn = self.create_3d_glow_button(
                    row_frame, text, command, glow_color, 
                    is_primary=(text == "📝 Veri Giriş Başlat")
                )
                btn.pack(side='left', padx=15, pady=10)

    def create_3d_glow_button(self, parent, text, command, glow_color, is_primary=False):
        """🔥 3D ışıldayan buton"""
        # Button container
        btn_container = tk.Frame(parent, bg='#313244')
        
        # Main button with 3D effect
        btn = tk.Button(
            btn_container,
            text=text,
            command=command,
            font=('Segoe UI', 11 if is_primary else 10, 'bold'),
            bg=glow_color,
            fg='#1e1e2e',
            relief='raised' if is_primary else 'flat',
            borderwidth=3 if is_primary else 1,
            width=22,
            height=2,
            cursor='hand2'
        )
        btn.pack(padx=5, pady=5)
        
        # Enhanced hover effects
        def on_enter(e):
            btn.configure(
                relief='raised',
                borderwidth=4,
                bg='#ffffff',
                fg=glow_color
            )
            # Glow animation could be added here
            
        def on_leave(e):
            btn.configure(
                relief='raised' if is_primary else 'flat',
                borderwidth=3 if is_primary else 1,
                bg=glow_color,
                fg='#1e1e2e'
            )
            
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn_container

    def create_flowing_status_display(self, parent):
        """🌊 Akan durum gösterimi"""
        status_frame = tk.Frame(parent, bg='#313244')
        status_frame.pack(fill='x', pady=20)
        
        # Status label with flowing effect
        self.process_status_label = tk.Label(
            status_frame,
            text="🟢 Sistem hazır - Veri kaynağı seçin",
            font=('Segoe UI', 12, 'bold'),
            bg='#313244',
            fg='#a6e3a1'
        )
        self.process_status_label.pack(pady=15)
        
        # Animated status dots
        self.create_animated_status_dots(status_frame)

    def create_animated_status_dots(self, parent):
        """✨ Animasyonlu durum noktaları"""
        dots_canvas = tk.Canvas(parent, height=30, highlightthickness=0, bg='#313244')
        dots_canvas.pack(fill='x', pady=10)
        
        # Create 5 animated dots
        self.status_dots = []
        for i in range(5):
            x = 100 + (i * 40)
            dot = dots_canvas.create_oval(
                x-5, 10, x+5, 20,
                fill='#89b4fa', outline='',
                tags=f"dot_{i}"
            )
            self.status_dots.append(dot)
        
        # Start dot animation
        self.animate_status_dots(dots_canvas)

    def animate_status_dots(self, canvas):
        """✨ Durum noktası animasyonu"""
        if not self.animation_running:
            return
            
        try:
            # Pulse effect on dots
            pulse_time = time.time() * 2
            
            for i, dot in enumerate(self.status_dots):
                phase = (pulse_time + i * 0.5) % (2 * math.pi)
                alpha = 0.3 + 0.7 * (math.sin(phase) + 1) / 2
                
                # Color intensity based on alpha
                if alpha > 0.8:
                    color = '#89b4fa'
                elif alpha > 0.5:
                    color = '#74c0fc'
                else:
                    color = '#4dabf7'
                
                canvas.itemconfig(dot, fill=color)
                
        except tk.TclError:
            self.animation_running = False
            return
            
        canvas.after(100, lambda: self.animate_status_dots(canvas))

    def create_3d_simple_module(self, module_key):
        """🎴 3D basit modül içeriği"""
        frame = self.tabs[module_key]
        frame.configure(bg='#0d1117')
        
        # Glassmorphism placeholder
        placeholder_frame = ttk.LabelFrame(
            frame,
            text=f"🔧 {module_key.title()} Modülü - Level 3",
            padding=50,
            style='Glass3D.TLabelframe'
        )
        placeholder_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Animated coming soon message
        coming_soon_label = tk.Label(
            placeholder_frame,
            text=f"🚧 {module_key.title()} modülü geliştiriliyor...\n\n✨ Level 3 Aesthetic ile güncellenecek!",
            font=('Segoe UI', 16, 'bold'),
            bg='#313244',
            fg='#cdd6f4',
            justify='center'
        )
        coming_soon_label.pack(expand=True)

    def create_3d_placeholder_content(self, frame, key):
        """🎴 3D placeholder içerik"""
        frame.configure(bg='#0d1117')
        
        placeholder = ttk.LabelFrame(
            frame,
            text=f"🔧 {key.title()} - Level 3",
            padding=40,
            style='Glass3D.TLabelframe'
        )
        placeholder.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(
            placeholder,
            text=f"✨ {key.title()} modülü Level 3 Aesthetic ile geliştiriliyor...",
            font=('Segoe UI', 14, 'bold'),
            bg='#313244',
            fg='#89b4fa',
            justify='center'
        ).pack(expand=True)

    def create_glowing_status_bar(self):
        """✨ Işıldayan durum çubuğu"""
        # Status bar with gradient
        status_canvas = tk.Canvas(self.root, height=40, highlightthickness=0)
        status_canvas.pack(fill='x', side='bottom')
        
        self.create_gradient_background(status_canvas, '#181825', '#0d1117')
        
        # Status text with glow
        self.status_text_id = status_canvas.create_text(
            20, 20,
            text="🟢 Sistem Hazır - Enterprise ERP v5.0 Level 3",
            fill='#a6e3a1',
            font=('Segoe UI', 10, 'bold'),
            anchor='w',
            tags="status_text"
        )
        
        # Right side info with glow
        info_text = f"💻 Admin | 📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | 🚀 RPA Level 3 Hazır"
        status_canvas.create_text(
            1580, 20,
            text=info_text,
            fill='#cdd6f4',
            font=('Segoe UI', 9),
            anchor='e',
            tags="info_text"
        )
        
        self.status_canvas = status_canvas

    def update_status_with_glow(self, message):
        """✨ Glow efekti ile durum güncelleme"""
        if hasattr(self, 'status_canvas') and hasattr(self, 'status_text_id'):
            try:
                self.status_canvas.itemconfig(
                    self.status_text_id,
                    text=f"🔄 {message}",
                    fill='#89b4fa'
                )
                
                # Glow effect - fade back to green
                self.root.after(2000, lambda: self.status_canvas.itemconfig(
                    self.status_text_id,
                    fill='#a6e3a1'
                ))
            except:
                pass

    # === LEVEL 3 MODAL SISTEMI ===
    
    def open_advanced_data_entry(self) -> bool:
        """🎨 Level 3 Gelişmiş Veri Giriş Modal'ı"""
        print("🎨 Level 3 Modal açılıyor!")
        self.update_status_with_glow("🎨 Level 3 Veri Giriş sistemi açılıyor...")

        try:
            # Önceki modal'ı temizle
            if hasattr(self, 'data_entry_window') and self.data_entry_window:
                try:
                    self.data_entry_window.destroy()
                except:
                    pass
                self.data_entry_window = None

            # 🎨 LEVEL 3 MODAL WINDOW
            self.data_entry_window = tk.Toplevel(self.root)
            self.data_entry_window.title("🎨 Level 3 Veri Giriş Sistemi")
            self.data_entry_window.geometry("700x550+150+100")
            self.data_entry_window.configure(bg='#0d1117')

            # Modal properties
            self.data_entry_window.transient(self.root)
            self.data_entry_window.attributes('-alpha', 0.95)  # Slight transparency
            self.data_entry_window.lift()
            self.data_entry_window.focus_set()

            print("🎨 Level 3 Modal pencere oluşturuldu, içerik ekleniyor...")

            # 🎨 LEVEL 3 MODAL CONTENT
            self.create_level3_modal_content()
            
            # Modal hazır kontrolü
            self.root.update_idletasks()
            self.data_entry_window.update_idletasks()

            if hasattr(self, 'modal_entries') and self.modal_entries:
                for key, entry in self.modal_entries.items():
                    try:
                        entry.winfo_exists()
                    except tk.TclError:
                        print(f"❌ Entry widget {key} mevcut değil!")
                        return False
                
                print("✅ Level 3 Modal entries hazır!")
                self.update_status_with_glow("✅ Level 3 Modal başarıyla açıldı")
                return True
            else:
                print("❌ Level 3 Modal entries hazır değil!")
                return False
                
        except Exception as e:
            print(f"❌ Level 3 Modal açma hatası: {e}")
            return False

    def create_level3_modal_content(self):
        """🎨 Level 3 modal içeriği"""
        modal = self.data_entry_window

        # 🌊 GRADIENT HEADER
        header_canvas = tk.Canvas(modal, height=80, highlightthickness=0, bg='#0d1117')
        header_canvas.pack(fill='x', pady=(0, 10))
        
        self.create_gradient_background(header_canvas, '#1e1e2e', '#313244')
        
        header_canvas.create_text(
            350, 40,
            text="🎨 Level 3 Gelişmiş Veri Giriş Sistemi",
            fill='#89b4fa',
            font=('Segoe UI', 16, 'bold'),
            anchor='center'
        )

        # 🎴 GLASSMORPHISM FORM
        form_frame = ttk.LabelFrame(
            modal,
            text="📝 Kayıt Bilgileri - Level 3",
            padding=20,
            style='Glass3D.TLabelframe'
        )
        form_frame.pack(fill='x', pady=15, padx=20)

        # 🔥 GLOWING FORM FIELDS
        self.create_glowing_form_fields(form_frame)

        # 🎯 3D CONTROL BUTTONS
        self.create_3d_control_buttons(modal)

        # 🌊 FLOWING PROGRESS SYSTEM
        self.create_flowing_progress_system(modal)

    def create_glowing_form_fields(self, parent):
        """🔥 Işıldayan form alanları"""
        fields = [
            ("📅 Tarih:", "date_entry", "#89b4fa"),
            ("📝 Açıklama:", "desc_entry", "#a6e3a1"),
            ("💰 Tutar:", "amount_entry", "#f9e2af"),
            ("📁 Dosya:", "file_entry", "#f38ba8")
        ]

        self.modal_entries = {}
        for i, (label_text, entry_key, glow_color) in enumerate(fields):
            # Label with glow
            label = tk.Label(
                parent,
                text=label_text,
                font=('Segoe UI', 11, 'bold'),
                fg=glow_color,
                bg='#313244'
            )
            label.grid(row=i, column=0, sticky='w', pady=10, padx=(10, 20))
            
            # Entry with 3D effect
            entry = tk.Entry(
                parent,
                width=45,
                font=('Segoe UI', 11),
                bg='#1e1e2e',
                fg='#cdd6f4',
                insertbackground='#89b4fa',
                relief='solid',
                borderwidth=2
            )
            entry.grid(row=i, column=1, sticky='ew', pady=10, padx=(0, 10))
            
            # Hover effects for entries
            def on_entry_focus(e, color=glow_color):
                e.widget.configure(borderwidth=3, relief='raised')
                
            def on_entry_unfocus(e):
                e.widget.configure(borderwidth=2, relief='solid')
                
            entry.bind('<FocusIn>', on_entry_focus)
            entry.bind('<FocusOut>', on_entry_unfocus)
            
            self.modal_entries[entry_key] = entry

        parent.columnconfigure(1, weight=1)

    def create_3d_control_buttons(self, parent):
        """🎯 3D kontrol butonları"""
        control_frame = tk.Frame(parent, bg='#0d1117')
        control_frame.pack(fill='x', pady=20, padx=20)

        buttons = [
            ("💾 Kaydet", self.save_advanced_record, "#a6e3a1"),
            ("🧹 Temizle", self.clear_advanced_form, "#f9e2af"),
            ("📊 Göster", self.show_current_data, "#89b4fa"),
            ("❌ Kapat", self.close_modal, "#f38ba8")
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                control_frame,
                text=text,
                command=command,
                font=('Segoe UI', 11, 'bold'),
                bg=color,
                fg='#1e1e2e',
                relief='raised',
                borderwidth=3,
                width=14,
                height=2,
                cursor='hand2'
            )
            btn.pack(side='left', padx=10)
            
            # 3D Hover effects
            def on_btn_enter(e, original_color=color):
                e.widget.configure(bg='#ffffff', fg=original_color, borderwidth=4)
                
            def on_btn_leave(e, original_color=color):
                e.widget.configure(bg=original_color, fg='#1e1e2e', borderwidth=3)
                
            btn.bind('<Enter>', on_btn_enter)
            btn.bind('<Leave>', on_btn_leave)

    def create_flowing_progress_system(self, parent):
        """🌊 Akan progress sistemi"""
        progress_frame = tk.Frame(parent, bg='#0d1117')
        progress_frame.pack(fill='x', pady=15, padx=20)

        tk.Label(
            progress_frame,
            text="📈 İşlem İlerlemesi - Level 3:",
            font=('Segoe UI', 10, 'bold'),
            fg='#cdd6f4',
            bg='#0d1117'
        ).pack(anchor='w')

        # Custom progress bar with gradient
        self.modal_progress = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=400,
            style='TProgressbar'
        )
        self.modal_progress.pack(fill='x', pady=8)

        # Flowing status with glow
        self.modal_status = tk.Label(
            progress_frame,
            text="🟢 Hazır - Level 3 kayıt girişi bekliyor",
            font=('Segoe UI', 10),
            fg='#a6e3a1',
            bg='#0d1117'
        )
        self.modal_status.pack(anchor='w', pady=8)

    # === LEVEL 3 ENHANCED ORIGINAL FUNCTIONS ===
    
    def save_advanced_record(self):
        """💾 Level 3 gelişmiş kayıt kaydetme"""
        # Form verilerini al (orijinal fonksiyonellik)
        data = {}
        for key, entry in self.modal_entries.items():
            data[key] = entry.get().strip()
            
        if not all(data.values()):
            self.show_level3_modal_warning("Uyarı", "Lütfen tüm alanları doldurun!")
            return
            
        try:
            amount_val = float(data['amount_entry'].replace(',', '.'))
        except ValueError:
            self.show_level3_modal_error("Hata", "Geçersiz tutar formatı!")
            return
            
        # Ana tabloya ekle (orijinal fonksiyonellik korunuyor)
        record_id = len(self.main_data) + 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        self.main_data.append({
            'id': record_id,
            'date': data['date_entry'],
            'file': data['file_entry'],
            'description': data['desc_entry'],
            'amount': amount_val,
            'status': 'Kaydedildi',
            'time': timestamp
        })
        
        # Ana tabloyu güncelle (orijinal)
        self.main_tree.insert('', 'end', values=[
            record_id, data['date_entry'], data['file_entry'],
            data['desc_entry'], f"{amount_val:.2f} TL",
            'Kaydedildi', timestamp
        ])
        
        # 🎨 LEVEL 3 ENHANCEMENTS
        self.update_3d_dashboard_stats()
        self.create_save_success_animation()
        
        # Progress güncelle (orijinal mantık)
        total_expected = len(self.current_records) if self.current_records else 100
        current_progress = len(self.main_data)
        progress_percent = min(100, (current_progress / total_expected) * 100)
        self.modal_progress['value'] = progress_percent

        # Level 3 status update
        self.modal_status.config(
            text=f"✅ Level 3 Kayıt {record_id} kaydedildi! ({current_progress}/{total_expected})",
            fg='#a6e3a1'
        )

        # Form temizle
        self.clear_advanced_form()
        
        # Ana tabloya scroll
        children = self.main_tree.get_children()
        if children:
            self.main_tree.see(children[-1])

    def create_save_success_animation(self):
        """✨ Kaydetme başarı animasyonu"""
        # Subtle flash effect on modal
        if hasattr(self, 'data_entry_window'):
            try:
                original_alpha = self.data_entry_window.attributes('-alpha')
                self.data_entry_window.attributes('-alpha', 1.0)
                self.root.after(150, lambda: self.data_entry_window.attributes('-alpha', original_alpha))
            except:
                pass

    def update_3d_dashboard_stats(self):
        """📊 3D dashboard istatistik güncelleme"""
        if hasattr(self, 'total_transactions_label'):
            total = len(self.main_data)
            today = len([
                r for r in self.main_data
                if r['date'] == datetime.now().strftime('%d.%m.%Y')
            ])

            # Level 3 güncelleme - glow effect ile
            self.total_transactions_label.config(text=str(total), fg='#a6e3a1')
            if hasattr(self, 'today_transactions_label'):
                self.today_transactions_label.config(text=str(today), fg='#89b4fa')
            
            # Glow effect - fade back
            self.root.after(1500, lambda: self.total_transactions_label.config(fg='#a6e3a1'))

    def show_level3_modal_warning(self, title: str, message: str):
        """⚠️ Level 3 modal uyarı"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        popup.geometry("350x150")
        popup.configure(bg='#1e1e2e')
        popup.attributes('-alpha', 0.95)

        # Center on modal
        modal_x = self.data_entry_window.winfo_rootx()
        modal_y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"350x150+{modal_x + 175}+{modal_y + 200}")

        popup.transient(self.data_entry_window)
        popup.attributes('-topmost', True)
        popup.grab_set()

        tk.Label(popup, text="⚠️", font=('Segoe UI Emoji', 24),
                 bg='#1e1e2e', fg='#f9e2af').pack(pady=10)
        tk.Label(popup, text=message, font=('Segoe UI', 11),
                 bg='#1e1e2e', fg='#cdd6f4', wraplength=300).pack(pady=5)
        
        btn = tk.Button(popup, text="Tamam", command=popup.destroy,
                  bg='#f38ba8', fg='#1e1e2e', font=('Segoe UI', 10, 'bold'),
                  relief='raised', borderwidth=2)
        btn.pack(pady=10)

    def show_level3_modal_error(self, title: str, message: str):
        """❌ Level 3 modal hata"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        popup.geometry("350x150")
        popup.configure(bg='#1e1e2e')
        popup.attributes('-alpha', 0.95)

        # Center on modal
        modal_x = self.data_entry_window.winfo_rootx()
        modal_y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"350x150+{modal_x + 175}+{modal_y + 200}")

        popup.transient(self.data_entry_window)
        popup.attributes('-topmost', True)
        popup.grab_set()

        tk.Label(popup, text="❌", font=('Segoe UI Emoji', 24),
                 bg='#1e1e2e', fg='#f38ba8').pack(pady=10)
        tk.Label(popup, text=message, font=('Segoe UI', 11),
                 bg='#1e1e2e', fg='#cdd6f4', wraplength=300).pack(pady=5)
        
        btn = tk.Button(popup, text="Tamam", command=popup.destroy,
                  bg='#f38ba8', fg='#1e1e2e', font=('Segoe UI', 10, 'bold'),
                  relief='raised', borderwidth=2)
        btn.pack(pady=10)

    # === LEVEL 3 ENHANCED ORIGINAL METHODS ===
    
    def clear_advanced_form(self):
        """🧹 Level 3 form temizleme"""
        for entry in self.modal_entries.values():
            entry.delete(0, tk.END)
            # Level 3 clear animation
            entry.configure(bg='#a6e3a1')
            self.root.after(200, lambda e=entry: e.configure(bg='#1e1e2e'))
            
        self.modal_status.config(
            text="🧹 Form temizlendi - Level 3 yeni kayıt girişi hazır",
            fg='#f9e2af'
        )

    def close_modal(self):
        """❌ Level 3 modal kapatma"""
        if self.data_entry_window:
            # Level 3 closing animation
            try:
                for alpha in [0.8, 0.6, 0.4, 0.2, 0.0]:
                    self.data_entry_window.attributes('-alpha', alpha)
                    self.data_entry_window.update()
                    time.sleep(0.05)
            except:
                pass
            
            self.data_entry_window.destroy()
            self.data_entry_window = None
        self.update_status_with_glow("🎨 Level 3 Veri giriş sistemi kapatıldı")

    def _show_info_left(self, title: str, message: str) -> None:
        """Sol tarafta bilgi mesajı göster"""
        messagebox.showinfo(title, message, parent=self.root)

    def _ask_yes_no_left(self, title: str, message: str) -> bool:
        """Sol tarafta evet/hayır sorusu"""
        return messagebox.askyesno(title, message, parent=self.root)

    # === ORIGINAL FUNCTIONALITY PRESERVED ===
    
    def create_comprehensive_menu(self):
        """📋 Kapsamlı menü sistemi (orijinal fonksiyonellik korunuyor)"""
        menubar = tk.Menu(self.root, background='#181825', foreground='#cdd6f4')
        self.root.config(menu=menubar)
        
        # Ana modüller (orijinal)
        modules = {
            "🏠 Ana Sayfa": ["Dashboard", "Hızlı Erişim", "Raporlar", "Ayarlar"],
            "📚 Muhasebe": ["Hesap Planı", "Yevmiye", "Mizan", "Bilanço", "Gelir Tablosu"],
            "💰 Finans": ["Nakit Akışı", "Banka", "Kasa", "Çek-Senet", "Kredi Kartı"],
            "💳 Finans-Tahsilat": ["Tahsilat İşlemleri", "Müşteri Hesapları", "Vadeli İşlemler", "Komisyon"],
            "🛒 Satış": ["Sipariş", "Fatura", "İade", "Müşteri", "Fiyat Listesi"],
            "📦 Stok": ["Stok Kartları", "Giriş-Çıkış", "Sayım", "Transfer", "Depo"],
            "👥 Personel": ["Bordro", "Puantaj", "İzin", "Mesai", "SGK"],
            "🏭 Üretim": ["Üretim Emri", "Malzeme İhtiyacı", "Kapasite", "Kalite"],
            "📈 Raporlar": ["Mali Tablolar", "Analitik", "Grafik", "Dashboard"],
            "⚙️ Sistem": ["Kullanıcılar", "Yetki", "Backup", "Log", "Parametreler"]
        }
        
        for module_name, sub_menus in modules.items():
            module_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=module_name, menu=module_menu)
            
            for sub_menu in sub_menus:
                module_menu.add_command(
                    label=sub_menu,
                    command=lambda m=module_name, s=sub_menu: self.menu_selected(m, s)
                )

    # Step functions (orijinal fonksiyonellik korunuyor)
    def step1_select_source(self):
        """Adım 1: Veri kaynağı seçimi onayı"""
        return self._ask_yes_no_left(
            "Adım 1 - Veri Kaynağı",
            "Veri kaynağı seçildi mi?"
        )

    def step2_filter_records(self):
        """Adım 2: Kayıt filtreleme onayı"""
        return self._ask_yes_no_left(
            "Adım 2 - Kayıt Filtreleme",
            "Kayıtları filtrelemek istiyor musunuz?"
        )

    def step3_preview_data(self):
        """Adım 3: Veri önizleme bilgilendirmesi"""
        self._show_info_left(
            "Adım 3 - Önizleme",
            "Önizleme tamamlandı."
        )
        return True

    def step4_set_parameters(self):
        """Adım 4: Parametre ayarlama onayı"""
        return self._ask_yes_no_left(
            "Adım 4 - Parametreler",
            "Parametreler ayarlandı mı?"
        )

    def step5_start_data_entry(self):
        """Level 3 veri giriş modalini normal şekilde aç"""
        print("🎨 Level 3 veri giriş modalı açılıyor")

        result = self.open_advanced_data_entry()
        if result:
            self._delayed_modal_confirmation()
        return result

    def _delayed_modal_confirmation(self):
        """Level 3 Modal açıldıktan sonra gecikmeli onay"""
        try:
            proceed = self._ask_yes_no_left(
                "Level 3 Veri Girişi Onayı",
                f"Level 3 Modal başarıyla açıldı.\n\n📊 {len(self.current_records) if self.current_records else 0} kayıt işlenecek.\n\n🎨 RPA ile otomatik veri girişi başlatılsın mı?"
            )
            
            if proceed:
                self.update_process_status("✅ Kullanıcı onayladı - Level 3 RPA başlayabilir")
            else:
                self.update_process_status("⏹️ Kullanıcı iptal etti")
                if self.data_entry_window:
                    self.close_modal()
                    
        except Exception as e:
            print(f"❌ Level 3 Gecikmeli onay hatası: {e}")
            
    def step6_batch_confirm(self):
        print("✅ Adım 6: Otomatik onaylandı")

    # Utility functions (orijinal fonksiyonellik korunuyor)
    def update_process_status(self, message):
        """Süreç durumunu güncelle"""
        if hasattr(self, 'process_status_label'):
            self.process_status_label.config(text=message)
        self.update_status_with_glow(message)
        
    def update_status(self, message):
        """Ana durum çubuğunu güncelle"""
        self.update_status_with_glow(message)
        self.root.update_idletasks()

    def tab_changed(self, event):
        """Sekme değişim eventi (orijinal)"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        # Level 3 enhancement already handled in on_tab_changed_with_effects
        
    def menu_selected(self, module, sub_menu):
        """Menü seçim eventi (orijinal)"""
        self.update_status_with_glow(f"Menü: {module} > {sub_menu}")
        
        # Finans-Tahsilat menüsü seçilirse ilgili sekmeye git
        if "Finans" in module and "Tahsilat" in sub_menu:
            self.notebook.select(2)  # Finans sekmesi

    # Quick access functions (orijinal fonksiyonellik korunuyor)
    def go_home(self):
        """Ana sayfaya git"""
        self.notebook.select(0)
        self.update_status_with_glow("🏠 Ana sayfa")
        
    def open_dashboard(self):
        """Dashboard aç"""
        self.notebook.select(0)
        self.update_status_with_glow("📊 Dashboard açıldı")
        
    def quick_save(self):
        """Hızlı kaydet"""
        self.update_status_with_glow("💾 Hızlı kaydetme...")
        messagebox.showinfo("Bilgi", "Veriler kaydedildi!")
        
    def quick_search(self):
        """Hızlı arama"""
        search_term = simpledialog.askstring("🔍 Hızlı Arama", "Aranacak terimi girin:")
        if search_term:
            self.update_status_with_glow(f"🔍 Arama: '{search_term}'")
            
    def quick_print(self):
        """Hızlı yazdır"""
        self.update_status_with_glow("🖨️ Yazdırma...")
        messagebox.showinfo("Bilgi", "Yazdırma işlemi başlatıldı!")

    def show_current_data(self):
        """Mevcut veriyi göster (orijinal fonksiyonellik korunuyor)"""
        if not self.current_records:
            messagebox.showinfo("Bilgi", "Gösterilecek veri bulunamadı.")
            return
            
        # Level 3 preview window
        preview = tk.Toplevel(self.data_entry_window)
        preview.title("📊 Level 3 Yüklenen Veriler")
        preview.geometry("900x650")
        preview.configure(bg='#0d1117')
        preview.attributes('-alpha', 0.95)
        
        # Veri tablosu
        if self.current_records:
            columns = list(self.current_records[0].keys())
            tree = ttk.Treeview(preview, columns=columns, show="headings", height=25)
            
            for col in columns:
                tree.heading(col, text=f"✨ {col.title()}")
                tree.column(col, width=150, anchor="w")
                
            for rec in self.current_records:
                tree.insert("", "end", values=[rec.get(col, "") for col in columns])
                
            tree.pack(fill="both", expand=True, padx=20, pady=20)
            
        # Level 3 close button
        close_btn = tk.Button(preview, text="❌ Kapat", command=preview.destroy,
                  font=('Segoe UI', 12, 'bold'), bg='#f38ba8', fg='#1e1e2e',
                  relief='raised', borderwidth=3, width=15, height=2)
        close_btn.pack(pady=15)

    # External access methods (orijinal API korunuyor)
    def get_data_entry_button_action(self):
        """RPA için Veri Giriş butonunun fonksiyonu"""
        return self.step5_start_data_entry
        
    def get_main_data(self):
        """Ana veri listesini döndür"""
        return self.main_data
        
    def set_current_records(self, records):
        """Mevcut kayıtları ayarla"""
        self.current_records = records
        
    def set_processing_files(self, file_list):
        """İşlenecek dosya listesini ayarla"""
        self.processing_files = file_list

    def run(self):
        """🎨 Level 3 Uygulamayı çalıştır"""
        self.update_status_with_glow("🎨 Level 3 Enterprise ERP Sistemi hazır - Karmaşık navigasyon aktif")
        try:
            self.root.mainloop()
        finally:
            # Cleanup animations
            self.animation_running = False


# Level 3 GUI'yi EnterpriseGUI olarak alias et (backward compatibility)
EnterpriseGUI = Level3EnterpriseGUI


# Test
if __name__ == "__main__":
    print("🎨 Level 3 Enterprise ERP - Test Modu")
    app = Level3EnterpriseGUI()
    app.run()
