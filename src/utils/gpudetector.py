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
# Unfortunately lspci is Linux only
# If someone knows a platform independent alternative feel free to contribute
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

    def __init__(
            self, vendor: str | None = None,
            model: str | None = None,
            memory: int | float | None = None,
            vendor_id: str | None = None,
            device_id: str | None = None
    ):
        """
        Constructor
        @param model: GPU model
        @param vendor: GPU vendor
        @param memory: Size of video RAM in MB
        @param vendor_id: GPU PCI vendor id
        @param device_id: GPU PCI model id
        """
        self.model = model
        self.vendor = vendor
        self.memory = memory
        self.vendor_id = vendor_id
        self.device_id = device_id

    def __str__(self) -> str:
        """
        String representation in the format of
        NVIDIA GeForce GT 1030 (2 GB)
        AMD Radeon HD 6570
        Intel Corporation UHD Graphics 630 (Mobile)
        """

        memory_formatted = ""

        # If we were able to get the VRAM of the GPU
        if self.memory and self.memory > 0:
            memory = self.memory / 1024

            # If the GB size is even remove decimals
            if memory % 1 == 0:
                memory = int(memory)

            # Format VRAM
            memory_formatted = f"({memory} GB)"

        return ' '.join(
            [
                self.vendor,  # NVIDIA
                self.model,  # GeForce GT 1030
                memory_formatted  # (2 GB)
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
        gpus.append(
            GPUInfo(model=name_without_vendor, vendor=VENDOR_NVIDIA_SHORT, memory=gpu.memoryTotal)
        )

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


def detect_lspci() -> list:
    """ Detect other GPUs using lspci """
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
        # Skip all non GPU devices
        if '[03' not in str(device.cls):
            continue

        # Skip NVIDIA and AMD GPUs since they were already detected
        if device.vendor.name in IGNORE_VENDORS_LSPCI:
            # TODO: try to match PCI Vendor and model ID to already found GPUs
            continue

        # Add the GPU
        gpus.append(
            GPUInfo(
                # Vendor Name (Intel Corporation)
                vendor=device.vendor.name,
                # Model Name (UHD Graphics 630)
                model=device.device.name,
                # PCI Vendor ID (8086)
                vendor_id=device.vendor.id,
                # PCI Device ID (591B)
                device_id=device.device.id
            )
        )

    return gpus


def detect_gpus() -> list:
    """
    Detect the GPUS in this system
    @return:
    """
    available = []

    # Detect NVIDIA GPUs using GPUtil
    available += detect_nvidia()
    # Detect AMD GPUs using pyadl
    available += detect_amd()

    # Detect other GPUs using lspci
    available += detect_lspci()

    return available
