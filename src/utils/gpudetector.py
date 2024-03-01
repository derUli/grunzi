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
        if self.vram:
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
                GPUInfo(name=device.device.name, vendor=device.vendor, vram=None)
            )


    return gpus


def detect():
    available = []

    available += detect_nvidia()

    available += detect_lspci("""
    00:00.0 Host bridge: Intel Corporation 8th Gen Core Processor Host Bridge/DRAM Registers (rev 07)00:01.0 PCI bridge: Intel Corporation Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor PCIe Controller (x16) (rev 07)
00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 630 (Mobile)
00:08.0 System peripheral: Intel Corporation Xeon E3-1200 v5/v6 / E3-1500 v5 / 6th/7th Gen Core Processor Gaussian Mixture Model
00:12.0 Signal processing controller: Intel Corporation Cannon Lake PCH Thermal Controller (rev 10)
00:14.0 USB controller: Intel Corporation Cannon Lake PCH USB 3.1 xHCI Host Controller (rev 10)
00:14.2 RAM memory: Intel Corporation Cannon Lake PCH Shared SRAM (rev 10)
00:16.0 Communication controller: Intel Corporation Cannon Lake PCH HECI Controller (rev 10)
00:1b.0 PCI bridge: Intel Corporation Cannon Lake PCH PCI Express Root Port #19 (rev f0)
00:1b.3 PCI bridge: Intel Corporation Cannon Lake PCH PCI Express Root Port #20 (rev f0)
00:1d.0 PCI bridge: Intel Corporation Cannon Lake PCH PCI Express Root Port #9 (rev f0)
00:1d.4 PCI bridge: Intel Corporation Cannon Lake PCH PCI Express Root Port #13 (rev f0)
00:1f.0 ISA bridge: Intel Corporation Device a30d (rev 10)
00:1f.3 Audio device: Intel Corporation Cannon Lake PCH cAVS (rev 10)
00:1f.4 SMBus: Intel Corporation Cannon Lake PCH SMBus Controller (rev 10)
00:1f.5 Serial bus controller [0c80]: Intel Corporation Cannon Lake PCH SPI Controller (rev 10)
02:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 16)
03:00.0 Network controller: Intel Corporation Wireless 8265 / 8275 (rev 78)
04:00.0 Non-Volatile memory controller: Intel Corporation SSD Pro 7600p/760p/E 6100p Series (rev 03)
""")

    return available
