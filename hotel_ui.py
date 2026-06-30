import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading

from scrap import CrawlerHotel  # adjust import path to match your project structure


class HotelSearchApp(tk.Tk):
    """Desktop UI for searching hotels via CrawlerHotel."""

    def __init__(self):
        super().__init__()
        self.title("Hotel Search")
        self.geometry("900x500")

        self.crawler = CrawlerHotel()
        self._build_widgets()

    # ---------------- UI BUILDING ----------------
    def _build_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        self.search_button = ttk.Button(
            top_frame, text="Search Hotels", command=self.start_search
        )
        self.search_button.pack(side="left")

        self.status_label = ttk.Label(top_frame, text="Idle")
        self.status_label.pack(side="left", padx=10)

        columns = (
            "provider_name",
            "destination",
            "persian_title",
            "english_title",
            "address",
            "hotel_ranking",
            "adult_price",
        )
        headers = {
            "provider_name": "Provider",
            "destination": "Destination",
            "persian_title": "Hotel (FA)",
            "english_title": "Hotel (EN)",
            "address": "Address",
            "hotel_ranking": "Ranking",
            "adult_price": "Price",
        }

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=120, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.place(in_=self.tree, relx=1.0, rely=0, relheight=1.0, anchor="ne")

    # ---------------- ACTIONS ----------------
    def start_search(self):
        """Disable button, update status, and kick off the crawl in a background thread."""
        self.search_button.config(state="disabled")
        self.status_label.config(text="Searching...")
        self.tree.delete(*self.tree.get_children())

        thread = threading.Thread(target=self._run_crawler_thread, daemon=True)
        thread.start()

    def _run_crawler_thread(self):
        """Runs in a background thread: creates its own event loop and runs the async crawler."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            hotels = loop.run_until_complete(self.crawler.crawler())
        except Exception as e:
            hotels = None
            error = str(e)
        else:
            error = None
        finally:
            loop.close()

        # Hand results back to the Tkinter main thread safely
        self.after(0, self._on_crawler_done, hotels, error)

    def _on_crawler_done(self, hotels, error):
        self.search_button.config(state="normal")

        if error:
            self.status_label.config(text="Error")
            messagebox.showerror("Crawler Error", error)
            return

        if not hotels:
            self.status_label.config(text="No results")
            return

        for hotel in hotels:
            self.tree.insert(
                "",
                "end",
                values=(
                    hotel.get("provider_name", ""),
                    hotel.get("destination", ""),
                    hotel.get("persian_title", ""),
                    hotel.get("english_title", ""),
                    hotel.get("address", ""),
                    hotel.get("hotel_ranking", ""),
                    hotel.get("adult_price", ""),
                ),
            )

        self.status_label.config(text=f"Found {len(hotels)} hotels")


if __name__ == "__main__":
    app = HotelSearchApp()
    app.mainloop()