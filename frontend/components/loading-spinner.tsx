"use client"

export function LoadingSpinner({ label = "Cargando" }: { label?: string }) {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="space-y-3 text-center">
        <div className="inline-block">
          <div className="relative w-8 h-8">
            <div className="absolute inset-0 border-4 border-transparent border-t-primary rounded-full animate-spin" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground">{label}...</p>
      </div>
    </div>
  )
}
