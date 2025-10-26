# Sistema de Reserva de Salas UCU
Estructura base del proyecto

Informe:
(https://correoucuedu-my.sharepoint.com/:w:/g/personal/facundo_diaz_correo_ucu_edu_uy/EXNML6CHFlVFpsL-GjQm3c4Bm36Gj-0a1oUQCpvc0GCKAQ?e=rf0P8R)

Estado actual del proyecto segun GPT el mas crack

## 🧭 ESTADO ACTUAL DEL PROYECTO — *Sistema de Reserva de Salas UCU*

### 🧩 **FASE 1 — Base de datos y conexión** ✅ **COMPLETA**

| Tarea                                                | Estado |
| ---------------------------------------------------- | ------ |
| Diseño de tablas según la letra                      | ✅      |
| Script `schema.sql` creado                           | ✅      |
| Datos de prueba (`inserts.sql`) cargados             | ✅      |
| Conexión Python–MySQL (`db_connection.py`) funcional | ✅      |
| Pruebas de conexión ejecutadas                       | ✅      |

💬 *Tenés una base estable, estructurada y accesible desde Python.*

---

### ⚙️ **FASE 2 — Backend funcional (ABM + reglas de negocio)** 🟢 **90% COMPLETA**

| Subtarea                                           | Estado                         |
| -------------------------------------------------- | ------------------------------ |
| Validaciones clave (`validaciones.py`)             | ✅                              |
| Lógica principal de reservas (`logica.py`)         | ✅                              |
| Registro de logs de acciones (`logs.py`)           | ✅                              |
| Manejo de errores SQL (`try/except/rollback`)      | ✅                              |
| ABM completo (crear, modificar, eliminar reservas) | 🟡 *Solo “crear” implementado* |

💬 *Tu sistema ya valida todas las restricciones del enunciado, registra logs y maneja errores. Solo faltan funciones complementarias:*

* `cancelar_reserva()`
* `registrar_asistencia()`
* `crear_sancion()` *(automática o manual)*

---

### 📊 **FASE 3 — Consultas y reportes** ✅ **COMPLETA**

| Tarea                                                   | Estado |
| ------------------------------------------------------- | ------ |
| Archivo `consultas.sql` con todas las queries pedidas   | ✅      |
| Módulo `reportes.py` funcional (1 función por consulta) | ✅      |
| Integración con `app.py` (menú interactivo)             | ✅      |

💬 *Ya ejecutás todos los reportes directamente desde el sistema, con conexión a MySQL.*

---

### 💻 **FASE 4 — Interfaz / Menú principal** 🟢 **En progreso (80%)**

| Tarea                                                                | Estado                                 |
| -------------------------------------------------------------------- | -------------------------------------- |
| Menú principal en `app.py`                                           | ✅                                      |
| Submenú de reportes                                                  | ✅                                      |
| Integración con creación de reservas                                 | ✅                                      |
| ABM completo (agregar más opciones: cancelar, asistencia, sanciones) | 🟡 *Falta agregar opciones 3, 4, etc.* |

💬 *Tenés la estructura lista para expandir el menú y cubrir el resto de operaciones.*

---

### 🧱 **FASE 5 — Docker e Informe final** ⚪ **Pendiente**

| Tarea                                                 | Estado      |
| ----------------------------------------------------- | ----------- |
| Dockerfile + docker-compose.yml                       | ❌ pendiente |
| README con instrucciones de ejecución                 | ❌ pendiente |
| Informe (decisiones, mejoras, bitácora, bibliografía) | ❌ pendiente |

💬 *Esta será la última parte antes de la entrega — más “documentación” que código.*

---

## 🚀 RESUMEN VISUAL

| Fase                         | Estado      |
| ---------------------------- | ----------- |
| 1️⃣ Base de datos y conexión | ✅           |
| 2️⃣ Backend y validaciones   | 🟢 90%      |
| 3️⃣ Consultas / reportes     | ✅           |
| 4️⃣ Menú / interfaz          | 🟢 80%      |
| 5️⃣ Docker + informe         | ⚪ pendiente |

---

## 🎯 Siguiente paso recomendado

👉 **Completar la Fase 2 y 4 con las operaciones restantes:**

1. `cancelar_reserva()`
2. `registrar_asistencia()`
3. `crear_sancion()` *(automática o manual)*
4. Integrarlas como opciones nuevas en el menú principal (`app.py`).

Con eso, el sistema quedaría **funcional al 100%**, y podríamos pasar a la **fase Docker + README + Informe**.

---

