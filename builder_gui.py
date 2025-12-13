#!/usr/bin/env python3
"""
HF Site Builder - GUI tool for managing your Hugging Face Space website
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from pathlib import Path
from typing import Dict

CONFIG_FILE = Path(__file__).parent / "config.json"

class HFSiteBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HF Site Builder - GUI Manager")
        self.root.geometry("900x700")

        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4F46E5"
        self.root.configure(bg=self.bg_color)

        # Load config
        self.config = self.load_config()

        # Create main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header
        self.create_header(main_frame)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Create tabs
        self.create_site_info_tab()
        self.create_categories_tab()
        self.create_models_tab()
        self.create_datasets_tab()
        self.create_preview_tab()

        # Footer buttons
        self.create_footer(main_frame)

    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        title_label = ttk.Label(
            header_frame,
            text="🚀 HF Site Builder",
            font=('Helvetica', 20, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)

        subtitle_label = ttk.Label(
            header_frame,
            text="Manage your Hugging Face Space website",
            font=('Helvetica', 10)
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)

    def create_site_info_tab(self):
        """Create Site Information tab"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="🏠 Site Info")

        # Title
        ttk.Label(tab, text="Site Title:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.site_title = ttk.Entry(tab, width=50)
        self.site_title.insert(0, self.config['site']['title'])
        self.site_title.grid(row=0, column=1, pady=5, padx=5)

        # Description
        ttk.Label(tab, text="Description:", font=('Helvetica', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.site_desc = ttk.Entry(tab, width=50)
        self.site_desc.insert(0, self.config['site']['description'])
        self.site_desc.grid(row=1, column=1, pady=5, padx=5)

        # Author
        ttk.Label(tab, text="Author:", font=('Helvetica', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.site_author = ttk.Entry(tab, width=50)
        self.site_author.insert(0, self.config['site']['author'])
        self.site_author.grid(row=2, column=1, pady=5, padx=5)

        # Theme Color
        ttk.Label(tab, text="Theme Color:", font=('Helvetica', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.site_color = ttk.Entry(tab, width=50)
        self.site_color.insert(0, self.config['site'].get('theme_color', '#4F46E5'))
        self.site_color.grid(row=3, column=1, pady=5, padx=5)

        # Social Links
        ttk.Label(tab, text="Social Links", font=('Helvetica', 12, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(20, 10)
        )

        ttk.Label(tab, text="GitHub:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.social_github = ttk.Entry(tab, width=50)
        self.social_github.insert(0, self.config['site']['social_links'].get('github', ''))
        self.social_github.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(tab, text="Twitter:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.social_twitter = ttk.Entry(tab, width=50)
        self.social_twitter.insert(0, self.config['site']['social_links'].get('twitter', ''))
        self.social_twitter.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(tab, text="LinkedIn:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.social_linkedin = ttk.Entry(tab, width=50)
        self.social_linkedin.insert(0, self.config['site']['social_links'].get('linkedin', ''))
        self.social_linkedin.grid(row=7, column=1, pady=5, padx=5)

        # Save button
        save_btn = ttk.Button(
            tab,
            text="💾 Save Site Info",
            command=self.save_site_info
        )
        save_btn.grid(row=8, column=0, columnspan=2, pady=20)

    def create_categories_tab(self):
        """Create Categories tab"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="📂 Categories")

        # Split into two frames: list and form
        list_frame = ttk.LabelFrame(tab, text="Existing Categories", padding="10")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        form_frame = ttk.LabelFrame(tab, text="Add New Category", padding="10")
        form_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)

        # Categories list
        self.categories_listbox = tk.Listbox(list_frame, height=15)
        self.categories_listbox.pack(fill=tk.BOTH, expand=True)
        self.refresh_categories_list()

        # Delete button
        delete_btn = ttk.Button(
            list_frame,
            text="🗑️ Delete Selected",
            command=self.delete_category
        )
        delete_btn.pack(pady=(5, 0))

        # Form fields
        ttk.Label(form_frame, text="Category ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cat_id = ttk.Entry(form_frame, width=30)
        self.cat_id.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cat_name = ttk.Entry(form_frame, width=30)
        self.cat_name.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Icon (emoji):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cat_icon = ttk.Entry(form_frame, width=30)
        self.cat_icon.insert(0, "📁")
        self.cat_icon.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cat_desc = tk.Text(form_frame, width=30, height=4)
        self.cat_desc.grid(row=3, column=1, pady=5, padx=5)

        # Add button
        add_btn = ttk.Button(
            form_frame,
            text="➕ Add Category",
            command=self.add_category
        )
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def create_models_tab(self):
        """Create Models tab"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="🤖 Models")

        # Split into two frames
        list_frame = ttk.LabelFrame(tab, text="Existing Models", padding="10")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        form_frame = ttk.LabelFrame(tab, text="Add New Model", padding="10")
        form_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)

        # Models list
        self.models_listbox = tk.Listbox(list_frame, height=15)
        self.models_listbox.pack(fill=tk.BOTH, expand=True)
        self.refresh_models_list()

        # Delete button
        delete_btn = ttk.Button(
            list_frame,
            text="🗑️ Delete Selected",
            command=self.delete_model
        )
        delete_btn.pack(pady=(5, 0))

        # Form fields with scrollbar
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Label(scrollable_frame, text="Model Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.model_name = ttk.Entry(scrollable_frame, width=30)
        self.model_name.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(scrollable_frame, text="HF Repo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_repo = ttk.Entry(scrollable_frame, width=30)
        self.model_repo.grid(row=1, column=1, pady=5, padx=5)
        ttk.Label(scrollable_frame, text="(username/repo)", font=('Helvetica', 8)).grid(
            row=1, column=2, sticky=tk.W
        )

        ttk.Label(scrollable_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.model_category = ttk.Combobox(scrollable_frame, width=28)
        self.model_category['values'] = [cat['id'] for cat in self.config['categories']]
        self.model_category.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(scrollable_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.model_desc = tk.Text(scrollable_frame, width=30, height=3)
        self.model_desc.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(scrollable_frame, text="Tags:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.model_tags = ttk.Entry(scrollable_frame, width=30)
        self.model_tags.grid(row=4, column=1, pady=5, padx=5)
        ttk.Label(scrollable_frame, text="(comma-separated)", font=('Helvetica', 8)).grid(
            row=4, column=2, sticky=tk.W
        )

        ttk.Label(scrollable_frame, text="Demo URL:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.model_demo = ttk.Entry(scrollable_frame, width=30)
        self.model_demo.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(scrollable_frame, text="Paper URL:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.model_paper = ttk.Entry(scrollable_frame, width=30)
        self.model_paper.grid(row=6, column=1, pady=5, padx=5)

        # Add button
        add_btn = ttk.Button(
            scrollable_frame,
            text="➕ Add Model",
            command=self.add_model
        )
        add_btn.grid(row=7, column=0, columnspan=3, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_datasets_tab(self):
        """Create Datasets tab"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="📊 Datasets")

        # Split into two frames
        list_frame = ttk.LabelFrame(tab, text="Existing Datasets", padding="10")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        form_frame = ttk.LabelFrame(tab, text="Add New Dataset", padding="10")
        form_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)

        # Datasets list
        self.datasets_listbox = tk.Listbox(list_frame, height=15)
        self.datasets_listbox.pack(fill=tk.BOTH, expand=True)
        self.refresh_datasets_list()

        # Delete button
        delete_btn = ttk.Button(
            list_frame,
            text="🗑️ Delete Selected",
            command=self.delete_dataset
        )
        delete_btn.pack(pady=(5, 0))

        # Form fields
        ttk.Label(form_frame, text="Dataset Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dataset_name = ttk.Entry(form_frame, width=30)
        self.dataset_name.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="HF Repo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dataset_repo = ttk.Entry(form_frame, width=30)
        self.dataset_repo.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dataset_category = ttk.Combobox(form_frame, width=28)
        self.dataset_category['values'] = [cat['id'] for cat in self.config['categories']]
        self.dataset_category.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.dataset_desc = tk.Text(form_frame, width=30, height=3)
        self.dataset_desc.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Tags:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.dataset_tags = ttk.Entry(form_frame, width=30)
        self.dataset_tags.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Size:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.dataset_size = ttk.Entry(form_frame, width=30)
        self.dataset_size.grid(row=5, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text="(e.g., 100K samples)", font=('Helvetica', 8)).grid(
            row=5, column=2, sticky=tk.W
        )

        # Add button
        add_btn = ttk.Button(
            form_frame,
            text="➕ Add Dataset",
            command=self.add_dataset
        )
        add_btn.grid(row=6, column=0, columnspan=3, pady=10)

    def create_preview_tab(self):
        """Create Preview tab"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="👁️ Preview")

        ttk.Label(
            tab,
            text="Configuration Preview",
            font=('Helvetica', 12, 'bold')
        ).pack(pady=(0, 10))

        # Scrolled text for JSON preview
        self.preview_text = scrolledtext.ScrolledText(
            tab,
            width=80,
            height=30,
            font=('Courier', 9)
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Refresh button
        refresh_btn = ttk.Button(
            tab,
            text="🔄 Refresh Preview",
            command=self.refresh_preview
        )
        refresh_btn.pack(pady=10)

        self.refresh_preview()

    def create_footer(self, parent):
        """Create footer with action buttons"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Button(
            footer_frame,
            text="✅ Validate Config",
            command=self.validate_config
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            footer_frame,
            text="💾 Save All",
            command=self.save_config
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            footer_frame,
            text="🔄 Reload Config",
            command=self.reload_config
        ).pack(side=tk.LEFT, padx=5)

    # Helper methods
    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {e}")
            return {"site": {}, "categories": [], "models": [], "datasets": []}

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.refresh_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def reload_config(self):
        """Reload configuration from file"""
        self.config = self.load_config()
        self.refresh_all()
        messagebox.showinfo("Success", "Configuration reloaded!")

    def refresh_all(self):
        """Refresh all UI elements"""
        self.refresh_categories_list()
        self.refresh_models_list()
        self.refresh_datasets_list()
        self.refresh_preview()

        # Update comboboxes
        if hasattr(self, 'model_category'):
            self.model_category['values'] = [cat['id'] for cat in self.config['categories']]
        if hasattr(self, 'dataset_category'):
            self.dataset_category['values'] = [cat['id'] for cat in self.config['categories']]

    def save_site_info(self):
        """Save site information"""
        self.config['site']['title'] = self.site_title.get()
        self.config['site']['description'] = self.site_desc.get()
        self.config['site']['author'] = self.site_author.get()
        self.config['site']['theme_color'] = self.site_color.get()
        self.config['site']['social_links']['github'] = self.social_github.get()
        self.config['site']['social_links']['twitter'] = self.social_twitter.get()
        self.config['site']['social_links']['linkedin'] = self.social_linkedin.get()

        self.save_config()

    def refresh_categories_list(self):
        """Refresh categories listbox"""
        self.categories_listbox.delete(0, tk.END)
        for cat in self.config['categories']:
            self.categories_listbox.insert(
                tk.END,
                f"{cat['icon']} {cat['name']} ({cat['id']})"
            )

    def add_category(self):
        """Add a new category"""
        cat_id = self.cat_id.get().strip()
        cat_name = self.cat_name.get().strip()
        cat_icon = self.cat_icon.get().strip()
        cat_desc = self.cat_desc.get("1.0", tk.END).strip()

        if not cat_id or not cat_name:
            messagebox.showwarning("Warning", "Category ID and Name are required!")
            return

        # Check if ID already exists
        if any(cat['id'] == cat_id for cat in self.config['categories']):
            messagebox.showwarning("Warning", "Category ID already exists!")
            return

        new_category = {
            "id": cat_id,
            "name": cat_name,
            "icon": cat_icon or "📁",
            "description": cat_desc
        }

        self.config['categories'].append(new_category)
        self.save_config()
        self.refresh_all()

        # Clear form
        self.cat_id.delete(0, tk.END)
        self.cat_name.delete(0, tk.END)
        self.cat_icon.delete(0, tk.END)
        self.cat_icon.insert(0, "📁")
        self.cat_desc.delete("1.0", tk.END)

    def delete_category(self):
        """Delete selected category"""
        selection = self.categories_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a category to delete!")
            return

        index = selection[0]
        cat_name = self.config['categories'][index]['name']

        if messagebox.askyesno("Confirm", f"Delete category '{cat_name}'?"):
            del self.config['categories'][index]
            self.save_config()
            self.refresh_all()

    def refresh_models_list(self):
        """Refresh models listbox"""
        self.models_listbox.delete(0, tk.END)
        for model in self.config.get('models', []):
            self.models_listbox.insert(
                tk.END,
                f"{model['name']} [{model.get('category', 'N/A')}]"
            )

    def add_model(self):
        """Add a new model"""
        name = self.model_name.get().strip()
        repo = self.model_repo.get().strip()
        category = self.model_category.get().strip()
        desc = self.model_desc.get("1.0", tk.END).strip()
        tags = self.model_tags.get().strip()
        demo_url = self.model_demo.get().strip()
        paper_url = self.model_paper.get().strip()

        if not name or not repo or not category:
            messagebox.showwarning("Warning", "Name, Repo, and Category are required!")
            return

        new_model = {
            "name": name,
            "repo": repo,
            "category": category,
            "description": desc,
            "tags": [t.strip() for t in tags.split(',') if t.strip()],
            "demo_url": demo_url or None,
            "paper_url": paper_url or None
        }

        if 'models' not in self.config:
            self.config['models'] = []

        self.config['models'].append(new_model)
        self.save_config()
        self.refresh_models_list()

        # Clear form
        self.model_name.delete(0, tk.END)
        self.model_repo.delete(0, tk.END)
        self.model_category.set('')
        self.model_desc.delete("1.0", tk.END)
        self.model_tags.delete(0, tk.END)
        self.model_demo.delete(0, tk.END)
        self.model_paper.delete(0, tk.END)

    def delete_model(self):
        """Delete selected model"""
        selection = self.models_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a model to delete!")
            return

        index = selection[0]
        model_name = self.config['models'][index]['name']

        if messagebox.askyesno("Confirm", f"Delete model '{model_name}'?"):
            del self.config['models'][index]
            self.save_config()
            self.refresh_models_list()

    def refresh_datasets_list(self):
        """Refresh datasets listbox"""
        self.datasets_listbox.delete(0, tk.END)
        for dataset in self.config.get('datasets', []):
            self.datasets_listbox.insert(
                tk.END,
                f"{dataset['name']} [{dataset.get('category', 'N/A')}]"
            )

    def add_dataset(self):
        """Add a new dataset"""
        name = self.dataset_name.get().strip()
        repo = self.dataset_repo.get().strip()
        category = self.dataset_category.get().strip()
        desc = self.dataset_desc.get("1.0", tk.END).strip()
        tags = self.dataset_tags.get().strip()
        size = self.dataset_size.get().strip()

        if not name or not repo or not category:
            messagebox.showwarning("Warning", "Name, Repo, and Category are required!")
            return

        new_dataset = {
            "name": name,
            "repo": repo,
            "category": category,
            "description": desc,
            "tags": [t.strip() for t in tags.split(',') if t.strip()],
            "size": size
        }

        if 'datasets' not in self.config:
            self.config['datasets'] = []

        self.config['datasets'].append(new_dataset)
        self.save_config()
        self.refresh_datasets_list()

        # Clear form
        self.dataset_name.delete(0, tk.END)
        self.dataset_repo.delete(0, tk.END)
        self.dataset_category.set('')
        self.dataset_desc.delete("1.0", tk.END)
        self.dataset_tags.delete(0, tk.END)
        self.dataset_size.delete(0, tk.END)

    def delete_dataset(self):
        """Delete selected dataset"""
        selection = self.datasets_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a dataset to delete!")
            return

        index = selection[0]
        dataset_name = self.config['datasets'][index]['name']

        if messagebox.askyesno("Confirm", f"Delete dataset '{dataset_name}'?"):
            del self.config['datasets'][index]
            self.save_config()
            self.refresh_datasets_list()

    def refresh_preview(self):
        """Refresh JSON preview"""
        self.preview_text.delete("1.0", tk.END)
        json_str = json.dumps(self.config, indent=2, ensure_ascii=False)
        self.preview_text.insert("1.0", json_str)

    def validate_config(self):
        """Validate configuration"""
        errors = []

        # Check required fields
        if 'site' not in self.config:
            errors.append("Missing 'site' section")
        if 'categories' not in self.config:
            errors.append("Missing 'categories' section")

        # Check category IDs
        category_ids = [c['id'] for c in self.config.get('categories', [])]

        # Validate models
        for model in self.config.get('models', []):
            if model.get('category') not in category_ids:
                errors.append(
                    f"Model '{model.get('name')}' has invalid category: {model.get('category')}"
                )

        # Validate datasets
        for dataset in self.config.get('datasets', []):
            if dataset.get('category') not in category_ids:
                errors.append(
                    f"Dataset '{dataset.get('name')}' has invalid category: {dataset.get('category')}"
                )

        if errors:
            messagebox.showerror(
                "Validation Failed",
                "Configuration has errors:\n\n" + "\n".join(errors)
            )
        else:
            messagebox.showinfo("Success", "✅ Configuration is valid!")

def main():
    root = tk.Tk()
    app = HFSiteBuilderGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
