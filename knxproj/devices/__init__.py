"""Module that defines vendor specific devices."""


from . import mdt


def dev2vendor(device):
    """Create vendor device from the generic device."""
    if "GT2" in device.product_id:
        return mdt.GT2.from_device(device, texts=device.other["texts"])
    return device
