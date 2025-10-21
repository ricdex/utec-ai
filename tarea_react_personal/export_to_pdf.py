#!/usr/bin/env python3
"""Exporta código, datos y plan a PDF para entrega universitaria"""

import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Configuración
TITLE = "Daily Planner Agent - ReAct con OpenAI"
AUTHOR = "Agente Inteligente"
CREATED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
PDF_FILENAME = f"Daily_Planner_Agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

def read_file(filepath):
    """Lee un archivo de texto"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo {filepath}: {str(e)}"

def create_pdf():
    """Crea el PDF con código, datos y plan"""
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a3a52'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#2e5090'),
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold',
        borderPadding=5,
        borderColor=colors.HexColor('#d0d0d0'),
        borderWidth=1
    )

    normal_style = styles['Normal']

    # Contenido del PDF
    content = []

    # Portada
    content.append(Spacer(1, 0.5*inch))
    content.append(Paragraph(TITLE, title_style))
    content.append(Spacer(1, 0.3*inch))

    # Información de generación
    info_text = f"<b>Generado:</b> {CREATED}<br/><b>Formato:</b> ReAct Agent con LangChain y OpenAI"
    content.append(Paragraph(info_text, normal_style))
    content.append(Spacer(1, 0.3*inch))

    # Tabla de contenidos
    toc_style = ParagraphStyle(
        'TOC',
        parent=normal_style,
        fontSize=10,
        leftIndent=20
    )
    content.append(Paragraph("<b>Contenido del Documento:</b>", heading_style))
    toc_items = [
        "1. Plan Diario Generado (último)",
        "2. Código Python: daily_planner_agent.py",
        "3. Datos: calendar_data.json",
        "4. Datos: projects_data.json",
        "5. Dependencias: requirements_planner.txt"
    ]
    for item in toc_items:
        content.append(Paragraph(item, toc_style))

    content.append(Spacer(1, 0.2*inch))
    content.append(PageBreak())

    # SECCIÓN 1: Plan Diario
    content.append(Paragraph("1. Plan Diario Generado", heading_style))
    plan_content = read_file("plan_20251021_180810.txt")
    plan_para = Preformatted(plan_content, ParagraphStyle(
        'Code',
        parent=normal_style,
        fontName='Courier',
        fontSize=9,
        textColor=colors.HexColor('#333333'),
        backColor=colors.HexColor('#f5f5f5'),
        borderPadding=10
    ))
    content.append(plan_para)
    content.append(Spacer(1, 0.2*inch))
    content.append(PageBreak())

    # SECCIÓN 2: Código Python
    content.append(Paragraph("2. Código Python: daily_planner_agent.py", heading_style))
    content.append(Paragraph("<i>Implementación del Agente ReAct para planificación diaria</i>", normal_style))
    content.append(Spacer(1, 0.1*inch))

    python_content = read_file("daily_planner_agent.py")
    python_para = Preformatted(python_content, ParagraphStyle(
        'PythonCode',
        parent=normal_style,
        fontName='Courier',
        fontSize=8,
        textColor=colors.HexColor('#000000'),
        backColor=colors.HexColor('#ffffcc'),
        borderPadding=8
    ))
    content.append(python_para)
    content.append(PageBreak())

    # SECCIÓN 3: calendar_data.json
    content.append(Paragraph("3. Datos: calendar_data.json", heading_style))
    content.append(Paragraph("<i>Eventos del calendario (reuniones, bloques personales)</i>", normal_style))
    content.append(Spacer(1, 0.1*inch))

    calendar_content = read_file("calendar_data.json")
    calendar_para = Preformatted(calendar_content, ParagraphStyle(
        'JSONCode',
        parent=normal_style,
        fontName='Courier',
        fontSize=9,
        textColor=colors.HexColor('#0066cc'),
        backColor=colors.HexColor('#f0f8ff'),
        borderPadding=8
    ))
    content.append(calendar_para)
    content.append(Spacer(1, 0.2*inch))
    content.append(PageBreak())

    # SECCIÓN 4: projects_data.json
    content.append(Paragraph("4. Datos: projects_data.json", heading_style))
    content.append(Paragraph("<i>Proyectos técnicos activos con estado y prioridad</i>", normal_style))
    content.append(Spacer(1, 0.1*inch))

    projects_content = read_file("projects_data.json")
    projects_para = Preformatted(projects_content, ParagraphStyle(
        'JSONCode',
        parent=normal_style,
        fontName='Courier',
        fontSize=9,
        textColor=colors.HexColor('#0066cc'),
        backColor=colors.HexColor('#f0f8ff'),
        borderPadding=8
    ))
    content.append(projects_para)
    content.append(Spacer(1, 0.2*inch))
    content.append(PageBreak())

    # SECCIÓN 5: requirements
    content.append(Paragraph("5. Dependencias: requirements_planner.txt", heading_style))
    content.append(Paragraph("<i>Librerías Python necesarias</i>", normal_style))
    content.append(Spacer(1, 0.1*inch))

    requirements_content = read_file("requirements_planner.txt")
    requirements_para = Preformatted(requirements_content, ParagraphStyle(
        'ReqCode',
        parent=normal_style,
        fontName='Courier',
        fontSize=10,
        textColor=colors.HexColor('#2d5016'),
        backColor=colors.HexColor('#f0f5f0'),
        borderPadding=8
    ))
    content.append(requirements_para)

    content.append(Spacer(1, 0.3*inch))

    # Pie de página
    content.append(PageBreak())
    content.append(Paragraph("<b>Información Técnica</b>", heading_style))

    info_items = [
        "<b>Patrón:</b> ReAct (Reasoning + Acting + Observation)",
        "<b>Framework:</b> LangChain 0.1.11",
        "<b>LLM:</b> OpenAI GPT-4o-mini",
        "<b>Herramientas:</b> GetCalendarEvents, ListProjects, BreakDownGoal",
        "<b>Líneas de código:</b> 182",
        f"<b>Fecha de generación:</b> {CREATED}"
    ]

    info_style = ParagraphStyle(
        'Info',
        parent=normal_style,
        fontSize=10,
        leftIndent=20,
        spaceAfter=6
    )

    for item in info_items:
        content.append(Paragraph(item, info_style))

    # Generar PDF
    doc.build(content)
    print(f"\n✅ PDF generado exitosamente: {PDF_FILENAME}")
    print(f"📄 Ubicación: /Users/ricdex/Documents/repos/ai/utec-ai/{PDF_FILENAME}")

if __name__ == "__main__":
    create_pdf()
