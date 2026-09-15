import os
import tkinter as tk
from tkinter import ttk, messagebox
from app.database.queries import get_dashboard_data
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PIL import Image, ImageDraw

###############################################################
# KARNEX AI
# MSSQL tabanli finansal dashboard
#
# Dashboard finansal verileri MSSQL veritabanindan alir.
# AI, RAG ve ML modulleri ilerleyen asamalarda eklenecektir.

###############################################################

BG = "#f3f7fc"
NAVY = "#10233d"
NAVY_2 = "#193452"
BLUE = "#247ce5"
LIGHT_BLUE = "#eaf3ff"
TEXT = "#15243d"
MUTED = "#6b7f9e"
WHITE = "#ffffff"
BORDER = "#d9e5f3"
GREEN = "#20b486"
ORANGE = "#f49a38"
RED = "#f05d5e"
PURPLE = "#8864df"


class KarnexApp(tk.Tk):

    def __init__(self):
        # ONEMLI:
        # Tkinter penceresi once olusturulmalidir.
        # self.iconbitmap() bundan sonra cagrilmalidir.
        super().__init__()

        self.load_dashboard_data()
        self.title("Kârnex AI")
        self.state('zoomed')
        self.minsize(1100, 700)
        self.configure(bg=BG)

        # Windows uygulama / gorev cubugu ikonu
        self.create_windows_icon()

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "Treeview.Heading",
            background="#eaf1fa",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold")
        )

        self.pages = {}
        self.active_page = None

        self.build_shell()
        self.create_pages()
        self.show_page("Ana Sayfa")

    # ========================================================
    # WINDOWS IKONU
    # ========================================================
    def load_dashboard_data(self):
        try:
            data = get_dashboard_data()

            self.dashboard_data = data

        except Exception as e:
            print("Dashboard veri yukleme hatasi:")
            print(e)

            self.dashboard_data = {
                "total_income": 0,
                "total_expense": 0,
                "net_profit": 0,
                "invoice_count": 0,
                "top_expenses": []
            }
    def create_windows_icon(self):
        """
        Kârnex logosunu otomatik olarak ICO dosyasina cevirir
        ve Windows pencere/gorev cubugu ikonu olarak kullanir.
        """
        # --- WINDOWS TASKBAR IKON COZUMU ---
        try:
            import ctypes
            # Windows'a bu uygulamanin python.exe'den bagimsiz bir AppUserModelID'ye sahip oldugunu bildiriyoruz
            myappid = 'karnex.ai.copilot.v1' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print("Windows AppUserModelID ayarlanamadi:", e)
        # -----------------------------------

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "karnex.ico")

            # 64x64 seffaf PNG benzeri temel goruntu
            img = Image.new(
                "RGBA",
                (64, 64),
                (0, 0, 0, 0)
            )

            draw = ImageDraw.Draw(img)

            # Sol mavi K parcasi
            draw.polygon(
                [
                    (5, 31),
                    (24, 9),
                    (37, 9),
                    (21, 31),
                    (37, 54),
                    (24, 54)
                ],
                fill="#2d9cf0"
            )

            # Sag koyu mavi K parcasi
            draw.polygon(
                [
                    (23, 31),
                    (42, 9),
                    (55, 9),
                    (39, 31),
                    (55, 54),
                    (42, 54)
                ],
                fill="#1769b4"
            )

            # Windows icin coklu boyutlu ICO
            img.save(
                icon_path,
                format="ICO",
                sizes=[
                    (16, 16),
                    (24, 24),
                    (32, 32),
                    (48, 48),
                    (64, 64)
                ]
            )

            # Windows pencere ikonu (Sol ust ikon)
            self.iconbitmap(icon_path)

            # Görev çubuğu ikonu için PhotoImage kullanımı
            self._icon_image = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, self._icon_image)

        except Exception as e:
            print(" ", e)

    # ========================================================
    # YARDIMCILAR
    # ========================================================

    def make_label(
        self,
        parent,
        text,
        size=10,
        color=TEXT,
        bold=False,
        bg=WHITE
    ):
        return tk.Label(
            parent,
            text=text,
            font=(
                "Segoe UI",
                size,
                "bold" if bold else "normal"
            ),
            fg=color,
            bg=bg,
            anchor="w"
        )

    def card(self, parent, padx=8, pady=8):
        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        frame.pack_propagate(False)

        return frame

    def page_title(self, parent, title, subtitle):

        self.make_label(
            parent,
            title,
            20,
            TEXT,
            True,
            BG
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 2)
        )

        self.make_label(
            parent,
            subtitle,
            10,
            MUTED,
            False,
            BG
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

    def add_stat_card(
        self,
        parent,
        title,
        value,
        change,
        icon,
        color
    ):

        frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        icon_box = tk.Frame(
            frame,
            bg=LIGHT_BLUE,
            width=44,
            height=44
        )

        icon_box.pack(
            side="left",
            padx=10,
            pady=14
        )

        icon_box.pack_propagate(False)

        self.make_label(
            icon_box,
            icon,
            19,
            color,
            True,
            LIGHT_BLUE
        ).pack(expand=True)

        body = tk.Frame(
            frame,
            bg=WHITE
        )

        body.pack(
            side="left",
            pady=10
        )

        self.make_label(
            body,
            title,
            9,
            TEXT,
            True
        ).pack(anchor="w")

        self.make_label(
            body,
            value,
            16,
            TEXT,
            True
        ).pack(
            anchor="w",
            pady=3
        )

        self.make_label(
            body,
            change,
            9,
            color,
            True
        ).pack(anchor="w")

    def make_action_button(
        self,
        parent,
        text,
        command=None
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=BLUE,
            fg=WHITE,
            activebackground="#1764c0",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8,
            cursor="hand2"
        )

    # ========================================================
    # ANA ISKELET
    # ========================================================

    def build_shell(self):

        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------------
        # UST BAR
        # ----------------------------------------------------

        top = tk.Frame(
            self,
            bg=NAVY,
            height=78
        )

        top.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        top.grid_propagate(False)

        # Kârnex logosu
        logo = tk.Canvas(
            top,
            width=58,
            height=65,
            bg=NAVY,
            highlightthickness=0
        )

        logo.pack(
            side="left",
            padx=(15, 4)
        )

        logo.create_polygon(
            5, 31,
            24, 9,
            37, 9,
            21, 31,
            37, 54,
            24, 54,
            fill="#2d9cf0",
            outline=""
        )

        logo.create_polygon(
            23, 31,
            42, 9,
            55, 9,
            39, 31,
            55, 54,
            42, 54,
            fill="#1769b4",
            outline=""
        )

        # Baslik
        title = tk.Frame(
            top,
            bg=NAVY
        )

        title.pack(
            side="left",
            pady=8
        )

        self.make_label(
            title,
            "Kârnex AI",
            20,
            WHITE,
            True,
            NAVY
        ).pack(anchor="w")

        self.make_label(
            title,
            "Finansal Zekâ, Daha İyi Kararlar",
            9,
            "#b8cce5",
            False,
            NAVY
        ).pack(anchor="w")

        # Sag bilgi kartlari
        info = tk.Frame(
            top,
            bg=NAVY
        )

        info.pack(
            side="right",
            padx=15,
            pady=10
        )

        self.top_info(
            info,
            "●  MSSQL Bağlantısı",
            "Bağlı",
            GREEN
        )

        self.top_info(
            info,
            "▣  MSSQL Server",
            "KARNEXDB",
            "#d9e7f8"
        )

        self.top_info(
            info,
            "●  Hüseyin Salman",
            "Muhasebe Uzmanı",
            "#d9e7f8"
        )

        # ----------------------------------------------------
        # SOL MENU
        # ----------------------------------------------------

        self.sidebar = tk.Frame(
            self,
            bg=NAVY,
            width=230
        )

        self.sidebar.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        menu = [
            ("⌂", "Ana Sayfa"),
            ("▤", "AI Chat / Copilot"),
            ("▥", "Veri Analizleri"),
            ("▲", "Anomali Tespiti"),
            ("▣", "RAG Doküman Arama"),
            ("▤", "Raporlar"),
            ("⚙", "Ayarlar"),
        ]

        self.menu_buttons = {}

        for icon, name in menu:

            btn = tk.Button(
                self.sidebar,
                text=f"{icon}   {name}",
                command=lambda n=name: self.show_page(n),
                bg=NAVY,
                fg=WHITE,
                activebackground=NAVY_2,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                anchor="w",
                font=("Segoe UI", 10),
                padx=18,
                pady=12,
                cursor="hand2"
            )

            btn.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.menu_buttons[name] = btn

        # ----------------------------------------------------
        # SIDEBAR PROMO
        # ----------------------------------------------------

        promo = tk.Frame(
            self.sidebar,
            bg="#142b47",
            highlightbackground="#284562",
            highlightthickness=1
        )

        promo.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=25
        )

        self.make_label(
            promo,
            "◉",
            30,
            "#2ca6f5",
            True,
            "#142b47"
        ).pack(
            pady=(12, 0)
        )

        self.make_label(
            promo,
            "Kârnex AI",
            13,
            WHITE,
            True,
            "#142b47"
        ).pack()

        self.make_label(
            promo,
            "MSSQL Tabanlı",
            9,
            "#c3d4e9",
            False,
            "#142b47"
        ).pack(pady=(8, 0))

        self.make_label(
            promo,
            "Yapay Zekâ Destekli",
            9,
            "#c3d4e9",
            False,
            "#142b47"
        ).pack()

        self.make_label(
            promo,
            "Muhasebe Copilot'u",
            9,
            "#c3d4e9",
            False,
            "#142b47"
        ).pack(pady=(0, 12))

        # ----------------------------------------------------
        # SIDEBAR ALT
        # ----------------------------------------------------

        bottom = tk.Frame(
            self.sidebar,
            bg=NAVY
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.make_label(
            bottom,
            "● Sistem Aktif",
            9,
            GREEN,
            False,
            NAVY
        ).pack(side="left")

        self.make_label(
            bottom,
            "v1.0.0",
            9,
            "#b9cce5",
            False,
            NAVY
        ).pack(side="right")

        # ----------------------------------------------------
        # ANA ICERIK
        # ----------------------------------------------------

        self.content = tk.Frame(
            self,
            bg=BG
        )

        self.content.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.content.grid_rowconfigure(
            0,
            weight=1
        )

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------------
        # ALT DURUM CUBUGU
        # ----------------------------------------------------

        status = tk.Frame(
            self,
            bg=NAVY,
            height=45
        )

        status.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        status.grid_propagate(False)

        # Kârnex AI logosu
        status_logo = tk.Canvas(
            status,
            width=38,
            height=38,
            bg=NAVY,
            highlightthickness=0
        )

        status_logo.pack(
            side="left",
            padx=(15, 5),
            pady=3
        )

        status_logo.create_polygon(
            4, 18,
            17, 4,
            25, 4,
            14, 18,
            25, 34,
            17, 34,
            fill="#2d9cf0",
            outline=""
        )

        status_logo.create_polygon(
            17, 18,
            29, 4,
            37, 4,
            26, 18,
            37, 34,
            29, 34,
            fill="#1769b4",
            outline=""
        )

        self.make_label(
            status,
            "Kârnex AI",
            9,
            WHITE,
            True,
            NAVY
        ).pack(
            side="left",
            padx=(0, 18)
        )

        self.make_label(
            status,
            "◷  MSSQL: KARNEXDB   |   Kullanıcı: Hüseyin Salman",
            8,
            "#d8e5f5",
            False,
            NAVY
        ).pack(side="left")

        self.make_label(
            status,
            "Daha akıllı analizler, daha güçlü kararlar...",
            8,
            "#d8e5f5",
            False,
            NAVY
        ).pack(
            side="right",
            padx=15
        )

    # ========================================================
    # UST BILGI KARTI
    # ========================================================

    def top_info(
        self,
        parent,
        title,
        value,
        color
    ):

        frame = tk.Frame(
            parent,
            bg="#1b3452",
            width=165,
            height=52,
            highlightbackground="#2b4867",
            highlightthickness=1
        )

        frame.pack(
            side="left",
            padx=4
        )

        frame.pack_propagate(False)

        self.make_label(
            frame,
            title,
            8,
            "#d9e7f8",
            True,
            "#1b3452"
        ).pack(
            anchor="w",
            padx=10,
            pady=(8, 0)
        )

        self.make_label(
            frame,
            value,
            8,
            color,
            False,
            "#1b3452"
        ).pack(
            anchor="w",
            padx=10
        )

    # ========================================================
    # SAYFALAR
    # ========================================================

    def create_pages(self):

        page_names = [
            "Ana Sayfa",
            "AI Chat / Copilot",
            "Veri Analizleri",
            "Anomali Tespiti",
            "RAG Doküman Arama",
            "Raporlar",
            "Ayarlar"
        ]

        for name in page_names:

            frame = tk.Frame(
                self.content,
                bg=BG
            )

            frame.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

            self.pages[name] = frame

        self.build_home(
            self.pages["Ana Sayfa"]
        )

        self.build_chat(
            self.pages["AI Chat / Copilot"]
        )

        self.build_analytics(
            self.pages["Veri Analizleri"]
        )

        self.build_anomalies(
            self.pages["Anomali Tespiti"]
        )

        self.build_rag(
            self.pages["RAG Doküman Arama"]
        )

        self.build_reports(
            self.pages["Raporlar"]
        )

        self.build_settings(
            self.pages["Ayarlar"]
        )

    def show_page(self, name):

        self.pages[name].tkraise()

        self.active_page = name

        for page_name, btn in self.menu_buttons.items():

            btn.configure(
                bg=NAVY_2
                if page_name == name
                else NAVY
            )

    # ========================================================
    # ANA SAYFA
    # ========================================================

    def build_home(self, page):

        self.page_title(
            page,
            "Hoş Geldiniz, Hüseyin Bey",
            "Finansal verilerinizi analiz edin, sorunları önceden görün ve daha iyi kararlar alın."
        )

        stats = tk.Frame(
            page,
            bg=BG
        )

        stats.pack(
            fill="x",
            padx=14
        )

        data = self.dashboard_data

        total_income = data["total_income"]
        total_expense = data["total_expense"]
        net_profit = data["net_profit"]

        if total_income > 0:
            profit_margin = (net_profit / total_income) * 100
        else:
            profit_margin = 0

        self.add_stat_card(
            stats,
            "Toplam Gelir",
            f"₺ {total_income:,.2f}",
            "MSSQL verisi",
            "↗",
            GREEN
        )

        self.add_stat_card(
            stats,
            "Toplam Gider",
            f"₺ {total_expense:,.2f}",
            "MSSQL verisi",
            "↘",
            RED
        )

        profit_color = GREEN if net_profit >= 0 else RED

        self.add_stat_card(
            stats,
            "Net Kâr / Zarar",
            f"₺ {net_profit:,.2f}",
            "MSSQL verisi",
            "$",
            profit_color
        )

        self.add_stat_card(
            stats,
            "Kâr Marjı",
            f"% {profit_margin:.2f}",
            "Gelire göre",
            "%",
            BLUE
        )

        middle = tk.Frame(
            page,
            bg=BG
        )

        middle.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=5
        )

        middle.grid_columnconfigure(
            0,
            weight=3
        )

        middle.grid_columnconfigure(
            1,
            weight=2
        )

        middle.grid_rowconfigure(
            0,
            weight=1
        )

        chart_card = self.card(
            middle
        )

        chart_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            chart_card,
            "Gelir - Gider - Kâr Trendi",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        self.add_trend_chart(
            chart_card
        )

        quick = self.card(
            middle
        )

        quick.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            quick,
            "Hızlı Erişim",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        buttons = [
            ("▤  Fatura Sorgula", "AI Chat / Copilot"),
            ("●  Cari Hesap Analizi", "Veri Analizleri"),
            ("▣  Stok Analizi", "Veri Analizleri"),
            ("⌕  Doküman Ara", "RAG Doküman Arama"),
            ("▤  Rapor Oluştur", "Raporlar"),
            ("◉  ML Analizleri", "Anomali Tespiti"),
        ]

        for text, target in buttons:

            b = tk.Button(
                quick,
                text=text,
                command=lambda t=target: self.show_page(t),
                bg=NAVY_2,
                fg=WHITE,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                pady=12,
                cursor="hand2"
            )

            b.pack(
                fill="x",
                padx=12,
                pady=4
            )

        bottom = self.card(
            page
        )

        bottom.pack(
            fill="x",
            padx=19,
            pady=5
        )

        self.make_label(
            bottom,
            "Son İşlemler",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=8
        )

        self.add_table(
            bottom,
            ["Tarih", "Açıklama", "Tutar", "Durum"],
            [
                [
                    "30.09.2025",
                    "Satış Faturası (F-0025-1045)",
                    "₺ 125.000",
                    "✓"
                ],
                [
                    "29.09.2025",
                    "Tedarikçi Ödemesi (T-2025-0876)",
                    "₺ 78.450",
                    "✓"
                ],
                [
                    "26.09.2025",
                    "Personel Maaşları",
                    "₺ 92.320",
                    "✓"
                ],
            ],
            height=4
        )

    # ========================================================
    # CHAT
    # ========================================================

    def build_chat(self, page):

        self.page_title(
            page,
            "AI Chat / Copilot",
            "Doğal dil ile sorular sorun, finansal verilerinizden anında yanıt alın."
        )

        panel = self.card(
            page
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=5
        )

        user = tk.Frame(
            panel,
            bg="#dcecff"
        )

        user.pack(
            anchor="e",
            padx=18,
            pady=15
        )

        self.make_label(
            user,
            "👤  Geçen ay neden kârımız düştü?",
            10,
            TEXT,
            True,
            "#dcecff"
        ).pack(
            padx=14,
            pady=10
        )

        answer = tk.Frame(
            panel,
            bg="#f7faff",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        answer.pack(
            fill="x",
            padx=18,
            pady=5
        )

        self.make_label(
            answer,
            "◉",
            23,
            BLUE,
            True,
            "#f7faff"
        ).pack(
            side="left",
            padx=12,
            pady=15,
            anchor="n"
        )

        body = tk.Frame(
            answer,
            bg="#f7faff"
        )

        body.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=15
        )

        self.make_label(
            body,
            "Geçen aya göre kârımızın düşmesinin temel nedenleri:",
            10,
            TEXT,
            True,
            "#f7faff"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        for text in [
            "1. Satışlar: Satışlar %8 artmış olsa da brüt kâr marjı %3,2 azalmıştır.",
            "2. Maliyetler: X ürün grubunun maliyet oranı %14 yükselmiştir.",
            "3. Giderler: Pazarlama ve genel yönetim giderleri %6 artmıştır."
        ]:

            self.make_label(
                body,
                text,
                10,
                TEXT,
                False,
                "#f7faff"
            ).pack(
                anchor="w",
                pady=4
            )

        result = tk.Frame(
            body,
            bg="#eaf4ff"
        )

        result.pack(
            fill="x",
            pady=10
        )

        self.make_label(
            result,
            "◈  Sonuç",
            10,
            BLUE,
            True,
            "#eaf4ff"
        ).pack(
            anchor="w",
            padx=10,
            pady=(8, 3)
        )

        self.make_label(
            result,
            "Maliyet oranındaki yükseliş ve artan giderler nedeniyle kâr %12,4 düşmüştür.",
            10,
            TEXT,
            False,
            "#eaf4ff"
        ).pack(
            anchor="w",
            padx=10,
            pady=(0, 8)
        )

        input_frame = tk.Frame(
            panel,
            bg="#f9fbff",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        input_frame.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=18
        )

        entry = tk.Entry(
            input_frame,
            bd=0,
            bg="#f9fbff",
            font=("Segoe UI", 10)
        )

        entry.insert(
            0,
            "Sorunuzu yazın..."
        )

        entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=13,
            padx=12
        )

        self.make_action_button(
            input_frame,
            "➤",
            lambda: messagebox.showinfo(
                "Demo",
                "AI yanıtı burada gösterilecek."
            )
        ).pack(
            side="right",
            padx=6,
            pady=5
        )

    # ========================================================
    # VERI ANALIZLERI
    # ========================================================

    def build_analytics(self, page):

        self.page_title(
            page,
            "Veri Analizleri",
            "Finansal verilerinizi analiz edin ve önemli göstergeleri takip edin."
        )

        # =========================
        # İSTATİSTİK KARTLARI
        # =========================

        stats = tk.Frame(
            page,
            bg=BG
        )

        stats.pack(
            fill="x",
            padx=14,
            pady=5
        )

        stats.grid_columnconfigure(0, weight=1)
        stats.grid_columnconfigure(1, weight=1)
        stats.grid_columnconfigure(2, weight=1)
        stats.grid_columnconfigure(3, weight=1)

        data = self.dashboard_data

        total_income = data["total_income"]
        total_expense = data["total_expense"]
        net_profit = data["net_profit"]

        if total_income > 0:
            profit_margin = (net_profit / total_income) * 100
        else:
            profit_margin = 0

        self.add_stat_card(
            stats,
            "Toplam Gelir",
            f"₺ {total_income:,.2f}",
            "MSSQL verisi",
            "↗",
            GREEN
        )

        self.add_stat_card(
            stats,
            "Toplam Gider",
            f"₺ {total_expense:,.2f}",
            "MSSQL verisi",
            "↘",
            RED
        )

        self.add_stat_card(
            stats,
            "Net Kâr / Zarar",
            f"₺ {net_profit:,.2f}",
            "MSSQL verisi",
            "$",
            GREEN if net_profit >= 0 else RED
        )

        self.add_stat_card(
            stats,
            "Kâr Marjı",
            f"% {profit_margin:.2f}",
            "Gelire göre",
            "%",
            BLUE
        )

        # =========================
        # ALT BÖLÜM
        # =========================

        content = tk.Frame(
            page,
            bg=BG
        )

        content.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=5
        )

        content.grid_columnconfigure(
            0,
            weight=3
        )

        content.grid_columnconfigure(
            1,
            weight=2
        )

        content.grid_rowconfigure(
            0,
            weight=1
        )

        # =========================
        # GRAFİK
        # =========================

        chart_card = self.card(
            content
        )

        chart_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            chart_card,
            "Gider Kategorileri",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        self.add_trend_chart(
            chart_card
        )

        # =========================
        # GİDER TABLOSU
        # =========================

        table_card = self.card(
            content
        )

        table_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            table_card,
            "Gider Dağılımı",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        expenses = self.dashboard_data.get(
            "top_expenses",
            []
        )

        total_expense = self.dashboard_data.get(
            "total_expense",
            0
        )

        expense_rows = []

        for item in expenses:

            amount = item["amount"]

            if total_expense > 0:
                share = (amount / total_expense) * 100
            else:
                share = 0

            expense_rows.append(
                [
                    item["category"],
                    f"₺ {amount:,.2f}",
                    f"%{share:.2f}"
                ]
            )

        self.add_table(
            table_card,
            ["Kategori", "Tutar", "Pay"],
            expense_rows,
            height=8
        )

    # ========================================================
    # ANOMALI
    # ========================================================

    def build_anomalies(self, page):

        self.page_title(
            page,
            "Anomali Tespiti",
            "MSSQL verilerinizde olağandışı durumları tespit edin."
        )

        stats = tk.Frame(
            page,
            bg=BG
        )

        stats.pack(
            fill="x",
            padx=14
        )

        self.add_stat_card(
            stats,
            "Tespit Edilen Anomali",
            "7",
            "Toplam kayıt",
            "!",
            RED
        )

        self.add_stat_card(
            stats,
            "Yüksek Risk",
            "3",
            "İncelenmesi gerekli",
            "!",
            ORANGE
        )

        self.add_stat_card(
            stats,
            "Düşük Risk",
            "4",
            "Kontrol altında",
            "✓",
            GREEN
        )

        panel = self.card(page)

        panel.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=10
        )

        self.make_label(
            panel,
            "Anomali Listesi",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        self.add_table(
            panel,
            [
                "Tarih",
                "Tip",
                "Açıklama",
                "Risk",
                "Durum"
            ],
            [
                [
                    "18.09.2025",
                    "Fatura",
                    "Tedarikçi faturası beklenenden yüksek",
                    "Yüksek",
                    "İnceleniyor"
                ],
                [
                    "16.09.2025",
                    "Stok",
                    "Stok hareketlerinde olağandışı değişim",
                    "Orta",
                    "Açık"
                ],
                [
                    "12.09.2025",
                    "Cari",
                    "Cari hesapta şüpheli işlem",
                    "Yüksek",
                    "İnceleniyor"
                ],
                [
                    "08.09.2025",
                    "Gider",
                    "Pazarlama giderlerinde ani artış",
                    "Orta",
                    "Kapalı"
                ],
                [
                    "04.09.2025",
                    "Fatura",
                    "Fatura tutarı ortalamanın üzerinde",
                    "Düşük",
                    "Kapalı"
                ],
            ],
            height=8
        )

        detail = tk.Frame(
            panel,
            bg="#fff1f1",
            highlightbackground="#ffcaca",
            highlightthickness=1
        )

        detail.pack(
            fill="x",
            padx=12,
            pady=12
        )

        self.make_label(
            detail,
            "⚠ Seçili Anomali Detayı",
            11,
            RED,
            True,
            "#fff1f1"
        ).pack(
            anchor="w",
            padx=12,
            pady=8
        )

        self.make_label(
            detail,
            "Tedarikçi faturası beklenenden yüksek. Tutar: ₺432.700 | Sapma: %45,4",
            10,
            TEXT,
            False,
            "#fff1f1"
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )

    # ========================================================
    # RAG
    # ========================================================

    def build_rag(self, page):

        self.page_title(
            page,
            "RAG Doküman Arama",
            "Şirket dokümanlarında arama yapın ve ilgili bilgileri bulun."
        )

        search = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        search.pack(
            fill="x",
            padx=18,
            pady=5
        )

        entry = tk.Entry(
            search,
            bd=0,
            font=("Segoe UI", 10)
        )

        entry.insert(
            0,
            "Dokümanlarda ara... Örn: satın alma prosedürü"
        )

        entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=12,
            ipady=12
        )

        self.make_action_button(
            search,
            "⌕ Ara",
            lambda: messagebox.showinfo(
                "RAG Demo",
                "Doküman arama burada yapılacak."
            )
        ).pack(
            side="right",
            padx=6,
            pady=5
        )

        body = tk.Frame(
            page,
            bg=BG
        )

        body.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=5
        )

        body.grid_columnconfigure(
            0,
            weight=1
        )

        body.grid_columnconfigure(
            1,
            weight=2
        )

        body.grid_rowconfigure(
            0,
            weight=1
        )

        docs = self.card(body)

        docs.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            docs,
            "Dokümanlar",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        for item in [
            "Satın Alma Prosedürü.pdf",
            "Tedarikçi Sözleşmesi.docx",
            "Muhasebe Prosedürü.pdf",
            "Finans Politikaları.docx",
            "İnsan Kaynakları.pdf",
        ]:

            tk.Button(
                docs,
                text="▣  " + item,
                anchor="w",
                bg=WHITE,
                fg=TEXT,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9),
                padx=12,
                pady=9
            ).pack(
                fill="x",
                padx=8,
                pady=2
            )

        preview = self.card(body)

        preview.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            preview,
            "Doküman Önizleme",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=12,
            pady=10
        )

        text = tk.Text(
            preview,
            wrap="word",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10),
            bd=0
        )

        text.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        text.insert(
            "1.0",
            "SATIN ALMA PROSEDÜRÜ\n\n"
            "1. Amaç\n"
            "Bu prosedür, şirketin satın alma süreçlerinde standartları "
            "sağlamak ve maliyetleri kontrol altında tutmak amacıyla hazırlanmıştır.\n\n"
            "2. Kapsam\n"
            "Tüm satın alma işlemlerini, tedarikçi seçimlerini ve sözleşme "
            "yönetimini kapsar.\n\n"
            "3. Onay Süreci\n"
            "Satın alma talepleri ilgili birim yöneticisi tarafından onaylanır."
        )

        text.configure(
            state="disabled"
        )

    # ========================================================
    # RAPORLAR
    # ========================================================

    def build_reports(self, page):

        self.page_title(
            page,
            "Raporlar",
            "Hazır raporları görüntüleyin veya yeni raporlar oluşturun."
        )

        top = tk.Frame(
            page,
            bg=BG
        )

        top.pack(
            fill="x",
            padx=18,
            pady=5
        )

        self.make_action_button(
            top,
            "+ Yeni Rapor Oluştur",
            lambda: messagebox.showinfo(
                "Demo",
                "Rapor oluşturma ekranı açılacak."
            )
        ).pack(
            side="right"
        )

        grid = tk.Frame(
            page,
            bg=BG
        )

        grid.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=5
        )

        for i in range(3):

            grid.grid_columnconfigure(
                i,
                weight=1
            )

        for i in range(3):

            grid.grid_rowconfigure(
                i,
                weight=1
            )

        reports = [
            ("◉", "Aylık Finansal Rapor", "Gelir, gider, kâr detayları"),
            ("▣", "Nakit Akış Raporu", "Nakit giriş ve çıkışları"),
            ("◉", "Stok Raporu", "Stok durumu ve hareketleri"),
            ("!", "Cari Hesap Raporu", "Müşteri ve tedarikçi bakiyeleri"),
            ("!", "Anomali Raporu", "Tespit edilen anormallikler"),
            ("▤", "Maliyet Analiz Raporu", "Gider kategorileri analizi"),
            ("▥", "Satış Analizi", "Ürün grubu bazında satışlar"),
            ("▣", "Bütçe Karşılaştırma", "Gerçekleşen ve planlanan bütçe"),
            ("▤", "Özet Yönetici Raporu", "Yönetici için özet rapor"),
        ]

        for i, (icon, title, desc) in enumerate(reports):

            r, c = divmod(i, 3)

            frame = self.card(
                grid
            )

            frame.grid(
                row=r,
                column=c,
                sticky="nsew",
                padx=5,
                pady=5
            )

            self.make_label(
                frame,
                icon,
                24,
                BLUE,
                True
            ).pack(
                anchor="w",
                padx=15,
                pady=(15, 3)
            )

            self.make_label(
                frame,
                title,
                11,
                TEXT,
                True
            ).pack(
                anchor="w",
                padx=15
            )

            self.make_label(
                frame,
                desc,
                9,
                MUTED,
                False
            ).pack(
                anchor="w",
                padx=15,
                pady=5
            )

            tk.Button(
                frame,
                text="Raporu Aç",
                bg=LIGHT_BLUE,
                fg=BLUE,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                command=lambda t=title: messagebox.showinfo(
                    "Rapor",
                    t + " açılacak."
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=10
            )

    # ========================================================
    # AYARLAR
    # ========================================================

    def build_settings(self, page):

        self.page_title(
            page,
            "Ayarlar",
            "Kârnex AI uygulamasının bağlantı ve görünüm ayarlarını yönetin."
        )

        body = tk.Frame(
            page,
            bg=BG
        )

        body.pack(
            fill="both",
            expand=True,
            padx=18
        )

        body.grid_columnconfigure(
            0,
            weight=1
        )

        body.grid_columnconfigure(
            1,
            weight=1
        )

        general = self.card(body)

        general.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            general,
            "Genel Ayarlar",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=12
        )

        self.make_label(
            general,
            "Uygulama Dili",
            9,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=(8, 2)
        )

        ttk.Combobox(
            general,
            values=["Türkçe", "English"],
            state="readonly"
        ).pack(
            fill="x",
            padx=15
        )

        self.make_label(
            general,
            "Tema",
            9,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        ttk.Combobox(
            general,
            values=["Açık", "Koyu"],
            state="readonly"
        ).pack(
            fill="x",
            padx=15
        )

        self.make_label(
            general,
            "Açılış Sayfası",
            9,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        ttk.Combobox(
            general,
            values=[
                "Ana Sayfa",
                "AI Chat / Copilot"
            ],
            state="readonly"
        ).pack(
            fill="x",
            padx=15
        )

        self.make_action_button(
            general,
            "Ayarları Kaydet",
            lambda: messagebox.showinfo(
                "Ayarlar",
                "Ayarlar kaydedildi."
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=20
        )

        db = self.card(body)

        db.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.make_label(
            db,
            "Veritabanı Ayarları",
            12,
            TEXT,
            True
        ).pack(
            anchor="w",
            padx=15,
            pady=12
        )

        fields = [
            ("Sunucu Adı", "localhost"),
            ("Veritabanı", "KARNEXDB"),
            ("Kullanıcı", "sa"),
            ("Şifre", "********"),
        ]

        for title, value in fields:

            self.make_label(
                db,
                title,
                9,
                TEXT,
                True
            ).pack(
                anchor="w",
                padx=15,
                pady=(8, 2)
            )

            entry = tk.Entry(
                db,
                font=("Segoe UI", 10),
                bd=1,
                relief="solid"
            )

            entry.insert(
                0,
                value
            )

            entry.pack(
                fill="x",
                padx=15
            )

        self.make_action_button(
            db,
            "Bağlantıyı Test Et",
            lambda: messagebox.showinfo(
                "MSSQL",
                "Demo bağlantı başarılı."
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=20
        )

    # ========================================================
    # GRAFIK
    # ========================================================

    def add_trend_chart(self, parent):

        fig = Figure(
            figsize=(7, 3),
            dpi=90
        )

        ax = fig.add_subplot(111)

        expenses = self.dashboard_data.get(
            "top_expenses",
            []
        )

        categories = [
            item["category"]
            for item in expenses
        ]

        amounts = [
            item["amount"]
            for item in expenses
        ]

        if not categories:
            ax.text(
                0.5,
                0.5,
                "Gider verisi bulunamadı",
                ha="center",
                va="center"
            )

            ax.set_axis_off()

        else:
            x = list(range(len(categories)))

            bars = ax.bar(
                x,
                amounts,
                width=0.55
            )

            ax.set_xticks(x)
            ax.set_xticklabels(
                categories,
                rotation=25,
                ha="right"
            )

            ax.set_ylabel("Tutar (₺)")

            ax.grid(
                axis="y",
                alpha=0.2
            )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            for bar, amount in zip(bars, amounts):

                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"₺ {amount:,.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(
            fig,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

    # ========================================================
    # TABLO
    # ========================================================

    def add_table(
        self,
        parent,
        columns,
        rows,
        height=5
    ):

        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=height
        )

        for col in columns:

            tree.heading(
                col,
                text=col
            )

            tree.column(
                col,
                width=150,
                anchor="w"
            )

        for row in rows:

            tree.insert(
                "",
                "end",
                values=row
            )

        tree.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        return tree


# ============================================================
# PROGRAMI BASLAT
# ============================================================

if __name__ == "__main__":

    app = KarnexApp()

    app.mainloop()

