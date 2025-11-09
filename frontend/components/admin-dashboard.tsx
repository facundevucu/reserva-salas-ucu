"use client"

import { useState } from "react"
import { Navbar } from "@/components/navbar"
import { AdminTabs } from "@/components/admin-tabs"
import type { User } from "@/hooks/use-auth"

interface AdminDashboardProps {
  user: User
  onLogout: () => void
}

export function AdminDashboard({ user, onLogout }: AdminDashboardProps) {
  const [activeTab, setActiveTab] = useState("dashboard")

  return (
    <div className="min-h-screen bg-background">
      <Navbar user={user} onLogout={onLogout} />

      <main className="max-w-7xl mx-auto px-4 py-8">
        <AdminTabs activeTab={activeTab} onTabChange={setActiveTab} />
      </main>
    </div>
  )
}
