import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

/********************************************
 Sistema de Gestión de Reservas - Frontend
 Conectado a Flask + MySQL
********************************************/

// --- Tipos ---
type EstadoReserva = "activa" | "cancelada" | "pendiente" | "finalizada";

type Sala = {
  id: number | string;
  nombre: string;
  tipo?: string;
  capacidad?: number;
  nombre_sala?: string;
  edificio?: string;
};

type Reserva = {
  id: number | string;
  ci_participante: string;
  participante?: string;
  sala_id: number | string;
  sala_nombre: string;
  fecha: string;
  hora_inicio?: string;
  hora_fin?: string;
  cantidad: number;
  estado: EstadoReserva;
  observaciones?: string;
};

type User = { id: string; nombre: string; email: string; rol?: string } | null;

// --- Utils ---
const todayISO = () => new Date().toISOString().slice(0, 10);
function classNames(...c: (string | false | undefined)[]) { return c.filter(Boolean).join(" "); }
function badgeClasses(estado: EstadoReserva) {
  switch (estado) {
    case "activa": return "bg-green-100 text-green-800 ring-1 ring-green-200";
    case "pendiente": return "bg-amber-100 text-amber-800 ring-1 ring-amber-200";
    case "cancelada": return "bg-rose-100 text-rose-800 ring-1 ring-rose-200";
    case "finalizada": return "bg-slate-100 text-slate-800 ring-1 ring-slate-200";
    default: return "bg-slate-100 text-slate-800 ring-slate-200";
  }
}
const ESTADOS_VALIDOS: EstadoReserva[] = ["activa", "cancelada", "pendiente", "finalizada"];

// --- Contexto de autenticación ---
const AuthCtx = createContext<{
  user: User;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (nombre: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}>({ user: null, token: null, login: async () => {}, register: async () => {}, logout: () => {} });

function useAuth() { return useContext(AuthCtx); }

// --- Cliente API conectado a Flask ---
function Api(base = "") {
  const apiBase = base || "";

  return {
    async login(email: string, password: string) {
      const res = await fetch(`${apiBase}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const raw = await res.text();
      let data: any = null;
      try { data = raw ? JSON.parse(raw) : null; } catch {}

      if (!res.ok || !data?.success) {
        const msg = data?.error || raw || "Error de autenticación";
        throw new Error(msg);
      }

      const rol = data.rol || "usuario";
      const display = rol === "admin"
        ? "Admin"
        : (email?.split("@")[0] || "Usuario");

      const usuario = { id: email, nombre: display, email, rol };
      return { ok: true, token: null, usuario };
    },

    // >>> ÚNICO CAMBIO DE PERSISTENCIA <<<
    async register(nombre: string, email: string, password: string) {
      const res = await fetch(`${apiBase}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, email, password }),
      });
      const raw = await res.text();
      let data: any = null;
      try { data = raw ? JSON.parse(raw) : null; } catch {}
      if (!res.ok || !data?.success) {
        throw new Error(data?.error || raw || "No se pudo registrar");
      }
      return { ok: true };
    },

    async me(_token: string | null) {
      const res = await fetch(`${apiBase}/api/me`);
      const data = await res.json();
      if (data && data.ok) return data;
      return { ok: false };
    },

    async salas() {
      const res = await fetch(`${apiBase}/api/salas`);
      if (!res.ok) throw new Error("Error al cargar salas");
      return await res.json();
    },

    async reservas(_token?: string | null, fecha?: string) {
      const url = fecha ? `${apiBase}/api/reservas?fecha=${encodeURIComponent(fecha)}` : `${apiBase}/api/reservas`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Error al cargar reservas");
      return await res.json();
    },

    async crearReserva(_token: string | null, data: any) {
      const res = await fetch(`${apiBase}/api/reservas`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      return await res.json();
    },

    async actualizarReserva(_token: string | null, id: string, patch: any) {
      const res = await fetch(`${apiBase}/api/reservas/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patch),
      });
      return await res.json();
    },

    async eliminarReserva(_token: string | null, id: string) {
      const res = await fetch(`${apiBase}/api/reservas/${id}`, { method: "DELETE" });
      return await res.json();
    },

    async cambiarEstado(_token: string | null, id: string, estado: EstadoReserva) {
      const res = await fetch(`${apiBase}/api/reservas/${id}/estado`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estado }),
      });
      return await res.json();
    },
  };
}

// --- Provider ---
function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));
  const api = useMemo(() => Api(""), []);

  useEffect(() => {
    (async () => {
      if (token && !user) {
        try {
          const r = await api.me(token);
          if (r.ok) setUser(r.usuario);
        } catch {}
      }
    })();
  }, [token]);

  async function login(email: string, password: string) {
    const r = await api.login(email, password);
    if (!r.ok) throw new Error("Login fallido");
    setUser(r.usuario);
  }

  async function register(nombre: string, email: string, password: string) {
    const r = await api.register(nombre, email, password);
    if (!r.ok) throw new Error("Registro fallido");
  }

  function logout() {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
  }

  return (
    <AuthCtx.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthCtx.Provider>
  );
}

// --- App ---
export default function App() {
  return (
    <AuthProvider>
      <Protected>
        <Dashboard />
      </Protected>
    </AuthProvider>
  );
}

// --- Rutas protegidas ---
function Protected({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  if (!user) return <LoginPage />;
  return <>{children}</>;
}

// --- Login Page ---
function LoginPage() {
  const { login, register } = useAuth();
  const [tab, setTab] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [nombre, setNombre] = useState("");
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setAlert(null);
    setLoading(true);
    try {
      if (tab === "login") await login(email, password);
      else {
        await register(nombre, email, password);
        setTab("login");
        setAlert("Registro exitoso. Ahora inicia sesión.");
      }
    } catch (er: any) {
      setAlert(er.message || "Error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen grid place-items-center bg-[#0B2F6B]">
      <div className="w-full max-w-md rounded-2xl bg-white border border-neutral-200 shadow-xl">
        <div className="px-6 pt-6 pb-3 text-center">
          <img src="/logo-ucu.png" alt="UCU" className="mx-auto h-12 w-12 rounded-2xl object-contain ring-1 ring-neutral-200" />
          <h1 className="mt-2 text-lg font-semibold">Gestión de Reservas</h1>
          <p className="text-sm text-neutral-500">Accedé con tu cuenta</p>
        </div>
        <div className="px-6">
          <div className="grid grid-cols-2 gap-1 p-1 bg-neutral-100 rounded-xl mb-4">
            <button onClick={() => setTab("login")} className={classNames("py-2 rounded-lg text-sm", tab === "login" ? "bg-white shadow font-medium" : "text-neutral-600")}>Iniciar sesión</button>
            <button onClick={() => setTab("register")} className={classNames("py-2 rounded-lg text-sm", tab === "register" ? "bg-white shadow font-medium" : "text-neutral-600")}>Crear cuenta</button>
          </div>
          {alert && <div className="mb-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm px-3 py-2">{alert}</div>}
        </div>
        <form onSubmit={onSubmit} className="px-6 pb-6 space-y-3">
          {tab === "register" && (
            <div className="space-y-1">
              <label className="text-sm text-neutral-600">Nombre</label>
              <input className={inputCls()} value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Nombre y apellido" />
            </div>
          )}
          <div className="space-y-1">
            <label className="text-sm text-neutral-600">Email</label>
            <input type="email" className={inputCls()} value={email} onChange={(e) => setEmail(e.target.value)} placeholder="usuario@dominio.com" />
          </div>
          <div className="space-y-1">
            <label className="text-sm text-neutral-600">Contraseña</label>
            <input type="password" className={inputCls()} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
          </div>
          <button type="submit" disabled={loading} className={classNames("w-full px-4 py-2 rounded-xl text-white", loading ? "bg-neutral-400" : "bg-[#0B2F6B] hover:brightness-110")}>{loading ? "Procesando…" : tab === "login" ? "Entrar" : "Registrarme"}</button>
        </form>
      </div>
    </div>
  );
}

// --- Dashboard ---
function Dashboard() {
  const { user, logout } = useAuth();
  const [salas, setSalas] = useState<Sala[]>([]);
  const [reservas, setReservas] = useState<Reserva[]>([]);
  const api = useMemo(() => Api(""), []);
  const isAdmin = user?.rol === "admin";

  // carga inicial + polling cada 10s
  useEffect(() => {
    let alive = true;
    async function load() {
      try {
        const [salasData, reservasData] = await Promise.all([
          api.salas(),
          api.reservas(null, todayISO()),
        ]);
        if (!alive) return;
        setSalas(salasData);
        setReservas(reservasData);
      } catch (e) { console.error(e); }
    }
    load();
    const id = setInterval(load, 10000);
    return () => { alive = false; clearInterval(id); };
  }, []);

  async function refrescar() {
    const data = await api.reservas(null, todayISO());
    setReservas(data);
  }

  async function onNuevaReserva() {
    if (!isAdmin) return;
    const sala = window.prompt(
      `Ingresá sala en formato "nombre_sala|edificio".\nEj: Sala 1|Edificio Central`
    );
    if (!sala) return;
    const [nombre_sala, edificio] = sala.split("|").map((x) => x?.trim());
    const id_turno = window.prompt("ID de turno (número). Ej: 1");
    if (!id_turno) return;
    const fecha = window.prompt("Fecha (YYYY-MM-DD)", todayISO());
    if (!fecha) return;

    const r = await api.crearReserva(null, {
      nombre_sala,
      edificio,
      id_turno: Number(id_turno),
      fecha,
      estado: "activa",
    });
    if (!r?.ok) {
      alert(r?.error || "No se pudo crear la reserva");
      return;
    }
    await refrescar();
  }

  function nextEstado(e: EstadoReserva): EstadoReserva {
    if (e === "activa") return "cancelada";
    if (e === "cancelada") return "finalizada";
    if (e === "finalizada") return "activa";
    return "activa";
  }

  // --- BOTONES GLOBALES ABM ---
  async function eliminarPorId() {
    if (!isAdmin) return;
    const id = window.prompt("ID de la reserva a eliminar:");
    if (!id) return;
    const ok = confirm(`¿Eliminar la reserva ${id}?`);
    if (!ok) return;
    const r = await api.eliminarReserva(null, String(id));
    if (!r?.ok) return alert(r?.error || "No se pudo eliminar.");
    await refrescar();
  }

  async function modificarPorId() {
    if (!isAdmin) return;
    const id = window.prompt("ID de la reserva a modificar:");
    if (!id) return;

    const nuevaFecha = window.prompt("Nueva fecha (YYYY-MM-DD) o dejar vacío para no cambiar:");
    const nuevoTurno = window.prompt("Nuevo id_turno (número) o vacío:");
    const nuevaSala = window.prompt('Nueva sala "nombre_sala|edificio" o vacío:');
    const nuevoEstado = window.prompt('Nuevo estado (activa|cancelada|pendiente|finalizada) o vacío:');

    const patch: any = {};
    if (nuevaFecha) patch.fecha = nuevaFecha;
    if (nuevoTurno) patch.id_turno = Number(nuevoTurno);
    if (nuevaSala) {
      const [nombre_sala, edificio] = nuevaSala.split("|").map(s => s?.trim());
      if (nombre_sala) patch.nombre_sala = nombre_sala;
      if (edificio) patch.edificio = edificio;
    }
    if (nuevoEstado) {
      const e = nuevoEstado.trim() as EstadoReserva;
      if (!ESTADOS_VALIDOS.includes(e)) return alert("Estado inválido.");
      patch.estado = e;
    }

    if (Object.keys(patch).length === 0) {
      alert("No hay cambios para aplicar.");
      return;
    }

    const r = await api.actualizarReserva(null, String(id), patch);
    if (!r?.ok) return alert(r?.error || "No se pudo modificar.");
    await refrescar();
  }

  async function cambiarEstadoPorId() {
    const id = window.prompt("ID de la reserva para cambiar estado:");
    if (!id) return;
    const nuevo = (window.prompt('Estado nuevo (activa|cancelada|pendiente|finalizada):') || "").trim() as EstadoReserva;
    if (!ESTADOS_VALIDOS.includes(nuevo)) return alert("Estado inválido.");
    const r = await api.cambiarEstado(null, String(id), nuevo);
    if (!r?.ok) return alert(r?.error || "No se pudo cambiar el estado.");
    await refrescar();
  }

  return (
    <div className="min-h-screen bg-[#0B2F6B] text-neutral-100">
      <header className="p-4 flex justify-between items-center">
        <h1 className="font-semibold text-lg">Dashboard de Reservas</h1>
        <div className="flex items-center gap-3">
          <span className="text-sm">
            Hola, <span className="font-medium">{user?.nombre}</span>
            {user?.rol ? ` (${user?.rol})` : ""}
          </span>
          <button onClick={logout} className="text-sm px-3 py-1 rounded-lg border border-neutral-300/30 hover:bg-white/10">
            Cerrar sesión
          </button>
        </div>
      </header>

      <main className="max-w-5xl mx-auto p-6 space-y-4">
        {/* KPIs */}
        <div className="grid sm:grid-cols-3 gap-4">
          <Kpi label="Salas" value={salas.length} />
          <Kpi label="Reservas hoy" value={reservas.length} />
          <Kpi label="Personas" value={reservas.reduce((a, r) => a + (r.cantidad || 0), 0)} />
        </div>

        {/* Card de reservas */}
        <div className="bg-white text-neutral-900 rounded-2xl border border-neutral-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-semibold">Reservas del día</h2>
            <div className="flex flex-wrap gap-2">
              {isAdmin && (
                <>
                  <button
                    className="text-sm px-3 py-1 rounded-lg border border-neutral-300 hover:bg-neutral-100"
                    onClick={onNuevaReserva}
                  >
                    Nueva reserva
                  </button>
                  <button
                    className="text-sm px-3 py-1 rounded-lg border border-neutral-300 hover:bg-neutral-100"
                    onClick={modificarPorId}
                  >
                    Modificar por ID
                  </button>
                  <button
                    className="text-sm px-3 py-1 rounded-lg border border-neutral-300 hover:bg-neutral-100"
                    onClick={eliminarPorId}
                  >
                    Eliminar por ID
                  </button>
                </>
              )}
              <button
                className="text-sm px-3 py-1 rounded-lg border border-neutral-300 hover:bg-neutral-100"
                onClick={cambiarEstadoPorId}
                title="Disponible para todos los usuarios"
              >
                Cambiar estado por ID
              </button>
              <button
                className="text-sm px-3 py-1 rounded-lg border border-neutral-300 hover:bg-neutral-100"
                onClick={refrescar}
              >
                Refrescar
              </button>
            </div>
          </div>

          <table className="w-full text-sm">
            <thead className="text-neutral-600 bg-neutral-50">
              <tr>
                <th className="text-left p-2">Hora</th>
                <th className="text-left p-2">Sala</th>
                <th className="text-left p-2">Participante</th>
                <th className="text-left p-2">Cant.</th>
                <th className="text-left p-2">Estado</th>
                <th className="text-left p-2">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {reservas.map(r => (
                <tr key={r.id} className="border-t border-neutral-100 hover:bg-neutral-50">
                  <td className="p-2">{r.hora_inicio || "?"} - {r.hora_fin || "?"}</td>
                  <td className="p-2">{r.sala_nombre}</td>
                  <td className="p-2">{r.participante}</td>
                  <td className="p-2">{r.cantidad}</td>
                  <td className="p-2">
                    <span className={classNames("px-2 py-1 rounded-full text-xs", badgeClasses(r.estado))}>{r.estado}</span>
                  </td>
                  <td className="p-2">
                    {isAdmin ? (
                      <div className="flex gap-2">
                        <button
                          className="text-xs px-2 py-1 rounded border border-neutral-300 hover:bg-neutral-100"
                          title="Cambiar estado"
                          onClick={async () => {
                            const nuevo = nextEstado(r.estado);
                            const rr = await api.cambiarEstado(null, String(r.id), nuevo);
                            if (!rr?.ok) return alert(rr?.error || "No se pudo cambiar el estado");
                            await refrescar();
                          }}
                        >
                          Cambiar estado
                        </button>
                        <button
                          className="text-xs px-2 py-1 rounded border border-neutral-300 hover:bg-neutral-100"
                          title="Eliminar"
                          onClick={async () => {
                            if (!confirm("¿Eliminar reserva?")) return;
                            await api.eliminarReserva(null, String(r.id));
                            await refrescar();
                          }}
                        >
                          Eliminar
                        </button>
                      </div>
                    ) : (
                      <span className="text-neutral-400">—</span>
                    )}
                  </td>
                </tr>
              ))}
              {reservas.length === 0 && (
                <tr><td className="p-3 text-neutral-500" colSpan={6}>Sin reservas hoy.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

// --- KPI component ---
function Kpi({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-white text-neutral-900 rounded-xl border border-neutral-200 p-3 text-center">
      <div className="text-xs text-neutral-500">{label}</div>
      <div className="text-lg font-semibold">{value}</div>
    </div>
  );
}

function inputCls() {
  return "w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#0B2F6B]";
}
