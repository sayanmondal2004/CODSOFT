import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path


class ContactBookPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System - Professional Edition")
        self.root.geometry("1000x780")
        self.root.configure(bg="#f8f9fa")
        
        # Professional Office Color Palette
        self.colors = {
            'bg_primary': '#2c3e50',
            'bg_secondary': '#34495e',
            'bg_light': '#ecf0f1',
            'bg_panel': '#ffffff',
            'bg_list': '#f8f9fa',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'text_light': '#ffffff',
            'accent_primary': '#3498db',
            'accent_success': '#27ae60',
            'accent_danger': '#e74c3c',
            'accent_warning': '#f39c12',
            'border': '#bdc3c7',
        }
        
        self.contacts_file = Path("contacts.json")
        self.contacts = self.load_contacts()
        self.selected_contact = None
        self.edit_btn = None
        self.delete_btn = None
        
        self.setup_ui()
        self.refresh_list()
    
    def load_contacts(self):
        try:
            if self.contacts_file.exists():
                with open(self.contacts_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print("Load error:", e)
        return {}
    
    def save_contacts(self):
        try:
            with open(self.contacts_file, 'w') as f:
                json.dump(self.contacts, f, indent=2)
            print("Saved contacts to", self.contacts_file)
        except Exception as e:
            print("Save error:", e)
    
    def setup_ui(self):
        # Header with integrated search
        header_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Main title
        title = tk.Label(header_frame, text="CONTACT MANAGEMENT SYSTEM", 
                        font=("Segoe UI", 20, "bold"),
                        fg=self.colors['text_light'], bg=self.colors['bg_primary'])
        title.pack(pady=(15, 5))
        
        # Classic search bar - always visible
        search_container = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        search_container.pack(fill="x", padx=30, pady=(0, 15))
        
        tk.Label(search_container, text="🔍 Search Contacts:", 
                font=("Segoe UI", 11, "bold"), fg="#bdc3c7", 
                bg=self.colors['bg_primary']).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_container, textvariable=self.search_var,
                                    font=("Segoe UI", 11), width=40,
                                    bg="#ffffff", fg=self.colors['text_primary'],
                                    relief="solid", bd=1,
                                    insertbackground=self.colors['text_primary'])
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10,10), pady=1)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Clear search button
        self.clear_search_btn = tk.Button(search_container, text="Clear", 
                                        command=self.clear_search,
                                        bg=self.colors['text_secondary'], fg="white",
                                        font=("Segoe UI", 9, "bold"), 
                                        relief="solid", bd=1, width=8)
        self.clear_search_btn.pack(side="right")
        
        version = tk.Label(header_frame, text="Professional Edition | Real-time Search", 
                        font=("Segoe UI", 9), fg="#95a5a6",
                        bg=self.colors['bg_primary'])
        version.pack(pady=(0, 10))
        
        # Main content area
        content_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left panel - Contact list
        list_panel = tk.LabelFrame(content_frame, text="Contact Directory", 
                                font=("Segoe UI", 12, "bold"),
                                fg=self.colors['text_primary'], 
                                bg=self.colors['bg_panel'],
                                relief="solid", bd=1)
        list_panel.pack(side="left", fill="both", expand=True, padx=(0,20))
        
        list_container = tk.Frame(list_panel, bg=self.colors['bg_panel'])
        list_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.contact_listbox = tk.Listbox(list_container, font=("Segoe UI", 11),
                                        bg=self.colors['bg_list'], 
                                        fg=self.colors['text_primary'],
                                        selectbackground=self.colors['accent_primary'],
                                        selectforeground=self.colors['text_light'],
                                        relief="flat", bd=0,
                                        highlightthickness=0,
                                        height=25)
        self.contact_listbox.pack(side="left", fill="both", expand=True)
        self.contact_listbox.bind("<<ListboxSelect>>", self.on_select)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.contact_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.contact_listbox.yview)
        
        # Right panel
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_light'], width=350)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Action buttons (removed search toggle)
        action_frame = tk.LabelFrame(right_panel, text="Quick Actions", 
                                    font=("Segoe UI", 11, "bold"),
                                    fg=self.colors['text_primary'], 
                                    bg=self.colors['bg_panel'],
                                    relief="solid", bd=1)
        action_frame.pack(fill="x", pady=(0,15))
        
        self.add_btn = self.create_button(action_frame, "Add New Contact", 
                                        self.add_contact, self.colors['accent_primary'])
        self.edit_btn = self.create_button(action_frame, "Edit Contact", 
                                        self.edit_contact, self.colors['accent_warning'], 
                                        state="disabled")
        self.delete_btn = self.create_button(action_frame, "Delete Contact", 
                                            self.delete_contact, self.colors['accent_danger'], 
                                            state="disabled")
        
        # Details panel
        details_panel = tk.LabelFrame(right_panel, text="Contact Details", 
                                    font=("Segoe UI", 12, "bold"),
                                    fg=self.colors['text_primary'], 
                                    bg=self.colors['bg_panel'],
                                    relief="solid", bd=1)
        details_panel.pack(fill="both", expand=True)
        
        details_container = tk.Frame(details_panel, bg=self.colors['bg_panel'])
        details_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.details_text = tk.Text(details_container, font=("Consolas", 11),
                                    bg=self.colors['bg_list'],
                                    fg=self.colors['text_primary'],
                                    relief="flat", bd=0,
                                    wrap="word", state="disabled",
                                    insertbackground=self.colors['text_primary'],
                                    selectbackground=self.colors['accent_primary'],
                                    height=18)
        self.details_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Contact Management System - Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                            font=("Segoe UI", 9), fg=self.colors['text_secondary'],
                            bg=self.colors['bg_secondary'], relief="solid", bd=1, anchor="w")
        status_bar.pack(side="bottom", fill="x")
    
    def create_button(self, parent, text, command, color, state="normal"):
        btn = tk.Button(parent, text=text, command=command,
                       bg=color, fg="white",
                       font=("Segoe UI", 10, "bold"),
                       relief="solid", bd=1,
                       activebackground=self.colors['bg_secondary'],
                       activeforeground="white",
                       cursor="hand2", state=state,
                       padx=10, pady=5)
        btn.pack(fill="x", padx=12, pady=6)
        return btn
    
    def set_status(self, message):
        self.status_var.set(f"Status: {message}")
    
    def refresh_list(self, filtered=None):
        self.contact_listbox.delete(0, tk.END)
        data = filtered or self.contacts
        count = len(data)
        search_term = self.search_var.get().strip()
        if search_term:
            self.set_status(f"Search '{search_term}' - Found {count} result{'s' if count != 1 else ''}")
        else:
            self.set_status(f"Showing {count} total contact{'s' if count != 1 else ''}")
        
        for name in sorted(data.keys()):
            self.contact_listbox.insert(tk.END, name)
    
    def on_select(self, event):
        selection = self.contact_listbox.curselection()
        if selection:
            self.selected_contact = self.contact_listbox.get(selection[0])
            self.edit_btn.config(state="normal")
            self.delete_btn.config(state="normal")
            self.show_details(self.selected_contact)
            self.set_status(f"Selected: {self.selected_contact}")
    
    def show_details(self, name):
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        info = self.contacts.get(name, {})
        
        details = f"""Name: {name}


Phone: {info.get('phone', 'Not specified')}


Email: {info.get('email', 'Not specified')}


Address: {info.get('address', 'Not specified')}"""
        
        self.details_text.insert(1.0, details)
        self.details_text.config(state="disabled")
    
    def clear_search(self):
        self.search_var.set("")
        self.refresh_list()
        self.contact_listbox.selection_clear(0, tk.END)
        self.selected_contact = None
        self.edit_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        self.details_text.config(state="normal")
        self.details_text.delete(1.0, tk.END)
        self.details_text.config(state="disabled")
    
    def on_search(self, event=None):
        query = self.search_var.get().lower().strip()
        if not query:
            self.refresh_list()
            return
        
        filtered = {}
        for name, info in self.contacts.items():
            if (query in name.lower() or 
                query in str(info.get('phone', '')).lower() or
                query in str(info.get('email', '')).lower()):
                filtered[name] = info
        
        self.refresh_list(filtered)
        # Clear selection when searching
        self.contact_listbox.selection_clear(0, tk.END)
        self.selected_contact = None
        self.edit_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
    
    def add_contact(self):
        dialog = ContactDialog(self.root, self.colors, "Add New Contact")
        if dialog.result:
            name, info = dialog.result
            if name in self.contacts:
                messagebox.showerror("Error", "Contact name already exists!", parent=self.root)
            else:
                self.contacts[name] = info
                self.save_contacts()
                self.refresh_list()
                messagebox.showinfo("Success", f"Contact '{name}' added successfully", parent=self.root)
                self.set_status(f"Added new contact: {name}")
    
    def edit_contact(self):
        if not self.selected_contact:
            return
        
        current = self.contacts[self.selected_contact]
        dialog = ContactDialog(self.root, self.colors, "Edit Contact", current)
        if dialog.result:
            name, info = dialog.result
            if name != self.selected_contact and name in self.contacts:
                messagebox.showerror("Error", "Contact name already exists!", parent=self.root)
                return
            
            old_name = self.selected_contact
            self.contacts[name] = info
            if old_name != name:
                del self.contacts[old_name]
            
            self.save_contacts()
            self.refresh_list()
            self.selected_contact = name
            self.show_details(name)
            messagebox.showinfo("Success", "Contact updated successfully", parent=self.root)
    
    def delete_contact(self):
        if not self.selected_contact:
            return
        if messagebox.askyesno("Confirm Delete", 
                            f"Delete contact '{self.selected_contact}' permanently?",
                            parent=self.root):
            del self.contacts[self.selected_contact]
            self.save_contacts()
            self.refresh_list()
            self.details_text.config(state="normal")
            self.details_text.delete(1.0, tk.END)
            self.details_text.config(state="disabled")
            self.edit_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
            self.selected_contact = None
            self.set_status("Contact deleted")
            messagebox.showinfo("Success", "Contact deleted successfully", parent=self.root)


class ContactDialog:
    def __init__(self, parent, colors, title, current_data=None):
        self.result = None
        self.colors = colors
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("420x400")
        self.dialog.configure(bg=colors['bg_panel'])
        self.dialog.transient(parent)
        self.dialog.resizable(False, False)
        
        self.setup_dialog(current_data)
        self.dialog.grab_set()           # grab the events
        parent.wait_window(self.dialog)  # wait until dialog closes

    def setup_dialog(self, current_data):
        tk.Label(self.dialog, text=self.dialog.title(), font=("Segoe UI", 14, "bold"),
                fg=self.colors['text_primary'], bg=self.colors['bg_panel']).pack(pady=20)
        
        fields = [("Name *", "name"), ("Phone", "phone"), 
                ("Email", "email"), ("Address", "address")]
        
        self.entries = {}
        for label, key in fields:
            frame = tk.Frame(self.dialog, bg=self.colors['bg_panel'])
            frame.pack(fill="x", padx=30, pady=8)
            
            tk.Label(frame, text=label, font=("Segoe UI", 10, "bold"), 
                    fg=self.colors['text_primary'], bg=self.colors['bg_panel'],
                    anchor="w").pack(anchor="w")
            entry = tk.Entry(frame, font=("Segoe UI", 10), bg="#ffffff",
                            fg=self.colors['text_primary'], relief="solid", bd=1)
            if current_data and key in current_data:
                entry.insert(0, current_data[key])
            entry.pack(fill="x", pady=(0,5))
            self.entries[key] = entry
        
        btn_frame = tk.Frame(self.dialog, bg=self.colors['bg_panel'])
        btn_frame.pack(pady=25)
        
        tk.Button(btn_frame, text="Save", command=self.save,
                bg=self.colors['accent_primary'], fg="white",
                font=("Segoe UI", 10, "bold"), width=12, relief="solid", bd=1).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy,
                bg=self.colors['text_secondary'], fg="white",
                font=("Segoe UI", 10, "bold"), width=12, relief="solid", bd=1).pack(side="left", padx=10)
    
    def save(self):
        name = self.entries['name'].get().strip()
        if not name:
            messagebox.showerror("Validation Error", "Name is required!", parent=self.dialog)
            return
        
        info = {key: entry.get().strip() for key, entry in self.entries.items()}
        self.result = (name, info)
        self.dialog.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookPro(root)
    root.mainloop()
