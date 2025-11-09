"use client"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { User } from "@/hooks/use-auth"

interface UserProfileModalProps {
  user: User
  isOpen: boolean
  onClose: () => void
}

export function UserProfileModal({ user, isOpen, onClose }: UserProfileModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-foreground mb-4">Mi Perfil</h2>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-muted-foreground mb-1">Correo Electrónico</p>
              <p className="font-medium text-foreground">{user.email}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Tipo de Usuario</p>
              <p className="font-medium text-foreground capitalize">
                {user.role === "admin" ? "Administrador" : "Estudiante/Docente"}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Nombre</p>
              <p className="font-medium text-foreground">{user.name}</p>
            </div>
          </div>
        </div>

        <Button onClick={onClose} className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
          Cerrar
        </Button>
      </Card>
    </div>
  )
}
