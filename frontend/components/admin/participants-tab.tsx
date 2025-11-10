"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Participant {
  ci: string
  nombre: string
  apellido: string
  email: string
}

export function ParticipantsTab() {
  const [participants, setParticipants] = useState<Participant[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingCi, setEditingCi] = useState<string | null>(null)
  const [formData, setFormData] = useState({
    nombre: "",
    apellido: "",
    email: "",
  })

  useEffect(() => {
    fetchParticipants()
  }, [])

  const fetchParticipants = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/participantes")
      if (response.ok) {
        const data = await response.json()
        setParticipants(data)
      }
    } catch (error) {
      console.error("Error fetching participants:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const method = editingCi ? "PUT" : "POST"
    const url = editingCi ? `http://127.0.0.1:5000/api/participantes/${editingCi}` : "http://127.0.0.1:5000/api/participantes"

    try {
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await fetchParticipants()
        setFormData({ nombre: "", apellido: "", email: "" })
        setShowForm(false)
        setEditingCi(null)
      }
    } catch (error) {
      console.error("Error saving participant:", error)
    }
  }

  const handleDelete = async (ci: string) => {
    if (!confirm("¿Está seguro de eliminar este participante?")) return

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/participantes/${ci}`, {
        method: "DELETE",
      })

      if (response.ok) {
        await fetchParticipants()
      }
    } catch (error) {
      console.error("Error deleting participant:", error)
    }
  }

  const handleEdit = (participant: Participant) => {
    setFormData({
      nombre: participant.nombre,
      apellido: participant.apellido,
      email: participant.email,
    })
    setEditingCi(participant.ci)
    setShowForm(true)
  }

  if (isLoading) {
    return <div className="text-center py-8 text-muted-foreground">Cargando...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-foreground">Gestión de Participantes</h2>
        <Button
          onClick={() => {
            setShowForm(!showForm)
            setEditingCi(null)
            setFormData({ nombre: "", apellido: "", email: "" })
          }}
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
        >
          {showForm ? "Cancelar" : "+ Nuevo Participante"}
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
                placeholder="Nombre"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Apellido</label>
              <input
                type="text"
                value={formData.apellido}
                onChange={(e) => setFormData({ ...formData, apellido: e.target.value })}
                placeholder="Apellido"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="usuario@ucu.edu.uy"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
              {editingCi ? "Actualizar" : "Crear"} Participante
            </Button>
          </form>
        </Card>
      )}

      <div className="grid gap-4">
        {participants.map((participant) => (
          <Card key={participant.ci} className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-foreground">{participant.nombre} {participant.apellido}</h3>
                <p className="text-sm text-muted-foreground">{participant.email}</p>
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleEdit(participant)}
                  className="text-foreground border-border hover:bg-secondary"
                >
                  Editar
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleDelete(participant.ci)}
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
