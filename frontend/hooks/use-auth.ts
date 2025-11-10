"use client"

import { useState, useCallback, useEffect } from "react"
import { useRouter } from "next/navigation"

export interface User {
  email: string
  role: "student" | "admin"
  name: string
}

interface AuthState {
  user: User | null
  isLoading: boolean
  error: string | null
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: false,
    error: null,
  })
  const router = useRouter()

  const login = useCallback(
    async (email: string, password: string) => {
      setState({ user: null, isLoading: true, error: null })
      try {
        const response = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || "Credenciales incorrectas")
        }

        const data = await response.json()

        if (!data.success) {
          throw new Error("Credenciales incorrectas")
        }

        const user: User = {
          email,
          role: data.rol === "admin" ? "admin" : "student",
          name: email.split("@")[0],
        }

        setState({ user, isLoading: false, error: null })
        localStorage.setItem("user", JSON.stringify(user))

        if (user.role === "admin") {
          router.push("/panel-admin")
        } else {
          router.push("/panel-usuario")
        }

        return user
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : "Error en la autenticación"
        setState({ user: null, isLoading: false, error: errorMsg })
        throw error
      }
    },
    [router],
  )

  const logout = useCallback(() => {
    setState({ user: null, isLoading: false, error: null })
    localStorage.removeItem("user")
    router.push("/") // o "/login" si tenés una ruta dedicada
  }, [router])

  useEffect(() => {
    const handleBeforeUnload = () => {
      localStorage.removeItem("user")
    }
    window.addEventListener("beforeunload", handleBeforeUnload)
    return () => window.removeEventListener("beforeunload", handleBeforeUnload)
  }, [])

  return { ...state, login, logout }
}
