#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import json

link = "ens4"

def parse_tx_throughput(fn):

    bpses = []
    with open(fn, "r") as f:
        j = json.load(f)
        stats = j["sysstat"]["hosts"][0]["statistics"]
        for s in stats:
            for dev_stat in s["network"]["net-dev"]:
                if dev_stat["iface"] == link:
                    thr = dev_stat["txkB"] * 8 / 1000 / 1000 # Gbps
                    bpses.append(thr)
    return bpses

def main():

    plt.style.use("./myplot.mpstyle")

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", choices = ["osaka", "oregon", "sydney"],
                        default = "osaka",
                        help = "region to be plotted")
    parser.add_argument("-a", "--aspect", type = float, default = 0.5,
                        help = "graph aspect")
    parser.add_argument("-z", "--zoom", type = float, default = 1.0,
                        help = "zoom ratio")
    parser.add_argument("-p", "--pdffile", default = None,
                        help = "output graph filename")

    args = parser.parse_args()

    bpses = parse_tx_throughput("{}/mscp.sar.net.json".format(args.region))
    print("Gbps: {}".format(" ".join(map(lambda x: "{:.2f}".format(x), bpses))))

    width = 6.4 * args.zoom
    fig = plt.figure(figsize = (width, width * args.aspect))
    ax = fig.subplots()

    xaxis = list(range(1, len(bpses) + 1))

    ax.plot(xaxis, bpses, marker = "")
    ax.set_ylim(0, 10)
    ax.set_ylabel("throughput (Gbps)")

    ax.set_xlim([min(xaxis) - 1, max(xaxis) + 1])
    ax.set_xlabel("time (second)")

    ax.set_box_aspect(args.aspect)

    if not args.pdffile:
        args.pdffile = "graph/thr-{}.pdf".format(args.region)

    print("save to {}".format(args.pdffile))
    plt.savefig(args.pdffile, bbox_inches = "tight", pad_inches = 0.05)

main()
