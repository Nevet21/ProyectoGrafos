"""
Tests para el grafo y el cargador JSON
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.graphBase import graphBase
from src.utils.json_loader import load_constellations


def test_load_json():
    """Prueba que el JSON se carga correctamente"""
    print("\n" + "="*60)
    print("TEST 1: Carga de JSON")
    print("="*60)
    
    graph = graphBase()
    star_map, constellations, burro_data, graph = load_constellations(
        "data/constellations.json", 
        graph
    )
    
    # Verificar que se cargaron estrellas
    assert len(star_map) > 0, "No se cargaron estrellas"
    print(f"✅ Se cargaron {len(star_map)} estrellas únicas")
    
    # Verificar que hay constelaciones
    assert len(constellations) == 2, "Deberían haber 2 constelaciones"
    print(f"✅ Se cargaron {len(constellations)} constelaciones")
    
    # Verificar estrella compartida (ID 3)
    assert 3 in star_map, "La estrella 3 debería existir"
    assert star_map[3]["shared_by_coords"] == True, "La estrella 3 debería estar marcada como compartida"
    assert len(star_map[3]["constellations"]) == 2, "La estrella 3 debería estar en 2 constelaciones"
    print(f"✅ Estrella compartida detectada correctamente")
    
    # Verificar datos del burro
    assert burro_data["burroenergiaInicial"] == 100
    assert burro_data["estadoSalud"] == "Excelente"
    print(f"✅ Datos del burro cargados: Energía={burro_data['burroenergiaInicial']}, Salud={burro_data['estadoSalud']}")
    
    # Verificar que el grafo tiene vértices
    assert len(graph.get_vertices()) > 0, "El grafo debería tener vértices"
    print(f"✅ Grafo poblado con {len(graph.get_vertices())} vértices")
    
    # Verificar conexiones del grafo
    neighbors_1 = graph.get_neighbors(1)
    assert len(neighbors_1) == 3, "La estrella 1 debería tener 3 vecinos"
    assert 2 in neighbors_1 and neighbors_1[2] == 120, "Estrella 1 debería conectar con 2 a distancia 120"
    print(f"✅ Aristas del grafo correctas")
    
    return True


def test_graph_operations():
    """Prueba operaciones básicas del grafo"""
    print("\n" + "="*60)
    print("TEST 2: Operaciones del Grafo")
    print("="*60)
    
    graph = graphBase()
    
    # Agregar vértices
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    assert len(graph.get_vertices()) == 3, "Deberían haber 3 vértices"
    print(f"✅ Vértices agregados correctamente: {graph.get_vertices()}")
    
    # Agregar aristas
    graph.add_edge(1, 2, 100)
    graph.add_edge(2, 3, 50)
    graph.add_edge(1, 3, 150)
    
    # Verificar vecinos
    neighbors_1 = graph.get_neighbors(1)
    assert 2 in neighbors_1, "Vértice 1 debería tener a 2 como vecino"
    assert neighbors_1[2] == 100, "Distancia 1->2 debería ser 100"
    print(f"✅ Vecinos de 1: {neighbors_1}")
    
    # Verificar simetría (grafo no dirigido)
    neighbors_2 = graph.get_neighbors(2)
    assert 1 in neighbors_2, "Vértice 2 debería tener a 1 como vecino"
    assert neighbors_2[1] == 100, "Distancia 2->1 debería ser 100"
    print(f"✅ Grafo no dirigido verificado (simetría correcta)")
    
    return True


def test_star_properties():
    """Prueba las propiedades específicas de las estrellas"""
    print("\n" + "="*60)
    print("TEST 3: Propiedades de las Estrellas")
    print("="*60)
    
    graph = graphBase()
    star_map, constellations, burro_data, graph = load_constellations(
        "data/constellations.json", 
        graph
    )
    
    # Verificar propiedades de la estrella 1
    star1 = star_map[1]
    assert star1["label"] == "Alpha1", "Label incorrecto"
    assert star1["radius"] == 0.4, "Radio incorrecto"
    assert star1["timeToEat"] == 3, "Tiempo de comer incorrecto"
    assert star1["amountOfEnergy"] == 1, "Cantidad de energía incorrecta"
    assert star1["hypergiant"] == False, "No debería ser hipergigante"
    print(f"✅ Estrella 1 (Alpha1) verificada: radio={star1['radius']}, energy={star1['amountOfEnergy']}")
    
    # Verificar estrella hipergigante (ID 3)
    star3 = star_map[3]
    assert star3["hypergiant"] == True, "Debería ser hipergigante"
    assert star3["radius"] == 1, "Radio de hipergigante incorrecto"
    print(f"✅ Estrella 3 (Alpha53) es hipergigante: radius={star3['radius']}")
    
    # Verificar linkedTo
    assert len(star1["linkedTo"]) == 3, "Estrella 1 debería tener 3 conexiones"
    linked_ids = [link["starId"] for link in star1["linkedTo"]]
    assert 2 in linked_ids, "Estrella 1 debería conectar con estrella 2"
    print(f"✅ Conexiones verificadas: Estrella 1 conecta con {linked_ids}")
    
    return True


def test_constellation_colors():
    """Prueba que cada constelación tenga asignación de estrellas correcta"""
    print("\n" + "="*60)
    print("TEST 4: Constelaciones y Asignaciones")
    print("="*60)
    
    graph = graphBase()
    star_map, constellations, burro_data, graph = load_constellations(
        "data/constellations.json", 
        graph
    )
    
    # Verificar nombres de constelaciones
    const_names = [c["name"] for c in constellations]
    assert "Constelación del Burro" in const_names, "Falta constelación del Burro"
    assert "Constelación de la Araña" in const_names, "Falta constelación de la Araña"
    print(f"✅ Constelaciones encontradas: {const_names}")
    
    # Verificar que las estrellas tienen constelación asignada
    for star_id, star in star_map.items():
        assert len(star["constellations"]) > 0, f"Estrella {star_id} sin constelación"
    print(f"✅ Todas las estrellas tienen constelación asignada")
    
    # Verificar estrella compartida
    star3 = star_map[3]
    assert len(star3["constellations"]) == 2, "Estrella 3 debería estar en 2 constelaciones"
    assert "Constelación del Burro" in star3["constellations"], "Falta constelación del Burro"
    assert "Constelación de la Araña" in star3["constellations"], "Falta constelación de la Araña"
    print(f"✅ Estrella 3 compartida entre: {star3['constellations']}")
    
    return True


def test_shared_coordinates():
    """Prueba la detección de estrellas con coordenadas compartidas"""
    print("\n" + "="*60)
    print("TEST 5: Detección de Coordenadas Compartidas")
    print("="*60)
    
    graph = graphBase()
    star_map, constellations, burro_data, graph = load_constellations(
        "data/constellations.json", 
        graph
    )
    
    # Contar estrellas compartidas
    shared_stars = [s for s in star_map.values() if s.get("shared_by_coords")]
    print(f"✅ Estrellas con coordenadas compartidas: {len(shared_stars)}")
    
    # Verificar estrella 3
    star3 = star_map[3]
    assert star3["shared_by_coords"] == True, "Estrella 3 debería estar marcada como compartida"
    assert star3["coordenates"]["x"] == 75, "Coordenada X incorrecta"
    assert star3["coordenates"]["y"] == 43, "Coordenada Y incorrecta"
    print(f"✅ Estrella 3 en coordenadas ({star3['coordenates']['x']}, {star3['coordenates']['y']})")
    
    # Verificar que tiene shared_ids
    if "shared_ids" in star3:
        print(f"✅ IDs compartidos detectados: {star3['shared_ids']}")
    
    return True


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "🚀"*30)
    print("EJECUTANDO SUITE COMPLETA DE TESTS")
    print("🚀"*30)
    
    tests = [
        test_load_json,
        test_graph_operations,
        test_star_properties,
        test_constellation_colors,
        test_shared_coordinates,
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
    print("📊 RESULTADOS FINALES")
    print("="*60)
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Porcentaje de éxito: {(passed / (passed + failed) * 100):.1f}%")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON! 🎉")
    else:
        print(f"\n⚠️  {failed} test(s) necesitan atención")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
