#!/usr/bin/python3
"""
High-performance asynchronous subdomain enumerator (optimized for speed).
Keep SHODAN_API_KEY in code per user request.
"""
import re
import sys
import argparse
import asyncio
import logging
from datetime import date, timedelta
from typing import Optional, Set, Awaitable
import aiohttp
from aiohttp import ClientTimeout, TCPConnector
from Enumeration.setting import SHODAN_API_KEY
try:
    import uvloop  # optional: much faster on Linux when installed
except Exception:
    uvloop = None
    
# tune these values up or down depending on your environment and target rate-limits
DEFAULT_CONCURRENCY = 10       # total concurrent HTTP requests
DEFAULT_LIMIT_PER_HOST = 10     # concurrent connections per host
REQUEST_TIMEOUT = 5            # seconds
RETRY_ATTEMPTS = 1
RETRY_BACKOFF = 0.25            # seconds base

# HTTP
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; fast-subenum/2.0)"}

# Precompiled regex patterns (fast)
HOSTNAME_JSON_RE = re.compile(r'"hostname"\s*:\s*"(.*?)"')
TD_RE = re.compile(r'<td[^>]*>(.*?)</td>', re.IGNORECASE | re.DOTALL)
HREF_RE_TEMPLATE = r'href\s*=\s*"(.*?)"'
CRTSH_TD_RE = re.compile(r'<TD>([\w\d\.\-\*]+)</TD>')
# quick host token pattern (used to filter candidate tokens)
CAND_RE = re.compile(r'[A-Za-z0-9\-\._]+')

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", stream=sys.stderr)
logger = logging.getLogger("RiftEnum")

# ---------------- HELPERS ----------------
def normalize(host: str, root: str) -> Optional[str]:
    """Return normalized subdomain only if it ends with root."""
    if not host:
        return None
    h = host.strip().rstrip('.')
    return h if h.endswith(root) else None

async def fetch(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore, *, ssl: Optional[bool], timeout: ClientTimeout) -> Optional[str]:
    """Fetch text with a couple of lightweight retries and backoff."""
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            async with sem:
                async with session.get(url, headers=HEADERS, timeout=timeout, ssl=ssl, allow_redirects=True) as resp:
                    # read as text; ignore partial decode errors
                    txt = await resp.text(errors='ignore')
                    # treat all text as useful; caller can inspect
                    return txt
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            if attempt < RETRY_ATTEMPTS:
                await asyncio.sleep(RETRY_BACKOFF * (2 ** (attempt - 1)))
                continue
            logger.debug("fetch give up %s -> %s", url, e)
            return None
        except asyncio.CancelledError:
            raise
        except Exception as e:  # unexpected errors
            logger.warning("fetch unexpected error %s -> %s", url, e, exc_info=logger.isEnabledFor(logging.DEBUG))
            return None
    return None

async def fetch_json(session: aiohttp.ClientSession, url: str, sem: asyncio.Semaphore, *, ssl: Optional[bool], timeout: ClientTimeout):
    """Fetch JSON with light retries."""
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            async with sem:
                async with session.get(url, headers=HEADERS, timeout=timeout, ssl=ssl, allow_redirects=True) as resp:
                    # read as json - set content_type None to ignore content-type mismatch
                    return await resp.json(content_type=None)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
            if attempt < RETRY_ATTEMPTS:
                await asyncio.sleep(RETRY_BACKOFF * (2 ** (attempt - 1)))
                continue
            logger.debug("fetch_json give up %s -> %s", url, e)
            return None
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.warning("fetch_json unexpected error %s -> %s", url, e, exc_info=logger.isEnabledFor(logging.DEBUG))
            return None
    return None

# ---------------- COLLECTORS ----------------
# All collectors return Set[str]

async def c99(session, target, sem, *, ssl, timeout) -> Set[str]:
    """c99 - iterate previous year's June->Dec scan pages but process results as they arrive."""
    logger.info("[c99] start")
    subs = set()
    year = date.today().year - 1
    start = date(year, 6, 1)
    end = date(year, 12, 31)
    delta = timedelta(days=1)
    urls = []
    d = start
    while d <= end:
        urls.append(f"https://subdomainfinder.c99.nl/scans/{d}/{target}")
        d += delta

    href_re = re.compile(HREF_RE_TEMPLATE.replace("()", ""), re.IGNORECASE)  # small local compile (we'll use generic pattern)
    tasks = [fetch(session, u, sem, ssl=ssl, timeout=timeout) for u in urls]
    # as_completed so we process pages as they come back
    for coro in asyncio.as_completed(tasks):
        txt = await coro
        if not txt:
            continue
        if "Something went wrong while scanning" in txt:
            continue
        # fast href extraction; then filter
        for match in re.finditer(r'href\s*=\s*"(.*?)"', txt, flags=re.IGNORECASE):
            href = match.group(1)
            if target in href and "subdomainfinder.c99.nl/scans" not in href:
                candidate = href.lstrip("/").lstrip("//").split("/")[0]
                n = normalize(candidate, target)
                if n:
                    subs.add(n)
    return subs

async def jldc(session, target, sem, *, ssl, timeout) -> Set[str]:
    logger.info("[jldc] start")
    url = f"https://jldc.me/anubis/subdomains/{target}"
    res = set()
    data = await fetch_json(session, url, sem, ssl=ssl, timeout=timeout)
    if isinstance(data, (list, tuple, set)):
        for s in data:
            n = normalize(str(s), target)
            if n:
                res.add(n)
    return res

async def alienvault(session, target, sem, *, ssl, timeout) -> Set[str]:
    logger.info("[alienvault] start")
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{target}/passive_dns"
    res = set()
    txt = await fetch(session, url, sem, ssl=ssl, timeout=timeout)
    if not txt:
        return res
    for m in HOSTNAME_JSON_RE.findall(txt):
        n = normalize(m, target)
        if n:
            res.add(n)
    return res

async def rapiddns(session, target, sem, *, ssl, timeout) -> Set[str]:
    """
    rapiddns: instead of BeautifulSoup, extract <td>...</td> entries via regex.
    """
    logger.info("[rapiddns] start")
    url = f"https://rapiddns.io/subdomain/{target}?full=1"
    res = set()
    txt = await fetch(session, url, sem, ssl=ssl, timeout=timeout)
    if not txt:
        return res
    for td in TD_RE.findall(txt):
        # strip tags if any inside td (quick)
        # limit token extraction to safe token pattern
        cand = ''.join(CAND_RE.findall(td))
        if cand.endswith(target):
            n = normalize(cand, target)
            if n:
                res.add(n)
    return res

async def anubis(session, target, sem, *, ssl, timeout) -> Set[str]:
    logger.info("[anubis] start")
    url = f"https://jonlu.ca/anubis/subdomains/{target}"
    res = set()
    data = await fetch_json(session, url, sem, ssl=ssl, timeout=timeout)
    if isinstance(data, (list, tuple, set)):
        for s in data:
            n = normalize(str(s), target)
            if n:
                res.add(n)
    return res

async def crtsh(session, target, sem, *, ssl, timeout) -> Set[str]:
    logger.info("[crtsh] start")
    url = f"https://crt.sh/?q=%.{target}&dir=^&sort=1"
    res = set()
    txt = await fetch(session, url, sem, ssl=ssl, timeout=timeout)
    if not txt:
        return res
    for s in CRTSH_TD_RE.findall(txt):
        if "*" in s:
            continue
        n = normalize(s, target)
        if n:
            res.add(n)
    return res

async def hackertarget(session, target, sem, *, ssl, timeout) -> Set[str]:
    logger.info("[hackertarget] start")
    url = f"https://api.hackertarget.com/hostsearch/?q={target}"
    res = set()
    txt = await fetch(session, url, sem, ssl=ssl, timeout=timeout)
    if not txt:
        return res
    for line in txt.splitlines():
        if not line:
            continue
        candidate = line.split(",")[0].strip()
        n = normalize(candidate, target)
        if n:
            res.add(n)
    return res

async def shodan(session, target, sem, *, ssl, timeout) -> Set[str]:
    logger.info("[shodan] start")
    res = set()
    if not SHODAN_API_KEY:
        return res
    url = f"https://api.shodan.io/dns/domain/{target}?key={SHODAN_API_KEY}"
    data = await fetch_json(session, url, sem, ssl=ssl, timeout=timeout)
    if not data:
        return res
    pre_subs = data.get("subdomains", []) if isinstance(data, dict) else []
    for p in pre_subs:
        if isinstance(p, str) and "*" not in p:
            candidate = f"{p}.{target}"
            n = normalize(candidate, target)
            if n:
                res.add(n)
    return res

# ---------------- ORCHESTRATION ----------------
async def _run_collector(name: str, coro: Awaitable) -> Set[str]:
    """Guard a collector so one failure does not stop the overall enumeration."""
    try:
        result = await coro
        if isinstance(result, (set, list, tuple)):
            return set(result)
        return set()
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        if logger.isEnabledFor(logging.DEBUG):
            logger.exception("[%s] collector failed", name)
        else:
            logger.warning("[%s] collector failed: %s", name, exc)
        return set()

async def run_all(target: str, concurrency: int, limit_per_host: int, ssl_verify: bool) -> Set[str]:
    timeout = ClientTimeout(total=REQUEST_TIMEOUT)
    sem = asyncio.Semaphore(concurrency)

    # connector tuned for speed and re-use
    connector = TCPConnector(limit=concurrency,
                             limit_per_host=limit_per_host,
                             ttl_dns_cache=300,
                             force_close=False)

    ssl_param = ssl_verify if ssl_verify else False

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        collectors = [
            ("c99", c99(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("jldc", jldc(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("alienvault", alienvault(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("rapiddns", rapiddns(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("anubis", anubis(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("crtsh", crtsh(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("hackertarget", hackertarget(session, target, sem, ssl=ssl_param, timeout=timeout)),
            ("shodan", shodan(session, target, sem, ssl=ssl_param, timeout=timeout)),
        ]
        subs = set()
        # process collector coroutines as they complete (faster result streaming)
        # asyncio.create_task was added in 3.7; fall back to ensure_future on older Pythons
        create_task_fn = getattr(asyncio, "create_task", None)
        if create_task_fn is None:
            create_task_fn = asyncio.ensure_future
        tasks = [create_task_fn(_run_collector(name, coro)) for name, coro in collectors]
        for fut in asyncio.as_completed(tasks):
            out = await fut
            subs.update(out)
        return subs

def rift_main(domain) -> set:
    # use uvloop if available and on unix for faster event loop
    if uvloop is not None:
        try:
            uvloop.install()
            logger.debug("uvloop installed for faster event loop")
        except Exception:
            pass

    created_loop = False
    loop = None
    try:
        try:
            # may raise RuntimeError in non-main threads on Python 3.6
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # create and set a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            created_loop = True

        subs = loop.run_until_complete(
            run_all(domain, concurrency=DEFAULT_CONCURRENCY, limit_per_host=DEFAULT_LIMIT_PER_HOST, ssl_verify=False)
        )
    except Exception as exc:
        if logger.isEnabledFor(logging.DEBUG):
            logger.exception("fatal error during enumeration")
        else:
            logger.error("fatal error during enumeration: %s", exc)
        return set()
    finally:
        # if we created the loop for this thread, clean it up
        if created_loop and loop is not None:
            try:
                loop.close()
            finally:
                try:
                    asyncio.set_event_loop(None)
                except Exception:
                    pass

    logger.info("total found subdomains: %d", len(subs))
    return subs

