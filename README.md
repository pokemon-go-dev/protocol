protocol
========

<!-- Tools for consuming and reversing the Pokemon Go API. -->

This repository consists of reconstructions of Pokemon Go's protobuf files and
a [mitmdump] script, `decode.py` to deserialize and reverse engineer the
Pokemon Go API.

Installation
------------

	protoc --python_out=protocol/ spec/*.proto

Usage
-----

To mitm and decode messages, use `decode.py`

	mitmdump --script ./decode.py --port 8080

The `*.proto` files are in `spec/`.

Inspired By
-----------

* [bettse/mitmdump_decoder]
* [Mila432/Pokemon_Go_API]
* [tejado/pokemongo-api-demo]
* [/r/pokemongodev]

[/r/pokemongodev]: https://reddit.com/r/pokemongodev
[Mila432/Pokemon_Go_API]: https://github.com/Mila432/Pokemon_Go_API
[tejado/pokemongo-api-demo]: https://github.com/tejado/pokemongo-api-demo
[bettse/mitmdump_decoder]: https://github.com/bettse/mitmdump_decoder
[mitmdump]: https://github.com/mitmproxy/mitmproxy
