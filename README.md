# KUKSA-VISS

**NOTE: KUKSA-VISS is deprecated and will reach End-of-Life 2024-12-31!**

*Basic [VISS version 2](https://www.w3.org/TR/viss2-transport/) websocket support has been added to*
*[KUKSA Databroker](https://github.com/eclipse/kuksa.val/blob/master/doc/protocol/support.md)*
*and this adapter is no longer needed!*

A VISS2 compatible adapter for KUKSA databroker.

VISS2 Spec: https://github.com/w3c/automotive

Supported calls
 - Simple get (no filters)
 - Simple set (no filters)
 - Simple subsribe (no filters)

To install and run

```
pip install -r requirements.txt
python tinyvissv2.py
```

See `test.py` for a simple client for testing
