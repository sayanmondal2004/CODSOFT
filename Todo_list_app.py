import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AdvancedTodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Nexus Task Manager")
        self.geometry("550x850")
        self.tasks_file = "tasks_v3.json"
        
        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text="NEXUS MISSION CONTROL", font=("Orbitron", 26, "bold"), text_color="#00d4ff")
        self.label.grid(row=0, column=0, pady=20)
        
        self.entry = ctk.CTkEntry(self, placeholder_text="Identify New Objective...", width=320, height=40, font=("Arial", 14))
        self.entry.grid(row=1, column=0, padx=20, pady=10)
        
        self.priority_menu = ctk.CTkOptionMenu(self, values=["High", "Medium", "Low"], fg_color="#1f538d")
        self.priority_menu.grid(row=2, column=0, pady=5)
        
        self.add_button = ctk.CTkButton(self, text="DEPLOY MISSION", font=("Arial", 13, "bold"), 
                                        command=self.add_task, fg_color="#00ff88", text_color="#000000", hover_color="#00cc6e")
        self.add_button.grid(row=3, column=0, pady=20)
        
        self.active_frame = ctk.CTkScrollableFrame(self, width=450, height=250, label_text="ACTIVE OBJECTIVES", label_text_color="#00ff88")
        self.active_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        
        self.history_frame = ctk.CTkScrollableFrame(self, width=450, height=200, label_text="COMPLETED MISSIONS", label_text_color="#7f8c8d")
        self.history_frame.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")
        
        self.load_tasks()

    def add_task(self):
        task_text = self.entry.get()
        priority = self.priority_menu.get()
        if task_text:
            self.create_task_row(task_text, priority, status="active")
            self.refresh_list_numbers()
            self.save_tasks()
            self.entry.delete(0, 'end')

    def create_task_row(self, text, priority, status="active"):
       
        neon_colors = {"High": "#ff0055", "Medium": "#ffcc00", "Low": "#00d4ff"}
        bg_highlights = {"High": "#4d001a", "Medium": "#4d3d00", "Low": "#00334d"}
        
        target_frame = self.active_frame if status == "active" else self.history_frame
        
        row_frame = ctk.CTkFrame(target_frame, fg_color=bg_highlights.get(priority, "#2b2b2b") if status == "active" else "transparent")
        row_frame.pack(fill="x", pady=5, padx=5)
        
        row_frame.task_text = text
        row_frame.priority = priority
        row_frame.status = status

        if status == "active":
            txt_color = neon_colors.get(priority, "white")
            font_style = ("Arial", 14, "bold")
        else:
            txt_color = "#555555" 
            font_style = ("Arial", 13, "overstrike")
            
        label = ctk.CTkLabel(row_frame, text="", text_color=txt_color, font=font_style, padx=10)
        label.pack(side="left", padx=5, pady=5)
        row_frame.display_label = label 
        
        btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=5)

        if status == "active":
            done_btn = ctk.CTkButton(btn_frame, text="✓", width=30, height=25, fg_color="#00ff88", text_color="#000000",
                                    command=lambda: self.complete_task(row_frame, text, priority))
            done_btn.pack(side="left", padx=2)
            
        del_btn = ctk.CTkButton(btn_frame, text="×", width=30, height=25, fg_color="#ff4444", 
                                command=lambda: self.delete_task(row_frame))
        del_btn.pack(side="left", padx=2)

    def refresh_list_numbers(self):
        """Updates the 1, 2, 3... numbering for both lists."""
        for frame, _ in [(self.active_frame, "active"), (self.history_frame, "history")]:
            count = 1
            for child in frame.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    child.display_label.configure(text=f"{count}. {child.task_text}")
                    count += 1

    def complete_task(self, frame, text, priority):
        frame.destroy()
        self.create_task_row(text, priority, status="history")
        self.after(10, self.refresh_list_numbers)
        self.after(20, self.save_tasks)

    def delete_task(self, frame):
        frame.destroy()
        self.after(10, self.refresh_list_numbers)
        self.after(20, self.save_tasks)

    def save_tasks(self):
        tasks_data = []
        for f_name, frame in [("active", self.active_frame), ("history", self.history_frame)]:
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'task_text'):
                    tasks_data.append({
                        "text": widget.task_text,
                        "priority": widget.priority,
                        "status": f_name
                    })
        
        with open(self.tasks_file, "w") as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r") as f:
                    tasks = json.load(f)
                    for item in tasks:
                        self.create_task_row(item["text"], item["priority"], status=item["status"])
                self.refresh_list_numbers()
            except Exception as e:
                print(f"Error loading: {e}")

if __name__ == "__main__":
    app = AdvancedTodoApp()
    app.mainloop()