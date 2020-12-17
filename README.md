# AsciiMagic karton service

Extracts next stages of various ASCII files containind malware, for example hex, base64, etc.

Author: CERT.pl
Maintainers: ola, msm, nazywam

**Consumes:**
```json
{
    "type": "sample",
    "stage": "recognized"
    "kind": "ascii"
} 
```

**Produces:**
```json
{
    "type": "sample",
    "kind": "runnable",
    "stage": "recognized",
    "platform": "win32",
    "extension": "exe",
}, {
    "type": "sample",
    "kind": "raw"
}
```
