import tkinter as tk
from tkinter import PhotoImage
import threading
import speedtest
import time # Para simular o progresso no Canvas
from tkinter import ttk # Para estilos mais modernos (opcional)

class SpeedTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Speed Test")
        master.geometry("700x650") # Aumenta um pouco para o gráfico
        master.resizable(False, False)
        # Definindo o ícone
        icone = PhotoImage(file="speedteste.png") 
        root.iconphoto(True, icone)

        # Cores do tema escuro
        self.bg_color = "#2c2c2c"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#007bff" # Um azul vibrante para destaque
        self.text_color = "#ffffff" # Branco puro para texto principal
        self.button_bg = "#4CAF50" # Verde para o botão de iniciar
        self.button_fg = "#ffffff"

        master.configure(bg=self.bg_color)

        # --- Frames para organização ---
        self.header_frame = tk.Frame(master, bg=self.bg_color)
        self.header_frame.pack(pady=10)

        self.canvas_frame = tk.Frame(master, bg=self.bg_color)
        self.canvas_frame.pack(pady=10)

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
                                   relief="flat", # Sem borda 3D
                                   padx=20, pady=10,
                                   cursor="hand2") # Muda o cursor ao passar por cima
        self.btn_start.pack()

    def draw_initial_circle(self):
        # Desenha o círculo externo e o texto inicial
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)
        self.canvas.create_text(100, 100, text="PRONTO", font=("Segoe UI", 20, "bold"), fill=self.fg_color)

    def update_canvas_progress(self, progress_type, percentage):
        self.canvas.delete("all") # Limpa o canvas

        # Desenha o círculo externo
        self.canvas.create_oval(10, 10, 190, 190, outline=self.fg_color, width=2)

        # Desenha o arco de progresso
        if progress_type == "download":
            color = "#FFD700" # Amarelo para download
            text = f"Baixando...\n{percentage:.0f}%"
        elif progress_type == "upload":
            color = "#00BFFF" # Azul claro para upload
            text = f"Enviando...\n{percentage:.0f}%"
        else:
            color = self.accent_color
            text = f"Testando...\n{percentage:.0f}%"

        # Desenha o arco (0 a 360 graus)
        arc_angle = 3.6 * percentage # 360 graus / 100%
        self.canvas.create_arc(10, 10, 190, 190, 
                               start=90, extent=-arc_angle, # Começa no topo e vai no sentido horário
                               outline=color, style=tk.ARC, width=10) # Aumenta a largura do arco

        self.canvas.create_text(100, 100, text=text, font=("Segoe UI", 16, "bold"), fill=self.text_color, justify="center")
        self.master.update_idletasks() # Força a atualização da interface


    def run_speed_test(self):
        self.btn_start['state'] = 'disabled'
        self.status_label['text'] = "Iniciando teste..."
        self.download_label['text'] = "Download: -- Mbps"
        self.upload_label['text'] = "Upload: -- Mbps"
        self.ping_label['text'] = "Ping: -- ms"
        
        # Resetar o canvas
        self.draw_initial_circle()

        # Inicia o teste em uma thread separada para não travar a GUI
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
            
            # Não tem progresso para st.get_best_server(), apenas esperar
            # st.get_best_server() não fornece progresso, então faremos uma breve pausa e mensagem
            for i in range(1, 4):
                self.canvas.create_text(100, 130, text="."*i, font=("Segoe UI", 20, "bold"), fill=self.text_color)
                self.master.update_idletasks()
                time.sleep(0.5)
            
            st.get_best_server()
            ping_result = st.results.ping
            self.ping_label['text'] = f"Ping: {ping_result:.2f} ms"


            # --- Teste de Download ---
            self.status_label['text'] = "Testando Download..."
            # Simula um progresso para o download
            bytes_downloaded = 0
            # st.download() aceita um callback, mas para uma simulação simples...
            # A biblioteca speedtest-cli não fornece progresso incremental de forma nativa para o download/upload
            # Para ter progresso real, você precisaria reimplementar a lógica de download/upload com chunks
            # Aqui, vou simular um progresso para demonstrar o update_canvas_progress
            total_bytes_for_sim = 1000 * 1024 * 1024 # 1GB simulado
            
            start_time = time.time()
            # Esta é a chamada real para o download
            download_speed_bps = st.download() 
            end_time = time.time()
            
            duration = end_time - start_time
            # Para fins de simulação visual do progresso, vamos fingir um loop
            # Na realidade, o st.download() é bloqueante. Para progresso real, use um callback customizado.
            for i in range(101):
                self.master.after(10) # Pequeno atraso para visualização
                self.update_canvas_progress("download", i)
            
            download_speed = download_speed_bps / 1_000_000 # Mbps
            self.download_label['text'] = f"Download: {download_speed:.2f} Mbps"


            # --- Teste de Upload ---
            self.status_label['text'] = "Testando Upload..."
            # Simula um progresso para o upload
            # Assim como o download, o st.upload() é bloqueante.
            upload_speed_bps = st.upload() 
            for i in range(101):
                self.master.after(10) # Pequeno atraso para visualização
                self.update_canvas_progress("upload", i)
            
            upload_speed = upload_speed_bps / 1_000_000 # Mbps
            self.upload_label['text'] = f"Upload: {upload_speed:.2f} Mbps"
            
            self.status_label['text'] = "Teste Concluído!"
            self.draw_final_results_on_canvas(download_speed, upload_speed, ping_result)


        except speedtest.SpeedTestException as e:
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
        self.canvas.create_text(100, 100, text=f"D: {download:.1f}", font=("Segoe UI", 18, "bold"), fill="#FFD700") # Amarelo
        self.canvas.create_text(100, 130, text=f"U: {upload:.1f}", font=("Segoe UI", 18, "bold"), fill="#00BFFF") # Azul
        self.canvas.create_text(100, 160, text=f"P: {ping:.0f} ms", font=("Segoe UI", 14), fill=self.fg_color)
        
        self.master.update_idletasks()


# Inicia o aplicativo
root = tk.Tk()
app = SpeedTestApp(root)
root.mainloop()