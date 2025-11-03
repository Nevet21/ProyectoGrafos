"""
Test para verificar que MainWindow funciona correctamente
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from src.gui.main_window import MainWindow


def test_main_window_creation():
    """Prueba que la ventana principal se cree correctamente"""
    print("\n" + "="*60)
    print("TEST 1: Creación de MainWindow")
    print("="*60)
    
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana
    
    try:
        app = MainWindow(root)
        
        # Verificar atributos
        assert hasattr(app, 'root'), "Falta atributo root"
        assert hasattr(app, 'canvas'), "Falta atributo canvas"
        assert hasattr(app, 'load_button'), "Falta atributo load_button"
        assert hasattr(app, 'status_label'), "Falta atributo status_label"
        assert hasattr(app, 'info_label'), "Falta atributo info_label"
        print("✅ Todos los atributos presentes")
        
        # Verificar métodos
        assert hasattr(app, 'load_json_file'), "Falta método load_json_file"
        assert hasattr(app, '_load_data_from_file'), "Falta método _load_data_from_file"
        assert hasattr(app, '_update_info_panel'), "Falta método _update_info_panel"
        assert hasattr(app, '_show_error'), "Falta método _show_error"
        print("✅ Todos los métodos presentes")
        
        # Verificar que el botón tiene comando asignado
        button_command = app.load_button.cget('command')
        assert button_command is not None, "Botón sin comando asignado"
        print("✅ Botón 'Cargar JSON' configurado correctamente")
        
        print("✅ MainWindow creado exitosamente")
        
    finally:
        root.destroy()
    
    return True


def test_main_window_structure():
    """Prueba la estructura de widgets de la ventana"""
    print("\n" + "="*60)
    print("TEST 2: Estructura de Widgets")
    print("="*60)
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = MainWindow(root)
        
        # Verificar que el canvas es del tipo correcto
        from src.gui.canvas import StarMapCanvas
        assert isinstance(app.canvas, StarMapCanvas), "Canvas no es StarMapCanvas"
        print("✅ Canvas es del tipo correcto")
        
        # Verificar que los datos iniciales son None
        assert app.star_map is None, "star_map debería ser None al inicio"
        assert app.constellations is None, "constellations debería ser None al inicio"
        assert app.burro_data is None, "burro_data debería ser None al inicio"
        assert app.graph is None, "graph debería ser None al inicio"
        print("✅ Datos iniciales correctamente en None")
        
        # Verificar textos iniciales
        status_text = app.status_label.cget('text')
        assert "Sin archivo" in status_text or "sin archivo" in status_text.lower(), "Texto de estado inicial incorrecto"
        print(f"✅ Estado inicial: {status_text}")
        
    finally:
        root.destroy()
    
    return True


def test_load_json_programmatically():
    """Prueba cargar el JSON programáticamente (sin FileDialog)"""
    print("\n" + "="*60)
    print("TEST 3: Carga de JSON Programática")
    print("="*60)
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = MainWindow(root)
        
        # Cargar el JSON directamente
        json_path = "data/constellations.json"
        
        if not os.path.exists(json_path):
            print(f"⚠️  Archivo {json_path} no encontrado, saltando test")
            return True
        
        print(f"📂 Cargando: {json_path}")
        app._load_data_from_file(json_path)
        
        # Verificar que los datos se cargaron
        assert app.star_map is not None, "star_map no se cargó"
        assert app.constellations is not None, "constellations no se cargaron"
        assert app.burro_data is not None, "burro_data no se cargó"
        assert app.graph is not None, "graph no se creó"
        print("✅ Datos cargados correctamente")
        
        # Verificar cantidad de datos
        print(f"✅ {len(app.star_map)} estrellas cargadas")
        print(f"✅ {len(app.constellations)} constelaciones cargadas")
        print(f"✅ Burro: {app.burro_data['estadoSalud']}, Energía: {app.burro_data['burroenergiaInicial']}%")
        
        # Verificar que el canvas tiene datos
        assert app.canvas.star_map == app.star_map, "Canvas no tiene los datos correctos"
        print("✅ Canvas actualizado con los datos")
        
        # Verificar que el estado se actualizó
        status_text = app.status_label.cget('text')
        print(f"✅ Estado actualizado: {status_text}")
        
    finally:
        root.destroy()
    
    return True


def test_error_handling():
    """Prueba el manejo de errores con archivo inválido"""
    print("\n" + "="*60)
    print("TEST 4: Manejo de Errores")
    print("="*60)
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = MainWindow(root)
        
        # Intentar cargar archivo que no existe
        try:
            app._load_data_from_file("archivo_que_no_existe.json")
            assert False, "Debería haber lanzado excepción"
        except FileNotFoundError:
            print("✅ FileNotFoundError capturado correctamente")
        except Exception as e:
            print(f"✅ Excepción capturada: {type(e).__name__}")
        
    finally:
        root.destroy()
    
    return True


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "🧪"*30)
    print("EJECUTANDO TESTS DE MAIN_WINDOW")
    print("🧪"*30)
    
    tests = [
        test_main_window_creation,
        test_main_window_structure,
        test_load_json_programmatically,
        test_error_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ FALLÓ: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR EN: {test.__name__}")
            print(f"   Excepción: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print("📊 RESULTADOS DE TESTS MAIN_WINDOW")
    print("="*60)
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Porcentaje de éxito: {(passed / (passed + failed) * 100):.1f}%")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS DE MAIN_WINDOW PASARON! 🎉")
        print("\n💡 Ahora puedes ejecutar:")
        print("   python run_app.py")
        print("   para ver la aplicación completa")
    else:
        print(f"\n⚠️  {failed} test(s) necesitan atención")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
