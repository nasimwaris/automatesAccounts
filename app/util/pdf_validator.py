import magic

def is_valid_pdf(file_path):
    mime_type = magic.from_file(file_path, mime=True)
    return mime_type == 'application/pdf'
