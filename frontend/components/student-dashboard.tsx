"use client"

import { useState } from "react"
import { Navbar } from "@/components/navbar"
import { ReservationPanel } from "@/components/reservation-panel"
import { ReservationList } from "@/components/reservation-list"
import type { User } from "@/hooks/use-auth"

interface StudentDashboardProps {
  user: User
  onLogout: () => void
}

export function StudentDashboard({ user, onLogout }: StudentDashboardProps) {
  const [activeTab, setActiveTab] = useState("reservations")
  const [refreshKey, setRefreshKey] = useState(0)

  return (
    <div className="min-h-screen bg-background">
      <Navbar user={user} onLogout={onLogout} />

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Sidebar - Form */}
          <div className="lg:col-span-1">
            <ReservationPanel onSuccess={() => setRefreshKey((k) => k + 1)} />
          </div>

          {/* Right Content - List */}
          <div className="lg:col-span-2">
            <ReservationList key={refreshKey} userEmail={user.email} />
          </div>
        </div>
      </main>
    </div>
  )
}
