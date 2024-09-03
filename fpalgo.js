const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

function processFingerprint(_0x36bb43) {
      var _0x216bb6;
      var _0xc9fde2 = unescape(encodeURIComponent(JSON.stringify(_0x36bb43)));
      var _0x1d5e1e = [];
      var _0x3dc4c6 = 0;
      var _0x194769 = '';
      for (var _0x3e2978 = 0; _0x3e2978 < 256; _0x3e2978++) {
        _0x1d5e1e[_0x3e2978] = _0x3e2978;
      }
      for (var _0x3326d3 = 0; _0x3326d3 < 256; _0x3326d3++) {
        _0x3dc4c6 = (_0x3dc4c6 + _0x1d5e1e[_0x3326d3] + "FZMÛSê/·V«xÞhí¢³4<`ô2ª,µ¦Yû".charCodeAt(_0x3326d3 % "FZMÛSê/·V«xÞhí¢³4<`ô2ª,µ¦Yû".length)) % 256;
        _0x216bb6 = _0x1d5e1e[_0x3326d3];
        _0x1d5e1e[_0x3326d3] = _0x1d5e1e[_0x3dc4c6];
        _0x1d5e1e[_0x3dc4c6] = _0x216bb6;
      }
      var _0x3837e7 = 0;
      _0x3dc4c6 = 0;
      for (var _0x56c78d = 0; _0x56c78d < _0xc9fde2.length; _0x56c78d++) {
        _0x3dc4c6 = (_0x3dc4c6 + _0x1d5e1e[_0x3837e7 = (_0x3837e7 + 1) % 256]) % 256;
        _0x216bb6 = _0x1d5e1e[_0x3837e7];
        _0x1d5e1e[_0x3837e7] = _0x1d5e1e[_0x3dc4c6];
        _0x1d5e1e[_0x3dc4c6] = _0x216bb6;
        _0x194769 += String.fromCharCode(_0xc9fde2.charCodeAt(_0x56c78d) ^ _0x1d5e1e[(_0x1d5e1e[_0x3837e7] + _0x1d5e1e[_0x3dc4c6]) % 256]);
      }
      return btoa(_0x194769);
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











