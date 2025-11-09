"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"

interface Reservation {
  id: string
  sala: string
  edificio: string
  fecha: string
  turno: string
  participantes: number
  estado: "activa" | "cancelada" | "finalizada"
}

interface ReservationListProps {
  userEmail: string
}

export function ReservationList({ userEmail }: ReservationListProps) {
  const [reservations, setReservations] = useState<Reservation[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const response = await fetch(`/api/reservations?email=${userEmail}`)
        if (response.ok) {
          const data = await response.json()
          setReservations(data)
        }
      } catch (error) {
        console.error("Error fetching reservations:", error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchReservations()
  }, [userEmail])

  const getStatusColor = (estado: string) => {
    switch (estado) {
      case "activa":
        return "bg-green-50 border-green-200 hover:bg-green-100/50 transition-colors"
      case "cancelada":
        return "bg-red-50 border-red-200 hover:bg-red-100/50 transition-colors"
      case "finalizada":
        return "bg-gray-50 border-gray-200 hover:bg-gray-100/50 transition-colors"
      default:
        return "bg-secondary hover:bg-secondary/80 transition-colors"
    }
  }

  const getStatusLabel = (estado: string) => {
    const labels: { [key: string]: string } = {
      activa: "Activa",
      cancelada: "Cancelada",
      finalizada: "Finalizada",
    }
    return labels[estado] || estado
  }

  if (isLoading) {
    return (
      <Card className="p-8 text-center">
        <p className="text-muted-foreground">Cargando reservas...</p>
      </Card>
    )
  }

  if (reservations.length === 0) {
    return (
      <Card className="p-8 text-center">
        <p className="text-muted-foreground">No hay reservas</p>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-foreground">Mis Reservas</h2>
      {reservations.map((reservation) => (
        <Card key={reservation.id} className={`p-4 border-l-4 ${getStatusColor(reservation.estado)}`}>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <h3 className="font-semibold text-foreground">
                  {reservation.sala} - {reservation.edificio}
                </h3>
                <span className="text-xs px-2 py-1 bg-primary/10 text-primary rounded transition-all duration-200">
                  {getStatusLabel(reservation.estado)}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-sm text-muted-foreground">
                <p>📅 {new Date(reservation.fecha).toLocaleDateString()}</p>
                <p>🕐 {reservation.turno}</p>
                <p>👥 {reservation.participantes} participantes</p>
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  )
}
