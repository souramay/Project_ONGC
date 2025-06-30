from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk, ImageOps
from decimal import Decimal, getcontext
from PIL import Image, ImageTk
import time
import tkinter as tk
from PIL import Image, ImageTk

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)

    image = Image.open("logo.png")

    max_width, max_height = 400, 300
    img_width, img_height = image.size

    scale = min(max_width / img_width, max_height / img_height, 1)
    scale = min(scale * 1.1, 1)  # Slightly bigger than before

    new_size = (int(img_width * scale), int(img_height * scale))

    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.ANTIALIAS

    image = image.resize(new_size, resample_filter)

    logo = ImageTk.PhotoImage(image)

    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width - new_size[0]) // 2
    y = (screen_height - new_size[1]) // 2

    splash.geometry(f"{new_size[0]}x{new_size[1]}+{x}+{y}")

    label = tk.Label(splash, image=logo, bg='white')
    label.image = logo
    label.pack()

    splash.after(2000, splash.destroy)
    splash.mainloop()

show_splash()


# Set precision for decimal calculations - higher precision for accurate conversions
getcontext().prec = 15

# Load data
data = pd.read_csv("Monthly_Production_Volume_Students.csv")
data['PRODUCTION_DATE'] = pd.to_datetime(data['PRODUCTION_DATE'], format='%d-%b-%y')
well_name = sorted(data['WELL_NAME'].dropna().unique().tolist())


data_years = ["All"] + sorted(data['PRODUCTION_DATE'].dt.year.unique(), reverse=True)
data_months = ["All", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
fields = ["All"] + sorted(data['FIELD'].unique())
layers = ["All"] + sorted(data['LAYER_NAME'].unique())
units = ["SCM", "Million Cubic Meter"]

# Accurate conversion functions
def convert_scm_to_million_cubic_meters(scm_value):
    """Convert SCM to Million Cubic Meters with high precision"""
    if scm_value == 0:
        return 0.0
    return float(Decimal(str(scm_value)) / Decimal('1000000'))

def format_volume_display(value, unit):
    """Format volume values for display with appropriate precision"""
    if unit == "Million Cubic Meter":
        if value == 0:
            return "0.000"
        elif value < 0.001:
            return f'{value:.6f}'  # 6 decimal places for very small values
        elif value < 1:
            return f'{value:.4f}'  # 4 decimal places for values < 1
        else:
            return f'{value:.3f}'  # 3 decimal places for larger values
    else:
        return f'{value:,.0f}'  # SCM values as integers with comma separators

COLORS = {
    'primary': '#1e3a8a',
    'secondary': '#3b82f6',
    'accent': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'background': '#f8fafc',
    'surface': '#ffffff',
    'text': '#1f2937',
    'border': '#e5e7eb'
}
current_figure = None  # Global to store the currently displayed matplotlib figure


root = Tk()
root.title("ONGC Gas Production Dashboard")
root.state('zoomed')
root.config(bg=COLORS['background'])
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# Layout setup
main_container = Frame(root, bg=COLORS['background'])
main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

header_frame = Frame(main_container, bg='#820314')
header_frame.pack(fill=X, pady=(0, 20))
logo_img = Image.open("ongc.png")
logo_img = logo_img.resize((160, 100), Image.Resampling.LANCZOS)
logo_tk = ImageTk.PhotoImage(logo_img)
logo_label = Label(header_frame, image=logo_tk, bg='#820314')
logo_label.image = logo_tk
logo_label.pack(side=LEFT, padx=20, pady=10)

Label(header_frame, text="ONGC Monthly Gas Production Dashboard - Tripura Asset",
      bg='#820314', fg="white", font=("Segoe UI", 24, "bold")).pack(side=LEFT, pady=30)

content_frame = Frame(main_container, bg=COLORS['background'])
content_frame.pack(fill=BOTH, expand=True)

# Sidebar
sidebar = Frame(content_frame, bg=COLORS['surface'], relief=SOLID, bd=1)
sidebar.pack(side=LEFT, fill=Y, padx=(0, 20))
sidebar.config(width=320)

sidebar_header = Frame(sidebar, bg='#820314')
sidebar_header.pack(fill=X)
Label(sidebar_header, text="Production Filter Panel", bg='#820314', fg="white", 
      font=("Segoe UI", 16, "bold")).pack(pady=15)

# Scrollable controls_frame
scroll_canvas = Canvas(sidebar, bg=COLORS['surface'], highlightthickness=0)
scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(sidebar, orient=VERTICAL, command=scroll_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

scrollable_window = Frame(scroll_canvas, bg=COLORS['surface'])
scrollable_window.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

scroll_canvas.create_window((0, 0), window=scrollable_window, anchor='nw')
scroll_canvas.configure(yscrollcommand=scrollbar.set)

controls_frame = scrollable_window

def _on_mousewheel(event):
    scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

select = IntVar()

def state():
    if select.get() == 0:
        field.config(state=NORMAL)
        layer.config(state=DISABLED)
    else:
        field.config(state=DISABLED)
        layer.config(state=NORMAL)

def clear():
    # Clear chart area
    for widget in chart_frame.winfo_children():
        widget.destroy()

    # Reset main filters
    year.current(0)
    month.current(0)
    field.current(0)
    layer.current(0)

    # Reset compare period dropdowns
    compare_year1.current(0)
    compare_month1.current(0)
    compare_year2.current(0)
    compare_month2.current(0)

    # Reset compare field dropdowns
    cf1_year.current(0)
    cf1_month.current(0)
    cf1_field.current(0)
    cf2_year.current(0)
    cf2_month.current(0)
    cf2_field.current(0)

    # Reset well dropdown and well-year for monthly chart
    well_combo.current(0)
    well_year.current(0)

    # Reset compare well section
    compare_well.current(0)
    compare_year1.current(0)
    compare_year2.current(0)

    # Reset unit choice
    unit_choice.set("SCM")
    compare_well.current(0)
    compare_well_year1.current(0)
    compare_well_year2.current(0)

    # Reset filter type (field/sand)
    select.set(0)
    state()

def plot_well_monthly():
    selected_well = well_combo.get()
    selected_year = well_year.get()


    if selected_well == "Select Well" or selected_year == "All":
        return
    
    if selected_well == "Select Well" or selected_year == "All":
        messagebox.showwarning("Selection Error", "Please select both a Well and a Year.")
        return


    filtered_data = data[
        (data['WELL_NAME'] == selected_well) &
        (data['PRODUCTION_DATE'].dt.year == int(selected_year))
    ]

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    global current_figure
    current_figure = fig
    

    if filtered_data.empty:
        ax.text(0.5, 0.5, 'No Data Found', fontsize=20, ha='center', va='center', color='gray')
        ax.axis('off')
    else:
        monthly_data = filtered_data.groupby(filtered_data['PRODUCTION_DATE'].dt.month)['GAS_VOLUME'].sum()
        months = list(range(1, 13))
        volumes = [monthly_data.get(m, 0) for m in months]

        # Accurate unit conversion
        selected_unit = unit_choice.get()
        if selected_unit == "Million Cubic Meter":
            volumes = [convert_scm_to_million_cubic_meters(v) for v in volumes]
            y_label = "Gas Volume (Million m³)"
        else:
            y_label = "Gas Volume (SCM)"

        bars = ax.bar(months, volumes, color=COLORS['secondary'], edgecolor='white')
        
        # Add value labels on bars
        for bar, volume in zip(bars, volumes):
            if volume > 0:  # Only show label if volume > 0
                height = bar.get_height()
                formatted_value = format_volume_display(volume, selected_unit)
                ax.text(bar.get_x() + bar.get_width()/2., height, formatted_value, 
                       ha='center', va='bottom', fontsize=8, weight='bold')

        ax.set_xticks(months)
        ax.set_xticklabels(data_months[1:], rotation=45)
        ax.set_ylabel(y_label, fontsize=12, weight='bold')
        ax.set_xlabel("Month", fontsize=12, weight='bold')
        ax.set_title(f"Monthly Gas Production - Well: {selected_well} ({selected_year})",
                     fontsize=14, weight='bold', pad=20)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)

def plot():
    selected_year = year.get()
    selected_month = month.get()
    selected_field = field.get()
    selected_layer = layer.get()
    selected_option = select.get()

    filtered_data = data.copy()
    if selected_year != "All":
        filtered_data = filtered_data[filtered_data['PRODUCTION_DATE'].dt.year == int(selected_year)]
    if selected_month != "All":
        month_index = data_months.index(selected_month)
        filtered_data = filtered_data[filtered_data['PRODUCTION_DATE'].dt.month == month_index]
    if selected_option == 0 and selected_field != 'All':
        filtered_data = filtered_data[filtered_data['FIELD'] == selected_field]
    elif selected_option == 1 and selected_layer != 'All':
        filtered_data = filtered_data[filtered_data['LAYER_NAME'] == selected_layer]

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('white')
    global current_figure
    current_figure = fig


    if filtered_data.empty:
        ax.text(0.5, 0.5, 'No Records Available', fontsize=32, ha='center', va='center', color='#6b7280', weight='bold')
        ax.axis('off')
    else:
        gas_volume = filtered_data.groupby('WELL_NAME')['GAS_VOLUME'].sum()
        wells = gas_volume.index.tolist()
        
        # Accurate unit conversion
        selected_unit = unit_choice.get()
        if selected_unit == "Million Cubic Meter":
            volumes = [convert_scm_to_million_cubic_meters(vol) for vol in gas_volume.values]
            y_label = "Gas Volume (Million m³)"
        else:
            volumes = gas_volume.values
            y_label = "Gas Volume (SCM)"

        bars = ax.bar(wells, volumes, color=COLORS['secondary'], edgecolor='white', linewidth=1.5)
        
        # Enhanced value display on bars
        for bar, volume in zip(bars, volumes):
            height = bar.get_height()
            formatted_value = format_volume_display(volume, selected_unit)
            ax.text(bar.get_x() + bar.get_width()/2., height, formatted_value, 
                   ha='center', va='bottom', fontsize=8, weight='bold')

        ax.set_xticks(range(len(wells)))
        ax.set_xticklabels(wells, rotation=45, fontsize=9, ha='right')
        ax.set_ylabel(y_label, fontsize=14, weight='bold')
        ax.set_xlabel("Well Name", fontsize=14, weight='bold')
        title = f"Well-wise Production - {'Field: ' + selected_field if selected_option == 0 else 'Sand: ' + selected_layer}"
        subtitle = f"Year: {selected_year}, Month: {selected_month}"
        ax.set_title(f"{title}\n{subtitle}", fontsize=16, weight='bold', pad=30)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.subplots_adjust(left=0.1, right=0.95, top=0.88, bottom=0.28)
    plt.xticks(rotation=45, ha='right')
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)

def compare():
    y1 = compare_year1.get()
    m1 = compare_month1.get()
    y2 = compare_year2.get()
    m2 = compare_month2.get()
    option = select.get()
    selected_field = field.get()
    selected_layer = layer.get()

    def filter_data(y, m):
        d = data.copy()
        if y != "All":
            d = d[d['PRODUCTION_DATE'].dt.year == int(y)]
        if m != "All":
            m_idx = data_months.index(m)
            d = d[d['PRODUCTION_DATE'].dt.month == m_idx]
        if option == 0 and selected_field != "All":
            d = d[d['FIELD'] == selected_field]
        elif option == 1 and selected_layer != "All":
            d = d[d['LAYER_NAME'] == selected_layer]
        return d

    df1 = filter_data(y1, m1)
    df2 = filter_data(y2, m2)

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('white')
    global current_figure
    current_figure = fig


    if df1.empty or df2.empty:
        ax.text(0.5, 0.5, 'No data available for comparison', fontsize=30, ha='center', va='center', color='#6b7280', weight='bold')
        ax.axis('off')
    else:
        sum1 = df1.groupby('WELL_NAME')['GAS_VOLUME'].sum()
        sum2 = df2.groupby('WELL_NAME')['GAS_VOLUME'].sum()
        all_wells = sorted(set(sum1.index).union(set(sum2.index)))
        vol1 = [sum1.get(w, 0) for w in all_wells]
        vol2 = [sum2.get(w, 0) for w in all_wells]
        
        # Accurate unit conversion for comparison
        selected_unit = unit_choice.get()
        if selected_unit == "Million Cubic Meter":
            vol1 = [convert_scm_to_million_cubic_meters(v) for v in vol1]
            vol2 = [convert_scm_to_million_cubic_meters(v) for v in vol2]
            y_label = "Gas Volume (Million m³)"
        else:
            y_label = "Gas Volume (SCM)"

        x = range(len(all_wells))
        width = 0.35
        bars1 = ax.bar([i - width/2 for i in x], vol1, width=width, label=f'{y1}-{m1}', color=COLORS['secondary'], alpha=0.8)
        bars2 = ax.bar([i + width/2 for i in x], vol2, width=width, label=f'{y2}-{m2}', color=COLORS['accent'], alpha=0.8)

        # Add value labels on comparison bars
        for bar, volume in zip(bars1, vol1):
            if volume > 0:
                height = bar.get_height()
                formatted_value = format_volume_display(volume, selected_unit)
                ax.text(bar.get_x() + bar.get_width()/2., height, formatted_value, 
                       ha='center', va='bottom', fontsize=7, rotation=90)

        for bar, volume in zip(bars2, vol2):
            if volume > 0:
                height = bar.get_height()
                formatted_value = format_volume_display(volume, selected_unit)
                ax.text(bar.get_x() + bar.get_width()/2., height, formatted_value, 
                       ha='center', va='bottom', fontsize=7, rotation=90)

        ax.set_xticks(x)
        ax.set_xticklabels(all_wells, rotation=45, fontsize=9, ha='right')
        ax.set_ylabel(y_label, fontsize=12, weight='bold')
        ax.set_xlabel("Well Name", fontsize=12, weight='bold')
        ax.set_title(f"Production Comparison: {y1}-{m1} vs {y2}-{m2}", fontsize=14, weight='bold', pad=20)
        ax.legend(fontsize=12, loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)

def compare_fields(year1, month1, field1, year2, month2, field2):
    def get_field_total(field, year, month):
        df = data.copy()
        if field != "All":
            df = df[df['FIELD'] == field]
        if year != "All":
            df = df[df['PRODUCTION_DATE'].dt.year == int(year)]
        if month != "All":
            month_index = data_months.index(month)
            df = df[df['PRODUCTION_DATE'].dt.month == month_index]
        return df['GAS_VOLUME'].sum()

    val1 = get_field_total(field1, year1, month1)
    val2 = get_field_total(field2, year2, month2)

    selected_unit = unit_choice.get()
    if selected_unit == "Million Cubic Meter":
        val1 = convert_scm_to_million_cubic_meters(val1)
        val2 = convert_scm_to_million_cubic_meters(val2)
        y_label = "Gas Volume (Million m³)"
    else:
        y_label = "Gas Volume (SCM)"

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')
    global current_figure
    current_figure = fig

    
    labels = [f"{field1} ({year1}-{month1})", f"{field2} ({year2}-{month2})"]
    values = [val1, val2]
    bars = ax.bar(labels, values, width=0.2, color=[COLORS['secondary'], COLORS['accent']], edgecolor='white')

    for bar, volume in zip(bars, values):
        if volume > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    format_volume_display(volume, selected_unit),
                    ha='center', va='bottom', fontsize=10, weight='bold')

    ax.set_ylabel(y_label, fontsize=12, weight='bold')
    ax.set_title("Field Production Comparison", fontsize=14, weight='bold', pad=20)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)


def compare_well_monthly():
    y1 = compare_well_year1.get()
    m1 = compare_month1.get()
    y2 = compare_well_year2.get()
    m2 = compare_month2.get()
    well = compare_well.get()

    if well == "Select Well":
        messagebox.showwarning("Selection Error", "Please select a well.")
        return

    def get_monthly_data(y, well):
        d = data.copy()
        if y != "All":
            d = d[d['PRODUCTION_DATE'].dt.year == int(y)]
        d = d[d['WELL_NAME'] == well]
        return d.groupby(d['PRODUCTION_DATE'].dt.month)['GAS_VOLUME'].sum()

    df1 = get_monthly_data(y1, well)
    df2 = get_monthly_data(y2, well)

    months = range(1, 13)
    vol1 = [df1.get(m, 0) for m in months]
    vol2 = [df2.get(m, 0) for m in months]

    selected_unit = unit_choice.get()
    if selected_unit == "Million Cubic Meter":
        vol1 = [convert_scm_to_million_cubic_meters(v) for v in vol1]
        vol2 = [convert_scm_to_million_cubic_meters(v) for v in vol2]
        y_label = "Gas Volume (Million m³)"
    else:
        y_label = "Gas Volume (SCM)"

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('white')
    global current_figure
    current_figure = fig


    x = range(12)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    width = 0.35

    bars1 = ax.bar([i - width/2 for i in x], vol1, width=width, label=f'{y1}', color=COLORS['secondary'], alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], vol2, width=width, label=f'{y2}', color=COLORS['accent'], alpha=0.8)

    for bar, volume in zip(bars1, vol1):
        if volume > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, format_volume_display(volume, selected_unit),
                    ha='center', va='bottom', fontsize=7, rotation=90)

    for bar, volume in zip(bars2, vol2):
        if volume > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, format_volume_display(volume, selected_unit),
                    ha='center', va='bottom', fontsize=7, rotation=90)

    ax.set_xticks(x)
    ax.set_xticklabels(month_names, rotation=0, fontsize=10, weight='bold')
    ax.set_ylabel(y_label, fontsize=12, weight='bold')
    ax.set_xlabel("Month", fontsize=12, weight='bold')
    ax.set_title(f"Well Production Comparison: {well} | {y1} vs {y2}", fontsize=14, weight='bold', pad=20)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)

def download_chart():
    if current_figure is None:
        messagebox.showwarning("No Chart", "No chart to save. Please generate a chart first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Image", "*.png")],
                                             title="Save chart as...")
    if file_path:
        try:
            current_figure.savefig(file_path, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Saved", f"Chart saved successfully at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chart.\n{e}")

box1_frame = LabelFrame(controls_frame, text="Filter Type", bg=COLORS['surface'],
                        fg=COLORS['text'], font=("Segoe UI", 11, "bold"), bd=2, relief=GROOVE)
box1_frame.pack(fill=X, padx=10, pady=10)

Radiobutton(box1_frame, text="Field Wise", variable=select, value=0, command=state,
           bg=COLORS['surface'], font=("Segoe UI", 10), fg=COLORS['text']).pack(anchor=W, padx=10, pady=5)
Radiobutton(box1_frame, text="Sand Wise", variable=select, value=1, command=state,
           bg=COLORS['surface'], font=("Segoe UI", 10), fg=COLORS['text']).pack(anchor=W, padx=10, pady=5)

# --- Selection Section (No Box) ---
box2_frame = LabelFrame(controls_frame, text="Select Region or Sand Layer", bg=COLORS['surface'],
                        fg=COLORS['text'], font=("Segoe UI", 11, "bold"), bd=2, relief=GROOVE)
box2_frame.pack(fill=X, padx=10, pady=10)

# Field Label and Combobox
Label(box2_frame, text="Field:", bg=COLORS['surface'], font=("Segoe UI", 10)).grid(row=1, column=0, sticky=W, padx=10, pady=(5, 0))
field = ttk.Combobox(box2_frame, values=fields, font=("Segoe UI", 10), width=10)
field.grid(row=1, column=1, padx=(0, 10), pady=(5, 0), sticky='ew')
field.current(0)

# Sand/Layer Label and Combobox
Label(box2_frame, text="Sand/Layer:", bg=COLORS['surface'], font=("Segoe UI", 10)).grid(row=2, column=0, sticky=W, padx=10)
layer = ttk.Combobox(box2_frame, values=layers, font=("Segoe UI", 10), width=10, state=DISABLED)
layer.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
layer.current(0)

box2_frame.grid_columnconfigure(1, weight=1)
# --- Unit Section (Box) ---

box3_frame = LabelFrame(controls_frame, text="Choose Display Unit", bg=COLORS['surface'],
                        fg=COLORS['text'], font=("Segoe UI", 11, "bold"), bd=2, relief=GROOVE)
box3_frame.pack(fill=X, padx=10, pady=10)

unit_choice = StringVar()
unit_choice.set("SCM")  # default value

Radiobutton(box3_frame, text="SCM", variable=unit_choice, value="SCM",
            bg=COLORS['surface'], font=("Segoe UI", 10), fg=COLORS['text']).pack(anchor='w', padx=10)

Radiobutton(box3_frame, text="Million Cubic Meter", variable=unit_choice, value="Million Cubic Meter",
            bg=COLORS['surface'], font=("Segoe UI", 10), fg=COLORS['text']).pack(anchor='w', padx=10, pady=(0, 10))


# --- Compare Fields Section ---
box4_frame = LabelFrame(controls_frame, text="Compare Total Field Production", bg=COLORS['surface'],
                        fg=COLORS['text'], font=("Segoe UI", 11, "bold"), bd=2, relief=GROOVE)
box4_frame.pack(fill=X, padx=10, pady=10)

compare_fields_inner = Frame(box4_frame, bg=COLORS['surface'])
compare_fields_inner.pack(anchor='w')

# Column headers for dropdowns
Label(compare_fields_inner, text="Year", font=("Segoe UI", 9, "bold"), bg=COLORS['surface'])\
    .grid(row=0, column=0, padx=(0,5), sticky='w')
Label(compare_fields_inner, text="Month", font=("Segoe UI", 9, "bold"), bg=COLORS['surface'])\
    .grid(row=0, column=1, padx=(0,5), sticky='w')
Label(compare_fields_inner, text="Field", font=("Segoe UI", 9, "bold"), bg=COLORS['surface'])\
    .grid(row=0, column=2, padx=(0,5), sticky='w')

# Field 1 label on row 1
Label(compare_fields_inner, text="Field 1", font=("Segoe UI", 9, "bold"), bg=COLORS['surface'])\
    .grid(row=1, column=0, sticky='w', pady=(5, 2))

cf1_year = ttk.Combobox(compare_fields_inner, values=data_years, state="readonly", width=8)
cf1_year.current(0)
cf1_year.grid(row=2, column=0, padx=(0, 5), pady=(0, 5))

cf1_month = ttk.Combobox(compare_fields_inner, values=data_months, state="readonly", width=10)
cf1_month.current(0)
cf1_month.grid(row=2, column=1, padx=(0, 5), pady=(0, 5))

cf1_field = ttk.Combobox(compare_fields_inner, values=fields[1:], state="readonly", width=15)
cf1_field.current(0)
cf1_field.grid(row=2, column=2, padx=(0, 5), pady=(0, 5))

# Field 2 label on row 3
Label(compare_fields_inner, text="Field 2", font=("Segoe UI", 9, "bold"), bg=COLORS['surface'])\
    .grid(row=3, column=0, sticky='w', pady=(10, 2))

cf2_year = ttk.Combobox(compare_fields_inner, values=data_years, state="readonly", width=8)
cf2_year.current(0)
cf2_year.grid(row=4, column=0, padx=(0, 5), pady=(0, 5))

cf2_month = ttk.Combobox(compare_fields_inner, values=data_months, state="readonly", width=10)
cf2_month.current(0)
cf2_month.grid(row=4, column=1, padx=(0, 5), pady=(0, 5))

cf2_field = ttk.Combobox(compare_fields_inner, values=fields[1:], state="readonly", width=15)
cf2_field.current(0)
cf2_field.grid(row=4, column=2, padx=(0, 5), pady=(0, 5))

# Button
Button(box4_frame, text="View Field Comparison Chart", command=lambda: compare_fields(
    cf1_year.get(), cf1_month.get(), cf1_field.get(),
    cf2_year.get(), cf2_month.get(), cf2_field.get()
), bg=COLORS['primary'], fg="white",
       font=("Segoe UI", 10, "bold"), padx=8, pady=2).pack(anchor='center', pady=(5, 0))


# --- Time Period Section 
box5_frame = LabelFrame(controls_frame, text="Time Period & Compare Periods", bg=COLORS['surface'],
                        fg=COLORS['text'], font=("Segoe UI", 13, "bold"), bd=2, relief=GROOVE)
box5_frame.pack(fill=X, padx=10, pady=10)

Label(box5_frame, text="View Production for Selected Period:", bg=COLORS['surface'], font=("Segoe UI", 9, "bold"))\
    .pack(anchor='w', pady=(0, 5))

time_inner = Frame(box5_frame, bg=COLORS['surface'])
time_inner.pack(anchor='w')

Label(time_inner, text="Year", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=0, column=0, padx=(0, 10), sticky='w')
Label(time_inner, text="Month", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=0, column=1, padx=(0, 10), sticky='w')

year = ttk.Combobox(time_inner, values=data_years, state="readonly", width=8)
year.current(0)
year.grid(row=1, column=0, padx=(0, 10), pady=2)

month = ttk.Combobox(time_inner, values=data_months, state="readonly", width=10)
month.current(0)
month.grid(row=1, column=1, padx=(0, 10), pady=2)

Button(time_inner, text="Generate Time-Based Chart", command=plot, bg=COLORS['primary'], fg="white",
       font=("Segoe UI", 9, "bold"), padx=8).grid(row=1, column=2, pady=2)

# --- Well Selection Section
box6_frame = LabelFrame(controls_frame, text="Well-wise Monthly Analysis & Yearly Comparison", bg=COLORS['surface'],
                        fg=COLORS['text'], font=("Segoe UI", 11, "bold"), bd=2, relief=GROOVE)
box6_frame.pack(fill=X, padx=10, pady=10)
Label(box6_frame, text="Select Well & Year:", bg=COLORS['surface'], font=("Segoe UI", 10, "bold"))\
    .pack(anchor='w', pady=(0, 5))

well_inner = Frame(box6_frame, bg=COLORS['surface'])
well_inner.pack(anchor='w')

# Well dropdown
well_combo = ttk.Combobox(well_inner, values=["Select Well"] + sorted(data['WELL_NAME'].unique()),
                          state="readonly", width=18)
well_combo.current(0)
well_combo.grid(row=0, column=0, padx=(0, 5), pady=2)

# Year dropdown for well trend
well_year = ttk.Combobox(well_inner, values=data_years, state="readonly", width=10)
well_year.current(0)
well_year.grid(row=0, column=1, padx=(0, 5), pady=2)

# Button
Button(well_inner, text="Plot Monthly Trend", command=plot_well_monthly,
       bg=COLORS['primary'], fg="white", font=("Segoe UI", 9, "bold"), padx=8)\
       .grid(row=0, column=2, pady=2)

# --- Well Monthly Comparison UI ---
Label(box6_frame, text="Compare Monthly Trends:", bg=COLORS['surface'],
      font=("Segoe UI", 13, "bold")).pack(anchor='w', pady=(10, 5), padx=10)

wmc_inner = Frame(box6_frame, bg=COLORS['surface'])
wmc_inner.pack(anchor='w', padx=10, pady=5)

Label(wmc_inner, text="Well:", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=0, column=0, padx=5, pady=2)
compare_well = ttk.Combobox(wmc_inner, values=["Select Well"] + well_name, state="readonly", width=18)
compare_well.set("Select Well")
compare_well.grid(row=0, column=1, padx=5)

Label(wmc_inner, text="Year 1:", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=1, column=0, padx=5, pady=2)
compare_well_year1 = ttk.Combobox(wmc_inner, values=data_years, state="readonly", width=15)
compare_well_year1.current(0)
compare_well_year1.grid(row=1, column=1, padx=5)

Label(wmc_inner, text="Year 2:", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=2, column=0, padx=5, pady=2)
compare_well_year2 = ttk.Combobox(wmc_inner, values=data_years, state="readonly", width=15)
compare_well_year2.current(0)
compare_well_year2.grid(row=2, column=1, padx=5)

# Place the button in the row after Year 2
Button(wmc_inner, text="Compare Well Across Years", command=compare_well_monthly,
       bg=COLORS['primary'], fg="white", font=("Segoe UI", 10, "bold"))\
       .grid(row=3, column=1, pady=(10, 2), sticky='w')  # Just below Year 2



# --- Compare Periods Section ---
compare_frame = Frame(box5_frame, bg=COLORS['surface'])
compare_frame.pack(fill=X, padx=10, pady=5)
Label(compare_frame, text="Compare Production Across Two Time Periods:", font=("Segoe UI", 10, "bold"),
      bg=COLORS['surface'], fg=COLORS['text']).pack(anchor='w', padx=0, pady=(0, 5))

compare_inner = Frame(compare_frame, bg=COLORS['surface'])
compare_inner.pack(anchor='w')

Label(compare_inner, text="Period 1", bg=COLORS['surface'], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky='w', padx=(0, 10))
Label(compare_inner, text="Period 2", bg=COLORS['surface'], font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky='w', padx=(0, 10))

Label(compare_inner, text="Year", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=1, column=0, sticky='w', padx=(0, 5))
compare_year1 = ttk.Combobox(compare_inner, values=data_years, state="readonly", width=8)
compare_year1.current(0)
compare_year1.grid(row=1, column=1, padx=(0, 5), pady=2)

Label(compare_inner, text="Month", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=1, column=2, sticky='w', padx=(0, 5))
compare_month1 = ttk.Combobox(compare_inner, values=data_months, state="readonly", width=10)
compare_month1.current(0)
compare_month1.grid(row=1, column=3, padx=(0, 15), pady=2)

Label(compare_inner, text="Year", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=3, column=0, sticky='w', padx=(0, 5))
compare_year2 = ttk.Combobox(compare_inner, values=data_years, state="readonly", width=8)
compare_year2.current(0)
compare_year2.grid(row=3, column=1, padx=(0, 5), pady=2)

Label(compare_inner, text="Month", bg=COLORS['surface'], font=("Segoe UI", 9)).grid(row=3, column=2, sticky='w', padx=(0, 5))
compare_month2 = ttk.Combobox(compare_inner, values=data_months, state="readonly", width=10)
compare_month2.current(0)
compare_month2.grid(row=3, column=3, padx=(0, 15), pady=2)

Button(compare_frame, text="Show Period-to-Period Comparison", command=compare, bg=COLORS['primary'], fg="white",
       font=("Segoe UI", 10, "bold"), padx=8, pady=2).pack(anchor='center', pady=(5, 0))

# Buttons
button_frame = Frame(controls_frame, bg=COLORS['surface'])
button_frame.pack(fill=X, pady=10)
Button(button_frame, text="DOWNLOAD CHART", command=download_chart,
       font=("Segoe UI", 11, "bold"), bg=COLORS['accent'], fg="white",
       relief=FLAT, padx=20, pady=10, cursor="hand2").pack(fill=X, pady=(5, 0))


clear_btn = Button(button_frame, text="CLEAR ALL", command=clear,
                  font=("Segoe UI", 11, "bold"), bg=COLORS['danger'], fg="white",
                  relief=FLAT, padx=20, pady=10, cursor="hand2")
clear_btn.pack(fill=X)
Button(button_frame, text="EXIT APPLICATION", command=root.destroy,
       font=("Segoe UI", 11, "bold"), bg="#0B3692", fg="white",
       relief=FLAT, padx=20, pady=10, cursor="hand2").pack(fill=X, pady=(5, 0))


# Chart area
chart_frame = Frame(content_frame, bg=COLORS['surface'], relief=SOLID, bd=1)
chart_frame.pack(side=RIGHT, fill=BOTH, expand=True)

Label(chart_frame, text="Select filters and click 'Generate Chart' to view gas production data", 
      font=("Segoe UI", 16), fg=COLORS['text'], bg=COLORS['surface']).pack(expand=True)

root.bind('<Return>', lambda event: plot())
root.bind('<Control-c>', lambda event: compare())
root.bind('<Control-r>', lambda event: clear())

root.mainloop()