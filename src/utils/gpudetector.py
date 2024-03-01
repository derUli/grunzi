import GPUtil
from pylspci.parsers import SimpleParser

VENDOR_NVIDIA = 'NVIDIA'

class GPUInfo:
    def __init__(self, name=None, vendor=None, vram=None, vendor_id=None, device_id = None):
        self.name = name
        self.vendor = vendor
        self.vram = vram
        self.vendor_id = None
        self.device_id = None


    def __str__(self):
        # VRAM in GB

        vram_formatted = ''
        if self.vram and self.vram > 0:
            vram = self.vram / 1024

            if vram % 1 == 0:
                vram = int(vram)

            vram_formatted = f"({vram} GB)"

        return ' '.join(
            [
                self.vendor,
                self.name,
                vram_formatted
            ]
        )


def detect_nvidia():
    gpus = []
    for gpu in GPUtil.getGPUs():
        name_without_vendor = gpu.name.replace(VENDOR_NVIDIA, '').strip()
        gpus.append(GPUInfo(name=name_without_vendor, vendor=VENDOR_NVIDIA, vram=gpu.memoryTotal))
    return gpus

def detect_lspci(lspci_output = None):
    gpus = []


    if lspci_output:
        devices = SimpleParser().parse(lspci_output)
    else:
        try:
            devices = SimpleParser().run()
        except FileNotFoundError:
            devices = []

    for device in devices:
        if '[03' in str(device.cls):
            print(device)

            gpus.append(
                GPUInfo(
                    name=device.device.name,
                    vendor=device.vendor.name,
                    vram=None
                )
            )


    return gpus


def detect():
    available = []

    available += detect_nvidia()

    available += detect_lspci()

    return available
