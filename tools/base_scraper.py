import subprocess
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
from newspaper import Article
#get cookie from javascript disabled session
class BaseScraper:
    def execute_curl(self, url):
        try:
            result = subprocess.check_output([
                "curl",
                "--compressed",
                "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
                "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "-H", "Accept-Language: en-US,en;q=0.5",
                "-H", "Accept-Encoding: gzip, deflate, br",
                "-H", "Alt-Used: www.google.com",
                "-H", "Connection: keep-alive",
                "-H", "Upgrade-Insecure-Requests: 1",
                "-H", "Sec-Fetch-Dest: document",
                "-H", "Sec-Fetch-Mode: navigate",
                "-H", "Sec-Fetch-Site: same-origin",
                "-H", "Sec-Fetch-User: ?1",
                "-H", "Cookie: OTZ=7225810_68_72_104040_68_446700; NID=511=tMX3e3IaPeOYGNQjm-OMtMj-c2Y9GUSvxbP324oG013OJDRlWOSkj2oRtw55J2474xAlix9Vbzcv2KsEIKAHvW-3WRVI62TrRCDSj5b6l0DIjdsGGoYTPH76QU8xnLAM6BON3KeUNigbILeNKrXRreHS6mlArqX_cV8tmSX--ffMfcl1h4kbhxA-DwM", 
                url,
            ])
            return result
        except subprocess.CalledProcessError as e:
            print("Failed to execute curl command:", str(e))
            return None

