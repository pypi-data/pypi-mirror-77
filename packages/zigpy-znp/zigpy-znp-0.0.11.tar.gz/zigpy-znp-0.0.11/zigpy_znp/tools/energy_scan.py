import sys
import asyncio
import logging
import argparse
import itertools

from collections import defaultdict, deque

import zigpy_znp.types as t
import zigpy_znp.commands as c

from zigpy_znp.zigbee.application import ControllerApplication

LOGGER = logging.getLogger(__name__)


def channels_from_channel_mask(channels: t.Channels):
    for channel in range(11, 26 + 1):
        if channels & t.Channels.from_channel_list([channel]):
            yield channel


async def perform_energy_scan(radio_path, num_scans=None, auto_form=False):
    LOGGER.info("Starting up zigpy-znp")

    app = ControllerApplication(
        ControllerApplication.SCHEMA({"device": {"path": radio_path}})
    )

    try:
        await app.startup(auto_form=auto_form, write_nvram=auto_form)
    except RuntimeError:
        LOGGER.error("The hardware needs to be configured before this tool can work.")
        LOGGER.error("Re-run this command with -f (--form).")
        return

    LOGGER.info("Running scan...")

    # We compute an average over the last 5 scans
    channel_energies = defaultdict(lambda: deque([], maxlen=5))

    for i in itertools.count(start=1):
        if num_scans is not None and i > num_scans:
            break

        rsp = await app._znp.request_callback_rsp(
            request=c.ZDO.MgmtNWKUpdateReq.Req(
                Dst=0x0000,
                DstAddrMode=t.AddrMode.NWK,
                Channels=t.Channels.ALL_CHANNELS,
                ScanDuration=0x02,  # exponent
                ScanCount=1,
                NwkManagerAddr=0x0000,
            ),
            RspStatus=t.Status.SUCCESS,
            callback=c.ZDO.MgmtNWKUpdateNotify.Callback(partial=True, Src=0x0000),
        )

        for channel, energy in zip(
            channels_from_channel_mask(rsp.ScannedChannels), rsp.EnergyValues
        ):
            energies = channel_energies[channel]
            energies.append(energy)

        total = 0xFF * len(energies)

        print(f"Channel energy ({len(energies)} / {energies.maxlen}):")

        for channel, energies in channel_energies.items():
            count = sum(energies)

            print(
                f" - {channel:>02}: {count / total:>7.2%}  "
                + "#" * int(100 * count / total)
            )

        print()


async def main(argv):
    import coloredlogs

    parser = argparse.ArgumentParser(description="Perform an energy scan")
    parser.add_argument("serial", type=argparse.FileType("rb"), help="Serial port path")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        default=0,
        help="Increases verbosity",
    )
    parser.add_argument(
        "-n",
        "--num-scans",
        dest="num_scans",
        type=int,
        default=None,
        help="Number of scans to perform before exiting",
    )
    parser.add_argument(
        "-f",
        "--form",
        dest="form",
        action="store_true",
        default=False,
        help="Initializes the hardware by writing to NVRAM",
    )

    args = parser.parse_args(argv)

    log_level = [logging.INFO, logging.DEBUG][min(max(0, args.verbose), 1)]
    logging.getLogger("zigpy_znp").setLevel(log_level)
    coloredlogs.install(level=log_level)

    # We just want to make sure it exists
    args.serial.close()

    await perform_energy_scan(
        args.serial.name, auto_form=args.form, num_scans=args.num_scans
    )


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))  # pragma: no cover
