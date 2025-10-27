"""
Visualización GUI del Mapa Estelar
Ejecuta este archivo para ver el canvas con las estrellas y constelaciones
"""
import tkinter as tk
from src.gui.canvas import StarMapCanvas
from src.models.graphBase import graphBase
from src.utils.json_loader import load_constellations

def main():
    # Crear ventana
    root = tk.Tk()
    root.title("🌟 Proyecto Grafos - Mapa Estelar de la NASA")
    root.geometry("850x900")
    root.configure(bg="#1a1a1a")
    
    # Frame superior con título
    title_frame = tk.Frame(root, bg="#2c3e50", height=50)
    title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
    
    title_label = tk.Label(
        title_frame,
        text="🚀 Mapa Estelar de Constelaciones",
        font=("Arial", 16, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=10)
    
    # Frame para el canvas
    canvas_frame = tk.Frame(root, bg="#1a1a1a")
    canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Crear canvas
    canvas = StarMapCanvas(canvas_frame, width=800, height=800)
    canvas.pack()
    
    # Frame inferior con info
    info_frame = tk.Frame(root, bg="#34495e")
    info_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
    
    info_label = tk.Label(
        info_frame,
        text="Cargando datos...",
        font=("Arial", 10),
        bg="#34495e",
        fg="white",
        justify=tk.LEFT
    )
    info_label.pack(pady=5, padx=10)
    
    # Cargar datos
    try:
        print("📂 Cargando datos...")
        graph = graphBase()
        star_map, constellations, burro_data, graph = load_constellations(
            "data/constellations.json",
            graph
        )
        
        print(f"✅ {len(star_map)} estrellas | {len(constellations)} constelaciones")
        
        # Cargar en canvas
        canvas.load_data(star_map, constellations)
        canvas.draw_map()
        
        # Actualizar info
        shared_count = len([s for s in star_map.values() if s.get("shared_by_coords")])
        info_text = f"⭐ {len(star_map)} estrellas | 🌌 {len(constellations)} constelaciones | 🔴 {shared_count} compartida(s) | 🐴 Burro: {burro_data['estadoSalud']}"
        info_label.config(text=info_text)
        
        print("🎉 ¡GUI cargada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        info_label.config(text=f"❌ Error al cargar: {e}")
    
    # Iniciar aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
