"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"

export function ReportsTab() {
  const [reportes, setReportes] = useState<Array<{ nombre: string; titulo: string }>>([])
  const [reporteSeleccionado, setReporteSeleccionado] = useState<string | null>(null)
  const [columnas, setColumnas] = useState<string[]>([])
  const [filas, setFilas] = useState<Array<Record<string, any>>>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchReportes = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/reportes")
        if (response.ok) {
          const data = await response.json()
          setReportes(data.reportes || [])
          if (data.reportes && data.reportes.length > 0) {
            setReporteSeleccionado(data.reportes[0].nombre)
          }
        } else {
          setError("Error cargando la lista de reportes")
        }
      } catch (err) {
        setError("Error cargando la lista de reportes")
      }
    }
    fetchReportes()
  }, [])

  useEffect(() => {
    if (!reporteSeleccionado) return

    const fetchReporteData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const response = await fetch(`http://127.0.0.1:5000/reportes/${encodeURIComponent(reporteSeleccionado)}`)
        if (response.ok) {
          const data = await response.json()
          setColumnas(data.columnas || [])
          if (data.filas && Array.isArray(data.filas) && Array.isArray(data.columnas)) {
            const filasObj = data.filas.map((fila: any[]) => {
              const obj: Record<string, any> = {}
              data.columnas.forEach((col: string, idx: number) => {
                obj[col] = fila[idx]
              })
              return obj
            })
            setFilas(filasObj)
          } else {
            setFilas([])
          }
          setError(null)
        } else {
          console.error(`Error fetching report data: ${response.statusText}`)
          setError("Error cargando los datos del reporte")
          setColumnas([])
          setFilas([])
        }
      } catch (err) {
        console.error(err)
        setError("Error cargando los datos del reporte")
        setColumnas([])
        setFilas([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchReporteData()
  }, [reporteSeleccionado])

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-foreground">Reportes y Consultas</h2>

      <Card className="p-6">
        <h3 className="font-semibold text-foreground mb-4">Seleccionar Reporte</h3>
        <div className="flex flex-wrap gap-4">
          {reportes.map((r) => (
            <button
              key={r.nombre}
              className={`px-4 py-2 rounded ${
                r.nombre === reporteSeleccionado ? "bg-primary text-white" : "bg-secondary text-foreground"
              }`}
              onClick={() => setReporteSeleccionado(r.nombre)}
            >
              {r.titulo}
            </button>
          ))}
        </div>
      </Card>

      <Card className="p-6 overflow-auto">
        <h3 className="font-semibold text-foreground mb-4">Datos del Reporte: {reporteSeleccionado}</h3>
        {error && <div className="text-center py-4 text-destructive">{error}</div>}
        {isLoading ? (
          <div className="text-center py-8 text-muted-foreground">Cargando...</div>
        ) : columnas.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">No hay datos para mostrar</div>
        ) : (
          <table className="w-full table-auto border-collapse border border-border">
            <thead>
              <tr>
                {columnas.map((col) => (
                  <th key={col} className="border border-border px-4 py-2 text-left text-sm font-semibold text-foreground bg-muted">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filas.map((fila, idx) => (
                <tr key={idx} className={idx % 2 === 0 ? "bg-muted/50" : ""}>
                  {columnas.map((col) => (
                    <td key={col} className="border border-border px-4 py-2 text-sm text-foreground">
                      {fila[col] != null ? String(fila[col]) : ""}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  )
}
