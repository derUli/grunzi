import GPUtil
from pylspci.parsers import SimpleParser

VENDOR_NVIDIA = 'NVIDIA'

class GPUInfo:
    def __init__(self, name=None, vendor=None, vram=None):
        self.name = name
        self.vendor = vendor
        self.vram = vram


    def __str__(self):
        # VRAM in GB
        vram = self.vram / 1024

        if vram % 1 == 0:
            vram = int(vram)

        return ' '.join(
            [
                self.vendor,
                self.name,
                f"({vram} GB)"
            ]
        )


def detect_nvidia():
    gpus = []
    for gpu in GPUtil.getGPUs():
        name_without_vendor = gpu.name.replace(VENDOR_NVIDIA, '').strip()
        gpus.append(GPUInfo(name=name_without_vendor, vendor=VENDOR_NVIDIA, vram=gpu.memoryTotal))
    return gpus

def detect_lspci():
    gpus = []
    try:
        for device in SimpleParser().run():
            if '[03' in str(device.cls):
                print(device)

                gpus.append(
                    GPUInfo(name=device.device.name, vendor=device.vendor, vram=None)
                )

    except FileNotFoundError as e:
        return gpus

    return gpus


def detect():
    available = []

    available += detect_nvidia()

    available += detect_lspci()

    return available
