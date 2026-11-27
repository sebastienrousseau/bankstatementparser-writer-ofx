# Comparison

Where bankstatementparser-writer-ofx fits next to what a reader would
otherwise reach for. Every cell comes from this repository or the other
project's own PyPI description; nothing here is a measured ranking.

| Project | Writes OFX 1.x (SGML) | Writes OFX 2.x (XML) | Reads OFX | Input it writes from |
| :--- | :---: | :---: | :---: | :--- |
| **bankstatementparser-writer-ofx** | Yes (1.02) | No | No (the core `bankstatementparser` reads OFX) | `bankstatementparser` transactions, DataFrames, dicts |
| [`ofxtools`](https://pypi.org/project/ofxtools/) | Yes | Yes | Yes | Its own OFX object model |

## When each fits

- **bankstatementparser-writer-ofx**: your statements are already
  parsed by `bankstatementparser` (CAMT, MT940, CSV and the rest) and
  you want an OFX file an accounting tool can import, in one call.
- **ofxtools**: you need OFX 2.x, the full OFX object model, or to
  request statements from an OFX server.

The wider family is listed in [The suite](suite.md).
