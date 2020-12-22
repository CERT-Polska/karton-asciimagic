import binascii
import logging

from karton.core import Karton, Resource, Task

from .__version__ import __version__
from .asciiclassifier import AsciiClassifier
from .decoders import Decoder


class AsciiMagic(Karton):
    """
    Extract payloads from ASCII files containing variously encoded malware
    """

    identity = "karton.asciimagic"
    version = __version__
    filters = [{"type": "sample", "stage": "recognized", "kind": "ascii"}]
    persistent = True

    def process(self, task: Task) -> None:  # type: ignore
        sample = task.get_resource("sample")
        ascii_content = sample.content

        classifier = AsciiClassifier(ascii_content)
        classifier.classify()
        decoder = Decoder(ascii_content, classifier.verdict)
        try:
            decoder.decode()
        except binascii.Error:
            logging.warning("Error why trying to decode base64.")
            return

        if decoder.decoded:
            self.log.info("Decoded possible executable")
            if decoder.decoded[:2] == b"MZ":
                task_params = {
                    "type": "sample",
                    "kind": "runnable",
                    "stage": "recognized",
                    "platform": "win32",
                    "extension": "exe",
                }
            else:
                task_params = {"type": "sample", "kind": "raw"}
            new_sample = Resource(
                sample.name,
                decoder.decoded,
            )

            task = Task(task_params, payload={"sample": new_sample, "parent": sample})
            self.send_task(task)
