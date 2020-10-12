
from core.pdf.pdf import PDF
from models.member import Member
from typing import List
from utils.date_utils import format_date_to_locale

class MembersPDF() :

    def __init__(self):
        pass

    def generate_pdf(self, members : List[Member]) -> bytes:
        pdf = PDF()
        pdf.add_page('Landscape')
        pdf.alias_nb_pages()
        pdf.set_title('Members List')
        pdf.set_font('Times', '', 10)
        # Effective page width, or just epw
        epw = pdf.w - 2*pdf.l_margin
        
        # Set column width to 1/8 of effective page width to distribute content 
        # evenly across table and page
        col_width = epw/13
        fiscal_code_width   = 1.5*col_width
        birth_date_width    = 1.1*col_width
        address_width       = 2*col_width
        zip_code_width      = 13
        province_width      = 14
        gender_width        = 10
        email_width         = 1.5*col_width


        # Text height is the same as current font size
        th = pdf.font_size + 5

        pdf.cell(col_width, th,     'Nome', border=1)
        pdf.cell(col_width, th,     'Cognome', border=1)
        pdf.cell(birth_date_width, th,     'Data di nascita', border=1)
        pdf.cell(col_width, th,     'Luogo', border=1)
        pdf.cell(fiscal_code_width, th,     'Codice Fiscale', border=1)
        pdf.cell(address_width, th,     'Indirizzo', border=1)
        pdf.cell(zip_code_width, th,     'CAP', border=1)
        pdf.cell(col_width, th,     'Città', border=1)
        pdf.cell(province_width, th,     'Provincia', border=1)
        pdf.cell(gender_width, th,     'Sesso', border=1)
        pdf.cell(col_width, th,     'Telefono', border=1)
        pdf.cell(email_width, th,     'Email', border=1)
        pdf.ln(th)

        pdf.set_font('Times', '', 8)

        for member in members:
            #pdf.cell(0, 10, member.name, 0, 1)
            pdf.cell(col_width, th, member.name, border=1)
            pdf.cell(col_width, th, member.last_name, border=1)
            pdf.cell(birth_date_width, th, format_date_to_locale(str(member.birth_date)), border=1)
            pdf.cell(col_width, th, member.birth_place, border=1)
            pdf.cell(fiscal_code_width, th, member.fiscal_code, border=1)
            pdf.cell(address_width, th, member.address, border=1)
            pdf.cell(zip_code_width, th, member.zip_code, border=1)
            pdf.cell(col_width, th, member.city, border=1)
            pdf.cell(province_width, th, member.province, border=1)
            pdf.cell(gender_width, th, member.gender, border=1)
            pdf.cell(col_width, th, member.phone, border=1)
            pdf.cell(email_width, th, member.email, border=1)

            pdf.ln(th)

        pdf.output('tuto2.pdf', 'F')
        with open('tuto2.pdf','rb') as pdf:
            return pdf.read()