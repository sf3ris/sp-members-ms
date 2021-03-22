from mongoengine import Document
from typing import List


def import_document(
        document: Document,
        rows: List,
        name_field: str,
        last_name_field: str,
        birth_date_field: str,
        birth_place_field: str,
        fiscal_code_field: str,
        address_field: str,
        zip_code_field: str,
        city_field: str,
        province_field: str,
        gender_field: str,
        phone_field: str,
        email_field: str
) -> List:
    documents = []
    for row in rows:
        date = row[birth_date_field].split("/")
        birth_date = "-".join(
            [date[2], date[1], date[0]]
        ) if len(date) > 1 else ""

        doc = document(
            name=row.get(name_field, ""),
            last_name=row.get(last_name_field, ""),
            birth_date=birth_date,
            birth_place=row.get(birth_place_field),
            fiscal_code=row.get(fiscal_code_field),
            address=row.get(address_field, ""),
            zip_code=row.get(zip_code_field, ""),
            city=row.get(city_field, ""),
            province=row.get(province_field, ""),
            gender=row.get(gender_field, ""),
            phone=row.get(phone_field, ""),
            email=row.get(email_field, "")
        )

        if not doc.is_empty():
            documents.append(doc)

    document.objects.insert(documents)
    return [document.jsonify() for document in documents]
