from summarization import summarize
from dotenv import load_dotenv

load_dotenv(override=True)


def test_summarize():
    captures = [
        {
            "content": "This is the first document.",
            "metadata": {"author": "Alice", "date": "2022-01-01"},
        },
        {
            "content": "This is the second document.",
            "metadata": {"author": "Bob", "date": "2022-01-02"},
        },
    ]
    result = summarize(captures)
    print(result)


test_summarize()
