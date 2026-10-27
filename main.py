import tkinter as tk
from tkinter import messagebox
import math
import random

# Canlı & Modern Renk Paleti
PALETTE = [
    "#FF3366", "#33CC66", "#3399FF", "#FF9900", "#9933FF",
    "#00D2D3", "#FF6B6B", "#48DBFB", "#1DD1A1", "#FECA57",
    "#5F27CD", "#FF9FF3", "#54A0FF", "#10AC84", "#EE5253"
]

class Particle:
    """Fişek / Konfeti Parçacığı"""
    def __init__(self, x, y):
        self.x, self.y = x, y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 10)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - random.uniform(2, 4)
        self.color = random.choice(PALETTE)
        self.size = random.randint(5, 9)
        self.life = random.randint(35, 50)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.35  # Yerçekimi
        self.life -= 1

class CleanWheelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Canlı Çarkıfelek")
        self.root.geometry("890x630")
        self.root.configure(bg="#F8F9FA")
        self.root.resizable(False, False)

        # Temel Durum Verileri
        self.items = ["Hedef 1", "Sürpriz", "Büyük Ödül", "Şanslı Gün", "Pas"]
        self.max_items = 50
        self.cx, self.cy, self.radius = 265, 265, 210

        self.angle = 0.0
        self.speed = 0.0
        self.is_spinning = False
        self.particles = []

        self._init_ui()
        self.draw_wheel()

    def _init_ui(self):
        # Sol Panel (Canvas + Çevir Butonu)
        left = tk.Frame(self.root, bg="#F8F9FA")
        left.pack(side="left", padx=(20, 10), pady=20)

        self.canvas = tk.Canvas(left, width=530, height=530, bg="#FFFFFF", 
                                highlightthickness=1, highlightbackground="#E2E8F0")
        self.canvas.pack()

        ctl = tk.Frame(left, bg="#F8F9FA")
        ctl.pack(fill="x", pady=(12, 0))

        self.btn_spin = tk.Button(
            ctl, text="✨ ÇARKINI ÇEVİR! ✨", font=("Segoe UI", 12, "bold"),
            bg="#10AC84", fg="white", activebackground="#1DD1A1", activeforeground="white",
            relief="flat", padx=20, pady=8, cursor="hand2", command=self.start_spin
        )
        self.btn_spin.pack(side="left")

        self.lbl_status = tk.Label(ctl, text="Seçenekleri gir ve çevir!", font=("Segoe UI", 11, "bold"),
                                   bg="#F8F9FA", fg="#636E72")
        self.lbl_status.pack(side="right", padx=10)

        # Sağ Panel (Seçenekler & Liste Yönetimi)
        right = tk.Frame(self.root, bg="#FFFFFF", padx=15, pady=15, 
                         highlightthickness=1, highlightbackground="#E2E8F0")
        right.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

        header = tk.Frame(right, bg="#FFFFFF")
        header.pack(fill="x", pady=(0, 10))

        tk.Label(header, text="Çark Seçenekleri", font=("Segoe UI", 12, "bold"),
                 bg="#FFFFFF", fg="#2D3436").pack(side="left")
        self.lbl_count = tk.Label(header, font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#0984E3")
        self.lbl_count.pack(side="right")

        # Girdi Kutusu & Ekleme Butonu
        box = tk.Frame(right, bg="#FFFFFF")
        box.pack(fill="x", pady=5)

        self.entry = tk.Entry(box, font=("Segoe UI", 11), bg="#F1F2F6", fg="#2D3436", 
                              relief="flat", highlightthickness=1, highlightbackground="#DFE4EA")
        self.entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        self.entry.bind("<Return>", lambda _: self.add_item())

        tk.Button(box, text="Ekle", font=("Segoe UI", 10, "bold"), bg="#0984E3", fg="white",
                  relief="flat", padx=14, pady=5, cursor="hand2", command=self.add_item).pack(side="right")

        # Liste Kutusu
        list_frame = tk.Frame(right, bg="#FFFFFF")
        list_frame.pack(fill="both", expand=True, pady=10)

        self.listbox = tk.Listbox(list_frame, font=("Segoe UI", 10), bg="#F8F9FA", fg="#2D3436",
                                  selectbackground="#74B9FF", relief="flat", highlightthickness=1,
                                  highlightbackground="#DFE4EA")
        self.listbox.pack(side="left", fill="both", expand=True)

        sc = tk.Scrollbar(list_frame, command=self.listbox.yview)
        sc.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=sc.set)

        # Silme & Temizleme Butonları
        btn_bar = tk.Frame(right, bg="#FFFFFF")
        btn_bar.pack(fill="x", pady=(4, 0))

        tk.Button(btn_bar, text="Seçileni Sil", font=("Segoe UI", 9, "bold"), bg="#FF7675",
                  fg="white", relief="flat", pady=6, cursor="hand2", command=self.delete_item
                  ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        tk.Button(btn_bar, text="Tümünü Temizle", font=("Segoe UI", 9, "bold"), bg="#B2BEC3",
                  fg="white", relief="flat", pady=6, cursor="hand2", command=self.clear_items
                  ).pack(side="right", fill="x", expand=True, padx=(4, 0))

        self._refresh_list()

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for i, item in enumerate(self.items, 1):
            self.listbox.insert(tk.END, f"  {i}. {item}")
        self.lbl_count.config(text=f"({len(self.items)}/{self.max_items})")

    def add_item(self):
        if self.is_spinning: return
        val = self.entry.get().strip()
        if not val: return
        if len(self.items) >= self.max_items:
            messagebox.showwarning("Sınır", f"Maksimum {self.max_items} eleman ekleyebilirsiniz!")
            return
        self.items.append(val)
        self.entry.delete(0, tk.END)
        self._refresh_list()
        self.draw_wheel()

    def delete_item(self):
        if self.is_spinning or not self.listbox.curselection(): return
        self.items.pop(self.listbox.curselection()[0])
        self._refresh_list()
        self.draw_wheel()

    def clear_items(self):
        if self.is_spinning or not self.items: return
        self.items.clear()
        self._refresh_list()
        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.delete("wheel")
        n = len(self.items)
        if n == 0:
            self.canvas.create_text(self.cx, self.cy, text="Seçenek ekleyin", fill="#B2BEC3",
                                    font=("Segoe UI", 12, "bold"), tags="wheel")
            return

        step = 360 / n
        box = (self.cx - self.radius, self.cy - self.radius, self.cx + self.radius, self.cy + self.radius)

        for i, text in enumerate(self.items):
            start = (self.angle + i * step) % 360
            self.canvas.create_arc(*box, start=start, extent=step, fill=PALETTE[i % len(PALETTE)],
                                   outline="white", width=2, tags="wheel")

            # Metin Yerleşimi
            mid = math.radians(start + step / 2)
            tx = self.cx + (self.radius * 0.65) * math.cos(mid)
            ty = self.cy - (self.radius * 0.65) * math.sin(mid)
            size = 11 if n <= 12 else (9 if n <= 25 else 7)
            t = text if (n <= 25 or len(text) <= 9) else (text[:8] + "..")
            self.canvas.create_text(tx, ty, text=t, fill="white", font=("Segoe UI", size, "bold"), tags="wheel")

        # Merkez ve Sağ İbre
        self.canvas.create_oval(self.cx - 16, self.cy - 16, self.cx + 16, self.cy + 16,
                                fill="white", outline="#DFE4EA", width=3, tags="wheel")
        self.canvas.create_oval(self.cx - 6, self.cy - 6, self.cx + 6, self.cy + 6,
                                fill="#FF3366", outline="", tags="wheel")

        tip_x = self.cx + self.radius + 2
        self.canvas.create_polygon(tip_x, self.cy, tip_x + 22, self.cy - 13, tip_x + 22, self.cy + 13,
                                   fill="#FF3366", outline="white", width=2, tags="wheel")

    def start_spin(self):
        if self.is_spinning or not self.items: return
        self.canvas.delete("celebration")
        self.particles.clear()
        self.is_spinning = True
        self.btn_spin.config(state="disabled", bg="#B2BEC3")
        self.lbl_status.config(text="Dönüyor...", fg="#0984E3")
        self.speed = random.uniform(25.0, 38.0)
        self._animate()

    def _animate(self):
        if self.speed > 0.15:
            self.angle = (self.angle + self.speed) % 360
            self.speed *= 0.983  # Sürtünme / Yavaşlama
            self.draw_wheel()
            self.root.after(16, self._animate)
        else:
            self.is_spinning = False
            self.btn_spin.config(state="normal", bg="#10AC84")
            self._finish_spin()

    def _finish_spin(self):
        step = 360 / len(self.items)
        idx = int(((360 - (self.angle % 360)) % 360) // step)
        winner = self.items[idx]

        self.lbl_status.config(text=f"Kazanan: {winner}", fg="#10AC84")
        self.particles = [Particle(self.cx, self.cy) for _ in range(100)]
        self._run_celebration(winner)

    def _run_celebration(self, winner):
        self.canvas.delete("celebration")
        
        # Parçacık güncelleme
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()
            self.canvas.create_oval(p.x - p.size/2, p.y - p.size/2, p.x + p.size/2, p.y + p.size/2,
                                    fill=p.color, outline="", tags="celebration")

        # Tebrik Kartı
        cw, ch = 300, 100
        self.canvas.create_rectangle(self.cx - cw//2 + 3, self.cy - ch//2 + 3, self.cx + cw//2 + 3, self.cy + ch//2 + 3,
                                     fill="#DFE4EA", outline="", tags="celebration")
        self.canvas.create_rectangle(self.cx - cw//2, self.cy - ch//2, self.cx + cw//2, self.cy + ch//2,
                                     fill="white", outline="#10AC84", width=3, tags="celebration")

        self.canvas.create_text(self.cx, self.cy - 20, text="🎉 TEBRİKLER! 🎉", fill="#FF3366",
                                font=("Segoe UI", 12, "bold"), tags="celebration")
        txt = winner if len(winner) <= 16 else winner[:14] + "..."
        self.canvas.create_text(self.cx, self.cy + 15, text=txt, fill="#2D3436",
                                font=("Segoe UI", 15, "bold"), tags="celebration")

        if self.particles:
            self.root.after(20, lambda: self._run_celebration(winner))

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanWheelApp(root)
    root.mainloop()