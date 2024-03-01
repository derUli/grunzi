import logging

import GPUtil

try:
    import pyadl
except Exception as e:
    pyadl = None
    logging.error(e)

from pylspci import SimpleParser

VENDOR_NVIDIA_SHORT = 'NVIDIA'
VENDOR_NVIDIA_LONG = 'NVIDIA Corporation'

VENDOR_AMD_SHORT = 'AMD'
VENDOR_AMD_LONG = ' Advanced Micro Devices, Inc.'
VENDOR_ATI_SHORT = 'ATI'

VENDOR_NVIDIA_ALL = [
    VENDOR_NVIDIA_SHORT,
    VENDOR_NVIDIA_LONG
]

VENDOR_AMD_ALL = [
    VENDOR_ATI_SHORT,
    VENDOR_AMD_LONG,
    VENDOR_AMD_LONG,
]

IGNORE_VENDORS_LSPCI = VENDOR_NVIDIA_ALL + VENDOR_AMD_ALL


class GPUInfo:
    def __init__(self, name=None, vendor=None, vram=None, vendor_id=None, device_id=None):
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
        name_without_vendor = str(gpu.name)

        for vendor in VENDOR_NVIDIA_ALL:
            name_without_vendor = name_without_vendor.replace(vendor, '')
            name_without_vendor = name_without_vendor.strip()
        gpus.append(GPUInfo(name=name_without_vendor, vendor=VENDOR_NVIDIA_SHORT, vram=gpu.memoryTotal))

    return gpus


def detect_amd():
    gpus = []

    if not pyadl:
        return gpus

    for device in pyadl.ADLManager.getInstance().getDevices():
        name_without_vendor = str(device.adapterName)

        for vendor in VENDOR_AMD_ALL:
            name_without_vendor = name_without_vendor.replace(vendor, '')
            name_without_vendor = name_without_vendor.strip()

        gpus.append(
            GPUInfo(name=name_without_vendor, vendor=VENDOR_AMD_SHORT)
        )

    return gpus


def detect_lspci():
    gpus = []

    devices = []

    try:
        devices = SimpleParser().run()
    except Exception as e:
        logging.error(e)

    for device in devices:
        if '[03' in str(device.cls):
            # These vendors are already detected by other libraries
            if device.vendor.name in IGNORE_VENDORS_LSPCI:
                # TODO: try to figure out PCI IDs for already detected GPUs
                # because GPUtil don't return PCI stuff
                continue

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
    available += detect_amd()

    # lspci as fallback for all other
    available += detect_lspci()

    return available
