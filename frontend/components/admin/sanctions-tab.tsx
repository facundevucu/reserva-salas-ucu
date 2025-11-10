"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Sanction {
  ci_participante: number
  nombre?: string
  apellido?: string
  fecha_inicio: string
  fecha_fin: string
}

export function SanctionsTab() {
  const [sanctions, setSanctions] = useState<Sanction[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    ci_participante: "",
    fecha_inicio: "",
    fecha_fin: "",
  })

  useEffect(() => {
    fetchSanctions()
  }, [])

  const fetchSanctions = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/sanciones")
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
      const response = await fetch("http://127.0.0.1:5000/api/sanciones", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ci_participante: Number(formData.ci_participante),
          fecha_inicio: formData.fecha_inicio,
          fecha_fin: formData.fecha_fin,
        }),
      })

      if (response.ok) {
        await fetchSanctions()
        setFormData({ ci_participante: "", fecha_inicio: "", fecha_fin: "" })
        setShowForm(false)
      }
    } catch (error) {
      console.error("Error saving sanction:", error)
    }
  }

  const handleDeleteSanction = async (ci_participante: number, fecha_inicio: string) => {
    if (!confirm("¿Está seguro de eliminar esta sanción?")) return

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/sanciones`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ci_participante, fecha_inicio }),
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
            setFormData({ ci_participante: "", fecha_inicio: "", fecha_fin: "" })
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
              <label className="text-sm font-medium text-foreground">CI Participante</label>
              <input
                type="number"
                value={formData.ci_participante}
                onChange={(e) => setFormData({ ...formData, ci_participante: e.target.value })}
                placeholder="CI del participante"
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Fecha Inicio</label>
              <input
                type="date"
                value={formData.fecha_inicio}
                onChange={(e) => setFormData({ ...formData, fecha_inicio: e.target.value })}
                className="w-full px-3 py-2 border border-border rounded-lg bg-white text-foreground"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Fecha Fin</label>
              <input
                type="date"
                value={formData.fecha_fin}
                onChange={(e) => setFormData({ ...formData, fecha_fin: e.target.value })}
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
        {sanctions.map((sanction) => {
          const startDate = new Date(sanction.fecha_inicio)
          const endDate = new Date(sanction.fecha_fin)
          const duration = Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 3600 * 24))
          return (
            <Card key={`${sanction.ci_participante}-${sanction.fecha_inicio}`} className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="font-medium text-foreground">
                    Participante {sanction.ci_participante}
                    {sanction.nombre && ` - ${sanction.nombre}`}
                    {sanction.apellido && ` ${sanction.apellido}`}
                  </h3>
                  <div className="flex gap-3 mt-2 text-xs text-muted-foreground">
                    <span>Inicio: {startDate.toLocaleDateString()}</span>
                    <span>Fin: {endDate.toLocaleDateString()}</span>
                    <span>Duración: {duration} días</span>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => handleDeleteSanction(sanction.ci_participante, sanction.fecha_inicio)}
                    className="text-destructive hover:bg-destructive/10"
                  >
                    Eliminar
                  </Button>
                </div>
              </div>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
