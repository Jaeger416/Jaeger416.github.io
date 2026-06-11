from scholarly import scholarly, ProxyGenerator
import json
from datetime import datetime
import os
import sys
import signal

# Hard wall-clock timeout so a blocked / retrying crawl can never hang the CI
# job for hours (the historical failure mode: scholarly looping for the full
# 6h Actions limit until the run was force-cancelled).
TIMEOUT_SECONDS = int(os.environ.get('CRAWLER_TIMEOUT', '600'))


def _timeout(signum, frame):
    raise TimeoutError(f'Crawler exceeded {TIMEOUT_SECONDS}s')


signal.signal(signal.SIGALRM, _timeout)
signal.alarm(TIMEOUT_SECONDS)


def crawl():
    # Route requests through free proxies to reduce the chance of Google
    # Scholar blocking the shared GitHub Actions IP. Best-effort: if no proxy
    # can be set up we fall back to a direct connection.
    try:
        pg = ProxyGenerator()
        if pg.FreeProxies():
            scholarly.use_proxy(pg)
    except TimeoutError:
        raise  # let the wall-clock timeout abort cleanly, don't swallow it
    except Exception as e:
        print(f'::warning::Could not set up proxy, trying direct: {e}', file=sys.stderr)

    # The Scholar ID is public (it's in the site config / profile URL), so fall
    # back to it when the GOOGLE_SCHOLAR_ID secret isn't set, rather than crashing.
    scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID') or 'mlu1Oo4AAAAJ'
    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    return author


try:
    author = crawl()
except Exception as e:
    # Blocked / timed out / parse error. Exit cleanly (green run) and produce no
    # output files so the previous citation stats already on the
    # google-scholar-stats branch stay untouched.
    print(f'::warning::Google Scholar crawl failed, keeping previous data: {e}', file=sys.stderr)
    sys.exit(0)
finally:
    signal.alarm(0)

name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']: v for v in author['publications']}
print(json.dumps(author, indent=2))
os.makedirs('results', exist_ok=True)
with open('results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}
with open('results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
