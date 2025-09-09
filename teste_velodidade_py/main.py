import tkinter as tk
from tkinter import PhotoImage, ttk
import threading
import speedtest
import time
import json
import os
from datetime import datetime
import csv

# Importações para o gráfico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SpeedTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Speed Test")
        master.geometry("700x850")
        master.resizable(False, False)
        
        try:
            icone = PhotoImage(file="speedteste.png") 
            master.iconphoto(True, icone)
        except tk.TclError:
            print("Aviso: Imagem 'speedteste.png' não encontrada. A janela ficará sem ícone.")

        self.bg_color = "#2c2c2c"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#007bff"
        self.text_color = "#ffffff"
        self.button_bg = "#4CAF50"
        self.button_fg = "#ffffff"

        master.configure(bg=self.bg_color)
        
        # Estrutura de rolagem para acomodar todo o conteúdo
        self.main_canvas = tk.Canvas(master, bg=self.bg_color, highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )
        )

        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")
        
        # --- Widgets dentro do frame rolável ---
        self.header_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.header_frame.pack(pady=10)

        self.title_label = tk.Label(self.header_frame, text="Speed Test", 
                                    font=("Segoe UI", 24, "bold"), 
                                    bg=self.bg_color, fg=self.text_color)
        self.title_label.pack()

        self.status_label = tk.Label(self.header_frame, text="Pressione Iniciar para testar", 
                                     font=("Segoe UI", 12, "italic"), 
                                     bg=self.bg_color, fg=self.fg_color)
        self.status_label.pack(pady=5)
        
        self.canvas_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=200, height=200, 
                                bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()
        self.draw_initial_circle()

        self.server_label = tk.Label(self.scrollable_frame, text="Servidor: --",
                                     font=("Segoe UI", 10),
                                     bg=self.bg_color, fg=self.fg_color)
        self.server_label.pack(pady=2)
        
        self.ping_label = tk.Label(self.scrollable_frame, text="Ping: -- ms", 
                                   font=("Segoe UI", 14), 
                                   bg=self.bg_color, fg=self.fg_color)
        self.ping_label.pack(pady=2)

        self.jitter_label = tk.Label(self.scrollable_frame, text="Jitter: -- ms",
                                     font=("Segoe UI", 14),
                                     bg=self.bg_color, fg=self.fg_color)
        self.jitter_label.pack(pady=2)
        
        self.packet_loss_label = tk.Label(self.scrollable_frame, text="Perda de Pacotes: --%",
                                          font=("Segoe UI", 14),
                                          bg=self.bg_color, fg=self.fg_color)
        self.packet_loss_label.pack(pady=2)

        self.download_label = tk.Label(self.scrollable_frame, text="Download: -- Mbps", 
                                       font=("Segoe UI", 14), 
                                       bg=self.bg_color, fg=self.fg_color)
        self.download_label.pack(pady=2)

        self.upload_label = tk.Label(self.scrollable_frame, text="Upload: -- Mbps", 
                                     font=("Segoe UI", 14), 
                                     bg=self.bg_color, fg=self.fg_color)
        self.upload_label.pack(pady=2)
        
        self.avg_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.avg_frame.pack(pady=10)
        self.avg_download_label = tk.Label(self.avg_frame, text="Média Download: -- Mbps",
                                           font=("Segoe UI", 12),
                                           bg=self.bg_color, fg=self.fg_color)
        self.avg_download_label.pack(side=tk.LEFT, padx=10)
        self.avg_upload_label = tk.Label(self.avg_frame, text="Média Upload: -- Mbps",
                                         font=("Segoe UI", 12),
                                         bg=self.bg_color, fg=self.fg_color)
        self.avg_upload_label.pack(side=tk.RIGHT, padx=10)

        self.button_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.button_frame.pack(pady=10)
        
        self.btn_start = tk.Button(self.button_frame, text="Iniciar Teste", 
                                   command=self.run_speed_test,
                                   font=("Segoe UI", 16, "bold"),
                                   bg=self.button_bg, fg=self.button_fg,
                                   activebackground=self.button_bg,
                                   activeforeground=self.button_fg,
                                   relief="flat",
                                   padx=20, pady=10,
                                   cursor="hand2")
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_clear_history = tk.Button(self.button_frame, text="Limpar Histórico", 
                                           command=self.clear_history,
                                           font=("Segoe UI", 10, "bold"),
                                           bg="#ff4f4f", fg=self.button_fg,
                                           activebackground="#ff4f4f",
                                           activeforeground=self.button_fg,
                                           relief="flat",
                                           cursor="hand2")
        self.btn_clear_history.pack(side=tk.LEFT, padx=5)
        
        self.btn_export_csv = tk.Button(self.button_frame, text="Exportar CSV",
                                       command=self.export_to_csv,
                                       font=("Segoe UI", 10, "bold"),
                                       bg="#6A5ACD", fg=self.button_fg,
                                       activebackground="#6A5ACD",
                                       activeforeground=self.button_fg,
                                       relief="flat",
                                       cursor="hand2")
        self.btn_export_csv.pack(side=tk.RIGHT, padx=5)

        # Configuração do estilo para a Treeview
        style = ttk.Style(master)
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=self.bg_color, 
                        foreground=self.fg_color, 
                        fieldbackground=self.bg_color)
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#444444", 
                        foreground=self.text_color)
        
        self.history_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.history_tree = ttk.Treeview(self.history_frame, columns=("ping", "jitter", "packet_loss", "download", "upload", "date"), show="headings")
        self.history_tree.heading("ping", text="Ping (ms)")
        self.history_tree.heading("jitter", text="Jitter (ms)")
        self.history_tree.heading("packet_loss", text="Perda (%)")
        self.history_tree.heading("download", text="Download (Mbps)")
        self.history_tree.heading("upload", text="Upload (Mbps)")
        self.history_tree.heading("date", text="Data/Hora")
        
        self.history_tree.column("ping", width=80, anchor=tk.CENTER)
        self.history_tree.column("jitter", width=80, anchor=tk.CENTER)
        self.history_tree.column("packet_loss", width=80, anchor=tk.CENTER)
        self.history_tree.column("download", width=120, anchor=tk.CENTER)
        self.history_tree.column("upload", width=120, anchor=tk.CENTER)
        self.history_tree.column("date", width=150, anchor=tk.CENTER)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        self.graph_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        self.graph_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 3.5), facecolor=self.bg_color)
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas_graph.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        plt.style.use('dark_background')
        self.ax.set_facecolor(self.bg_color)
        self.ax.tick_params(colors=self.fg_color)
        self.ax.spines['bottom'].set_color(self.fg_color)
        self.ax.spines['left'].set_color(self.fg_color)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_title("Histórico de Velocidade", color=self.text_color)
        self.ax.set_xlabel("Testes", color=self.fg_color)
        self.ax.set_ylabel("Velocidade (Mbps)", color=self.fg_color)
        self.ax.grid(color=self.fg_color, linestyle='--', linewidth=0.5, alpha=0.5)

        self.test_history = []
        self.load_history()
        self.master.after(0, self.status_label.config, {'text': 'Pressione Iniciar para testar'})
        plt.close('all')

    def load_history(self):
        if os.path.exists("test_history.json"):
            with open("test_history.json", "r") as f:
                try:
                    self.test_history = json.load(f)
                    self.update_history_tree()
                    self.update_graph()
                    self.calculate_averages()
                except json.JSONDecodeError:
                    self.test_history = []

    def save_history(self):
        with open("test_history.json", "w") as f:
            json.dump(self.test_history, f, indent=4)
            
    def clear_history(self):
        if os.path.exists("test_history.json"):
            os.remove("test_history.json")
        self.test_history = []
        self.update_history_tree()
        self.update_graph()
        self.calculate_averages()
        self.status_label['text'] = "Histórico Limpo."
        
    def export_to_csv(self):
        if not self.test_history:
            self.status_label['text'] = "Histórico vazio. Nada para exportar."
            return
            
        try:
            with open("speed_test_history.csv", "w", newline='', encoding='utf-8') as csvfile:
                fieldnames = ["ping", "jitter", "packet_loss", "download", "upload", "date", "server_name", "server_country"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for record in self.test_history:
                    row = {
                        "ping": record.get("ping", "--"),
                        "jitter": record.get("jitter", "--"),
                        "packet_loss": record.get("packet_loss", "--"),
                        "download": record.get("download", "--"),
                        "upload": record.get("upload", "--"),
                        "date": record.get("date", "--"),
                        "server_name": record["server"].get("name", "--"),
                        "server_country": record["server"].get("country", "--")
                    }
                    writer.writerow(row)
            self.status_label['text'] = "Histórico exportado para speed_test_history.csv"
        except Exception as e:
            self.status_label['text'] = f"Erro ao exportar: {e}"

    def calculate_averages(self):
        if not self.test_history:
            self.avg_download_label['text'] = "Média Download: -- Mbps"
            self.avg_upload_label['text'] = "Média Upload: -- Mbps"
            return
        
        # Filtra registros incompletos para evitar erros de KeyError
        complete_downloads = [r['download'] for r in self.test_history if 'download' in r and r['download'] is not None]
        complete_uploads = [r['upload'] for r in self.test_history if 'upload' in r and r['upload'] is not None]
        
        avg_download = sum(complete_downloads) / len(complete_downloads) if complete_downloads else 0
        avg_upload = sum(complete_uploads) / len(complete_uploads) if complete_uploads else 0
        
        self.avg_download_label['text'] = f"Média Download: {avg_download:.2f} Mbps"
        self.avg_upload_label['text'] = f"Média Upload: {avg_upload:.2f} Mbps"

    def update_history_tree(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for record in self.test_history:
            jitter = record.get("jitter")
            packet_loss = record.get("packet_loss")
            
            jitter_str = f"{jitter:.2f}" if jitter is not None else "--"
            packet_loss_str = f"{packet_loss:.2f}" if packet_loss is not None else "--"
            
            self.history_tree.insert("", "end", values=(
                f"{record.get('ping', '--'):.2f}",
                jitter_str,
                packet_loss_str,
                f"{record.get('download', '--'):.2f}",
                f"{record.get('upload', '--'):.2f}",
                record.get('date', '--')
            ))

    def update_graph(self):
        self.ax.clear()
        
        # Filtra registros incompletos para evitar erros de KeyError
        downloads = [rec['download'] for rec in self.test_history if 'download' in rec and rec['download'] is not None]
        uploads = [rec['upload'] for rec in self.test_history if 'upload' in rec and rec['upload'] is not None]
        
        if downloads or uploads:
            tests = range(1, len(downloads) + 1)
            
            self.ax.plot(tests, downloads, label="Download", color="#FFD700", marker='o')
            self.ax.plot(tests, uploads, label="Upload", color="#00BFFF", marker='o')
            self.ax.legend(facecolor=self.bg_color, edgecolor=self.fg_color, labelcolor=self.fg_color)
            self.ax.set_xticks(tests)
        
        self.ax.set_title("Histórico de Velocidade", color=self.text_color)
        self.ax.set_xlabel("Testes", color=self.fg_color)
        self.ax.set_ylabel("Velocidade (Mbps)", color=self.fg_color)
        self.ax.grid(color=self.fg_color, linestyle='--', linewidth=0.5, alpha=0.5)
        self.ax.set_facecolor(self.bg_color)
        self.ax.tick_params(colors=self.fg_color)
        self.ax.spines['bottom'].set_color(self.fg_color)
        self.ax.spines['left'].set_color(self.fg_color)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        self.fig.tight_layout()
        self.canvas_graph.draw()

    def draw_initial_circle(self):
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)
        self.canvas.create_text(100, 100, text="PRONTO", font=("Segoe UI", 20, "bold"), fill=self.fg_color)

    def update_canvas_progress(self, progress_type, percentage):
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)
        
        if progress_type == "download":
            color = "#FFD700"
            text = f"Baixando...\n{percentage:.0f}%"
        elif progress_type == "upload":
            color = "#00BFFF"
            text = f"Enviando...\n{percentage:.0f}%"
        else:
            color = self.accent_color
            text = f"Testando...\n{percentage:.0f}%"

        arc_angle = 3.6 * percentage
        self.canvas.create_arc(10, 10, 190, 190, 
                                start=90, extent=-arc_angle,
                                outline=color, style=tk.ARC, width=10)

        self.canvas.create_text(100, 100, text=text, font=("Segoe UI", 16, "bold"), fill=self.text_color, justify="center")
        self.master.update_idletasks()

    def run_speed_test(self):
        self.btn_start['state'] = 'disabled'
        self.status_label['text'] = "Iniciando teste..."
        self.download_label['text'] = "Download: -- Mbps"
        self.upload_label['text'] = "Upload: -- Mbps"
        self.ping_label['text'] = "Ping: -- ms"
        self.jitter_label['text'] = "Jitter: -- ms"
        self.packet_loss_label['text'] = "Perda de Pacotes: --%"
        self.server_label['text'] = "Servidor: --"
        self.draw_initial_circle()

        threading.Thread(target=self.perform_test).start()

    def perform_test(self):
        try:
            st = speedtest.Speedtest()
            
            self.status_label['text'] = "Encontrando melhor servidor..."
            self.canvas.delete("all")
            self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)
            self.canvas.create_text(100, 100, text="PING...", font=("Segoe UI", 20, "bold"), fill=self.text_color)
            self.master.update_idletasks()
            
            st.get_best_server()

            ping_result = st.results.ping
            # Usa getattr para verificar a existência do atributo antes de acessá-lo
            jitter_result = getattr(st.results, 'jitter', None)
            packet_loss_result = getattr(st.results, 'packet_loss', None)

            self.ping_label['text'] = f"Ping: {ping_result:.2f} ms"
            self.jitter_label['text'] = f"Jitter: {jitter_result:.2f} ms" if jitter_result is not None else "Jitter: N/A"
            self.packet_loss_label['text'] = f"Perda de Pacotes: {packet_loss_result:.2f}%" if packet_loss_result is not None else "Perda de Pacotes: N/A"
            
            server_info = st.results.server
            server_display = f"{server_info['name']}, {server_info['country']} ({server_info['sponsor']})"
            self.server_label['text'] = f"Servidor: {server_display}"

            self.status_label['text'] = "Testando Download..."
            for i in range(101):
                self.master.after(10, self.update_canvas_progress, "download", i)
                time.sleep(0.01)
            download_speed_bps = st.download()
            download_speed = download_speed_bps / 1_000_000
            self.download_label['text'] = f"Download: {download_speed:.2f} Mbps"

            self.status_label['text'] = "Testando Upload..."
            for i in range(101):
                self.master.after(10, self.update_canvas_progress, "upload", i)
                time.sleep(0.01)
            upload_speed_bps = st.upload()
            upload_speed = upload_speed_bps / 1_000_000
            self.upload_label['text'] = f"Upload: {upload_speed:.2f} Mbps"
            
            self.status_label['text'] = "Teste Concluído!"
            self.draw_final_results_on_canvas(download_speed, upload_speed, ping_result)
            
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            new_record = {
                "ping": ping_result,
                "jitter": jitter_result,
                "packet_loss": packet_loss_result,
                "download": download_speed,
                "upload": upload_speed,
                "date": timestamp,
                "server": server_info
            }
            self.test_history.append(new_record)
            self.save_history()
            self.update_history_tree()
            self.update_graph()
            self.calculate_averages()

        except speedtest.SpeedtestException as e:
            self.status_label['text'] = f"Erro no SpeedTest: {e}"
        except Exception as e:
            self.status_label['text'] = f"Erro inesperado: {e}"
            
        finally:
            self.btn_start['state'] = 'normal'
            self.master.update_idletasks()

    def draw_final_results_on_canvas(self, download, upload, ping):
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)
        
        self.canvas.create_text(100, 60, text="RESULTADOS", font=("Segoe UI", 16, "bold"), fill=self.text_color)
        
        self.canvas.create_text(100, 100, text=f"↓: {download:.1f}", font=("Segoe UI", 18, "bold"), fill="#FFD700")
        self.canvas.create_text(100, 130, text=f"↑: {upload:.1f}", font=("Segoe UI", 18, "bold"), fill="#00BFFF")
        self.canvas.create_text(100, 160, text=f"P: {ping:.0f} ms", font=("Segoe UI", 14), fill=self.fg_color)
        
        self.master.update_idletasks()

# Inicia o aplicativo
root = tk.Tk()
app = SpeedTestApp(root)
root.mainloop()
