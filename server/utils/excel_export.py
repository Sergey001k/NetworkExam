from openpyxl import Workbook
import os
import io

async def export_results(results, session_date):
    wb = Workbook()
    sheet = wb.active
    sheet.append(["ФИО", "Группа", "Результат"])

    for result in results:
        sheet.append([result.student_name, result.group, result.score])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f"Results-{session_date.date()} {session_date.hour}.{session_date.minute}.xlsx"

    return buffer, filename
