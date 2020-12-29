# AsciiMagic karton service

Extracts next stages of various ASCII files containind malware, for example hex, base64, etc.

**Author**: CERT.pl

**Maintainers**: ola, msm, nazywam

**Consumes:**
```json
{
    "type": "sample",
    "stage": "recognized",
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


## Usage

First of all, make sure you have setup the core system: https://github.com/CERT-Polska/karton

Then install karton-asciimagic from PyPi:

```shell
$ pip install karton-asciimagic

$ karton-asciimagic
```

![Co-financed by the Connecting Europe Facility by of the European Union](https://www.cert.pl/wp-content/uploads/2019/02/en_horizontal_cef_logo-1.png)
