"use client"

import type React from "react"
import { useState } from "react"
import { useAuth } from "@/hooks/use-auth"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

interface LoginFormProps {
  onLoginSuccess: (user: any) => void
}

export function LoginForm({ onLoginSuccess }: LoginFormProps) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const { isLoading, error, login } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const user = await login(email, password)
      onLoginSuccess(user)
    } catch (err) {
      // Error is handled by the hook
      console.log("[v0] Login error handled:", err)
    }
  }

  return (
    <Card className="w-full max-w-md p-8 shadow-lg transition-all duration-300 hover:shadow-xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">Sistema de Gestión</h1>
        <p className="text-sm text-muted-foreground mt-2">Salas UCU</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="email" className="text-sm font-medium text-foreground">
            Correo Electrónico
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="user@ucu.edu.uy"
            className="w-full px-4 py-2 border border-border rounded-lg bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
            disabled={isLoading}
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="password" className="text-sm font-medium text-foreground">
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full px-4 py-2 border border-border rounded-lg bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            required
            disabled={isLoading}
          />
        </div>

        {error && (
          <div className="p-3 bg-destructive/10 border border-destructive/30 rounded-lg animate-in fade-in duration-200">
            <p className="text-sm text-destructive">{error}</p>
            {error.includes("Flask") && (
              <p className="text-xs text-muted-foreground mt-1">
                Asegúrate de que el servidor Flask esté corriendo en http://127.0.0.1:5000
              </p>
            )}
          </div>
        )}

        <Button
          type="submit"
          disabled={isLoading}
          className="w-full mt-6 bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 disabled:opacity-50"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="animate-spin">⏳</span>
              Cargando…
            </span>
          ) : (
            "Iniciar Sesión"
          )}
        </Button>
      </form>
    </Card>
  )
}
