import GPUtil
from pylspci.parsers import SimpleParser

class GPUInfo:
    def __init__(self, name=None, vram=None):
        self.name = name
        self.vram = vram

    def __str__(self):
        # VRAM in GB
        vram = self.vram / 1024

        if vram % 1 == 0:
            vram = int(vram)

        return ' '.join(
            [
                self.name,
                f"({vram} GB)"
            ]
        )


def detect_nvidia():
    gpus = []
    for gpu in GPUtil.getGPUs():
        gpus.append(GPUInfo(name=gpu.name, vram=gpu.memoryTotal))
    return gpus

def detect_lspci():
    gpus = []
    try:
        for device in SimpleParser().run():
            if '[03' in str(device.cls):
                print(device)

    except FileNotFoundError as e:
        return gpus

    return gpus


def detect():
    available = []

    available += detect_nvidia()

    detect_lspci()

    return available
