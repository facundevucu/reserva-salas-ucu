"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import type { User } from "@/hooks/use-auth"
import { StudentDashboard } from "@/components/student-dashboard"

export default function PanelUsuarioPage() {
  const [user, setUser] = useState<User | null>(null)
  const [mounted, setMounted] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    if (!storedUser) {
      router.push("/")
      return
    }

    try {
      const parsedUser = JSON.parse(storedUser)
      if (parsedUser.role !== "student") {
        router.push("/")
        return
      }
      setUser(parsedUser)
    } catch (e) {
      router.push("/")
    }
    setMounted(true)
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem("user")
    router.push("/")
  }

  if (!mounted || !user) return null

  return <StudentDashboard user={user} onLogout={handleLogout} />
}
