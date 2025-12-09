import customtkinter as ctk
import subprocess
import os
from PIL import Image
import tempfile
import threading

class PlantUMLApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PlantUML Wrapper")
        self.geometry("1000x700")

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Frame: Input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_input = ctk.CTkLabel(self.input_frame, text="Code PlantUML:")
        self.label_input.pack(pady=5)

        self.textbox = ctk.CTkTextbox(self.input_frame, font=("Consolas", 12))
        self.textbox.pack(expand=True, fill="both", padx=5, pady=5)
        self.textbox.insert("0.0", "@startuml\nAlice -> Bob: Hello\n@enduml")

        self.btn_generate = ctk.CTkButton(self.input_frame, text="Prévisualiser (Générer)", command=self.start_generation_thread)
        self.btn_generate.pack(pady=10)

        # Progress Bar (Hidden by default)
        self.progress_bar = ctk.CTkProgressBar(self.input_frame, mode="indeterminate")
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()

        # Right Frame: Preview
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label_preview = ctk.CTkLabel(self.preview_frame, text="Prévisualisation:")
        self.label_preview.pack(pady=5)

        # Scrollable frame for image
        self.image_container = ctk.CTkScrollableFrame(self.preview_frame, label_text="Image")
        self.image_container.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.image_label = ctk.CTkLabel(self.image_container, text="Aucune image générée.")
        self.image_label.pack()

        # Save Button
        self.btn_save = ctk.CTkButton(self.preview_frame, text="Enregistrer l'image", command=self.save_image, state="disabled")
        self.btn_save.pack(pady=10)

        self.current_image_path = None
        self.plantuml_jar = "plantuml-1.2025.10.jar"

    def start_generation_thread(self):
        # 1. UI updates: Show loading, disable button
        self.btn_generate.configure(state="disabled", text="Génération en cours...")
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        self.image_label.configure(text="Chargement...")
        self.image_label.configure(image=None) # clear previous image

        # 2. Start thread
        thread = threading.Thread(target=self.run_generation_task)
        thread.start()

    def run_generation_task(self):
        puml_code = self.textbox.get("0.0", "end")
        
        # Determine jar path
        import sys
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
            
        jar_path = os.path.join(base_path, self.plantuml_jar)
        
        result = {}

        if not os.path.exists(jar_path):
            result["error"] = "Erreur: jar non trouvé!"
            self.after(0, self.on_generation_complete, result)
            return

        try:
            cmd = ["java", "-jar", jar_path, "-pipe"]
            # Pass input via stdin, capture output via stdout (binary)
            # We encode puml_code to utf-8 bytes
            proc = subprocess.run(cmd, input=puml_code.encode("utf-8"), 
                                  capture_output=True, text=False)
            
            if proc.returncode == 0 and len(proc.stdout) > 0:
                result["success"] = True
                result["data"] = proc.stdout
            else:
                err_msg = proc.stderr.decode("utf-8", errors="replace") if proc.stderr else "Erreur inconnue"
                if len(proc.stdout) == 0:
                     err_msg += " (Aucune donnée reçue)"
                result["error"] = f"Erreur PlantUML ({proc.returncode}): {err_msg}"

        except Exception as e:
            result["error"] = f"Erreur: {str(e)}"
        
        # Schedule UI update on main thread
        self.after(0, self.on_generation_complete, result)

    def on_generation_complete(self, result):
        # Stop loading animation
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_generate.configure(state="normal", text="Prévisualiser (Générer)")

        if "error" in result:
             self.image_label.configure(text=result["error"])
        elif "success" in result:
             data = result["data"]
             try:
                import io
                self.img_pil = Image.open(io.BytesIO(data))
                w, h = self.img_pil.size
                my_image = ctk.CTkImage(light_image=self.img_pil, dark_image=self.img_pil, size=(w, h))
                self.image_label.configure(image=my_image, text="")
                # We don't have a file path anymore, but we have the PIL object
                self.btn_save.configure(state="normal")
             except Exception as e:
                self.image_label.configure(text=f"Erreur affichage: {e}")

    def save_image(self):
        if hasattr(self, 'img_pil'):
            file_path = ctk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.img_pil.save(file_path)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = PlantUMLApp()
    app.mainloop()
