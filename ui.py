import tkinter as tk
from tkinter import ttk, messagebox


# ═══════════════════════════════════════════════════════════════════════════════
#  🔌 PLUG YOUR CODE HERE — replace every function marked with  ← YOUR CODE
# ═══════════════════════════════════════════════════════════════════════════════

def search_tickets(origin: str, destination: str, date: str, passengers: int) -> list[dict]:
    """
    ← YOUR CODE: call your ticket-finding logic here.

    Must return a list of dicts, each with these keys:
      {
        "id":        str,   # unique ticket ID
        "name":      str,   # carrier / train / bus name
        "dep_time":  str,   # departure  e.g. "08:30"
        "arr_time":  str,   # arrival    e.g. "14:15"
        "duration":  str,   # e.g. "5:45"
        "transport": str,   # e.g. "Train" / "Bus" / "Flight"
        "price":     int,   # price per person
        "seats":     int,   # available seats
      }
    """
    # ── REMOVE this stub and plug your real function ──────────────────────────
    return []


def buy_ticket(ticket: dict, origin: str, destination: str,
               date: str, passengers: int) -> dict:
    """
    ← YOUR CODE: handle the purchase when user clicks 'Buy Ticket'.

    Return a dict:
      { "success": bool, "message": str, "booking_code": str }
    """
    # ── REMOVE this stub and plug your real function ──────────────────────────
    return {"success": False, "message": "Not connected yet", "booking_code": ""}


def get_cities() -> list[str]:
    """
    ← YOUR CODE (optional): return list of city names for the dropdowns.
    Default list is used if you leave this as-is.
    """
    return [
        "Tehran", "Mashhad", "Isfahan", "Shiraz", "Tabriz",
        "Ahvaz", "Kermanshah", "Rasht", "Kerman", "Yazd",
        "Bandar Abbas", "Urmia", "Zahedan", "Arak", "Hamadan",
    ]


# ═══════════════════════════════════════════════════════════════════════════════
#  UI — no need to edit below unless you want to change layout / style
# ═══════════════════════════════════════════════════════════════════════════════

# ── Palette ────────────────────────────────────────────────────────────────────
C = {
    "bg": "#0F1117",
    "card": "#1A1D27",
    "input": "#252836",
    "border": "#2E3347",
    "blue": "#4A7CFF",
    "blue_dim": "#3A64D8",
    "green": "#3DD68C",
    "red": "#FF5F5F",
    "gold": "#FFD166",
    "text": "#EAEDF3",
    "muted": "#7C839A",
    "hdr": "#0A0C13",
}

FONT_BOLD = ("Tahoma", 11, "bold")
FONT_NORM = ("Tahoma", 10)
FONT_SMALL = ("Tahoma", 9)
FONT_MONO = ("Courier New", 14, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ticket Seller")
        self.geometry("1120x740")
        self.minsize(860, 580)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        self._cities = get_cities()
        self._results: list[dict] = []

        self._style()
        self._header()
        self._search_bar()
        self._results_area()

    # ── TTK styles ─────────────────────────────────────────────────────────────
    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        for name, bg in [("Dark.TFrame", C["bg"]), ("Card.TFrame", C["card"])]:
            s.configure(name, background=bg)
        s.configure("Dark.TCombobox",
                    fieldbackground=C["input"], background=C["input"],
                    foreground=C["text"], selectbackground=C["blue"],
                    bordercolor=C["border"], lightcolor=C["border"],
                    darkcolor=C["border"], arrowcolor=C["muted"])
        s.configure("TScrollbar",
                    background=C["card"], troughcolor=C["bg"],
                    bordercolor=C["bg"], arrowcolor=C["muted"])

    # ── Header ─────────────────────────────────────────────────────────────────
    def _header(self):
        h = tk.Frame(self, bg=C["hdr"], height=52)
        h.pack(fill="x")
        h.pack_propagate(False)
        tk.Label(h, text="🎫  Ticket Seller", bg=C["hdr"], fg=C["blue"],
                 font=("Courier New", 14, "bold")).pack(side="left", padx=20)
        tk.Label(h, text="Online Ticket Sales", bg=C["hdr"], fg=C["muted"],
                 font=FONT_SMALL).pack(side="left", padx=4)

    # ── Search bar ─────────────────────────────────────────────────────────────
    def _search_bar(self):
        wrap = tk.Frame(self, bg=C["bg"])
        wrap.pack(fill="x", padx=28, pady=18)

        panel = tk.Frame(wrap, bg=C["card"],
                         highlightthickness=1, highlightbackground=C["border"])
        panel.pack(fill="x")

        row = tk.Frame(panel, bg=C["card"], padx=18, pady=16)
        row.pack(fill="x")

        def labeled_combo(parent, label, values, default, width=15):
            f = tk.Frame(parent, bg=C["card"])
            f.pack(side="left", padx=8, expand=True, fill="x")
            tk.Label(f, text=label, bg=C["card"], fg=C["muted"],
                     font=FONT_SMALL).pack(anchor="w")
            cb = ttk.Combobox(f, values=values, style="Dark.TCombobox",
                              font=FONT_NORM, state="readonly",
                              width=width, justify="left")
            cb.set(default)
            cb.pack(fill="x", ipady=6)
            return cb

        self.cb_origin = labeled_combo(row, "From", self._cities, self._cities[0])

        # Swap button
        sf = tk.Frame(row, bg=C["card"])
        sf.pack(side="left", padx=2, pady=14)
        sw = tk.Label(sf, text=" ⇄ ", bg=C["input"], fg=C["blue"],
                      font=("Arial", 13, "bold"), padx=8, pady=7, cursor="hand2")
        sw.pack()
        sw.bind("<Button-1>", self._swap)

        self.cb_dest = labeled_combo(row, "To", self._cities,
                                     self._cities[1] if len(self._cities) > 1 else self._cities[0])

        # Date
        from datetime import datetime, timedelta
        today = datetime.now()
        dates = [(today + timedelta(days=i)).strftime("%Y/%m/%d") for i in range(60)]
        self.cb_date = labeled_combo(row, "Date", dates, dates[0], width=13)

        # Passengers
        pf = tk.Frame(row, bg=C["card"])
        pf.pack(side="left", padx=8)
        tk.Label(pf, text="Passengers", bg=C["card"], fg=C["muted"],
                 font=FONT_SMALL).pack(anchor="w")
        self.pax_var = tk.IntVar(value=1)
        tk.Spinbox(pf, from_=1, to=9, textvariable=self.pax_var, width=4,
                   bg=C["input"], fg=C["text"], buttonbackground=C["input"],
                   relief="flat", font=("Tahoma", 12), justify="center",
                   highlightthickness=1, highlightbackground=C["border"]
                   ).pack(ipady=7)

        # Search button
        bf = tk.Frame(row, bg=C["card"])
        bf.pack(side="left", padx=12, pady=12)
        self.search_btn = tk.Label(bf, text="  Search  ", bg=C["blue"],
                                   fg="white", font=FONT_BOLD,
                                   padx=18, pady=10, cursor="hand2")
        self.search_btn.pack()
        self.search_btn.bind("<Button-1>", lambda e: self._search())
        self.search_btn.bind("<Enter>", lambda e: self.search_btn.config(bg=C["blue_dim"]))
        self.search_btn.bind("<Leave>", lambda e: self.search_btn.config(bg=C["blue"]))

    # ── Results area ───────────────────────────────────────────────────────────
    def _results_area(self):
        self.res_wrap = tk.Frame(self, bg=C["bg"])
        self.res_wrap.pack(fill="both", expand=True, padx=28, pady=(0, 18))
        self._show_placeholder("Select origin and destination, then click Search 🔍")

    def _show_placeholder(self, msg):
        for w in self.res_wrap.winfo_children():
            w.destroy()
        tk.Label(self.res_wrap, text=msg, bg=C["bg"], fg=C["muted"],
                 font=("Tahoma", 12)).pack(expand=True)

    # ── Search action ──────────────────────────────────────────────────────────
    def _search(self):
        origin = self.cb_origin.get()
        dest = self.cb_dest.get()
        date = self.cb_date.get()
        pax = self.pax_var.get()

        if origin == dest:
            messagebox.showwarning("Error", "Origin and destination cannot be the same!")
            return

        self._show_placeholder("Searching...")
        self.update_idletasks()

        try:
            tickets = search_tickets(origin, dest, date, pax)
        except Exception as ex:
            self._show_placeholder(f"Search error:\n{ex}")
            return

        self._results = tickets
        self._render_results(origin, dest, date, pax)

    # ── Render result cards ────────────────────────────────────────────────────
    def _render_results(self, origin, dest, date, pax):
        for w in self.res_wrap.winfo_children():
            w.destroy()

        tickets = self._results

        # Status bar
        bar = tk.Frame(self.res_wrap, bg=C["bg"])
        bar.pack(fill="x", pady=(0, 8))
        tk.Label(bar, text=f"{origin}  →  {dest}   |   {date}   |   {pax} passenger(s)",
                 bg=C["bg"], fg=C["text"], font=FONT_BOLD).pack(side="left")
        color = C["green"] if tickets else C["red"]
        tk.Label(bar, text=f"{len(tickets)} result(s)", bg=C["bg"],
                 fg=color, font=FONT_NORM).pack(side="right")

        if not tickets:
            tk.Label(self.res_wrap,
                     text="No tickets found.\nsearch_tickets() returned an empty list.",
                     bg=C["bg"], fg=C["muted"], font=("Tahoma", 11),
                     justify="center").pack(expand=True)
            return

        # Scrollable list
        canvas = tk.Canvas(self.res_wrap, bg=C["bg"], bd=0, highlightthickness=0)
        vsb = ttk.Scrollbar(self.res_wrap, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=C["bg"])
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        for t in tickets:
            self._card(sf, t, origin, dest, date, pax)

    # ── Single ticket card ─────────────────────────────────────────────────────
    def _card(self, parent, t: dict, origin, dest, date, pax):
        card = tk.Frame(parent, bg=C["card"], padx=18, pady=14,
                        highlightthickness=1, highlightbackground=C["border"])
        card.pack(fill="x", pady=4)
        card.bind("<Enter>", lambda e: card.config(highlightbackground=C["blue"]))
        card.bind("<Leave>", lambda e: card.config(highlightbackground=C["border"]))

        row = tk.Frame(card, bg=C["card"])
        row.pack(fill="x")

        # ── Left: transport type + name ───────────────────────────────────────
        info = tk.Frame(row, bg=C["card"])
        info.pack(side="left")
        tk.Label(info, text=t.get("transport", "—"), bg=C["card"],
                 fg=C["text"], font=FONT_BOLD).pack(anchor="w")
        tk.Label(info, text=t.get("name", ""), bg=C["card"],
                 fg=C["muted"], font=FONT_SMALL).pack(anchor="w")

        # ── Center: timeline ──────────────────────────────────────────────────
        timeline = tk.Frame(row, bg=C["card"])
        timeline.pack(side="left", padx=32, expand=True)

        tk.Label(timeline, text=t.get("dep_time", "--:--"), bg=C["card"],
                 fg=C["text"], font=FONT_MONO).pack(side="left")

        mid = tk.Frame(timeline, bg=C["card"])
        mid.pack(side="left", padx=10)
        tk.Label(mid, text=f"⏱ {t.get('duration', '?')}",
                 bg=C["card"], fg=C["muted"], font=FONT_SMALL).pack()
        tk.Frame(mid, bg=C["border"], height=2, width=110).pack(pady=3)
        tk.Label(mid, text=f"{origin} → {dest}",
                 bg=C["card"], fg=C["muted"], font=FONT_SMALL).pack()

        tk.Label(timeline, text=t.get("arr_time", "--:--"), bg=C["card"],
                 fg=C["text"], font=FONT_MONO).pack(side="left")

        # ── Right: price + buy ────────────────────────────────────────────────
        price_area = tk.Frame(row, bg=C["card"])
        price_area.pack(side="right")

        price = t.get("price", 0)
        total = price * pax
        tk.Label(price_area, text=f"${total:,.2f}", bg=C["card"],
                 fg=C["gold"], font=FONT_BOLD).pack(anchor="e")

        seats = t.get("seats", 0)
        seat_color = C["red"] if seats <= 5 else C["green"]
        tk.Label(price_area, text=f"{seats} seat(s) left",
                 bg=C["card"], fg=seat_color, font=FONT_SMALL).pack(anchor="e", pady=2)

        btn = tk.Label(price_area, text="  Buy Ticket  ", bg=C["blue"],
                       fg="white", font=FONT_BOLD, padx=12, pady=6, cursor="hand2")
        btn.pack(anchor="e", pady=(6, 0))
        btn.bind("<Button-1>", lambda e: self._buy(t, origin, dest, date, pax))
        btn.bind("<Enter>", lambda e: btn.config(bg=C["blue_dim"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=C["blue"]))

    # ── Buy action ─────────────────────────────────────────────────────────────
    def _buy(self, t: dict, origin, dest, date, pax):
        price = t.get("price", 0)
        confirm = messagebox.askyesno(
            "Confirm Purchase",
            f"Type:        {t.get('transport', '')}  —  {t.get('name', '')}\n"
            f"Route:       {origin} → {dest}\n"
            f"Date:        {date}\n"
            f"Departs:     {t.get('dep_time', '')}   Arrives: {t.get('arr_time', '')}\n"
            f"Passengers:  {pax}   Total: ${price * pax:,.2f}\n\n"
            "Do you want to continue?"
        )
        if not confirm:
            return

        try:
            result = buy_ticket(t, origin, dest, date, pax)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
            return

        if result.get("success"):
            messagebox.showinfo("Success ✅",
                                f"Ticket booked!\nBooking code: {result.get('booking_code', '')}\n\n{result.get('message', '')}")
        else:
            messagebox.showerror("Failed", result.get("message", "Unknown error"))

    # ── Swap cities ────────────────────────────────────────────────────────────
    def _swap(self, _=None):
        o, d = self.cb_origin.get(), self.cb_dest.get()
        self.cb_origin.set(d)
        self.cb_dest.set(o)


if __name__ == "__main__":
    App().mainloop()


