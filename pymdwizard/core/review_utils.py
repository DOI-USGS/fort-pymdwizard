
try:
    from docx import Document
    from docx.shared import Inches
    from docx.shared import Pt
    from docx.shared import RGBColor
    from docx.enum.style import WD_STYLE_TYPE
except ImportError:
    docx = None

from pymdwizard.core import xml_utils
from pymdwizard.core import fgdc_utils

FGDC_LOOKUP = fgdc_utils.get_fgdc_lookup()


def _get_longname(tag):
    try:
        long_name = FGDC_LOOKUP[tag]['long_name']
    except KeyError:
        long_name = tag

    return long_name


def _load_styles(doc):
    heading1 = doc.styles['Normal']
    font = heading1.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(24)
    font.bold = True

    styles = doc.styles
    new_heading_style = styles.add_style('fgdc title', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 1']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(24)
    font.bold = True

    new_heading_style = styles.add_style('fgdc heading 2', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 2']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(18)
    font.bold = True

    new_heading_style = styles.add_style('fgdc heading 3', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Heading 3']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(13.5)
    font.bold = True

    new_heading_style = styles.add_style('fgdc bar', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    font.size = Pt(12)
    font.bold = True

    new_heading_style = styles.add_style('fgdc tag', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x48, 0x8A, 0xC7)
    font.size = Pt(12)
    font.italic = True

    new_heading_style = styles.add_style('fgdc tag content', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x15, 0x15, 0x15)
    font.size = Pt(12)
    font.italic = False
    font.bold = False

    new_heading_style = styles.add_style('fgdc content', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['Normal']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    font.size = Pt(12)
    font.italic = False

    new_heading_style = styles.add_style('fgdc link', WD_STYLE_TYPE.PARAGRAPH)
    new_heading_style.base_style = styles['List Bullet']
    font = new_heading_style.font
    font.name = 'Times New Roman'
    font.color.rgb = RGBColor(0x00, 0x00, 0xFF)
    font.size = Pt(12)
    font.underline = True
    font.bold = False


def _add_tag(doc, tag, content='', indent=None):
    cit = doc.add_paragraph(tag + ': ', style='fgdc tag')
    cit.paragraph_format.space_after = Inches(.005)
    if content:
        if len(content) > 70:
            content = doc.add_paragraph(content, style='fgdc tag content')
            content.paragraph_format.left_indent = Inches(indent)
            content.paragraph_format.line_spacing=1
        else:
            content = cit.add_run(content)
            content.italic = False
            content.bold = False
            content.font.color.rgb = RGBColor(0x15, 0x15, 0x15)

    return cit

def _add_child_content(doc, node, indent=0.25):
    line = _add_tag(doc, _get_longname(node.tag), node.text, indent)
    line.paragraph_format.left_indent = Inches(indent)
    for child in node.children:
        _add_child_content(doc, child, indent+0.25)

def generate_review_report(xml_document, docx_fname):
    document = Document()
    _load_styles(document)

    try:
        title_str = xml_document.metadata.idinfo.citation.citeinfo.title.text
    except:
        title_str = "No FGDC Title found at metadta/idinfo/citation/citeinfo/title"
    title = document.add_heading(title_str, level=1)
    title.style = document.styles['fgdc title']
    title.paragraph_format.line_spacing=1

    title2 = document.add_heading('Metadata:', level=2)
    title2.style = document.styles['fgdc heading 2']

    for child in xml_document.metadata.children:
        long_name = _get_longname(child.tag)
        link = document.add_paragraph(text=long_name, style='fgdc link')
        link.paragraph_format.left_indent = Inches(0.5)
        link.paragraph_format.line_spacing=1

    for child in xml_document.metadata.children:
        long_name = _get_longname(child.tag)
        bar = document.add_paragraph('_'*72, style='fgdc bar')

        section_title = document.add_heading(long_name+ ':', level=3)
        section_title.style = document.styles['fgdc heading 3']
        section_title.paragraph_format.space_after = Inches(.15)
        _add_child_content(document, child)

    document.save(docx_fname)