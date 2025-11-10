"use client"

import type React from "react"

import { useState, useEffect } from "react"
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
    hora: "",
    participantes: "",
  })
  const [edificios, setEdificios] = useState<string[]>([])
  const [salas, setSalas] = useState<{ nombre: string; edificio: string; capacidad: number }[]>([])
  const [horas, setHoras] = useState<string[]>([])
  const [error, setError] = useState("")
  const [success, setSuccess] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/edificios")
      .then((res) => res.json())
      .then((data) => setEdificios(data))
      .catch((err) => console.error("Error cargando edificios:", err))
  }, [])

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/salas")
      .then((res) => res.json())
      .then((data) => setSalas(data))
      .catch((err) => console.error("Error cargando salas:", err))
  }, [])

  const salasFiltradas = formData.edificio
    ? salas.filter((s) => s.edificio === formData.edificio)
    : salas

  const edificiosFiltrados = formData.sala
    ? edificios.filter(
        (e) => salas.find((s) => s.nombre === formData.sala)?.edificio === e
      )
    : edificios

  const capacidadMax = formData.sala
    ? salas.find((s) => s.nombre === formData.sala)?.capacidad || ""
    : ""

  useEffect(() => {
    if (formData.turno === "mañana") {
      setHoras(["08:00", "09:00", "10:00", "11:00"])
    } else if (formData.turno === "tarde") {
      setHoras(["12:00", "13:00", "14:00", "15:00", "16:00"])
    } else if (formData.turno === "noche") {
      setHoras(["17:00", "18:00", "19:00", "20:00", "21:00"])
    } else {
      setHoras([])
    }
  }, [formData.turno])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess(false)
    setIsLoading(true)

    try {
      if (!formData.sala || !formData.edificio || !formData.fecha || !formData.turno || !formData.hora || !formData.participantes) {
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
      setFormData({ sala: "", edificio: "", fecha: "", turno: "", hora: "", participantes: "" })
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
          <select
            value={formData.sala}
            onChange={(e) => {
              const salaSeleccionada = e.target.value
              const edificioRelacionado = salas.find((s) => s.nombre === salaSeleccionada)?.edificio || ""
              setFormData({ ...formData, sala: salaSeleccionada, edificio: edificioRelacionado })
            }}
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
          >
            <option value="">Seleccionar sala...</option>
            {salasFiltradas.map((s) => (
              <option key={s.nombre} value={s.nombre}>{s.nombre}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Edificio</label>
          <select
            value={formData.edificio}
            onChange={(e) => setFormData({ ...formData, edificio: e.target.value, sala: "" })}
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
          >
            <option value="">Seleccionar edificio...</option>
            {edificiosFiltrados.map((e) => (
              <option key={e} value={e}>{e}</option>
            ))}
          </select>
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
          <label className="text-sm font-medium text-foreground">Hora</label>
          <select
            value={formData.hora}
            onChange={(e) => setFormData({ ...formData, hora: e.target.value })}
            className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
            disabled={!formData.turno}
          >
            <option value="">Seleccionar hora...</option>
            {horas.map((h) => (
              <option key={h} value={h}>{h}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Participantes</label>
          <input
            type="number"
            value={formData.participantes}
            onChange={(e) => {
              const value = Number(e.target.value)
              if (!capacidadMax || value <= capacidadMax) {
                setFormData({ ...formData, participantes: e.target.value })
              }
            }}
            placeholder={
              capacidadMax
                ? `Hasta ${capacidadMax} participantes`
                : "Selecciona una sala primero"
            }
            max={capacidadMax || undefined}
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
