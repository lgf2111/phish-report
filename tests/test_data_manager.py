# Offline tests for data_manager.
# We run these in a temporary folder so the real reports.json is never touched.
# The 'tmp_path' and 'monkeypatch' bits are provided by pytest.

import data_manager


def test_load_returns_empty_list_when_no_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # work in an empty temp folder
    assert data_manager.load() == []


def test_save_then_load_round_trip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data_manager.save({"message": "hi", "result": {"priority": "review"}})
    records = data_manager.load()
    assert len(records) == 1
    assert records[0]["message"] == "hi"


def test_save_appends_records(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data_manager.save({"message": "one"})
    data_manager.save({"message": "two"})
    records = data_manager.load()
    assert len(records) == 2
    assert records[1]["message"] == "two"


def test_query_filters_records(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data_manager.save({"message": "a", "result": {"priority": "high"}})
    data_manager.save({"message": "b", "result": {"priority": "review"}})
    high_only = data_manager.query(lambda r: r["result"]["priority"] == "high")
    assert len(high_only) == 1
    assert high_only[0]["message"] == "a"


def test_load_handles_corrupt_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # write junk that is not valid JSON
    (tmp_path / "reports.json").write_text("this is not json {{{")
    # should not crash - just return an empty list
    assert data_manager.load() == []
