#!/usr/bin/env python3
"""
Script para generar PDF de documentación del proyecto LangGraph
Asistente de Planificación Diaria
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

# Crear PDF
pdf_file = "Asistente_Planificacion_Diaria_LangGraph.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                       rightMargin=0.75*inch, leftMargin=0.75*inch,
                       topMargin=0.75*inch, bottomMargin=0.75*inch)

# Estilos
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2e5c8a'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=12,
    leading=16
)

code_style = ParagraphStyle(
    'CodeStyle',
    parent=styles['BodyText'],
    fontSize=9,
    fontName='Courier',
    textColor=colors.HexColor('#333333'),
    spaceAfter=10,
    leftIndent=20,
    rightIndent=20,
    backColor=colors.HexColor('#f0f0f0')
)

# Contenido del documento
content = []

# Portada
content.append(Spacer(1, 0.5*inch))
content.append(Paragraph("🗓️ Asistente de Planificación Diaria", title_style))
content.append(Paragraph("con LangGraph + Llama 3.2", styles['Heading2']))
content.append(Spacer(1, 0.3*inch))
content.append(Paragraph("Sistema Agéntico para Optimización de Horarios Diarios", styles['Normal']))
content.append(Spacer(1, 0.2*inch))
content.append(Paragraph(f"<i>Generado: {datetime.now().strftime('%d de %B de %Y')}</i>", styles['Normal']))
content.append(Spacer(1, 0.5*inch))

# Sección: Descripción General
content.append(Paragraph("1. Descripción General del Proyecto", heading_style))
content.append(Paragraph(
    """Este proyecto implementa un asistente inteligente de planificación diaria que utiliza
    LangGraph para orquestar un flujo de trabajo compuesto por tres nodos especializados.
    El sistema recibe descripciones naturales de las actividades que el usuario desea realizar
    durante el día y genera un horario personalizado, validando automáticamente que el plan
    incluya descansos adecuados después de actividades intensivas.""",
    body_style
))
content.append(Spacer(1, 0.2*inch))

# Sección: Objetivos
content.append(Paragraph("2. Objetivos del Proyecto", heading_style))
objectives = [
    "<b>Análisis Inteligente:</b> Utilizar Llama 3.2 para extraer actividades de forma semántica, no solo mediante palabras clave.",
    "<b>Generación de Horarios:</b> Crear horarios personalizados que se adapten a las actividades específicas del usuario.",
    "<b>Validación de Salud:</b> Rechazar planes que incluyan actividades intensivas sin descansos adecuados.",
    "<b>Modularidad:</b> Implementar un flujo modular con LangGraph para facilitar el mantenimiento y expansión."
]
for obj in objectives:
    content.append(Paragraph(f"• {obj}", body_style))
content.append(Spacer(1, 0.2*inch))

# Sección: Arquitectura
content.append(Paragraph("3. Arquitectura del Sistema", heading_style))
content.append(Paragraph(
    """El proyecto está diseñado como un grafo dirigido acíclico (DAG) con tres nodos principales
    que se ejecutan secuencialmente. Cada nodo procesa el estado de la solicitud y lo transmite
    al siguiente, permitiendo una separación clara de responsabilidades.""",
    body_style
))
content.append(Spacer(1, 0.15*inch))

# Tabla de arquitectura
arch_data = [
    ['Nodo', 'Función', 'Tecnología'],
    ['Analizador', 'Extrae actividades del texto de entrada', 'Llama 3.2 + JSON'],
    ['Planificador', 'Genera horario personalizado 07:00-22:00+', 'Lógica determinística'],
    ['Validador', 'Valida descansos e intensidad del plan', 'Llama 3.2 + Lógica híbrida']
]

arch_table = Table(arch_data, colWidths=[1.2*inch, 2.5*inch, 1.5*inch])
arch_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
content.append(arch_table)
content.append(Spacer(1, 0.3*inch))

# Sección: Flujo del Sistema
content.append(Paragraph("4. Flujo de Ejecución", heading_style))
flow_text = """
START → Analizador (Llama 3.2) → Planificador → Validador (Llama 3.2) → END

El flujo es determinístico y secuencial. El estado se transmite entre nodos como un TypedDict
que contiene: entrada del usuario, actividades extraídas, plan generado, validez, y mensaje de validación.
"""
content.append(Paragraph(flow_text, body_style))
content.append(Spacer(1, 0.2*inch))

# Sección: Implementación Técnica
content.append(Paragraph("5. Implementación Técnica", heading_style))

content.append(Paragraph("<b>5.1 Nodo Analizador</b>", styles['Heading3']))
content.append(Paragraph(
    """Utiliza Llama 3.2 con un prompt estructurado que instrye al modelo a extraer actividades
    en formato JSON. El prompt incluye un mapeo explícito de palabras clave (cine, pasear, ejercicio, etc.)
    a tipos de actividad. Maneja excepciones gracefully asignando una actividad genérica si el
    JSON es inválido.""",
    body_style
))
content.append(Spacer(1, 0.1*inch))

content.append(Paragraph("<b>5.2 Nodo Planificador</b>", styles['Heading3']))
content.append(Paragraph(
    """Define un horario base (07:00-22:00+) y marca las actividades del usuario con checkmarks (✓).
    Incluye un mapeo de actividades a franjas horarias (estudio: 13:30-15:30, ejercicio: 16:00-17:30, etc.).
    Genera recomendaciones personalizadas basadas en las actividades detectadas.""",
    body_style
))
content.append(Spacer(1, 0.1*inch))

content.append(Paragraph("<b>5.3 Nodo Validador</b>", styles['Heading3']))
content.append(Paragraph(
    """Implementa una lógica híbrida que combina reglas determinísticas con evaluación de Llama 3.2.
    Las reglas son:<br/><br/>
    • Si SOLO hay actividades relajadas (cine, lectura, pasear, estudio) → APROBADO<br/>
    • Si hay actividades intensivas (clases, ejercicio, trabajo) Y el horario incluye descansos
    (Pausa, Relax, Cena) → APROBADO<br/>
    • Si hay actividades intensivas SIN descansos en el horario → RECHAZADO<br/>
    • Fallback a Llama 3.2 si no coincide ninguna regla anterior<br/>
    """,
    body_style
))
content.append(Spacer(1, 0.2*inch))

# Sección: Ejecución y Salida
content.append(Paragraph("6. Ejemplo de Ejecución", heading_style))
content.append(Paragraph("<b>Entrada del usuario:</b>", styles['Heading3']))
content.append(Paragraph(
    '"Hoy quiero salir a pasear con mis hijos, estudiar para un examen e ir al gimnasio"',
    code_style
))
content.append(Spacer(1, 0.1*inch))

content.append(Paragraph("<b>Salida generada:</b>", styles['Heading3']))
output_text = """
ACTIVIDADES DETECTADAS: pasear, estudio, ejercicio

HORARIO:
  07:00-08:00  → Desayuno
  13:30-15:30  → ✓ Estudio
  15:30-16:00  → Pausa
  16:00-17:30  → ✓ Ejercicio
  17:30-19:00  → ✓ Pasear con familia

VALIDACIÓN: ✅ PLAN APROBADO - Plan equilibrado con descansos adecuados

JSON: {"user_input": "...", "extracted_activities": [...], "is_valid": true, ...}
"""
content.append(Paragraph(output_text, code_style))
content.append(Spacer(1, 0.2*inch))

# Nueva página
content.append(PageBreak())

# Sección: Tecnologías
content.append(Paragraph("7. Tecnologías y Dependencias", heading_style))
tech_data = [
    ['Tecnología', 'Versión', 'Función'],
    ['LangGraph', '0.0.84', 'Orquestación de flujos agénticos'],
    ['LangChain', '0.1.11', 'Framework para LLMs'],
    ['Ollama', '0.1.0', 'Runtime local para Llama 3.2'],
    ['Llama 3.2', 'N/A', 'Modelo de lenguaje para análisis y validación'],
    ['Python', '3.8+', 'Lenguaje de programación']
]

tech_table = Table(tech_data, colWidths=[1.8*inch, 1.2*inch, 2.7*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
content.append(tech_table)
content.append(Spacer(1, 0.3*inch))

# Sección: Validaciones Implementadas
content.append(Paragraph("8. Tipos de Validación", heading_style))
validation_text = """
<b>Validación de Actividades Intensivas:</b><br/>
Se considera intensiva: clases, ejercicio, trabajo<br/>
Se considera relajada: cine, lectura, personal, descanso, estudio, pasear<br/><br/>

<b>Validación de Descansos:</b><br/>
El sistema verifica explícitamente en el horario generado la presencia de:<br/>
• Pausa (15:30-16:00)<br/>
• Almuerzo (12:00-13:30)<br/>
• Cena (19:00-20:00)<br/>
• Relax (20:00-22:00)<br/>
• Desayuno (07:00-08:00)<br/><br/>

<b>Criterios de Aprobación:</b><br/>
✅ Plan APROBADO si: (a) solo actividades relajadas, (b) actividades intensivas con descansos<br/>
❌ Plan RECHAZADO si: actividades intensivas sin descansos<br/>
⚠️ Plan ADVERTENCIA si: pocas pausas con múltiples actividades
"""
content.append(Paragraph(validation_text, body_style))
content.append(Spacer(1, 0.2*inch))

# Sección: Características Clave
content.append(Paragraph("9. Características Clave", heading_style))
features = [
    "Análisis semántico de entrada natural con Llama 3.2",
    "Generación de horarios personalizados y dinámicos",
    "Validación inteligente de descansos basada en actividades",
    "Mapeo flexible de actividades a franjas horarias",
    "Recomendaciones personalizadas por actividad",
    "Salida estructurada en JSON para integración programática",
    "Manejo robusto de excepciones y fallbacks",
    "Modularidad mediante LangGraph para fácil extensión"
]

for feat in features:
    content.append(Paragraph(f"✓ {feat}", body_style))
content.append(Spacer(1, 0.3*inch))

# Sección: Casos de Uso
content.append(Paragraph("10. Casos de Uso", heading_style))
cases_text = """
<b>Caso 1: Día Relajado</b><br/>
Entrada: "Ir al cine, estudiar un poco"<br/>
Resultado: ✅ APROBADO - Día relajado y equilibrado<br/><br/>

<b>Caso 2: Día Intenso con Descansos</b><br/>
Entrada: "Clases de IA, gimnasio, estudiar para examen"<br/>
Resultado: ✅ APROBADO - Plan equilibrado con descansos adecuados<br/><br/>

<b>Caso 3: Día Sobrecargado</b><br/>
Entrada: "Clases por la mañana, trabajo por la tarde, más trabajo por la noche"<br/>
Resultado: ❌ RECHAZADO - Actividades intensivas sin descanso
"""
content.append(Paragraph(cases_text, body_style))
content.append(Spacer(1, 0.3*inch))

# Sección: Conclusiones
content.append(Paragraph("11. Conclusiones", heading_style))
conclusion_text = """
El proyecto demuestra la aplicación práctica de LangGraph para orquestar flujos de procesamiento
de lenguaje natural complejos. La combinación de análisis semántico (Llama 3.2) con lógica
determinística permite crear un sistema robusto y predecible que:

• Entiende contexto y requiere validación inteligente de planes diarios
• Genera recomendaciones personalizadas basadas en actividades específicas
• Valida automáticamente la salud y equilibrio del plan
• Produce salida estructurada para integración con otros sistemas

La arquitectura modular permite agregar nuevas actividades, ajustar horarios o mejorar
la validación sin modificar la estructura base del sistema.
"""
content.append(Paragraph(conclusion_text, body_style))
content.append(Spacer(1, 0.3*inch))

# Sección: Repositorio
content.append(Paragraph("12. Repositorio y Acceso", heading_style))
repo_text = """
<b>GitHub Repository:</b><br/>
<font color="blue">https://github.com/ricdex/utec-ai/tree/main/tarea_langgraph</font><br/><br/>

<b>Archivos Principales:</b><br/>
• <b>daily_planner_with_llama.py</b> - Código principal (~240 líneas)<br/>
• <b>requirements.txt</b> - Dependencias (langgraph, langchain, ollama)<br/>
• <b>README.md</b> - Documentación de instalación y uso<br/><br/>

<b>Instrucciones de Ejecución:</b><br/>
1. Instalar Ollama desde ollama.ai<br/>
2. Descargar modelo: <font face="Courier">ollama pull llama3.2</font><br/>
3. Instalar dependencias: <font face="Courier">pip install -r requirements.txt</font><br/>
4. Ejecutar servidor: <font face="Courier">ollama serve</font><br/>
5. En otra terminal: <font face="Courier">python daily_planner_with_llama.py</font>
"""
content.append(Paragraph(repo_text, body_style))
content.append(Spacer(1, 0.5*inch))

# Footer
content.append(Paragraph("_" * 100, styles['Normal']))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    f"<i>Documento generado: {datetime.now().strftime('%d/%m/%Y - %H:%M')} | Proyecto Académico LangGraph</i>",
    styles['Normal']
))

# Generar PDF
doc.build(content)
print(f"✅ PDF generado exitosamente: {pdf_file}")
