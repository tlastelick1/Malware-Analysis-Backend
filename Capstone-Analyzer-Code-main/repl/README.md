# JS Deobfuscation
JS Deobfuscation is a Python script that deobfuscates JS code and it's time saver for you. Although it may not work with high degrees of obfuscation, it's a pretty nice tool to help you even if it's just a bit. You can see some example in the ``examples/`` folder. This idea came to me when I saw an obfuscated script on GitHub. I reversed it for sure lmao. All these examples are extracted from GitHub. There are some references in the script's header.

# Usage
```bash
~$ git clone https://github.com/Ximaz/js-deobfuscator
~$ cd js-deobfuscator
~$ python3 main.py <source.js>
```

# Patterns

### The OSA (Obfuscated String Array)
A plenty of online obfuscators creates an array at the top of the obfuscated code. In this array, you can find strings which are generally escaped. This array might then be shuffled, it depends on the obfuscation configuration. Then, in the script, all strings are refered to this array, which can include function names, require statements, console.log string, or some URLs such as API URLs.

This code ... :
```js
const fs = require("fs")
```
... might become :
```js
const _0x1e5f=["\x66\x73"],_0x1e6a=require(_0x1e5f[0])
```

### The OSA shuffler (not supported yet)
As mentionned above, in some case, the OSA might be shuffled. This means that all index you can see on the script aren't the same from declaration to runtime.

This code ... :
```js
const strings = ["fs", "./any.json"]
const fs = require(strings[0])
const anyJson = require(strings[1])
```
... might become :
```js
const osa=["\x66\x73", "\x2e\x2f\x61\x6e\x79\x2e\x6a\x73\x6f\x6e"];(function(osa, ...){ /* Anonymouse function that shuffles the OSA */ })(osa, ...);const _0x1e6a=require(osa[1]),_0x1e71=require(osa[0]);
```
In this example, the indexes ``0`` and ``1`` might not change because the array isn't that huge. With a greater OSA, it will be shuffled for sure.
