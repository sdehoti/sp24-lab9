from io import StringIO
from textwrap import dedent

from objects import SaveObjects, LoadObjects

saveObjects = SaveObjects
loadObjects = LoadObjects

def generic_test(input):
    with open("test.txt", "w") as f:
        saver = SaveObjects(f)
        saver.save(input)
    with open("test.txt", "r") as f:
        loader = LoadObjects(f)
        return loader.load()

def test_save_bool_single():
    assert generic_test(True)

def test_save_dict_empty():
    assert generic_test({}) == {}

def test_save_dict_flat():
    assert generic_test({"alpha": "beta", 1: 2}) == {"alpha": "beta", 1: 2}

def test_save_float_single():
    assert generic_test(1.23) == 1.23

def test_save_int_single():
    assert generic_test(-456) == -456


# [test_save_list_flat]
def test_save_list_flat():
    assert generic_test([0, False]) == [0, False]
# [/test_save_list_flat]


def test_save_str_single():
    assert generic_test("""abc""") == """abc"""

def test_save_set_flat():
   assert generic_test({1, "a"}) == {1, "a"}

def test_roundtrip():
    assert generic_test(["a", {"b": 987.6}, {"c", True}]) == ["a", {"b": 987.6}, {"c", True}]

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
