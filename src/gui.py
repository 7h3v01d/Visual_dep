import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import shlex
import os
import tempfile
import webbrowser

class VisualDepGUI(tk.Tk):
    """
    A GUI application for the Python import dependency visualization script.

    This GUI provides a user-friendly interface to configure and run the
    command-line tool, VisualDep.py. It handles directory selection,
    option toggling, and displays the output.
    """
    def __init__(self):
        super().__init__()
        self.title("Python Import Visualizer")
        self.geometry("700x500")
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and places all the GUI widgets.
        """
        # Main frame
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Directory Selection
        dir_frame = tk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(dir_frame, text="Root Directory:", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
        self.dir_path = tk.Entry(dir_frame)
        self.dir_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        tk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side=tk.LEFT)

        # Options Frame
        options_frame = tk.LabelFrame(main_frame, text="Graph Options", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=10)

        # Checkboxes
        self.include_external = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Include External Dependencies", variable=self.include_external).grid(row=0, column=0, sticky='w')

        self.show_shared = tk.BooleanVar(value=False)
        tk.Checkbutton(options_frame, text="Show Top Shared Modules", variable=self.show_shared).grid(row=1, column=0, sticky='w')

        # Dimensions Radio Buttons
        tk.Label(options_frame, text="Dimension:").grid(row=0, column=1, padx=(20, 5), sticky='w')
        self.dim_var = tk.IntVar(value=3)
        tk.Radiobutton(options_frame, text="2D", variable=self.dim_var, value=2).grid(row=0, column=2, sticky='w')
        tk.Radiobutton(options_frame, text="3D", variable=self.dim_var, value=3).grid(row=1, column=2, sticky='w')

        # Other Settings Frame
        settings_frame = tk.LabelFrame(main_frame, text="Settings", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=10)
        tk.Label(settings_frame, text="Output HTML File (optional):").grid(row=0, column=0, sticky='w')
        self.output_path = tk.Entry(settings_frame)
        self.output_path.grid(row=0, column=1, sticky='ew', padx=(5, 5))
        tk.Button(settings_frame, text="Browse", command=self.browse_output).grid(row=0, column=2)

        tk.Label(settings_frame, text="Layout Seed:").grid(row=1, column=0, sticky='w')
        self.seed_val = tk.Entry(settings_frame)
        self.seed_val.insert(0, "42")
        self.seed_val.grid(row=1, column=1, sticky='ew', padx=(5, 5))
        settings_frame.grid_columnconfigure(1, weight=1)

        # Action Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Generate Graph", command=self.run_script).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        # Output Console
        console_frame = tk.LabelFrame(main_frame, text="Output Console", padx=5, pady=5)
        console_frame.pack(fill=tk.BOTH, expand=True)
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, height=10)
        self.console.pack(fill=tk.BOTH, expand=True)

    def browse_directory(self):
        """Opens a dialog to select a directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.delete(0, tk.END)
            self.dir_path.insert(0, directory)

    def browse_output(self):
        """Opens a dialog to save an HTML file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
        if file_path:
            self.output_path.delete(0, tk.END)
            self.output_path.insert(0, file_path)

    def run_script(self):
        """Constructs and executes the command for the external script."""
        self.console.delete('1.0', tk.END)
        directory = self.dir_path.get().strip()

        if not directory:
            messagebox.showerror("Error", "Please select a root directory.")
            self.console.insert(tk.END, "Error: No directory selected.\n")
            return

        # Build the command line arguments
        cmd_args = ["python", "VisualDep.py", directory]

        if self.dim_var.get() == 2:
            cmd_args.append("--dim")
            cmd_args.append("2")

        if self.include_external.get():
            cmd_args.append("--include-external")

        if self.show_shared.get():
            cmd_args.append("--show-shared")

        output_file = self.output_path.get().strip()
        
        # If no output file is specified, create a temporary one and open it
        if not output_file:
            temp_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_file = temp_file.name
            temp_file.close()
            cmd_args.append("--output")
            cmd_args.append(output_file)
            show_in_browser = True
        else:
            cmd_args.append("--output")
            cmd_args.append(output_file)
            show_in_browser = False

        seed_value = self.seed_val.get().strip()
        if seed_value:
            try:
                int(seed_value)
                cmd_args.append("--seed")
                cmd_args.append(seed_value)
            except ValueError:
                messagebox.showerror("Error", "Seed must be an integer.")
                self.console.insert(tk.END, "Error: Seed value is not an integer.\n")
                return

        self.console.insert(tk.END, f"Executing command: {' '.join(shlex.quote(arg) for arg in cmd_args)}\n\n")

        try:
            # Use subprocess to run the command
            process = subprocess.Popen(cmd_args, cwd=os.path.dirname(os.path.abspath(__file__)), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            for line in iter(process.stdout.readline, ''):
                self.console.insert(tk.END, line)
                self.console.see(tk.END)
                self.update()
            
            process.stdout.close()
            process.wait()
            self.console.insert(tk.END, f"\nProcess finished with exit code {process.returncode}.\n")

            if process.returncode == 0 and show_in_browser:
                self.console.insert(tk.END, f"Opening generated HTML file in your default web browser: {output_file}\n")
                webbrowser.open(f'file:///{output_file}')

        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find 'VisualDep.py' or 'python'. Ensure they are in your system's PATH.")
            self.console.insert(tk.END, "Error: Python script or executable not found.\n")
        except Exception as e:
            messagebox.showerror("An error occurred", str(e))
            self.console.insert(tk.END, f"An unexpected error occurred: {e}\n")

    def clear_form(self):
        """Resets all form fields to their default state."""
        self.dir_path.delete(0, tk.END)
        self.output_path.delete(0, tk.END)
        self.seed_val.delete(0, tk.END)
        self.seed_val.insert(0, "42")
        self.include_external.set(False)
        self.show_shared.set(False)
        self.dim_var.set(3)
        self.console.delete('1.0', tk.END)

if __name__ == '__main__':
    app = VisualDepGUI()
    app.mainloop()
