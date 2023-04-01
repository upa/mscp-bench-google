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
    parser.add_argument("-a", "--aspect", type = float, default = 0.2,
                        help = "graph aspect")
    parser.add_argument("-z", "--zoom", type = float, default = 1.8,
                        help = "zoom ratio")
    parser.add_argument("-p", "--pdffile", default = None,
                        help = "output graph filename")

    args = parser.parse_args()

    width = 6.4 * args.zoom
    fig = plt.figure(figsize = (width, width * args.aspect))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    axes = fig.subplots(2, 2, sharex = "all", sharey = "all")


    regions = [("osaka", 5), ("singapore", 5), ("oregon", 5), ("sydney", 4)]

    xmax = 25

    cmap = plt.get_cmap("tab10")

    for idx, (region, niter) in enumerate(regions):
        fn = "dat/{}/mscp/sysstat-{}.sar.net.json".format(region, niter)
        bpses = parse_tx_throughput(fn)
        print("{} Gbps: {}".format(region,
                                   " ".join(map(lambda x: "{:.2f}".format(x), bpses))))
        r = idx % 2
        c = int(idx / 2)
        print("{} {}".format(r, c))
        ax = axes[r][c]
        xaxis = list(range(1, len(bpses) + 1))
        ax.plot(xaxis, bpses, marker = "",
                label = region.capitalize(), color = cmap(idx))
        ax.legend(loc = "upper right", fontsize = 11.5)
        ax.set_xlim(0, xmax)
        ax.set_xticks([])

        ax.set_ylim(-1.5, 11.5)
        ax.set_yticks([0, 5, 10])
        ax.set_xticks([0, 5, 10, 15, 20, 25])


    fig.supxlabel("time (second)", y = -0.1 * args.zoom)
    fig.supylabel("throughput (Gbps)", x = 0.04 * args.zoom)

    if not args.pdffile:
        args.pdffile = "graph/thr-all.pdf"

    print("save to {}".format(args.pdffile))
    plt.savefig(args.pdffile, bbox_inches = "tight", pad_inches = 0.05)

main()
