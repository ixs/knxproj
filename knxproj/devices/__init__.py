"""Module that defines vendor specific devices."""


from . import mdt


def dev2vendor(device, gas):
    """Create vendor device from the generic device."""
    if "GT2" in device.product_id:
        return mdt.GT2.from_device(device, texts=device.other["texts"])
    if "BE.2D04001" in device.product_id:
        return mdt.BE4.from_device(device, gas=gas)
    return device
