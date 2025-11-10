"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { UserProfileModal } from "@/components/user-profile-modal"
import type { User } from "@/hooks/use-auth"

interface NavbarProps {
  user: User
  onLogout: () => void
}

export function Navbar({ user, onLogout }: NavbarProps) {
  const [showMenu, setShowMenu] = useState(false)
  const [showProfile, setShowProfile] = useState(false)

  return (
    <>
      <nav className="bg-white border-b border-border shadow-sm sticky top-0 z-40 transition-all duration-300">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-12 h-12 rounded flex items-center justify-center overflow-hidden hover:opacity-90 transition-opacity duration-200">
              <img
                src="/logo cucu.png"
                alt="Logo UCU"
                className="w-12 h-12 object-contain"
              />
            </div>
            <span className="font-semibold text-foreground hidden sm:inline">
              {user.role === "admin" ? "Panel Administrativo" : "Mis Reservas"}
            </span>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground hidden sm:inline">{user.email}</span>
            <div className="relative">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowMenu(!showMenu)}
                className="text-foreground hover:bg-secondary transition-all duration-200"
              >
                ⋮
              </Button>
              {showMenu && (
                <Card className="absolute right-0 mt-2 w-48 shadow-lg z-10 animate-in fade-in slide-in-from-top-2 duration-200">
                  <button
                    onClick={() => {
                      setShowMenu(false)
                      setShowProfile(true)
                    }}
                    className="w-full text-left px-4 py-2 text-sm text-foreground hover:bg-secondary transition-colors duration-150"
                  >
                    Mi Perfil
                  </button>
                  <button
                    onClick={() => {
                      setShowMenu(false)
                      onLogout()
                    }}
                    className="w-full text-left px-4 py-2 text-sm text-destructive hover:bg-destructive/5 transition-colors duration-150 border-t border-border"
                  >
                    Cerrar Sesión
                  </button>
                </Card>
              )}
            </div>
          </div>
        </div>
      </nav>

      <UserProfileModal user={user} isOpen={showProfile} onClose={() => setShowProfile(false)} />
    </>
  )
}
