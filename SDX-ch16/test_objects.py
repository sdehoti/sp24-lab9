from io import StringIO
from textwrap import dedent

from objects import SaveObjects, LoadObjects

saveObjects = SaveObjects
loadObjects = LoadObjects

def test_save_bool_single():
    output = StringIO()
    saveObjects.save_bool(output, True)
    assert output.getvalue() == "bool:True\n"


def test_save_dict_empty():
    output = StringIO()
    saveObjects.save_dict(output, {})
    assert output.getvalue() == "dict:0\n"


def test_save_dict_flat():
    fixture = {"alpha": "beta", 1: 2}
    expected = dedent("""\
    dict:2
    str:1
    alpha
    str:1
    beta
    int:1
    int:2
    """)
    output = StringIO()
    saveObjects.save_dict(output, fixture)
    assert output.getvalue() == expected


def test_save_float_single():
    output = StringIO()
    saveObjects.save_float(output, 1.23)
    assert output.getvalue() == "float:1.23\n"


def test_save_int_single():
    output = StringIO()
    saveObjects.save_int(output, -456)
    assert output.getvalue() == "int:-456\n"


# [test_save_list_flat]
def test_save_list_flat():
    fixture = [0, False]
    expected = dedent("""\
    list:2
    int:0
    bool:False
    """)
    output = StringIO()
    saveObjects.save_list(output, fixture)
    assert output.getvalue() == expected
# [/test_save_list_flat]


def test_save_str_single():
    fixture = dedent("""\
    a
    b
    c
    """)
    expected = dedent("""\
    str:4
    a
    b
    c

    """)
    output = StringIO()
    saveObjects.save_str(output, fixture)
    assert output.getvalue() == expected


def test_save_set_flat():
    fixture = {1, "a"}
    first = dedent("""\
    set:2
    int:1
    str:1
    a
    """
    )
    second = dedent("""\
    set:2
    str:1
    a
    int:1
    """
    )
    output = StringIO()
    saveObjects.save_set(output, fixture)
    actual = output.getvalue()
    assert actual in {first, second}


def test_load_bool_single():
    fixture = StringIO("bool:True\n")
    assert loadObjects.load_bool(fixture) == True


def test_load_dict_empty():
    fixture = StringIO("dict:0\n")
    assert loadObjects.load_dict(fixture) == {}


def test_load_dict_flat():
    fixture = StringIO(
        dedent("""\
        dict:2
        str:1
        alpha
        str:1
        beta
        int:1
        int:2
        """)
    )
    assert loadObjects.load_dict(fixture) == {"alpha": "beta", 1: 2}


def test_load_float_single():
    fixture = StringIO("float:1.23\n")
    assert loadObjects.load_float(fixture) == 1.23


def test_load_int_single():
    fixture = StringIO("int:-456\n")
    assert loadObjects.load_int(fixture) == -456


def test_load_list_flat():
    fixture = StringIO(
        dedent(
            """\
    list:2
    int:0
    bool:False
    """
        )
    )
    assert loadObjects.load_list(fixture) == [0, False]


def test_load_str_single():
    fixture = StringIO(
        dedent(
            """\
    str:4
    a
    b
    c

    """
        )
    )
    expected = dedent(
        """\
    a
    b
    c
    """
    )
    assert loadObjects.load_str(fixture) == expected


def test_load_set_flat():
    fixture = StringIO(
        dedent(
            """\
    set:2
    int:1
    str:1
    a
    """
        )
    )
    assert loadObjects.load_set(fixture) == {1, "a"}


def test_roundtrip():
    fixture = ["a", {"b": 987.6}, {"c", True}]
    output = StringIO()
    saveObjects.save_list(output, fixture)
    archive = output.getvalue()
    result = loadObjects.load_list(StringIO(archive))
    assert result == fixture

### Test runner
import time

def run_tests():
    results = {"pass": 0, "fail": 0, "error": 0}
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

if __name__ == '__main__':
    run_tests()
