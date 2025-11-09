"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"

interface ReportData {
  roomsReserved: Array<{ room: string; count: number }>
  turnsRequested: Array<{ turn: string; count: number }>
  avgParticipants: number
  occupancyByBuilding: Array<{ building: string; percentage: number }>
  activeSanctions: number
}

export function ReportsTab() {
  const [reportData, setReportData] = useState<ReportData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const response = await fetch("/api/reportes")
      if (response.ok) {
        const data = await response.json()
        setReportData(data)
      }
    } catch (error) {
      console.error("Error fetching reports:", error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return <div className="text-center py-8 text-muted-foreground">Cargando...</div>
  }

  if (!reportData) {
    return <div className="text-center py-8 text-muted-foreground">Error cargando reportes</div>
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-foreground">Reportes y Consultas</h2>

      {/* Most Reserved Rooms */}
      <Card className="p-6">
        <h3 className="font-semibold text-foreground mb-4">Salas Más Reservadas</h3>
        <div className="space-y-3">
          {reportData.roomsReserved.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between">
              <span className="text-sm text-foreground">{item.room}</span>
              <div className="flex items-center gap-2">
                <div className="w-32 bg-secondary rounded-full h-2">
                  <div
                    className="bg-primary rounded-full h-2 transition-all"
                    style={{
                      width: `${Math.min(
                        (item.count / Math.max(...reportData.roomsReserved.map((r) => r.count))) * 100,
                        100,
                      )}%`,
                    }}
                  />
                </div>
                <span className="text-sm font-medium text-foreground w-8">{item.count}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Most Requested Turns */}
      <Card className="p-6">
        <h3 className="font-semibold text-foreground mb-4">Turnos Más Demandados</h3>
        <div className="grid grid-cols-3 gap-4">
          {reportData.turnsRequested.map((item, idx) => (
            <div key={idx} className="text-center">
              <p className="text-2xl font-bold text-primary">{item.count}</p>
              <p className="text-xs text-muted-foreground mt-1">{item.turn}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Average Participants */}
      <Card className="p-6">
        <h3 className="font-semibold text-foreground mb-4">Promedio de Participantes por Sala</h3>
        <p className="text-3xl font-bold text-primary">{reportData.avgParticipants.toFixed(1)}</p>
      </Card>

      {/* Occupancy by Building */}
      <Card className="p-6">
        <h3 className="font-semibold text-foreground mb-4">Porcentaje de Ocupación por Edificio</h3>
        <div className="space-y-4">
          {reportData.occupancyByBuilding.map((item, idx) => (
            <div key={idx}>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-foreground">Edificio {item.building}</span>
                <span className="text-sm text-muted-foreground">{item.percentage}%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-2">
                <div
                  className="bg-primary rounded-full h-2 transition-all"
                  style={{ width: `${Math.min(item.percentage, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Active Sanctions */}
      <Card className="p-6">
        <h3 className="font-semibold text-foreground mb-4">Sanciones Activas</h3>
        <p className="text-3xl font-bold text-destructive">{reportData.activeSanctions}</p>
      </Card>
    </div>
  )
}
