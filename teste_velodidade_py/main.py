import tkinter as tk
from tkinter import PhotoImage
import threading
import speedtest
import time
from tkinter import ttk

class SpeedTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Speed Test")
        master.geometry("700x650")
        master.resizable(False, False)
        
        try:
            # Para o código funcionar, você precisará de um arquivo 'speedteste.png'
            # no mesmo diretório ou de um caminho completo para a imagem.
            icone = PhotoImage(file="speedteste.png") 
            master.iconphoto(True, icone)
        except tk.TclError:
            print("Aviso: Imagem 'speedteste.png' não encontrada. A janela ficará sem ícone.")

        # Cores do tema escuro
        self.bg_color = "#2c2c2c"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#007bff"
        self.text_color = "#ffffff"
        self.button_bg = "#4CAF50"
        self.button_fg = "#ffffff"

        master.configure(bg=self.bg_color)

        # --- Frames para organização ---
        self.header_frame = tk.Frame(master, bg=self.bg_color)
        self.header_frame.pack(pady=10)

        self.canvas_frame = tk.Frame(master, bg=self.bg_color)
        self.canvas_frame.pack(pady=10)

        self.server_info_frame = tk.Frame(master, bg=self.bg_color)
        self.server_info_frame.pack(pady=5)

        self.results_frame = tk.Frame(master, bg=self.bg_color)
        self.results_frame.pack(pady=10)

        self.button_frame = tk.Frame(master, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        # --- Widgets ---
        self.title_label = tk.Label(self.header_frame, text="Speed Test", 
                                    font=("Segoe UI", 24, "bold"), 
                                    bg=self.bg_color, fg=self.text_color)
        self.title_label.pack()

        self.status_label = tk.Label(self.header_frame, text="Pressione Iniciar para testar", 
                                     font=("Segoe UI", 12, "italic"), 
                                     bg=self.bg_color, fg=self.fg_color)
        self.status_label.pack(pady=5)

        # --- Canvas para o elemento gráfico ---
        self.canvas = tk.Canvas(self.canvas_frame, width=200, height=200, 
                                bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()
        self.draw_initial_circle()

        # --- Label de informações do servidor ---
        self.server_label = tk.Label(self.server_info_frame, text="Servidor: --",
                                     font=("Segoe UI", 10),
                                     bg=self.bg_color, fg=self.fg_color)
        self.server_label.pack(pady=2)

        # --- Labels de resultados ---
        self.download_label = tk.Label(self.results_frame, text="Download: -- Mbps", 
                                       font=("Segoe UI", 14), 
                                       bg=self.bg_color, fg=self.fg_color)
        self.download_label.pack(pady=2)

        self.upload_label = tk.Label(self.results_frame, text="Upload: -- Mbps", 
                                     font=("Segoe UI", 14), 
                                     bg=self.bg_color, fg=self.fg_color)
        self.upload_label.pack(pady=2)

        self.ping_label = tk.Label(self.results_frame, text="Ping: -- ms", 
                                   font=("Segoe UI", 14), 
                                   bg=self.bg_color, fg=self.fg_color)
        self.ping_label.pack(pady=2)

        # --- Botão Iniciar ---
        self.btn_start = tk.Button(self.button_frame, text="Iniciar Teste", 
                                   command=self.run_speed_test,
                                   font=("Segoe UI", 16, "bold"),
                                   bg=self.button_bg, fg=self.button_fg,
                                   activebackground=self.button_bg,
                                   activeforeground=self.button_fg,
                                   relief="flat",
                                   padx=20, pady=10,
                                   cursor="hand2")
        self.btn_start.pack()

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
        self.server_label['text'] = "Servidor: --"
        
        self.draw_initial_circle()

        threading.Thread(target=self.perform_test).start()

    def perform_test(self):
        try:
            st = speedtest.Speedtest()
            
            # --- Encontrando o melhor servidor (ping) ---
            self.status_label['text'] = "Encontrando melhor servidor..."
            self.canvas.delete("all")
            self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)
            self.canvas.create_text(100, 100, text="PING...", font=("Segoe UI", 20, "bold"), fill=self.text_color)
            self.master.update_idletasks()
            
            # Use o método get_best_server para encontrar o servidor ideal
            st.get_best_server()
            ping_result = st.results.ping
            self.ping_label['text'] = f"Ping: {ping_result:.2f} ms"
            
            # Atualizar o label com as informações do servidor encontrado
            server_info = st.results.server
            server_display = f"{server_info['name']}, {server_info['country']} ({server_info['sponsor']})"
            self.server_label['text'] = f"Servidor: {server_display}"


            # --- Teste de Download ---
            self.status_label['text'] = "Testando Download..."
            # Simulamos o progresso enquanto a chamada bloqueante é executada
            for i in range(101):
                self.master.after(10, self.update_canvas_progress, "download", i)
                time.sleep(0.01)

            download_speed_bps = st.download()
            download_speed = download_speed_bps / 1_000_000
            self.download_label['text'] = f"Download: {download_speed:.2f} Mbps"

            # --- Teste de Upload ---
            self.status_label['text'] = "Testando Upload..."
            # Simulamos o progresso enquanto a chamada bloqueante é executada
            for i in range(101):
                self.master.after(10, self.update_canvas_progress, "upload", i)
                time.sleep(0.01)

            upload_speed_bps = st.upload()
            upload_speed = upload_speed_bps / 1_000_000
            self.upload_label['text'] = f"Upload: {upload_speed:.2f} Mbps"
            
            self.status_label['text'] = "Teste Concluído!"
            self.draw_final_results_on_canvas(download_speed, upload_speed, ping_result)


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
        self.canvas.create_text(100, 100, text=f"D: {download:.1f}", font=("Segoe UI", 18, "bold"), fill="#FFD700")
        self.canvas.create_text(100, 130, text=f"U: {upload:.1f}", font=("Segoe UI", 18, "bold"), fill="#00BFFF")
        self.canvas.create_text(100, 160, text=f"P: {ping:.0f} ms", font=("Segoe UI", 14), fill=self.fg_color)
        
        self.master.update_idletasks()

# Inicia o aplicativo
root = tk.Tk()
app = SpeedTestApp(root)
root.mainloop()
