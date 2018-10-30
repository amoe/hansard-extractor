import pytest
from validation import validate

def test_answer():
    actual = 2 + 2
    expected = 4
    assert actual == expected

valid_xml = """
    <p>
      <member>The Lord Chancellor</member>
      <membercontribution> said, I have to acquaint you that</membercontribution>
   </p>
"""

# The rules for membercontributions are not enforced by the xml schema.
# According to the schema, the records are more-or-less just a long sequence of
# <p> which can have mixed content.  However, in practice relevant <p>
# will always contain a <member> followed by a <membercontribution> with
# nothing in between, before, or after, as above.  So we have to check for this.

def test_validate_contributions_pairs():
    assert validate(valid_xml) == True
