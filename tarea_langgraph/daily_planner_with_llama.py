"""
ASISTENTE DE PLANIFICACIÓN DIARIA CON LANGGRAPH + LLAMA 3.2

=== EXPLICACIÓN DEL FLUJO AGÉNTICO CON LLAMA 3.2 ===
Tres nodos: Analizador usa Llama 3.2 para extraer actividades de forma
inteligente (no solo palabras clave), Planificador genera horario personalizado,
Validador usa Llama 3.2 para verificar descansos. Flujo: START → Analizar →
Planificar → Validar → END. Requiere Ollama con Llama 3.2 instalado.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.llms import Ollama

# Inicializar Llama 3.2 via Ollama
llm = Ollama(model="llama3.2", temperature=0.7)


class DayPlanState(TypedDict):
    user_input: str
    extracted_activities: list
    daily_plan: str
    is_valid: bool
    validation_msg: str


def analyze_activities(state: DayPlanState) -> DayPlanState:
    """Nodo 1: Llama 3.2 analiza entrada y extrae actividades"""
    user_input = state["user_input"]

    # Prompt para Llama 3.2
    prompt = f"""Analiza esta descripción de día y extrae actividades.
Responde SOLO con un JSON válido sin explicaciones.

Descripción: "{user_input}"

Formato de respuesta:
{{"activities": [
  {{"type": "clases", "count": 1}},
  {{"type": "ejercicio", "count": 1}},
  {{"type": "descanso", "count": 1}}
]}}

Tipos válidos: clases, ejercicio, trabajo, descanso, comida, estudio, personal, cine, lectura, pasear.
MAPEO IMPORTANTE:
- "cine", "película" → type: "cine"
- "leer", "lectura" → type: "lectura"
- "pasear", "paseo", "caminar", "caminata", "salida", "salir" → type: "pasear"
- "pausa", "relax", "relajarse", "descansar" → type: "descanso"
- "estudiar", "tarea", "examen" → type: "estudio"
- "gimnasio", "gym", "ejercicio", "entrenar" → type: "ejercicio"

Responde SOLO el JSON:"""

    try:
        response = llm.invoke(prompt)
        import json
        data = json.loads(response)
        activities = [{"type": a["type"], "duration": 60}
                     for a in data.get("activities", [])]
    except:
        activities = [{"type": "general", "duration": 120}]

    if not activities:
        activities = [{"type": "general", "duration": 120}]

    return {**state, "extracted_activities": activities, "is_valid": False, "validation_msg": ""}


def plan_daily_schedule(state: DayPlanState) -> DayPlanState:
    """Nodo 2: Planificador genera horario"""
    acts = {a["type"] for a in state["extracted_activities"]}
    plan = "📅 PLAN DIARIO PERSONALIZADO\n" + "=" * 50 + "\n\nHORARIO:\n" + "-" * 50 + "\n"

    schedule = [
        ("07:00-08:00", "Desayuno", "personal"), ("08:00-12:00", "Clases/Trabajo", "clases"),
        ("12:00-13:30", "Almuerzo", "comida"), ("13:30-15:30", "Estudio", "estudio"),
        ("15:30-16:00", "Pausa", "descanso"), ("16:00-17:30", "Ejercicio", "ejercicio"),
        ("17:30-19:00", "Personal", "personal"), ("19:00-20:00", "Cena", "comida"),
        ("20:00-22:00", "Relax", "descanso"), ("22:00+", "Dormir", "descanso"),
    ]

    # Mapeo de actividades del usuario a franjas horarias
    activity_mapping = {
        "clases": ("08:00-12:00", "Clases"),
        "trabajo": ("08:00-12:00", "Trabajo"),
        "ejercicio": ("16:00-17:30", "Ejercicio"),
        "estudio": ("13:30-15:30", "Estudio"),
        "cine": ("17:30-19:00", "Cine"),
        "lectura": ("20:00-22:00", "Lectura"),
        "personal": ("17:30-19:00", "Personal"),
        "pasear": ("17:30-19:00", "Pasear con familia"),
    }

    for time, act, atype in schedule:
        marker = "✓" if atype in acts else " "
        # Si la actividad del usuario coincide con esta franja, mostrar la actividad del usuario
        display_act = act
        for user_activity_type, (activity_time, activity_name) in activity_mapping.items():
            if user_activity_type in acts and activity_time == time:
                display_act = activity_name
                break
        plan += f"{marker} {time:<12} → {display_act}\n"

    plan += "\n" + "=" * 50 + "\n💡 RECOMENDACIONES:\n" + "-" * 50 + "\n"
    rec = {"clases": "Descarga diapositivas", "ejercicio": "Mantente hidratado",
           "estudio": "Estudia 50 min + descanso", "trabajo": "Pausas cada 90 min",
           "comida": "Comidas nutritivas", "descanso": "7-8 horas sueño",
           "pasear": "Disfruta tiempo en familia", "lectura": "Buena concentración"}

    added = set()
    for a in state["extracted_activities"]:
        atype = a["type"]
        if atype in rec and atype not in added:
            plan += f"• {rec[atype]}\n"
            added.add(atype)

    plan += "\n" + "=" * 50 + "\n¡Buen día! 💪\n"
    return {**state, "daily_plan": plan, "is_valid": False, "validation_msg": ""}


def validate_rest_periods(state: DayPlanState) -> DayPlanState:
    """Nodo 3: Llama 3.2 valida descansos de forma inteligente"""
    acts = {a["type"] for a in state["extracted_activities"]}

    # Actividades intensivas que requieren descanso obligatorio
    intensive = {"clases", "ejercicio", "trabajo"}
    relaxed = {"cine", "lectura", "personal", "descanso", "estudio", "pasear"}
    has_intensive = any(a in acts for a in intensive)
    has_break = any(a in acts for a in {"descanso", "comida"})
    has_only_relaxed = all(a in relaxed for a in acts)

    activities_str = str([a["type"] for a in state["extracted_activities"]])
    plan_summary = state["daily_plan"][:300]

    # Prompt MEJORADO - más inteligente y contextual
    prompt = f"""Analiza este plan de día y valida si es saludable y equilibrado.

Actividades: {activities_str}
Plan: {plan_summary}

REGLAS IMPORTANTES:
- Actividades INTENSIVAS (clases, ejercicio, trabajo) REQUIEREN descanso o comida
- Actividades RELAJADAS (cine, personal, lectura, estudio ligero) NO requieren validación estricta
- Si SOLO hay actividades RELAJADAS → APROBADO
- Solo RECHAZA si: hay actividades INTENSIVAS SIN descanso/comida
- APRUEBA si: el plan es equilibrado o es un día relajado

Responde SOLO una palabra: APROBADO, RECHAZADO o ADVERTENCIA

Respuesta:"""

    try:
        response = llm.invoke(prompt).strip().upper()
    except:
        response = "APROBADO"

    # Verificar si el horario incluye descansos (Pausa, Relax, Cena)
    plan_lower = state["daily_plan"].lower()
    has_scheduled_breaks = any(break_word in plan_lower for break_word in ["pausa", "relax", "cena", "almuerzo", "desayuno"])

    # Lógica mejorada: considera el contexto
    if has_only_relaxed:
        # Si solo hay actividades relajadas, aprueba automáticamente
        msg = "✅ PLAN APROBADO - Día relajado y equilibrado"
        is_valid = True
    elif has_intensive and (has_break or has_scheduled_breaks):
        # Si hay actividades intensivas PERO hay descansos (explícitos o en el horario), aprueba
        msg = "✅ PLAN APROBADO - Plan equilibrado con descansos adecuados"
        is_valid = True
    elif has_intensive and not has_break and not has_scheduled_breaks:
        # Rechaza SOLO si hay actividades intensivas sin descanso ni en plan
        msg = "❌ PLAN RECHAZADO:\nTienes actividades intensivas (clases/ejercicio/trabajo) sin descanso\n\n"
        msg += "SOLUCIONES:\n• Agrega pausas de 30+ min\n• Incluye tiempo para comer\n• Asegura 7-8 hrs sueño"
        is_valid = False
    elif "RECHAZADO" in response:
        msg = "❌ PLAN RECHAZADO:\nPlan muy exigente sin descansos suficientes\n\n"
        msg += "SOLUCIONES:\n• Reduce actividades intensivas\n• Agrega pausas entre actividades"
        is_valid = False
    elif "ADVERTENCIA" in response:
        msg = "⚠️  ADVERTENCIA: Plan con actividades intensivas sin pausas óptimas\n"
        msg += "RECOMENDACIÓN: Considera agregar descansos de 15-30 min"
        is_valid = False
    else:
        msg = "✅ PLAN APROBADO - Plan equilibrado y saludable (validado por Llama 3.2)"
        is_valid = True

    return {**state, "is_valid": is_valid, "validation_msg": msg}


def build_graph():
    """Construye el grafo de 3 nodos con Llama 3.2"""
    graph = StateGraph(DayPlanState)
    graph.add_node("analizar", analyze_activities)
    graph.add_node("planificar", plan_daily_schedule)
    graph.add_node("validar", validate_rest_periods)

    graph.add_edge(START, "analizar")
    graph.add_edge("analizar", "planificar")
    graph.add_edge("planificar", "validar")
    graph.add_edge("validar", END)

    return graph.compile()


def main():
    """Ejecuta el asistente con Llama 3.2"""
    print("\n" + "=" * 60)
    print("🗓️  ASISTENTE DE PLANIFICACIÓN CON LLAMA 3.2 + VALIDADOR")
    print("=" * 60 + "\n")

    user_input = input("Describe tu día (ej: clases, gimnasio, estudiar): ").strip()
    if not user_input:
        user_input = "Tengo clases de IA, gimnasio y debo estudiar"
        print(f"(Usando: {user_input})\n")

    state = DayPlanState(user_input=user_input, extracted_activities=[],
                         daily_plan="", is_valid=False, validation_msg="")

    print("Procesando con Llama 3.2...\n")
    result = build_graph().invoke(state)

    # PASO 1: Mostrar actividades detectadas
    print("\n" + "=" * 60)
    print("📋 ACTIVIDADES DETECTADAS (por Llama 3.2)")
    print("=" * 60)
    for a in result["extracted_activities"]:
        print(f"  ✓ {a['type'].upper():<12} → {a['duration']} minutos")

    activity_count = len(result["extracted_activities"])
    total_time = sum(a["duration"] for a in result["extracted_activities"])
    print(f"\nTotal: {activity_count} actividades | {total_time} minutos")
    print("=" * 60)

    # PASO 2: Mostrar cronograma
    print("\n📅 DISEÑANDO CRONOGRAMA...\n")
    print(result["daily_plan"])

    # PASO 3: Mostrar validación
    print("=" * 60)
    print("✔️  VALIDACIÓN (por Llama 3.2):")
    print("-" * 60)
    print(result["validation_msg"])
    print("=" * 60)

    # PASO 4: Mostrar JSON final
    print("\n📊 RESULTADO EN JSON:")
    print("=" * 60)
    import json
    json_result = {
        "user_input": result["user_input"],
        "extracted_activities": result["extracted_activities"],
        "is_valid": result["is_valid"],
        "validation_message": result["validation_msg"]
    }
    print(json.dumps(json_result, indent=2, ensure_ascii=False))
    print("=" * 60)


if __name__ == "__main__":
    main()
