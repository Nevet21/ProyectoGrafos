"""
Tests para algoritmos de pathfinding
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.graph import Graph
from src.algorithms.pathfinding import dijkstra_simple


def test_dijkstra_basic():
    """Prueba básica de Dijkstra"""
    print("\n" + "="*60)
    print("TEST 1: Dijkstra - Camino Básico")
    print("="*60)
    
    # Crear un grafo simple
    graph = Graph()
    
    # Agregar vértices y aristas
    #   1 --100-- 2
    #   |         |
    #  150       50
    #   |         |
    #   3 -------
    graph.add_edge(1, 2, 100)
    graph.add_edge(2, 3, 50)
    graph.add_edge(1, 3, 150)
    
    print("\nGrafo creado:")
    print("  1 --100--> 2")
    print("  |          |")
    print(" 150        50")
    print("  |          |")
    print("  3 <-------")
    
    # Ejecutar Dijkstra de 1 a 3
    dist, pred, path = dijkstra_simple(graph, 1, 3)
    
    # Verificar que el camino más corto es 1 -> 2 -> 3 (distancia 150)
    assert dist[3] == 150, f"Distancia incorrecta: esperada 150, obtenida {dist[3]}"
    assert path == [1, 2, 3], f"Camino incorrecto: esperado [1, 2, 3], obtenido {path}"
    
    print(f"\n✅ Camino más corto encontrado: {' → '.join(map(str, path))}")
    print(f"✅ Distancia total: {dist[3]}")
    
    return True


def test_dijkstra_with_star_graph():
    """Prueba Dijkstra con el grafo de estrellas del JSON"""
    print("\n" + "="*60)
    print("TEST 2: Dijkstra - Grafo de Estrellas Real")
    print("="*60)
    
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    # Cargar el grafo real
    graph_base = graphBase()
    star_map, constellations, burro_data, graph_base = load_constellations(
        "data/constellations.json", 
        graph_base
    )
    
    print(f"\nGrafo cargado con {len(graph_base.get_vertices())} vértices")
    
    # Crear grafo compatible con dijkstra_simple
    graph = Graph()
    
    # Copiar todas las aristas
    for star_id in graph_base.get_vertices():
        neighbors = graph_base.get_neighbors(star_id)
        for neighbor_id, distance in neighbors.items():
            graph.add_edge(star_id, neighbor_id, distance)
    
    print(f"✅ Grafo convertido correctamente")
    
    # Probar Dijkstra entre estrellas 1 y 3
    if 1 in graph_base.get_vertices() and 3 in graph_base.get_vertices():
        print("\n🔍 Buscando camino más corto de estrella 1 a estrella 3...")
        dist, pred, path = dijkstra_simple(graph, 1, 3)
        
        print(f"✅ Camino encontrado: {' → '.join(map(str, path))}")
        print(f"✅ Distancia total: {dist[3]} años luz")
        
        # Mostrar detalles del camino
        print("\n📍 Detalles del camino:")
        for i, star_id in enumerate(path):
            star = star_map[star_id]
            print(f"   {i+1}. Estrella {star_id}: {star['label']}")
    else:
        print("⚠️  Estrellas 1 o 3 no encontradas en el grafo")
    
    return True


def test_dijkstra_unreachable():
    """Prueba Dijkstra con nodo inalcanzable"""
    print("\n" + "="*60)
    print("TEST 3: Dijkstra - Nodo Inalcanzable")
    print("="*60)
    
    graph = Graph()
    
    # Crear dos componentes desconectadas
    graph.add_edge(1, 2, 100)
    graph.add_edge(2, 3, 50)
    
    # Componente separada
    graph.add_edge(4, 5, 30)
    
    print("\nGrafo con componentes desconectadas:")
    print("  1 --100-- 2 --50-- 3")
    print("  (separado)")
    print("  4 --30-- 5")
    
    # Intentar llegar de 1 a 5 (imposible)
    dist, pred, path = dijkstra_simple(graph, 1, 5)
    
    import math
    assert dist[5] == math.inf, "Distancia a nodo inalcanzable debería ser infinita"
    print(f"\n✅ Correctamente detectado nodo inalcanzable")
    print(f"✅ Distancia a nodo 5: ∞")
    
    return True


def test_graph_properties():
    """Prueba propiedades del grafo"""
    print("\n" + "="*60)
    print("TEST 4: Propiedades del Grafo")
    print("="*60)
    
    from src.models.graphBase import graphBase
    from src.utils.json_loader import load_constellations
    
    graph = graphBase()
    star_map, constellations, burro_data, graph = load_constellations(
        "data/constellations.json", 
        graph
    )
    
    # Verificar que el grafo es no dirigido
    vertices = graph.get_vertices()
    print(f"\n📊 Grafo con {len(vertices)} vértices")
    
    # Para cada arista, verificar que existe en ambas direcciones
    symmetric = True
    for v in vertices:
        neighbors = graph.get_neighbors(v)
        for neighbor, dist in neighbors.items():
            reverse_neighbors = graph.get_neighbors(neighbor)
            if v not in reverse_neighbors or reverse_neighbors[v] != dist:
                symmetric = False
                print(f"❌ Arista {v}->{neighbor} no es simétrica")
    
    assert symmetric, "El grafo debería ser no dirigido (simétrico)"
    print(f"✅ Grafo es no dirigido (todas las aristas son simétricas)")
    
    # Verificar grados de algunos nodos
    star1_neighbors = len(graph.get_neighbors(1))
    print(f"✅ Estrella 1 tiene {star1_neighbors} vecinos")
    
    return True


def run_all_tests():
    """Ejecuta todos los tests de algoritmos"""
    print("\n" + "🚀"*30)
    print("EJECUTANDO TESTS DE ALGORITMOS")
    print("🚀"*30)
    
    tests = [
        test_dijkstra_basic,
        test_dijkstra_with_star_graph,
        test_dijkstra_unreachable,
        test_graph_properties,
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
    print("📊 RESULTADOS DE TESTS DE ALGORITMOS")
    print("="*60)
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Porcentaje de éxito: {(passed / (passed + failed) * 100):.1f}%")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS DE ALGORITMOS PASARON! 🎉")
    else:
        print(f"\n⚠️  {failed} test(s) necesitan atención")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
