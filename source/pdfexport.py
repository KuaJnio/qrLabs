import logging

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

LOGGER = logging.getLogger(__name__)

def convert_time(timestamp):
    return(datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M"))


def export_courses(data):
    try:
        for i in range(0,len(data)):
            tmp = int(data[i][0])
            LOGGER.debug(tmp)
            data[i][0] = convert_time(tmp)
            LOGGER.debug(convert_time(tmp))
        doc = SimpleDocTemplate('export.pdf',
                                rightMargin=0,
                                leftMargin=0,
                                topMargin=20,
                                bottomMargin=0,
                                pagesize=letter)

        elements = []
        im = Image("static/ban.png", 7*inch, 0.8*inch)
        elements.append(im)
        styleSheet = getSampleStyleSheet()
        elements.append(Paragraph('''<para fontSize="18"><br/><br/>DATE DU RELEVE : '''+str(datetime.now().strftime("%d-%m-%Y %H:%M"))+'''<br/><br/></para>''', styleSheet["Normal"]))
        head = ('DATE', 'LIEU', 'LABO', 'COURSIER', 'NB_TOTAL', 'SANGUINS', 'AUTRES')
        heads = [head]
        h=Table(heads)
        table_style = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('FONTSIZE', (0,0), (-1,-1), 10),
                               ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                               ('VALIGN', (0,0), (-1,-1), 'TOP')])
        h.setStyle(table_style)
        h.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.green)]))
        h._argW[0]=1.3*inch
        h._argW[1]=1.5*inch
        h._argW[2]=0.7*inch
        h._argW[3]=1.5*inch
        h._argW[4]=0.9*inch
        h._argW[5]=0.9*inch
        h._argW[6]=0.9*inch
        for i in range(0,len(h._argH)):
            h._argH[i] = 0.25*inch
        elements.append(h)
        if not len(data) == 0:
            t=Table(data)
            t.setStyle(table_style)
            t._argW[0]=1.3*inch
            t._argW[1]=1.5*inch
            t._argW[2]=0.7*inch
            t._argW[3]=1.5*inch
            t._argW[4]=0.9*inch
            t._argW[5]=0.9*inch
            t._argW[6]=0.9*inch
            for i in range(0,len(t._argH)):
                t._argH[i] = 0.25*inch
            table_style = []
            for i, row in enumerate(t._argH):
              if i % 2 == 0:
                table_style.append(('BACKGROUND',(0,i),(-1,i),colors.lightgrey))
              else:
                table_style.append(('BACKGROUND',(0,i),(-1,i),colors.white))
            t.setStyle(TableStyle(table_style))
            elements.append(t)
        doc.build(elements)
    except Exception as e:
        LOGGER.error("Error in export_courses(): "+str(e))
