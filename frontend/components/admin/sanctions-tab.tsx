"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Sanction {
  id: string
  personaId: string
  razon: string
  fechaInicio: string
  duracion: number
  activa: boolean
}

export function SanctionsTab() {
  const [sanctions, setSanctions] = useState<Sanction[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    personaId: "",
    razon: "",
    duracion: "",
  })

  useEffect(() => {
    fetchSanctions()
  }, [])

  const fetchSanctions = async () => {
    try {
      const response = await fetch("/api/sanciones")
      if (response.ok) {
        const data = await response.json()
        setSanctions(data)
      }
    } catch (error) {
      console.error("Error fetching sanctions:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const response = await fetch("/api/sanciones", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          duracion: Number.parseInt(formData.duracion),
        }),
      })

      if (response.ok) {
        await fetchSanctions()
        setFormData({ personaId: "", razon: "", duracion: "" })
        setShowForm(false)
      }
    } catch (error) {
      console.error("Error saving sanction:", error)
    }
  }

  const handleLiftSanction = async (id: string) => {
    if (!confirm("¿Está seguro de levantar esta sanción?")) return

    try {
      const response = await fetch(`/api/sanciones/${id}/levantar`, {
        method: "POST",
      })

      if (response.ok) {
        await fetchSanctions()
      }
    } catch (error) {
      console.error("Error lifting sanction:", error)
    }
  }

  const handleDeleteSanction = async (id: string) => {
    if (!confirm("¿Está seguro de eliminar esta sanción?")) return

    try {
      const response = await fetch(`/api/sanciones/${id}`, {
        method: "DELETE",
      })

      if (response.ok) {
        await fetchSanctions()
      }
    } catch (error) {
      console.error("Error deleting sanction:", error)
    }
  }

  if (isLoading) {
    return <div className="text-center py-8 text-muted-foreground">Cargando...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-foreground">Gestión de Sanciones</h2>
        <Button
          onClick={() => {
            setShowForm(!showForm)
            setFormData({ personaId: "", razon: "", duracion: "" })
          }}
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
        >
          {showForm ? "Cancelar" : "+ Nueva Sanción"}
        </Button>
      </div>

      {showForm && (
        <Card className="p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">ID Participante</label>
              <input
                type="text"
                value={formData.personaId}
                onChange={(e) => setFormData({ ...formData, personaId: e.target.value })}
                placeholder="ID del participante"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Razón</label>
              <textarea
                value={formData.razon}
                onChange={(e) => setFormData({ ...formData, razon: e.target.value })}
                placeholder="Motivo de la sanción"
                rows={3}
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Duración (días)</label>
              <input
                type="number"
                value={formData.duracion}
                onChange={(e) => setFormData({ ...formData, duracion: e.target.value })}
                placeholder="Número de días"
                min="1"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
              Crear Sanción
            </Button>
          </form>
        </Card>
      )}

      <div className="grid gap-4">
        {sanctions.map((sanction) => (
          <Card key={sanction.id} className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-medium text-foreground">Participante {sanction.personaId}</h3>
                <p className="text-sm text-muted-foreground mt-1">{sanction.razon}</p>
                <div className="flex gap-3 mt-2 text-xs text-muted-foreground">
                  <span>Inicio: {new Date(sanction.fechaInicio).toLocaleDateString()}</span>
                  <span>Duración: {sanction.duracion} días</span>
                </div>
                <span
                  className={`inline-block mt-2 text-xs px-2 py-1 rounded ${
                    sanction.activa ? "bg-red-100 text-red-700" : "bg-gray-100 text-gray-700"
                  }`}
                >
                  {sanction.activa ? "Activa" : "Levantada"}
                </span>
              </div>
              <div className="flex flex-col gap-2">
                {sanction.activa && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleLiftSanction(sanction.id)}
                    className="text-foreground border-border hover:bg-secondary"
                  >
                    Levantar
                  </Button>
                )}
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => handleDeleteSanction(sanction.id)}
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
