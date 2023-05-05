import io
import pathlib
import tempfile

import pytest

import replace


def test_read_from_stdin(monkeypatch):
    """
    Using '-' as the filename, we should read the input text from STDIN.
    """
    path = pathlib.Path("-")
    text = "foo\nbar\n"

    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    assert replace.read_file(path) == text


@pytest.mark.parametrize(
    "text",
    [
        # No line break at EOF
        "",
        " ",
        "1\n2",
        "1\r2",
        "1\r\n2",
        # Line break at EOF
        "1\n2\n",
        "1\r\n2\r\n",
        "1\r2\r",
        # Mixed-style line breaks
        "1\n2\r3\r\n",
        # Line break-only
        "\n",
        "\r",
        "\r\n",
    ],
)
def test_keep_original_line_breaks(text):
    """
    No matter how weird the original file is, we should never "normalize" the line
    breaks or loose data when reading or writing it. See also issue #2.
    """
    path = pathlib.Path(tempfile.mkstemp()[1])

    replace.save_file(path, text)
    assert replace.read_file(path) == text

    path.unlink()
