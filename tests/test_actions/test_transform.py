from pathlib import Path

import pytest
from bowler import Query

from dephell.actions._transform import transform_as_import


@pytest.mark.parametrize('code_in, code_out, old_name, new_name', [
    ('import foo\n', 'import bar as foo\n', 'foo', 'bar'),
])
def test_transform_as_import(code_in: str, code_out: str, old_name: str, new_name: str, temp_path: Path):
    path = temp_path / 'tmp.py'
    path.write_text(code_in)
    q = transform_as_import(query=Query(str(path)), old_name=old_name, new_name=new_name)
    q.execute(silent=True, write=True, interactive=False)
    result = path.read_text()
    if code_in == code_out:
        assert result != code_out, 'unexpected changes'
    else:
        assert result != code_in, 'nothing was changed'
        assert result == code_out, 'invalid changes'
