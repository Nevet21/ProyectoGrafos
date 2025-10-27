"""
Tests para la GUI - Canvas y Renderer
Prueba que el canvas y el renderer funcionan correctamente
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("\n" + "="*60)
    print("TEST 1: Importaciones GUI")
    print("="*60)
    
    try:
        import tkinter as tk
        print("✅ tkinter importado")
    except ImportError as e:
        print(f"❌ Error con tkinter: {e}")
        raise
    
    try:
        from src.gui.canvas import StarMapCanvas
        print("✅ StarMapCanvas importado")
    except Exception as e:
        print(f"❌ Error al importar StarMapCanvas: {e}")
        raise
    
    try:
        from src.gui.star_renderer import StarRenderer
        print("✅ StarRenderer importado")
    except Exception as e:
        print(f"❌ Error al importar StarRenderer: {e}")
        raise
    
    return True


def test_canvas_structure():
    """Prueba que StarMapCanvas tenga todos los métodos necesarios"""
    print("\n" + "="*60)
    print("TEST 2: Estructura de StarMapCanvas")
    print("="*60)
    
    from src.gui.canvas import StarMapCanvas
    
    required_methods = [
        '__init__',
        'load_data',
        'draw_map',
        '_scale_coords',
        '_calculate_scaling'
    ]
    
    for method in required_methods:
        assert hasattr(StarMapCanvas, method), f"Falta método {method}"
        print(f"✅ Método '{method}' presente")
    
    return True


def test_renderer_structure():
    """Prueba que StarRenderer tenga todos los métodos necesarios"""
    print("\n" + "="*60)
    print("TEST 3: Estructura de StarRenderer")
    print("="*60)
    
    from src.gui.star_renderer import StarRenderer
    
    required_methods = [
        '__init__',
        'draw_all',
        'draw_connections',
        'draw_stars',
        'draw_legend',
        '_get_star_color',
        '_get_star_radius',
        '_draw_star_label'
    ]
    
    for method in required_methods:
        assert hasattr(StarRenderer, method), f"Falta método {method}"
        print(f"✅ Método '{method}' presente")
    
    return True


def test_canvas_initialization():
    """Prueba que el canvas se inicialice correctamente"""
    print("\n" + "="*60)
    print("TEST 4: Inicialización de Canvas")
    print("="*60)
    
    import tkinter as tk
    from src.gui.canvas import StarMapCanvas
    
    # Crear root temporal (sin mostrar)
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana
    
    try:
        # Crear canvas
        canvas = StarMapCanvas(root, width=800, height=800)
        
        # Verificar atributos
        assert canvas.canvas_width == 800, "Ancho incorrecto"
        assert canvas.canvas_height == 800, "Alto incorrecto"
        print(f"✅ Canvas creado: {canvas.canvas_width}x{canvas.canvas_height}")
        
        # Verificar atributos iniciales
        assert hasattr(canvas, 'star_map'), "Falta atributo star_map"
        assert hasattr(canvas, 'constellations'), "Falta atributo constellations"
        assert hasattr(canvas, 'constellation_colors'), "Falta atributo constellation_colors"
        print(f"✅ Atributos inicializados correctamente")
        
        # Verificar colores
        assert len(canvas.constellation_colors) >= 2, "Deben haber al menos 2 colores"
        print(f"✅ Paleta de colores: {len(canvas.constellation_colors)} colores disponibles")
        
    finally:
        root.destroy()
    
    return True


def test_canvas_with_data():
    """Prueba que el canvas cargue y procese datos correctamente"""
    print("\n" + "="*60)
    print("TEST 5: Canvas con Datos Reales")
    print("="*60)
    
    import tkinter as tk
    from src.gui.canvas import StarMapCanvas
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    # Crear root temporal
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Cargar datos
        graph = graphBase()
        star_map, constellations, burro_data, graph = load_constellations(
            "data/constellations.json",
            graph
        )
        print(f"✅ Datos cargados: {len(star_map)} estrellas, {len(constellations)} constelaciones")
        
        # Crear canvas
        canvas = StarMapCanvas(root, width=800, height=800)
        
        # Cargar datos en el canvas
        canvas.load_data(star_map, constellations)
        
        # Verificar que se cargaron
        assert canvas.star_map == star_map, "star_map no se cargó correctamente"
        assert canvas.constellations == constellations, "constellations no se cargó correctamente"
        print(f"✅ Datos cargados en el canvas")
        
        # Verificar que se calculó el escalado
        assert hasattr(canvas, 'scale'), "Falta atributo scale"
        assert hasattr(canvas, 'min_x'), "Falta atributo min_x"
        assert hasattr(canvas, 'min_y'), "Falta atributo min_y"
        print(f"✅ Escalado calculado: scale={canvas.scale:.2f}")
        
    finally:
        root.destroy()
    
    return True


def test_coordinate_scaling():
    """Prueba que el escalado de coordenadas funcione correctamente"""
    print("\n" + "="*60)
    print("TEST 6: Escalado de Coordenadas")
    print("="*60)
    
    import tkinter as tk
    from src.gui.canvas import StarMapCanvas
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Cargar datos y crear canvas
        graph = graphBase()
        star_map, constellations, burro_data, graph = load_constellations(
            "data/constellations.json",
            graph
        )
        
        canvas = StarMapCanvas(root, width=800, height=800)
        canvas.load_data(star_map, constellations)
        
        # Probar escalado con coordenadas conocidas
        # Estrella 1 está en (25, 34)
        star1 = star_map[1]
        x_orig = star1["coordenates"]["x"]
        y_orig = star1["coordenates"]["y"]
        
        canvas_x, canvas_y = canvas._scale_coords(x_orig, y_orig)
        
        # Verificar que las coordenadas escaladas están dentro del canvas
        assert 0 <= canvas_x <= canvas.canvas_width, f"X escalada fuera de rango: {canvas_x}"
        assert 0 <= canvas_y <= canvas.canvas_height, f"Y escalada fuera de rango: {canvas_y}"
        
        print(f"✅ Coordenadas originales: ({x_orig}, {y_orig})")
        print(f"✅ Coordenadas escaladas: ({canvas_x:.1f}, {canvas_y:.1f})")
        print(f"✅ Coordenadas dentro del canvas [0-{canvas.canvas_width}]")
        
    finally:
        root.destroy()
    
    return True


def test_renderer_creation():
    """Prueba que el renderer se cree correctamente"""
    print("\n" + "="*60)
    print("TEST 7: Creación del Renderer")
    print("="*60)
    
    import tkinter as tk
    from src.gui.canvas import StarMapCanvas
    from src.gui.star_renderer import StarRenderer
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Cargar datos
        graph = graphBase()
        star_map, constellations, burro_data, graph = load_constellations(
            "data/constellations.json",
            graph
        )
        
        # Crear canvas
        canvas = StarMapCanvas(root, width=800, height=800)
        canvas.load_data(star_map, constellations)
        
        # Crear renderer
        renderer = StarRenderer(
            canvas=canvas,
            star_map=star_map,
            constellations=constellations,
            scale_func=canvas._scale_coords,
            constellation_colors=canvas.constellation_colors
        )
        
        print(f"✅ Renderer creado exitosamente")
        
        # Verificar atributos
        assert renderer.star_map == star_map, "star_map no asignado"
        assert renderer.constellations == constellations, "constellations no asignado"
        assert len(renderer.constellation_color_map) > 0, "Mapa de colores vacío"
        print(f"✅ Renderer con {len(renderer.constellation_color_map)} colores asignados")
        
    finally:
        root.destroy()
    
    return True


def test_star_color_detection():
    """Prueba que el renderer detecte correctamente los colores"""
    print("\n" + "="*60)
    print("TEST 8: Detección de Colores de Estrellas")
    print("="*60)
    
    import tkinter as tk
    from src.gui.canvas import StarMapCanvas
    from src.gui.star_renderer import StarRenderer
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Cargar datos
        graph = graphBase()
        star_map, constellations, burro_data, graph = load_constellations(
            "data/constellations.json",
            graph
        )
        
        canvas = StarMapCanvas(root, width=800, height=800)
        canvas.load_data(star_map, constellations)
        
        renderer = StarRenderer(
            canvas=canvas,
            star_map=star_map,
            constellations=constellations,
            scale_func=canvas._scale_coords,
            constellation_colors=canvas.constellation_colors
        )
        
        # Verificar color de estrella normal (estrella 1)
        star1 = star_map[1]
        color1 = renderer._get_star_color(star1)
        assert color1.startswith("#"), "Color debe ser hexadecimal"
        print(f"✅ Estrella 1 (no compartida): color = {color1}")
        
        # Verificar color de estrella compartida (estrella 3)
        star3 = star_map[3]
        color3 = renderer._get_star_color(star3)
        assert color3 == "#e74c3c", f"Estrella compartida debe ser roja, obtenido: {color3}"
        print(f"✅ Estrella 3 (compartida): color = {color3} (ROJO)")
        
    finally:
        root.destroy()
    
    return True


def test_drawing_without_errors():
    """Prueba que el dibujo se ejecute sin errores"""
    print("\n" + "="*60)
    print("TEST 9: Dibujo Completo sin Errores")
    print("="*60)
    
    import tkinter as tk
    from src.gui.canvas import StarMapCanvas
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Cargar datos
        graph = graphBase()
        star_map, constellations, burro_data, graph = load_constellations(
            "data/constellations.json",
            graph
        )
        
        # Crear canvas y cargar datos
        canvas = StarMapCanvas(root, width=800, height=800)
        canvas.load_data(star_map, constellations)
        
        # Intentar dibujar (esto llama al renderer internamente)
        canvas.draw_map()
        
        print(f"✅ Canvas dibujado sin errores")
        
        # Verificar que se dibujaron elementos
        # El canvas de tkinter guarda los IDs de los elementos dibujados
        items = canvas.find_all()
        assert len(items) > 0, "No se dibujó nada en el canvas"
        print(f"✅ {len(items)} elementos dibujados en el canvas")
        
        # Verificar que hay líneas (conexiones)
        connections = canvas.find_withtag("connection")
        print(f"✅ {len(connections)} líneas de conexión dibujadas")
        
        # Verificar que hay estrellas
        stars = [item for item in items if canvas.type(item) == "oval"]
        print(f"✅ {len(stars)} círculos (estrellas) dibujados")
        
    finally:
        root.destroy()
    
    return True


def run_all_tests():
    """Ejecuta todos los tests de GUI"""
    print("\n" + "🎨"*30)
    print("EJECUTANDO TESTS DE GUI (Canvas y Renderer)")
    print("🎨"*30)
    
    tests = [
        test_imports,
        test_canvas_structure,
        test_renderer_structure,
        test_canvas_initialization,
        test_canvas_with_data,
        test_coordinate_scaling,
        test_renderer_creation,
        test_star_color_detection,
        test_drawing_without_errors,
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
    print("📊 RESULTADOS DE TESTS GUI")
    print("="*60)
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Porcentaje de éxito: {(passed / (passed + failed) * 100):.1f}%")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS DE GUI PASARON! 🎉")
        print("\n💡 Ahora puedes ejecutar:")
        print("   python test_gui.py")
        print("   para ver la visualización completa")
    else:
        print(f"\n⚠️  {failed} test(s) necesitan atención")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
