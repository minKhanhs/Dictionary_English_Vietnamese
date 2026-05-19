from config.app_config import AppConfig
from models.word import Word


class WordTest:
    @staticmethod
    def run(runner):
        word = Word(" Hello ", "xin chao", "Hello!", ["hi"])
        runner.assert_equal("hello", word.get_english(), "word normalizes english")
        runner.assert_true(word.add_synonym("hey"), "add synonym succeeds")
        runner.assert_false(word.add_synonym("hey"), "duplicate synonym rejected")
        runner.assert_equal(2, word.get_synonym_count(), "synonym count is correct")

        line = word.to_file_line()
        parsed = Word.from_file_line(line)
        runner.assert_equal("hello", parsed.get_english(), "word round trip english")
        runner.assert_equal("xin chao", parsed.get_vietnamese(), "word round trip meaning")
        runner.assert_true(parsed.has_synonym("hi"), "word round trip synonym")

        limited = Word("run", "chay")
        synonym_values = [
            "jog",
            "sprint",
            "dash",
            "race",
            "hurry",
            "rush",
            "speed",
            "bolt",
            "scamper",
            "canter",
            "lope",
            "trot",
        ]
        for synonym in synonym_values:
            limited.add_synonym(synonym)
        runner.assert_equal(
            AppConfig.MAX_SYNONYMS,
            limited.get_synonym_count(),
            "word limits synonyms",
        )

        runner.assert_equal(None, Word.from_file_line("bad line"), "bad line returns None")
