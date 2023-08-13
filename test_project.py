from project import parse_resume
import pytest
from pdfminer.pdfparser import PDFSyntaxError


def test_parse_resume_valid_pdf():
    resume_bytes = b"%PDF-1.7\n..."
    parsed_result = parse_resume(resume_bytes)
    assert isinstance(parsed_result, dict)
    assert "Name" in parsed_result
    assert "Email" in parsed_result
    assert "Skills" in parsed_result


def test_parse_resume_invalid_pdf():

    resume_bytes = b"Invalid PDF content..."

    with pytest.raises(PDFSyntaxError):
        parse_resume(resume_bytes)


if __name__ == "__main__":
    test_parse_resume_valid_pdf()
    test_parse_resume_invalid_pdf()
