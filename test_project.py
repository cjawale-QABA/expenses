import pytest
import os
from unittest.mock import patch, MagicMock
import project as project


# ---------- extract_file_text ----------
@pytest.mark.parametrize("file_path,ext,expected_func", [
    ("test.jpg", ".jpg", "extract_text_from_image"),
    ("test.pdf", ".pdf", "extract_text_from_pdf"),
    ("test.msg", ".msg", "extract_text_from_email"),
    ("test.txt", ".txt", None),
])
def test_extract_file_text(file_path, ext, expected_func):
    with patch("project.extractor") as mock_extractor:
        mock_extractor.extract_text_from_image.return_value = "image text"
        mock_extractor.extract_text_from_pdf.return_value = "pdf text"
        mock_extractor.extract_text_from_email.return_value = "email text"

        result = project.extract_file_text(file_path)

        if expected_func:
            assert expected_func in mock_extractor.mock_calls[0][0]
            assert isinstance(result, str)
        else:
            assert result == ""


# ---------- parsing_text ----------
def test_parsing_text():
    with patch("project.parser") as mock_parser:
        mock_parser.split_lines.return_value = ["line1", "line2"]
        mock_parser.extract_dates.return_value = ["2025-01-01"]
        mock_parser.extract_total_amounts.return_value = [100]
        mock_parser.extract_vendors_info.return_value = "VendorX"

        result = project.parsing_text("dummy text")

        assert result["dates"] == ["2025-01-01"]
        assert result["amounts"] == [100]
        assert result["vendor"] == "VendorX"
        mock_parser.split_lines.assert_called_once()


# ---------- normalizing_info ----------
def test_normalizing_info_with_valid_data():
    fake_data = {"dates": ["2025-01-01"], "amounts": [50], "vendor": "Shop"}
    with patch("project.normalizer.create_transaction_record", return_value={"vendor": "Shop"}) as mock_norm:
        result = project.normalizing_info(fake_data, "file.pdf")

        assert "vendor" in result
        mock_norm.assert_called_once_with("file.pdf", ["2025-01-01"], [50], "Shop")


def test_normalizing_info_with_incomplete_data():
    result = project.normalizing_info({"dates": [], "amounts": []}, "file.pdf")
    assert result == {}


# ---------- file_processing ----------
@patch("project.extract_file_text", return_value="dummy text")
@patch("project.parsing_text", return_value={"dates": ["2025-01-01"], "amounts": [10], "vendor": "ABC"})
@patch("project.normalizing_info", return_value={"date": "2025-01-01", "vendor": "ABC", "amount": 10})
@patch("project.exporter")
@patch("project.sorter")
@patch("os.path.isfile", return_value=False)
def test_file_processing_creates_csv(mock_isfile, mock_sorter, mock_exporter, mock_norm, mock_parse, mock_extract):
    project.file_processing("test.pdf")

    mock_exporter.create_csv.assert_called_once()
    mock_sorter.create_folders.assert_called_once_with("processed")
    mock_sorter.move_files.assert_called_once()