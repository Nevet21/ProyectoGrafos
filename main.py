"""
🌟 PROYECTO DE GRAFOS - NASA
Mapa Estelar de Constelaciones

Para ejecutar: python main.py
"""
import tkinter as tk
from src.gui.main_window import MainWindow


def main():
    """Función principal de la aplicación"""
    print("="*60)
    print("🚀 INICIANDO MAPA ESTELAR DE LA NASA")
    print("="*60)
    print("\n📋 Instrucciones:")
    print("   1. Haz clic en '📂 Cargar Archivo JSON'")
    print("   2. Selecciona 'data/constellations.json'")
    print("   3. Observa el mapa estelar")
    print("   4. Estrella compartida aparece en ROJO 🔴\n")
    
    root = tk.Tk()
    app = MainWindow(root)
    
    print("✅ Ventana abierta. Cierra la ventana para salir.\n")
    root.mainloop()
    
    print("\n👋 Aplicación cerrada")


if __name__ == "__main__":
    main()
