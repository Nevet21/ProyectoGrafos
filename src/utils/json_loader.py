# json_loader.py
import json
from typing import Optional, Tuple, Dict, Any, List
from src.models.star import Star

def load_constellations(filepath: str, graph: Optional[object] = None
                        ) -> Tuple[Dict[int, dict], List[dict], dict, Optional[object]]:
    """
    Lee el JSON de constelaciones y:
      - Construye `star_map`: dict {star_id: {props...}}
      - Construye `constellations_list`: lista con las constelaciones y sus estrellas (útil para la GUI)
      - Extrae `burro_data` con los parámetros globales del JSON
      - Si se pasa `graph` (objeto con add_edge/add_vertex) lo pobla con las aristas encontradas.

    Retorna: (star_map, constellations_list, burro_data, graph)
    """

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    star_map: Dict[int, dict] = {}
    constellations_list: List[dict] = []

    # Recorremos constelaciones y estrellas
    for c in data.get("constellations", []):
        c_name = c.get("name", "Unnamed")
        c_entry = {"name": c_name, "stars": []}

        for s in c.get("starts", []):   # nota: "starts" según tu JSON
            sid = s.get("id")
            if sid is None:
                continue  # ignorar entradas sin id

            # Propiedades básicas de la estrella
            coords = s.get("coordenates", {})
            x = coords.get("x", 0)
            y = coords.get("y", 0)
            
            # Crear objeto Star con todas las propiedades
            star_obj = Star(
                star_id=sid,
                name=s.get("label", f"Star-{sid}"),
                x=x,
                y=y,
                time_to_eat_kg=s.get("timeToEat", 1.0),
                energy_cost_research=s.get("amountOfEnergy", 0.5),
                health_impact=s.get("healthImpact", 0),  # Si no está en JSON, usa 0
                lifespan_change=s.get("lifespanChange", 0),  # Si no está en JSON, usa 0
                is_hypergiant=bool(s.get("hypergiant", False)),
                max_stay_time=s.get("maxStayTime", 100)  # Si no está en JSON, usa 100
            )
            
            # Información adicional para la GUI y el grafo
            star_info = {
                "id": sid,
                "star_object": star_obj,  # ← NUEVO: guardamos el objeto Star
                "label": s.get("label"),
                "radius": s.get("radius"),
                "coordenates": {"x": x, "y": y},
                "linkedTo": s.get("linkedTo", []),
                "constellations": [c_name],
            }

            # Si ya existe la estrella (misma id), actualizamos lista de constelaciones y linkedTo
            if sid in star_map:
                existing = star_map[sid]
                
                # Unir constelaciones (evitar duplicados)
                if c_name not in existing["constellations"]:
                    existing["constellations"].append(c_name)
                
                # Unir linkedTo (agregar nuevas conexiones que no existan)
                existing_link_ids = {link["starId"] for link in existing["linkedTo"]}
                for new_link in star_info["linkedTo"]:
                    if new_link["starId"] not in existing_link_ids:
                        existing["linkedTo"].append(new_link)
                
                # NO actualizamos el star_object porque es el mismo (mismo ID)
            else:
                star_map[sid] = star_info

            # también agregamos a la lista de la constelación actual (para GUI)
            c_entry["stars"].append(star_map[sid])

            # Si pasaron un objeto grafo, agregamos vértices y aristas
            if graph is not None:
                # añadir vértice (si implementado)
                try:
                    graph.add_vertex(sid)
                except Exception:
                    # si el grafo no tiene add_vertex, seguimos (add_edge puede crear vértices)
                    pass

                for neighbor in s.get("linkedTo", []):
                    nid = neighbor.get("starId")
                    dist = neighbor.get("distance")
                    if nid is None or dist is None:
                        continue
                    # añadir arista en el grafo (se espera add_edge disponible)
                    try:
                        graph.add_edge(sid, nid, dist)
                    except Exception:
                        # si el grafo no soporta add_edge o falla, lo ignoramos para no romper la carga
                        pass

        constellations_list.append(c_entry)

    # Detectar estrellas compartidas (aparecen en múltiples constelaciones)
    # También detectar si múltiples IDs comparten las mismas coordenadas
    
    # 1. Marcar estrellas que aparecen en múltiples constelaciones
    for sid, info in star_map.items():
        if len(info["constellations"]) > 1:
            info["shared_by_constellations"] = True
            # También marcar como compartida para el requisito 1
            info["shared_by_coords"] = True
        else:
            info["shared_by_constellations"] = False
            info["shared_by_coords"] = False
        
        info["shared_ids"] = []
    
    # 2. Detectar múltiples estrellas (IDs diferentes) en las mismas coordenadas
    coords_map: Dict[Tuple[float, float], List[int]] = {}
    for sid, info in star_map.items():
        x = info["coordenates"]["x"]
        y = info["coordenates"]["y"]
        coords_map.setdefault((x, y), []).append(sid)
    
    # Marcar si hay múltiples IDs en las mismas coordenadas
    for coords, ids in coords_map.items():
        if len(ids) > 1:
            for sid in ids:
                star_map[sid]["shared_by_coords"] = True
                star_map[sid]["shared_ids"] = [other for other in ids if other != sid]

    # Burro-global (parámetros del JSON)
    burro_data = {
        "burroenergiaInicial": data.get("burroenergiaInicial", 100),
        "estadoSalud": data.get("estadoSalud", "Desconocido"),
        "pasto": data.get("pasto", 0),
        "number": data.get("number"),
        "startAge": data.get("startAge"),
        "deathAge": data.get("deathAge"),
    }

    return star_map, constellations_list, burro_data, graph