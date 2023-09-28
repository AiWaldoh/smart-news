
import httpx
import zlib
import gzip
from io import BytesIO

import brotli
import anyio

class BaseScraper:
    async def execute_curl(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Alt-Used": "www.google.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cookie": "OTZ=7225810_68_72_104040_68_446700; NID=511=tMX3e3IaPeOYGNQjm-OMtMj-c2Y9GUSvxbP324oG013OJDRlWOSkj2oRtw55J2474xAlix9Vbzcv2KsEIKAHvW-3WRVI62TrRCDSj5b6l0DIjdsGGoYTPH76QU8xnLAM6BON3KeUNigbILeNKrXRreHS6mlArqX_cV8tmSX--ffMfcl1h4kbhxA-DwM",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            for _ in range(3):  # try 3 times
                try:
                    response = await client.get(url, headers=headers)
                    return response.text
                except anyio.exceptions.ReadResourceBusy as e:
                    print(f"Retry due to {e}")
        
        return response.text
