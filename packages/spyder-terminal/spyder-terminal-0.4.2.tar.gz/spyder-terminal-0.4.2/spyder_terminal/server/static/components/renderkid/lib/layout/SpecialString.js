// Generated by CoffeeScript 1.9.3
var SpecialString, fn, i, len, prop, ref;

module.exports = SpecialString = (function() {
  var self;

  self = SpecialString;

  SpecialString._tabRx = /^\t/;

  SpecialString._tagRx = /^<[^>]+>/;

  SpecialString._quotedHtmlRx = /^&(gt|lt|quot|amp|apos|sp);/;

  function SpecialString(str) {
    if (!(this instanceof self)) {
      return new self(str);
    }
    this._str = String(str);
    this._len = 0;
  }

  SpecialString.prototype._getStr = function() {
    return this._str;
  };

  SpecialString.prototype.set = function(str) {
    this._str = String(str);
    return this;
  };

  SpecialString.prototype.clone = function() {
    return new SpecialString(this._str);
  };

  SpecialString.prototype.isEmpty = function() {
    return this._str === '';
  };

  SpecialString.prototype.isOnlySpecialChars = function() {
    return !this.isEmpty() && this.length === 0;
  };

  SpecialString.prototype._reset = function() {
    return this._len = 0;
  };

  SpecialString.prototype.splitIn = function(limit, trimLeftEachLine) {
    var buffer, bufferLength, justSkippedSkipChar, lines;
    if (trimLeftEachLine == null) {
      trimLeftEachLine = false;
    }
    buffer = '';
    bufferLength = 0;
    lines = [];
    justSkippedSkipChar = false;
    self._countChars(this._str, function(char, charLength) {
      if (bufferLength > limit || bufferLength + charLength > limit) {
        lines.push(buffer);
        buffer = '';
        bufferLength = 0;
      }
      if (bufferLength === 0 && char === ' ' && !justSkippedSkipChar && trimLeftEachLine) {
        return justSkippedSkipChar = true;
      } else {
        buffer += char;
        bufferLength += charLength;
        return justSkippedSkipChar = false;
      }
    });
    if (buffer.length > 0) {
      lines.push(buffer);
    }
    return lines;
  };

  SpecialString.prototype.trim = function() {
    return new SpecialString(this.str.trim());
  };

  SpecialString.prototype.trimLeft = function() {
    return new SpecialString(this.str.replace(/^\s+/, ''));
  };

  SpecialString.prototype.trimRight = function() {
    return new SpecialString(this.str.replace(/\s+$/, ''));
  };

  SpecialString.prototype._getLength = function() {
    var sum;
    sum = 0;
    self._countChars(this._str, function(char, charLength) {
      sum += charLength;
    });
    return sum;
  };

  SpecialString.prototype.cut = function(from, to, trimLeft) {
    var after, before, cur, cut;
    if (trimLeft == null) {
      trimLeft = false;
    }
    if (to == null) {
      to = this.length;
    }
    from = parseInt(from);
    if (from >= to) {
      throw Error("`from` shouldn't be larger than `to`");
    }
    before = '';
    after = '';
    cut = '';
    cur = 0;
    self._countChars(this._str, (function(_this) {
      return function(char, charLength) {
        if (_this.str === 'ab<tag>') {
          console.log(charLength, char);
        }
        if (cur === from && char.match(/^\s+$/) && trimLeft) {
          return;
        }
        if (cur < from) {
          before += char;
        } else if (cur < to || cur + charLength <= to) {
          cut += char;
        } else {
          after += char;
        }
        cur += charLength;
      };
    })(this));
    this._str = before + after;
    this._reset();
    return SpecialString(cut);
  };

  SpecialString._countChars = function(text, cb) {
    var char, charLength, m;
    while (text.length !== 0) {
      if (m = text.match(self._tagRx)) {
        char = m[0];
        charLength = 0;
        text = text.substr(char.length, text.length);
      } else if (m = text.match(self._quotedHtmlRx)) {
        char = m[0];
        charLength = 1;
        text = text.substr(char.length, text.length);
      } else if (text.match(self._tabRx)) {
        char = "\t";
        charLength = 8;
        text = text.substr(1, text.length);
      } else {
        char = text[0];
        charLength = 1;
        text = text.substr(1, text.length);
      }
      cb.call(null, char, charLength);
    }
  };

  return SpecialString;

})();

ref = ['str', 'length'];
fn = function() {
  var methodName;
  methodName = '_get' + prop[0].toUpperCase() + prop.substr(1, prop.length);
  return SpecialString.prototype.__defineGetter__(prop, function() {
    return this[methodName]();
  });
};
for (i = 0, len = ref.length; i < len; i++) {
  prop = ref[i];
  fn();
}
