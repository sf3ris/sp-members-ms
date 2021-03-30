from mongoengine import Document
from core.pdf.pdf import PDF
from typing import List

from models.athlete import Athlete
from models.member import Member
from utils.date_utils import format_date_to_locale

import uuid
import os


class MembersPDF():

    def __init__(self):
        pass

    def generate_athletes_pdf(
            self,
            athletes: List[Athlete],
            columns: List[str]) -> bytes:
        return self.generate_pdf('Elenco atleti', athletes, columns)

    def generate_members_pdf(
            self,
            athletes: List[Member],
            columns: List[str]) -> bytes:
        return self.generate_pdf('Elenco soci', athletes, columns)

    def generate_pdf(
            self,
            title: str,
            documents: List[Document],
            columns: List[str]
    ) -> bytes:
        pdf = PDF()
        pdf.add_page('Landscape')
        pdf.alias_nb_pages()
        pdf.set_title(title)
        pdf.set_font('Times', '', 9)
        pdf.set_fill_color(240, 240, 240)
        # Effective page width, or just epw
        epw = pdf.w - 2 * pdf.l_margin

        # Set column width to 1/8 of effective page width to distribute content
        # evenly across table and page
        col_width = epw / 14
        name_width = 1.5 * col_width
        fiscal_code_width = 1.5 * col_width
        birth_date_width = 0.8 * col_width
        birth_place_width = 2 * col_width
        address_width = 2.2 * col_width
        zip_code_width = 11
        province_width = 14
        gender_width = 10
        expiry_date_width = 0.8 * col_width
        email_width = 1.5 * col_width

        # Text height is the same as current font size
        th = pdf.font_size + 5

        if 'last_name' in columns:
            pdf.cell(name_width, th, 'Cognome', border=1, fill=True)
        if 'name' in columns:
            pdf.cell(name_width, th, 'Nome', border=1, fill=True)
        if 'birth_date' in columns:
            pdf.cell(birth_date_width, th, 'Nato il', border=1, fill=True)
        if 'birth_place' in columns:
            pdf.cell(birth_place_width, th, 'Luogo', border=1, fill=True)
        if 'fiscal_code' in columns:
            pdf.cell(fiscal_code_width, th, 'Codice Fiscale', border=1, fill=True)
        if 'address' in columns:
            pdf.cell(address_width, th, 'Indirizzo', border=1, fill=True)
        if 'zip_code' in columns:
            pdf.cell(zip_code_width, th, 'CAP', border=1, fill=True)
        if 'city' in columns:
            pdf.cell(col_width, th, 'Città', border=1, fill=True)
        if 'province' in columns:
            pdf.cell(province_width, th, 'Provincia', border=1, fill=True)
        if 'gender' in columns:
            pdf.cell(gender_width, th, 'Sesso', border=1, fill=True)
        if 'phone' in columns:
            pdf.cell(col_width, th, 'Telefono', border=1, fill=True)
        if 'email' in columns:
            pdf.cell(email_width, th, 'Email', border=1, fill=True)
        if 'membership' in columns:
            pdf.cell(expiry_date_width, th, 'Scadenza', border=1, fill=True)
        if 'status' in columns:
            pdf.cell(expiry_date_width, th, 'Stato', border=1, fill=True)
        pdf.ln(th)

        pdf.set_font('Times', '', 8)

        for document in documents:

            latest_membership = document.get_latest_membership()

            if 'last_name' in columns:
                pdf.cell(name_width, th, document.last_name, border=1)
            if 'name' in columns:
                pdf.cell(name_width, th, document.name, border=1)
            if 'birth_date' in columns:
                pdf.cell(birth_date_width, th, format_date_to_locale(str(document.birth_date)), border=1)
            if 'birth_place' in columns:
                pdf.cell(birth_place_width, th, document.birth_place, border=1)
            if 'fiscal_code' in columns:
                pdf.cell(fiscal_code_width, th, document.fiscal_code, border=1)
            if 'address' in columns:
                pdf.cell(address_width, th, document.address, border=1)
            if 'zip_code' in columns:
                pdf.cell(zip_code_width, th, document.zip_code, border=1)
            if 'city' in columns:
                pdf.cell(col_width, th, document.city, border=1)
            if 'province' in columns:
                pdf.cell(province_width, th, document.province, border=1)
            if 'gender' in columns:
                pdf.cell(gender_width, th, document.gender, border=1)
            if 'phone' in columns:
                pdf.cell(col_width, th, document.phone, border=1)
            if 'email' in columns:
                pdf.cell(email_width, th, document.email, border=1)
            if 'membership' in columns:
                pdf.cell(
                    expiry_date_width,
                    th,
                    format_date_to_locale(str(latest_membership))
                    if latest_membership is not None else '',
                    border=1
                )
            if 'status' in columns:
                pdf.cell(
                    expiry_date_width,
                    th,
                    'Attivo' if document.is_enabled() else 'Non Attivo',
                    border=1,
                    fill=True
                )
            pdf.ln(th)

        filename = "tmp/" + uuid.uuid4().hex + ".pdf"
        data = pdf.output(name=filename, dest="F")

        with open(filename, 'rb') as pdf:
            data = pdf.read()
            pdf.close()

        os.remove(filename)
        return data
