#!/usr/bin/env python3

import statistics as st
import glob
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
                    thr = dev_stat["txkB"] * 8 / 1000 # Mbps
                    bpses.append(thr)
    return bpses

def get_peek_speed(pathname):
    bpses = []
    for fn in glob.glob(pathname):
        bpses += parse_tx_throughput(fn)
    return max(bpses)

def parse_rtt(reg):
    with open("rtts/{}.rtt.txt".format(reg), "r") as f:
        for line in f:
            if not "rtt min/avg/max/mdev" in line:
                continue
            # parse the last output of ping: rtt min/avg/max/mdev = x/x/x/x ms
            s = line.split(" ")[3].split("/")
            avg = float(s[1])
            mdev = float(s[3])
    return avg, mdev

def main():

    regions = ["osaka", "oregon", "sydney"]

    print("Region    RTT   mscp stdev     scp stdev  mscp peak  scp peak  improve  reduction")
    print("---------------------------------------------------------------------------------")
    for reg in regions:
        mscp_times = []
        scp_times = []
        for fn in glob.glob("dat/{}/mscp/duration-*.txt".format(reg)):
            with open(fn, "r") as f:
                mscp_times.append(float(f.read().strip()))
        mscp_peak = get_peek_speed("dat/{}/mscp/sysstat-*.sar.net.json".format(reg))

        for fn in glob.glob("dat/{}/scp/duration-*.txt".format(reg)):
            with open(fn, "r") as f:
                scp_times.append(float(f.read().strip()))
        scp_peak = get_peek_speed("dat/{}/scp/sysstat-*.sar.net.json".format(reg))

        avg, mdev = parse_rtt(reg)
        
        mean_mscp = st.mean(mscp_times)
        mean_scp = st.mean(scp_times)
        

        print("{:6} {:>6.2f}   ".format(reg, avg) +
              "{:>4.2f} {:>4.2f}   {:>7.2f} {:>4.2f}".format(st.mean(mscp_times),
                                                             st.stdev(mscp_times),
                                                             st.mean(scp_times),
                                                             st.stdev(scp_times)) +
              "  {:>8.2f}  {:>8.2f}".format(mscp_peak, scp_peak) +
              "   {:>5.2f}".format(mscp_peak / scp_peak) +
              "     {:>5.1f}%".format((mean_scp - mean_mscp) / mean_scp * 100)
              )

        

main()
