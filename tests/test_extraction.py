
import pytest

from src.extract.csv_extractor import CSVExtractor


def test_extract_valid_csv_and_add_metadata(tmp_path):
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text(
        "customer_id,name\n1,Alice\n2,Bob\n",
        encoding="utf-8"
    )

    extractor = CSVExtractor()
    result = extractor.extract(str(csv_file), "TEST_RUN_001")

    assert len(result) == 2
    assert list(result["customer_id"]) == [1, 2]
    assert list(result["source_file"]) == ["customers.csv", "customers.csv"]
    assert list(result["source_record_number"]) == [1, 2]
    assert list(result["run_id"]) == ["TEST_RUN_001", "TEST_RUN_001"]


def test_extract_missing_file(tmp_path):
    csv_file = tmp_path / "missing.csv"
    extractor = CSVExtractor()

    with pytest.raises(FileNotFoundError):
        extractor.extract(str(csv_file), "TEST_RUN_002")


def test_extract_directory_instead_of_file(tmp_path):
    extractor = CSVExtractor()

    with pytest.raises(ValueError, match="Path is not a file"):
        extractor.extract(str(tmp_path), "TEST_RUN_003")


def test_extract_empty_csv(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    extractor = CSVExtractor()

    with pytest.raises(ValueError, match="CSV file is empty"):
        extractor.extract(str(csv_file), "TEST_RUN_004")


def test_extract_malformed_csv(tmp_path):
    csv_file = tmp_path / "malformed.csv"
    csv_file.write_text(
        'customer_id,name\n1,"Alice\n2,Bob\n',
        encoding="utf-8"
    )

    extractor = CSVExtractor()

    with pytest.raises(ValueError, match="Unable to parse CSV file"):
        extractor.extract(str(csv_file), "TEST_RUN_005")
