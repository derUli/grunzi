""" Generic GPU detection class """
import subprocess

# Used to detect NVIDIA GPUs
import GPUtil

# Used to detect amd GPUs
# UNTESTED since I don't own AMD GPUs.
try:
    import pyadl
except Exception as e:
    pyadl = None

# Use lspci as a fallback for all other (Intel, ???)
from pylspci import SimpleParser

# NVIDIA brand
VENDOR_NVIDIA_SHORT = 'NVIDIA'
VENDOR_NVIDIA_LONG = 'NVIDIA Corporation'

# AMD brand
VENDOR_AMD_SHORT = 'AMD'
VENDOR_AMD_LONG = ' Advanced Micro Devices, Inc.'
VENDOR_ATI_SHORT = 'ATI'

# All spellings of Nvidia brand
VENDOR_NVIDIA_ALL = [
    VENDOR_NVIDIA_SHORT,
    VENDOR_NVIDIA_LONG
]

# All spellings of AMD brand
VENDOR_AMD_ALL = [
    VENDOR_ATI_SHORT,
    VENDOR_AMD_LONG,
    VENDOR_AMD_LONG,
]

# lspci should only take care about the other GPUs
IGNORE_VENDORS_LSPCI = VENDOR_NVIDIA_ALL + VENDOR_AMD_ALL


class GPUInfo:
    """ Information about GPUs """

    def __init__(self, vendor=None, model=None, vram=None, vendor_id=None, device_id=None):
        """
        Constructor
        @param model: GPU model
        @param vendor: GPU vendor
        @param vram: Size of VRAM in MB
        @param vendor_id: GPU PCI vendor id
        @param device_id: GPU PCI model id
        """
        self.model = model
        self.vendor = vendor
        self.vram = vram
        self.vendor_id = vendor_id
        self.device_id = device_id

    def __str__(self) -> str:
        """
        String representation in the format of
        NVIDIA GeForce GT 1030 (2 GB)
        AMD Radeon HD 6570
        Intel Corporation UHD Graphics 630 (Mobile)
        """

        vram_formatted = ""

        # If we were able to get the VRAM of the GPU
        if self.vram and self.vram > 0:
            vram = self.vram / 1024

            # If the GB size is even remove decimals
            if vram % 1 == 0:
                vram = int(vram)

            # Format VRAM
            vram_formatted = f"({vram} GB)"

        return ' '.join(
            [
                self.vendor,
                self.model,
                vram_formatted
            ]
        )


def detect_nvidia() -> list:
    """
    Detect NVIDIA GPUs using GPUtil
    @return: Device
    """
    gpus = []
    for gpu in GPUtil.getGPUs():
        name_without_vendor = str(gpu.name)

        for vendor in VENDOR_NVIDIA_ALL:
            name_without_vendor = name_without_vendor.replace(vendor, '')
            name_without_vendor = name_without_vendor.strip()
        gpus.append(GPUInfo(model=name_without_vendor, vendor=VENDOR_NVIDIA_SHORT, vram=gpu.memoryTotal))

    return gpus


def detect_amd() -> list:
    """ Detect AMD GPUs using ADL """
    gpus = []

    # If there is no AMD driver there will be no pyadl
    if not pyadl:
        return gpus

    # Detect devices
    for device in pyadl.ADLManager.getInstance().getDevices():
        # Remove vendor name from device string
        name_without_vendor = str(device.adapterName)
        for vendor in VENDOR_AMD_ALL:
            name_without_vendor = name_without_vendor.replace(vendor, '')
            name_without_vendor = name_without_vendor.strip()

        # Add GPU to the list of gpus
        gpus.append(
            GPUInfo(model=name_without_vendor, vendor=VENDOR_AMD_SHORT)
        )

    return gpus


def detect_lspci():
    gpus = []

    # Try to run lspci
    try:
        devices = SimpleParser().run()
    except OSError:
        # If there is no lspci
        devices = []
    except subprocess.CalledProcessError:
        # lspci exists but can't be executed for some reason
        devices = []

    for device in devices:
        if '[03' in str(device.cls):
            # These vendors are already detected by other libraries
            if device.vendor.name in IGNORE_VENDORS_LSPCI:
                # TODO: try to figure out PCI IDs for already detected GPUs
                # because GPUtil don't return PCI stuff
                continue

            gpus.append(
                GPUInfo(
                    model=device.device.name,
                    vendor=device.vendor.name,
                    vendor_id=device.vendor.id,
                    device_id=device.device.id,
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
