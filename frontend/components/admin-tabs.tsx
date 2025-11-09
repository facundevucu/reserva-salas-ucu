"use client"

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
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Total de Salas</p>
        <p className="text-3xl font-bold text-primary">--</p>
      </Card>
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Reservas Activas</p>
        <p className="text-3xl font-bold text-primary">--</p>
      </Card>
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Participantes</p>
        <p className="text-3xl font-bold text-primary">--</p>
      </Card>
      <Card className="p-6 transition-all duration-200 hover:shadow-md hover:scale-105">
        <p className="text-sm text-muted-foreground mb-2">Sanciones Activas</p>
        <p className="text-3xl font-bold text-destructive">--</p>
      </Card>
    </div>
  )
}
