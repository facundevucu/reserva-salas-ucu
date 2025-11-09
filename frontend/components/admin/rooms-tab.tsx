"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Room {
  id: string
  nombre: string
  edificio: string
  capacidad: number
  disponible: boolean
}

export function RoomsTab() {
  const [rooms, setRooms] = useState<Room[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    nombre: "",
    edificio: "",
    capacidad: "",
  })

  useEffect(() => {
    fetchRooms()
  }, [])

  const fetchRooms = async () => {
    try {
      const response = await fetch("/api/salas")
      if (response.ok) {
        const data = await response.json()
        setRooms(data)
      }
    } catch (error) {
      console.error("Error fetching rooms:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const method = editingId ? "PUT" : "POST"
    const url = editingId ? `/api/salas/${editingId}` : "/api/salas"

    try {
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          capacidad: Number.parseInt(formData.capacidad),
        }),
      })

      if (response.ok) {
        await fetchRooms()
        setFormData({ nombre: "", edificio: "", capacidad: "" })
        setShowForm(false)
        setEditingId(null)
      }
    } catch (error) {
      console.error("Error saving room:", error)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm("¿Está seguro de eliminar esta sala?")) return

    try {
      const response = await fetch(`/api/salas/${id}`, {
        method: "DELETE",
      })

      if (response.ok) {
        await fetchRooms()
      }
    } catch (error) {
      console.error("Error deleting room:", error)
    }
  }

  const handleEdit = (room: Room) => {
    setFormData({
      nombre: room.nombre,
      edificio: room.edificio,
      capacidad: room.capacidad.toString(),
    })
    setEditingId(room.id)
    setShowForm(true)
  }

  if (isLoading) {
    return <div className="text-center py-8 text-muted-foreground">Cargando...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-foreground">Gestión de Salas</h2>
        <Button
          onClick={() => {
            setShowForm(!showForm)
            setEditingId(null)
            setFormData({ nombre: "", edificio: "", capacidad: "" })
          }}
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
        >
          {showForm ? "Cancelar" : "+ Nueva Sala"}
        </Button>
      </div>

      {showForm && (
        <Card className="p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Nombre</label>
              <input
                type="text"
                value={formData.nombre}
                onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                placeholder="Ej: Sala 101"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Edificio</label>
              <input
                type="text"
                value={formData.edificio}
                onChange={(e) => setFormData({ ...formData, edificio: e.target.value })}
                placeholder="Ej: A"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Capacidad</label>
              <input
                type="number"
                value={formData.capacidad}
                onChange={(e) => setFormData({ ...formData, capacidad: e.target.value })}
                placeholder="Número de personas"
                min="1"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
              {editingId ? "Actualizar" : "Crear"} Sala
            </Button>
          </form>
        </Card>
      )}

      <div className="grid gap-4">
        {rooms.map((room) => (
          <Card key={room.id} className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-foreground">{room.nombre}</h3>
                <p className="text-sm text-muted-foreground">
                  Edificio {room.edificio} - Capacidad: {room.capacidad} personas
                </p>
                <span
                  className={`inline-block mt-2 text-xs px-2 py-1 rounded ${
                    room.disponible ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                  }`}
                >
                  {room.disponible ? "Disponible" : "No disponible"}
                </span>
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleEdit(room)}
                  className="text-foreground border-border hover:bg-secondary"
                >
                  Editar
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleDelete(room.id)}
                  className="text-destructive hover:bg-destructive/10"
                >
                  Eliminar
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
