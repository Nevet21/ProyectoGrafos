"""
EditableTreeview - Tabla editable basada en Treeview
Componente reutilizable para crear tablas con celdas editables
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple, Callable, Optional


class EditableTreeview:
    """
    Treeview con celdas editables mediante doble clic.
    Permite validación personalizada y callbacks para cambios.
    """
    
    def __init__(self, parent, columns: List[Tuple[str, str, int]], 
                 editable_columns: List[str] = None):
        """
        Inicializa el Treeview editable.
        
        Args:
            parent: Frame padre
            columns: Lista de tuplas (id, heading, width)
            editable_columns: Lista de IDs de columnas editables
        """
        self.parent = parent
        self.columns = columns
        self.editable_columns = editable_columns or []
        
        # Callbacks para validación y actualización
        self.validation_callback = None
        self.update_callback = None
        
        # Crear widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea el Treeview con scrollbars"""
        # Frame contenedor
        container = tk.Frame(self.parent, bg="#2c3e50")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical")
        hsb = ttk.Scrollbar(container, orient="horizontal")
        
        # Crear Treeview
        column_ids = [col[0] for col in self.columns]
        self.tree = ttk.Treeview(
            container,
            columns=column_ids,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=20
        )
        
        # Configurar scrollbars
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configurar columnas
        for col_id, heading, width in self.columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor="center")
        
        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Bind para edición
        self.tree.bind("<Double-1>", self._on_double_click)
    
    def set_validation_callback(self, callback: Callable):
        """
        Establece función de validación para valores editados.
        
        Args:
            callback: Función (column_id, value) -> validated_value o Exception
        """
        self.validation_callback = callback
    
    def set_update_callback(self, callback: Callable):
        """
        Establece función callback para cuando se actualiza una celda.
        
        Args:
            callback: Función (row_id, column_id, new_value) -> None
        """
        self.update_callback = callback
    
    def insert_row(self, values: tuple, tags: tuple = None):
        """
        Inserta una fila en la tabla.
        
        Args:
            values: Tupla con valores de las columnas
            tags: Tags opcionales para la fila
        """
        return self.tree.insert("", "end", values=values, tags=tags)
    
    def clear(self):
        """Limpia todas las filas de la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_all_rows(self) -> List[Dict]:
        """
        Obtiene todos los datos de la tabla.
        
        Returns:
            Lista de diccionarios con los datos de cada fila
        """
        rows = []
        column_ids = [col[0] for col in self.columns]
        
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            row_data = dict(zip(column_ids, values))
            rows.append(row_data)
        
        return rows
    
    def _on_double_click(self, event):
        """
        Maneja el doble clic en una celda para editarla.
        
        Args:
            event: Evento de mouse
        """
        # Identificar la celda clickeada
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        
        if not row_id:
            return
        
        # Obtener ID de columna
        column_index = int(column.replace("#", "")) - 1
        column_id = self.columns[column_index][0]
        
        # Verificar si la columna es editable
        if column_id not in self.editable_columns:
            return
        
        # Obtener valor actual
        current_value = self.tree.item(row_id)["values"][column_index]
        
        # Crear entry para editar
        self._show_edit_entry(row_id, column, column_index, column_id, current_value)
    
    def _show_edit_entry(self, row_id, column, column_index, column_id, current_value):
        """
        Muestra un Entry para editar el valor de una celda.
        
        Args:
            row_id: ID de la fila
            column: ID de la columna (formato #N)
            column_index: Índice numérico de la columna
            column_id: ID string de la columna
            current_value: Valor actual
        """
        # Obtener bbox de la celda
        bbox = self.tree.bbox(row_id, column)
        if not bbox:
            return
        
        # Crear Entry sobre la celda
        entry = tk.Entry(self.tree, justify="center")
        entry.insert(0, str(current_value))
        entry.select_range(0, tk.END)
        entry.focus()
        
        # Posicionar Entry
        entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        
        def save_edit(event=None):
            """Guarda el valor editado"""
            new_value = entry.get()
            entry.destroy()
            
            # Validar y actualizar
            self._update_cell_value(row_id, column_index, column_id, new_value)
        
        def cancel_edit(event=None):
            """Cancela la edición"""
            entry.destroy()
        
        # Bindings
        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)
        entry.bind("<Escape>", cancel_edit)
    
    def _update_cell_value(self, row_id, column_index, column_id, new_value):
        """
        Actualiza el valor de una celda.
        
        Args:
            row_id: ID de la fila
            column_index: Índice de la columna
            column_id: ID de la columna
            new_value: Nuevo valor (string)
        """
        try:
            # Validar con callback si existe
            if self.validation_callback:
                validated_value = self.validation_callback(column_id, new_value)
            else:
                validated_value = new_value
            
            # Actualizar vista en la tabla
            current_values = list(self.tree.item(row_id)["values"])
            
            # Formatear si es float
            if isinstance(validated_value, float):
                current_values[column_index] = f"{validated_value:.1f}"
            else:
                current_values[column_index] = validated_value
            
            self.tree.item(row_id, values=current_values)
            
            # Llamar callback de actualización si existe
            if self.update_callback:
                self.update_callback(row_id, column_id, validated_value)
            
        except ValueError as e:
            messagebox.showerror(
                "Error de validación",
                f"Valor inválido: {str(e)}\n\nSe mantiene el valor anterior."
            )