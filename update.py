#!/usr/bin/env python

import os
import configparser
import xml.etree.ElementTree as ET

xml = "/config/config.xml"
autoProcess = os.environ.get("SMAPATH", "/usr/local/sma/sickbeard_mp4_automator")
autoProcess = os.path.join(autoProcess, "autoProcess.ini")


def main():
    if not os.path.isfile(xml):
        print("No Sonarr/Radarr config file found")
        return

    if not os.path.isfile(autoProcess):
        print("autoProcess.ini does not exist")
        return

    tree = ET.parse(xml)
    root = tree.getroot()
    port = root.find("Port").text
    sslport = root.find("SslPort").text
    webroot = root.find("UrlBase").text
    webroot = webroot if webroot else ""
    ssl = root.find("EnableSsl").text
    ssl = ssl.lower() in ["true", "yes", "t", "1", "y"] if ssl else False
    apikey = root.find("ApiKey").text
    section = os.environ.get("SMARS")
    if not section:
        print("No Sonarr/Radarr specifying ENV variable")
        return

    safeConfigParser = configparser.SafeConfigParser()
    safeConfigParser.read(autoProcess)

    # Set FFMPEG/FFProbe Paths
    safeConfigParser.set("MP4", "ffmpeg", "/usr/local/bin/ffmpeg")
    safeConfigParser.set("MP4", "ffprobe", "/usr/local/bin/ffprobe")

    # Set values from config.xml
    safeConfigParser.set(section, "apikey", apikey)
    safeConfigParser.set(section, "SSL", str(ssl))
    safeConfigParser.set(section, "port", sslport if ssl else port)
    safeConfigParser.set(section, "web_root", webroot)

    # Set IP from environment variable
    ip = os.environ.get("HOST")
    if ip:
        safeConfigParser.set(section, "host", ip)
    else:
        safeConfigParser.set(section, "host", "127.0.0.1")

    fp = open(autoProcess, "w")
    safeConfigParser.write(fp)
    fp.close()


if __name__ == '__main__':
    main()
