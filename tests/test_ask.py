from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        def __init__(self, *, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    timestamps = iter([10.0, 12.345])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(timestamps))

    assert ask_module.ask("質問") == "回答"
    output = capsys.readouterr().out
    assert "入力: 12" in output
    assert "出力: 34" in output
    assert "[response time] 2.35秒" in output