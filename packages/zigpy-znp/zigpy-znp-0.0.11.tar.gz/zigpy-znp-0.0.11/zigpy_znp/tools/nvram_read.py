import sys
import json
import asyncio
import logging
import argparse

import zigpy_znp.types as t
import zigpy_znp.commands as c

from zigpy_znp.api import ZNP
from zigpy_znp.config import CONFIG_SCHEMA
from zigpy_znp.exceptions import InvalidCommandResponse, CommandNotRecognized
from zigpy_znp.types.nvids import NwkNvIds, OsalExNvIds

LOGGER = logging.getLogger(__name__)


async def backup(radio_path):
    znp = ZNP(CONFIG_SCHEMA({"device": {"path": radio_path}}))

    await znp.connect()

    data = {
        "osal": {},
        "nwk": {},
    }

    for nwk_nvid in NwkNvIds:
        try:
            value = await znp.nvram_read(nwk_nvid)
            LOGGER.info("%s = %s", nwk_nvid, value)

            data["nwk"][nwk_nvid.name] = value.hex()
        except InvalidCommandResponse:
            LOGGER.warning("Read failed for %s", nwk_nvid)
            continue

    try:
        # Old versions of Z-Stack do not have the OSAL NVIDs
        await znp.request(
            c.SYS.NVLength.Req(SysId=1, ItemId=OsalExNvIds.DEVICE_LIST, SubId=0)
        )
    except CommandNotRecognized:
        return data

    for osal_nvid in OsalExNvIds:
        length_rsp = await znp.request(
            c.SYS.NVLength.Req(SysId=1, ItemId=osal_nvid, SubId=0)
        )
        length = length_rsp.Length

        if length == 0:
            LOGGER.warning("Read failed for %s", osal_nvid)
            continue

        value = (
            await znp.request(
                c.SYS.NVRead.Req(
                    SysId=1, ItemId=osal_nvid, SubId=0, Offset=0, Length=length
                ),
                RspStatus=t.Status.SUCCESS,
            )
        ).Value
        LOGGER.info("%s = %s", osal_nvid, value)

        data["osal"][osal_nvid.name] = value.hex()

    return data


async def main(argv):
    import coloredlogs

    parser = argparse.ArgumentParser(description="Backup a radio's NVRAM")
    parser.add_argument("serial", type=argparse.FileType("rb"), help="Serial port path")
    parser.add_argument(
        "--output", "-o", type=argparse.FileType("w"), help="Output file", default="-"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        default=0,
        help="increases verbosity",
    )

    args = parser.parse_args(argv)

    log_level = [logging.INFO, logging.DEBUG][min(max(0, args.verbose), 1)]
    logging.getLogger("zigpy_znp").setLevel(log_level)
    coloredlogs.install(level=log_level)

    # We just want to make sure it exists
    args.serial.close()

    obj = await backup(args.serial.name)

    args.output.write(json.dumps(obj, indent=4))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))  # pragma: no cover
