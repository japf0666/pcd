#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaz Gráfica (GUI) con tkinter para AgenciaAlquiler.
Implementa 3 paneles scrollables (vehículos, clientes, contratos)
con funcionalidad equivalente a UIInterface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from alquiler_vehiculos import (
    AgenciaAlquiler, Vehiculo, Coche, Bicicleta, Cliente, ContratoAlquiler
)


class GUInterface:
    """Interfaz gráfica con tkinter para AgenciaAlquiler."""
    
    def __init__(self, root, agencia):
        """Inicializa la GUI con una instancia de AgenciaAlquiler.
        
        Args:
            root: ventana tkinter raíz
            agencia: instancia de AgenciaAlquiler
        """
        if not isinstance(agencia, AgenciaAlquiler):
            raise TypeError("agencia debe ser una instancia de AgenciaAlquiler")
        
        self.root = root
        self.agencia = agencia
        self.root.title("Agencia de Alquiler de Vehículos")
        self.root.geometry("1000x600")
        
        # Inicializar referencias a listbox
        self.listbox_vehiculos = None
        self.listbox_clientes = None
        self.listbox_contratos = None
        self.info_label = None
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la estructura de la interfaz gráfica."""
        # Panel principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (3 paneles scrollables)
        left_frame = ttk.LabelFrame(main_frame, text="Información", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self._crear_paneles_scrollables(left_frame)
        
        # Panel derecho (controles y acciones)
        right_frame = ttk.LabelFrame(main_frame, text="Operaciones", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        self._crear_panel_controles(right_frame)
        
        # Actualizar listados al final
        self._actualizar_listados()
    
    def _crear_paneles_scrollables(self, parent):
        """Crea los 3 paneles scrollables (vehículos, clientes, contratos)."""
        
        # Panel de Vehículos
        self._crear_panel_listado(parent, "Vehículos", 0)
        
        # Panel de Clientes
        self._crear_panel_listado(parent, "Clientes", 1)
        
        # Panel de Contratos
        self._crear_panel_listado(parent, "Contratos Activos", 2)
    
    def _crear_panel_listado(self, parent, titulo, row):
        """Crea un panel scrollable individual.
        
        Args:
            parent: widget padre
            titulo: título del panel
            row: fila en la que posicionar
        """
        frame = ttk.LabelFrame(parent, text=titulo, padding=5)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Crear listbox con scrollbar
        scroll_frame = ttk.Frame(frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            scroll_frame, 
            yscrollcommand=scrollbar.set,
            height=8,
            width=40,
            font=("Courier", 9)
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Guardar referencia según tipo
        if titulo == "Vehículos":
            self.listbox_vehiculos = listbox
        elif titulo == "Clientes":
            self.listbox_clientes = listbox
        elif titulo == "Contratos Activos":
            self.listbox_contratos = listbox
    
    def _crear_panel_controles(self, parent):
        """Crea el panel de controles y operaciones."""
        
        # === AGREGAR VEHÍCULO ===
        frame_vehiculo = ttk.LabelFrame(parent, text="Agregar Vehículo", padding=5)
        frame_vehiculo.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            frame_vehiculo,
            text="+ Agregar Coche",
            command=self._agregar_coche
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            frame_vehiculo,
            text="+ Agregar Bicicleta",
            command=self._agregar_bicicleta
        ).pack(fill=tk.X, pady=2)
        
        # === AGREGAR CLIENTE ===
        frame_cliente = ttk.LabelFrame(parent, text="Agregar Cliente", padding=5)
        frame_cliente.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            frame_cliente,
            text="+ Nuevo Cliente",
            command=self._agregar_cliente
        ).pack(fill=tk.X, pady=2)
        
        # === ALQUILAR ===
        frame_alquiler = ttk.LabelFrame(parent, text="Alquiler", padding=5)
        frame_alquiler.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            frame_alquiler,
            text="🚗 Alquilar Vehículo",
            command=self._alquilar_vehiculo
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            frame_alquiler,
            text="↩️ Devolver Vehículo",
            command=self._devolver_vehiculo
        ).pack(fill=tk.X, pady=2)
        
        # === BÚSQUEDA ===
        frame_buscar = ttk.LabelFrame(parent, text="Búsqueda", padding=5)
        frame_buscar.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            frame_buscar,
            text="🔍 Buscar por Modelo",
            command=self._buscar_modelo
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            frame_buscar,
            text="🔍 Buscar Disponibles",
            command=self._buscar_disponibles
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            frame_buscar,
            text="🔍 Buscar por Año",
            command=self._buscar_por_anno
        ).pack(fill=tk.X, pady=2)
        
        # === ACTUALIZAR ===
        frame_actualizar = ttk.LabelFrame(parent, text="Actualizar", padding=5)
        frame_actualizar.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            frame_actualizar,
            text="🔄 Actualizar Listas",
            command=self._actualizar_listados
        ).pack(fill=tk.X, pady=2)
        
        # Separador vertical
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # === INFORMACIÓN ===
        self.info_label = ttk.Label(parent, text="Listo", foreground="green")
        self.info_label.pack(fill=tk.X, pady=5)
    
    def _actualizar_listados(self):
        """Actualiza los tres listados."""
        self._actualizar_vehiculos()
        self._actualizar_clientes()
        self._actualizar_contratos()
    
    def _actualizar_vehiculos(self):
        """Actualiza el listbox de vehículos."""
        self.listbox_vehiculos.delete(0, tk.END)
        for v in self.agencia.vehiculos:
            estado = "✓ Disponible" if v.disponible else "✗ Alquilado"
            texto = f"{v.vehiculo_id}: {v.modelo} ({v.año}) - {estado}"
            self.listbox_vehiculos.insert(tk.END, texto)
    
    def _actualizar_clientes(self):
        """Actualiza el listbox de clientes."""
        self.listbox_clientes.delete(0, tk.END)
        for c in self.agencia.clientes:
            texto = f"{c.cliente_id}: {c.nombre} - {c.contacto}"
            self.listbox_clientes.insert(tk.END, texto)
    
    def _actualizar_contratos(self):
        """Actualiza el listbox de contratos activos."""
        self.listbox_contratos.delete(0, tk.END)
        contratos_activos = [c for c in self.agencia.contratos if not c.finalizado]
        for c in contratos_activos:
            texto = f"{c.id}: {c.cliente.nombre} - {c.vehiculo.modelo} ({c.dias}d)"
            self.listbox_contratos.insert(tk.END, texto)
    
    def _agregar_coche(self):
        """Agregar un nuevo coche."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Coche")
        dialog.geometry("300x280")
        
        ttk.Label(dialog, text="ID Vehículo:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        entry_id = ttk.Entry(dialog, width=25)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Modelo:").grid(row=1, sticky=tk.W, padx=10, pady=5)
        entry_modelo = ttk.Entry(dialog, width=25)
        entry_modelo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Año:").grid(row=2, sticky=tk.W, padx=10, pady=5)
        entry_anno = ttk.Entry(dialog, width=25)
        entry_anno.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Tarifa Diaria:").grid(row=3, sticky=tk.W, padx=10, pady=5)
        entry_tarifa = ttk.Entry(dialog, width=25)
        entry_tarifa.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Número de Puertas:").grid(row=4, sticky=tk.W, padx=10, pady=5)
        entry_puertas = ttk.Entry(dialog, width=25)
        entry_puertas.grid(row=4, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                vid = entry_id.get().strip()
                modelo = entry_modelo.get().strip()
                anno = int(entry_anno.get())
                tarifa = float(entry_tarifa.get())
                puertas = int(entry_puertas.get())
                
                if not vid or not modelo:
                    messagebox.showwarning("Error", "ID y Modelo son requeridos")
                    return
                
                self.agencia.agregar_vehiculo(Coche(vid, modelo, anno, tarifa, puertas))
                messagebox.showinfo("Éxito", f"Coche '{modelo}' agregado correctamente")
                self._actualizar_listados()
                self._actualizar_info(f"Coche agregado: {modelo}")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Verifique los datos numéricos")
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=20)
    
    def _agregar_bicicleta(self):
        """Agregar una nueva bicicleta."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Bicicleta")
        dialog.geometry("300x280")
        
        ttk.Label(dialog, text="ID Vehículo:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        entry_id = ttk.Entry(dialog, width=25)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Modelo:").grid(row=1, sticky=tk.W, padx=10, pady=5)
        entry_modelo = ttk.Entry(dialog, width=25)
        entry_modelo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Año:").grid(row=2, sticky=tk.W, padx=10, pady=5)
        entry_anno = ttk.Entry(dialog, width=25)
        entry_anno.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Tarifa Diaria:").grid(row=3, sticky=tk.W, padx=10, pady=5)
        entry_tarifa = ttk.Entry(dialog, width=25)
        entry_tarifa.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Número de Piñones:").grid(row=4, sticky=tk.W, padx=10, pady=5)
        entry_pinnones = ttk.Entry(dialog, width=25)
        entry_pinnones.grid(row=4, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                vid = entry_id.get().strip()
                modelo = entry_modelo.get().strip()
                anno = int(entry_anno.get())
                tarifa = float(entry_tarifa.get())
                pinnones = int(entry_pinnones.get())
                
                if not vid or not modelo:
                    messagebox.showwarning("Error", "ID y Modelo son requeridos")
                    return
                
                self.agencia.agregar_vehiculo(Bicicleta(vid, modelo, anno, tarifa, pinnones))
                messagebox.showinfo("Éxito", f"Bicicleta '{modelo}' agregada correctamente")
                self._actualizar_listados()
                self._actualizar_info(f"Bicicleta agregada: {modelo}")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Verifique los datos numéricos")
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=20)
    
    def _agregar_cliente(self):
        """Agregar un nuevo cliente."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Cliente")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="ID Cliente:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        entry_id = ttk.Entry(dialog, width=25)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Nombre:").grid(row=1, sticky=tk.W, padx=10, pady=5)
        entry_nombre = ttk.Entry(dialog, width=25)
        entry_nombre.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Contacto:").grid(row=2, sticky=tk.W, padx=10, pady=5)
        entry_contacto = ttk.Entry(dialog, width=25)
        entry_contacto.grid(row=2, column=1, padx=10, pady=5)
        
        def guardar():
            cid = entry_id.get().strip()
            nombre = entry_nombre.get().strip()
            contacto = entry_contacto.get().strip()
            
            if not cid or not nombre:
                messagebox.showwarning("Error", "ID y Nombre son requeridos")
                return
            
            self.agencia.agregar_cliente(Cliente(cid, nombre, contacto))
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado correctamente")
            self._actualizar_listados()
            self._actualizar_info(f"Cliente agregado: {nombre}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=20)
    
    def _alquilar_vehiculo(self):
        """Alquilar un vehículo."""
        if not self.agencia.clientes or not self.agencia.vehiculos:
            messagebox.showwarning("Error", "Se requieren clientes y vehículos registrados")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Alquilar Vehículo")
        dialog.geometry("300x180")
        
        ttk.Label(dialog, text="ID Cliente:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        entry_cliente = ttk.Entry(dialog, width=25)
        entry_cliente.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="ID Vehículo:").grid(row=1, sticky=tk.W, padx=10, pady=5)
        entry_vehiculo = ttk.Entry(dialog, width=25)
        entry_vehiculo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Número de Días:").grid(row=2, sticky=tk.W, padx=10, pady=5)
        entry_dias = ttk.Entry(dialog, width=25)
        entry_dias.grid(row=2, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                cliente_id = entry_cliente.get().strip()
                vehiculo_id = entry_vehiculo.get().strip()
                dias = int(entry_dias.get())
                
                self.agencia.alquilar_vehiculo(cliente_id, vehiculo_id, dias)
                messagebox.showinfo("Éxito", "Vehículo alquilado correctamente")
                self._actualizar_listados()
                self._actualizar_info("Vehículo alquilado")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Los días deben ser un número")
        
        ttk.Button(dialog, text="Alquilar", command=guardar).grid(row=3, column=0, columnspan=2, pady=20)
    
    def _devolver_vehiculo(self):
        """Devolver un vehículo."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Devolver Vehículo")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="ID Cliente:").grid(row=0, sticky=tk.W, padx=10, pady=5)
        entry_cliente = ttk.Entry(dialog, width=25)
        entry_cliente.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="ID Vehículo:").grid(row=1, sticky=tk.W, padx=10, pady=5)
        entry_vehiculo = ttk.Entry(dialog, width=25)
        entry_vehiculo.grid(row=1, column=1, padx=10, pady=5)
        
        def guardar():
            cliente_id = entry_cliente.get().strip()
            vehiculo_id = entry_vehiculo.get().strip()
            
            self.agencia.devolver_vehiculo(cliente_id, vehiculo_id)
            messagebox.showinfo("Éxito", "Vehículo devuelto correctamente")
            self._actualizar_listados()
            self._actualizar_info("Vehículo devuelto")
            dialog.destroy()
        
        ttk.Button(dialog, text="Devolver", command=guardar).grid(row=2, column=0, columnspan=2, pady=20)
    
    def _buscar_modelo(self):
        """Buscar vehículos por modelo."""
        modelo = simpledialog.askstring("Buscar por Modelo", "Ingrese modelo (parcial):")
        if modelo:
            resultados = self.agencia.buscar_vehiculo(modelo)
            self._mostrar_resultados(resultados, "Búsqueda por Modelo")
    
    def _buscar_disponibles(self):
        """Buscar vehículos disponibles."""
        resultados = self.agencia.buscar_vehiculo_por(lambda v: v.disponible)
        self._mostrar_resultados(resultados, "Vehículos Disponibles")
    
    def _buscar_por_anno(self):
        """Buscar vehículos por año mínimo."""
        try:
            anno_min = simpledialog.askinteger("Buscar por Año", "Anno mínimo:")
            if anno_min:
                resultados = self.agencia.buscar_vehiculo_por(lambda v: v.año >= anno_min)
                self._mostrar_resultados(resultados, f"Vehículos desde {anno_min}")
        except (ValueError, TypeError):
            pass
    
    def _mostrar_resultados(self, resultados, titulo):
        """Muestra los resultados de búsqueda en una ventana."""
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("400x300")
        
        if not resultados:
            ttk.Label(dialog, text="No se encontraron resultados").pack(pady=20)
        else:
            text = tk.Text(dialog, width=50, height=15, font=("Courier", 9))
            text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            for v in resultados:
                text.insert(tk.END, f"{v}\n\n")
            
            text.config(state=tk.DISABLED)
    
    def _actualizar_info(self, mensaje):
        """Actualiza el label de información."""
        self.info_label.config(text=mensaje, foreground="blue")
        self.root.after(3000, lambda: self.info_label.config(text="Listo", foreground="green"))


def main():
    """Función principal para ejecutar la GUI."""
    root = tk.Tk()
    
    # Crear agencia de demostración
    agencia = AgenciaAlquiler()
    
    # Agregar datos de prueba
    agencia.agregar_vehiculo(Coche("C001", "Toyota Corolla", 2022, 50.0, 4))
    agencia.agregar_vehiculo(Coche("C002", "Honda Civic", 2021, 55.0, 2))
    agencia.agregar_vehiculo(Bicicleta("B001", "Trek X-Caliber", 2023, 15.0, 21))
    agencia.agregar_vehiculo(Bicicleta("B002", "Specialized Hardrock", 2022, 12.0, 18))
    
    agencia.agregar_cliente(Cliente("CLI001", "Juan Pérez", "juan@email.com"))
    agencia.agregar_cliente(Cliente("CLI002", "María García", "maria@email.com"))
    
    # Crear GUI
    gui = GUInterface(root, agencia)
    
    root.mainloop()


if __name__ == "__main__":
    main()
