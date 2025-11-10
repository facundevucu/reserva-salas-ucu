"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { ParticipantsTab } from "@/components/admin/participants-tab"
import { RoomsTab } from "@/components/admin/rooms-tab"
import { SanctionsTab } from "@/components/admin/sanctions-tab"
import { ReportsTab } from "@/components/admin/reports-tab"

interface AdminTabsProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

export function AdminTabs({ activeTab, onTabChange }: AdminTabsProps) {
  const tabs = [
    { id: "dashboard", label: "Dashboard" },
    { id: "participants", label: "Participantes" },
    { id: "rooms", label: "Salas" },
    { id: "sanctions", label: "Sanciones" },
    { id: "reports", label: "Reportes" },
  ]

  return (
    <>
      {/* Tab Navigation */}
      <div className="flex gap-2 border-b border-border mb-8 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`px-4 py-3 font-medium text-sm border-b-2 transition-all duration-200 whitespace-nowrap ${
              activeTab === tab.id
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground hover:border-primary/30"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="animate-in fade-in duration-300">
        {activeTab === "participants" && <ParticipantsTab />}
        {activeTab === "rooms" && <RoomsTab />}
        {activeTab === "sanctions" && <SanctionsTab />}
        {activeTab === "reports" && <ReportsTab />}
        {activeTab === "dashboard" && <AdminDashboardContent />}
      </div>
    </>
  )
}

function AdminDashboardContent() {
  const [stats, setStats] = useState<{
    total_salas: number | null
    reservas_activas: number | null
    total_participantes: number | null
    sanciones_activas: number | null
  }>({
    total_salas: null,
    reservas_activas: null,
    total_participantes: null,
    sanciones_activas: null,
  })

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/dashboard")
      .then((res) => res.json())
      .then((data) => {
        setStats({
          total_salas: data.total_salas ?? null,
          reservas_activas: data.reservas_activas ?? null,
          total_participantes: data.total_participantes ?? null,
          sanciones_activas: data.sanciones_activas ?? null,
        })
      })
      .catch(() => {
        // Opcional: manejar errores, por ahora dejar nulos
      })
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Total de Salas</p>
        <p className="text-3xl font-bold text-primary">
          {stats.total_salas !== null ? stats.total_salas : "--"}
        </p>
      </Card>
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Reservas Activas</p>
        <p className="text-3xl font-bold text-primary">
          {stats.reservas_activas !== null ? stats.reservas_activas : "--"}
        </p>
      </Card>
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Participantes</p>
        <p className="text-3xl font-bold text-primary">
          {stats.total_participantes !== null ? stats.total_participantes : "--"}
        </p>
      </Card>
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Sanciones Activas</p>
        <p className="text-3xl font-bold text-destructive">
          {stats.sanciones_activas !== null ? stats.sanciones_activas : "--"}
        </p>
      </Card>
    </div>
  )
}
