"use client"

import type React from "react"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface ReservationPanelProps {
  onSuccess: () => void
}

export function ReservationPanel({ onSuccess }: ReservationPanelProps) {
  const [formData, setFormData] = useState({
    sala: "",
    edificio: "",
    fecha: "",
    turno: "",
    participantes: "",
  })
  const [error, setError] = useState("")
  const [success, setSuccess] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess(false)
    setIsLoading(true)

    try {
      if (!formData.sala || !formData.edificio || !formData.fecha || !formData.turno || !formData.participantes) {
        throw new Error("Todos los campos son requeridos")
      }

      const response = await fetch("/api/reservations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          participantes: Number.parseInt(formData.participantes),
        }),
      })

      if (!response.ok) {
        throw new Error("Error creating reservation")
      }

      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
      setFormData({ sala: "", edificio: "", fecha: "", turno: "", participantes: "" })
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error creating reservation")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="p-6 sticky top-24 transition-all duration-300">
      <h2 className="text-lg font-semibold text-foreground mb-4">Nueva Reserva</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Sala</label>
          <input
            type="text"
            value={formData.sala}
            onChange={(e) => setFormData({ ...formData, sala: e.target.value })}
            placeholder="Ej: Sala 101"
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
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
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Fecha</label>
          <input
            type="date"
            value={formData.fecha}
            onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Turno</label>
          <select
            value={formData.turno}
            onChange={(e) => setFormData({ ...formData, turno: e.target.value })}
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
          >
            <option value="">Seleccionar...</option>
            <option value="mañana">Mañana (8:00 - 12:00)</option>
            <option value="tarde">Tarde (12:00 - 17:00)</option>
            <option value="noche">Noche (17:00 - 22:00)</option>
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Participantes</label>
          <input
            type="number"
            value={formData.participantes}
            onChange={(e) => setFormData({ ...formData, participantes: e.target.value })}
            placeholder="Número de participantes"
            min="1"
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
          />
        </div>

        {error && (
          <div className="p-3 bg-destructive/10 border border-destructive/30 rounded-lg animate-in fade-in duration-200">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        {success && (
          <div className="p-3 bg-green-50 border border-green-200 rounded-lg animate-in fade-in duration-200">
            <p className="text-sm text-green-700">Reserva creada exitosamente</p>
          </div>
        )}

        <Button
          type="submit"
          disabled={isLoading}
          className="w-full bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 disabled:opacity-50"
        >
          {isLoading ? "Creando..." : "Crear Reserva"}
        </Button>
      </form>
    </Card>
  )
}
