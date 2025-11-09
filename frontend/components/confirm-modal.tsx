"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface ConfirmModalProps {
  title: string
  message: string
  onConfirm: () => void
  onCancel: () => void
  isOpen: boolean
  isLoading?: boolean
}

export function ConfirmModal({ title, message, onConfirm, onCancel, isOpen, isLoading = false }: ConfirmModalProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-sm p-6">
        <h2 className="text-lg font-semibold text-foreground mb-2">{title}</h2>
        <p className="text-sm text-muted-foreground mb-6">{message}</p>
        <div className="flex gap-3 justify-end">
          <Button
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
            className="text-foreground border-border hover:bg-secondary bg-transparent"
          >
            Cancelar
          </Button>
          <Button
            onClick={onConfirm}
            disabled={isLoading}
            className="bg-destructive hover:bg-destructive/90 text-destructive-foreground"
          >
            {isLoading ? "Eliminando..." : "Eliminar"}
          </Button>
        </div>
      </Card>
    </div>
  )
}
