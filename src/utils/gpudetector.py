import GPUtil


class GPUInfo:
    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        return self.name

def detect_nvidia():
    gpus = []
    for gpu in GPUtil.getGPUs():
        gpus.append(GPUInfo(name=gpu.name))
    return gpus


def detect():
    available = []

    available += detect_nvidia()

    return available
