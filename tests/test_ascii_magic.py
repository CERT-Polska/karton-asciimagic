import os
from karton.asciimagic import AsciiMagic

from karton.core import Task
from karton.core.test import KartonTestCase, TestResource


class AsciiMagicTestCase(KartonTestCase):
    karton_class = AsciiMagic

    def test_ascii_magic(self):
        test_groups = os.path.join(os.path.dirname(__file__), "testdata")
        for group in os.listdir(test_groups):
            test_group_dir = os.path.join(test_groups, group)
            for case in os.listdir(test_group_dir):
                if "." in os.path.basename(case):
                    continue
                with self.subTest(group + "/" + case):
                    case_path = os.path.join(test_group_dir, case)
                    with open(case_path, "rb") as f:
                        content = f.read()
                    sample = TestResource(case, content)
                    if os.path.isfile(case_path + ".decoded"):
                        with open(
                            os.path.join(test_group_dir, case) + ".decoded", "rb"
                        ) as f:
                            decoded = f.read()
                        expected = Task(
                            {
                                "type": "sample",
                                "kind": "raw",
                                "origin": "karton.asciimagic",
                            },
                            payload={
                                "parent": sample,
                                "sample": TestResource(case, decoded),
                            },
                        )
                    elif os.path.isfile(case_path + ".exe.decoded"):
                        with open(
                            os.path.join(test_group_dir, case) + ".exe.decoded", "rb"
                        ) as f:
                            decoded = f.read()
                        expected = Task(
                            {
                                "type": "sample",
                                "kind": "runnable",
                                "platform": "win32",
                                "extension": "exe",
                                "stage": "recognized",
                                "origin": "karton.asciimagic",
                            },
                            payload={
                                "parent": sample,
                                "sample": TestResource(case, decoded),
                            },
                        )
                    else:
                        raise RuntimeError("No decoded file for testcase")
                    task = Task(
                        {"type": "sample", "stage": "recognized", "kind": "ascii"},
                        payload={"sample": sample},
                    )
                    results = self.run_task(task)

                    self.assertTasksEqual(results, [expected])
