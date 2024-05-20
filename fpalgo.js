const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

function processFingerprint(_0x4a761c) {
      var _0x2ce575;
      var _0x40db03 = unescape(encodeURIComponent(JSON.stringify(_0x4a761c)));
      var _0x16633c = [];
      var _0x446316 = 0;
      var _0x2e8cf0 = '';
      for (var _0x477886 = 0; _0x477886 < 256; _0x477886++) {
        _0x16633c[_0x477886] = _0x477886;
      }
      for (var _0x59729b = 0; _0x59729b < 256; _0x59729b++) {
        _0x446316 = (_0x446316 + _0x16633c[_0x59729b] + "FZMÛSê/·V«xÞhí¢³4<`ô2ª,µ¦Yû".charCodeAt(_0x59729b % "FZMÛSê/·V«xÞhí¢³4<`ô2ª,µ¦Yû".length)) % 256;
        _0x2ce575 = _0x16633c[_0x59729b];
        _0x16633c[_0x59729b] = _0x16633c[_0x446316];
        _0x16633c[_0x446316] = _0x2ce575;
      }
      var _0x710ce1 = 0;
      _0x446316 = 0;
      for (var _0x16418d = 0; _0x16418d < _0x40db03.length; _0x16418d++) {
        _0x446316 = (_0x446316 + _0x16633c[_0x710ce1 = (_0x710ce1 + 1) % 256]) % 256;
        _0x2ce575 = _0x16633c[_0x710ce1];
        _0x16633c[_0x710ce1] = _0x16633c[_0x446316];
        _0x16633c[_0x446316] = _0x2ce575;
        _0x2e8cf0 += String.fromCharCode(_0x40db03.charCodeAt(_0x16418d) ^ _0x16633c[(_0x16633c[_0x710ce1] + _0x16633c[_0x446316]) % 256]);
      }

      return btoa(_0x2e8cf0);
    }

app.post('/process_fingerprint', (req, res) => {
  const data = req.body;
  const result = processFingerprint(data);
  // console log part of the result like 100 chars
  console.log("fingerprint result: ", result.substring(0, 100));
  res.json({ result });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});











