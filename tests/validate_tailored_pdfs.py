from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
TAILORED = ROOT / "data" / "tailored"
OUTPUT = ROOT / "data" / "test_output" / "pdf_contact_sheets"
OUTPUT.mkdir(parents=True, exist_ok=True)

pdfs = sorted(TAILORED.glob("*.pdf"))
assert pdfs, "No tailored PDFs found"

for pdf_path in pdfs:
    reader = PdfReader(pdf_path)
    assert len(reader.pages) == 4, f"{pdf_path.name}: expected 4 pages, got {len(reader.pages)}"
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "Farzaneh Fayazbakhsh" in text
    assert "References" in text
    assert "#linebreak()" not in text
    assert "mailto:" not in text
    assert len(text) > 5000

    doc = pymupdf.open(pdf_path)
    rendered = []
    for page in doc:
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.15, 1.15), alpha=False)
        rendered.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))

    gap = 28
    label_height = 32
    width = max(image.width for image in rendered) * 2 + gap * 3
    height = (max(image.height for image in rendered) + label_height) * 2 + gap * 3
    sheet = Image.new("RGB", (width, height), "#d8dbe2")
    draw = ImageDraw.Draw(sheet)
    for index, image in enumerate(rendered):
        row, column = divmod(index, 2)
        x = gap + column * (image.width + gap)
        y = gap + row * (image.height + label_height + gap)
        draw.text((x, y), f"Page {index + 1}", fill="#111827")
        sheet.paste(image, (x, y + label_height))
    output = OUTPUT / f"{pdf_path.stem}_contact.png"
    sheet.save(output, optimize=True)
    print(f"{pdf_path.name}: pages=4 text_chars={len(text)} contact={output}")

print(f"pdf-structure-and-render-check: PASS ({len(pdfs)}/{len(pdfs)})")
