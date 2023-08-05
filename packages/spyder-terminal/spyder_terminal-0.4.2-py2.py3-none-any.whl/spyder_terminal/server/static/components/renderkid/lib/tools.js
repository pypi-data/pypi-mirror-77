// Generated by CoffeeScript 1.9.3
var htmlparser, object, objectToDom, self;

htmlparser = require('htmlparser2');

object = require('utila').object;

objectToDom = require('dom-converter').objectToDom;

module.exports = self = {
  repeatString: function(str, times) {
    var i, j, output, ref;
    output = '';
    for (i = j = 0, ref = times; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      output += str;
    }
    return output;
  },
  toDom: function(subject) {
    if (typeof subject === 'string') {
      return self.stringToDom(subject);
    } else if (object.isBareObject(subject)) {
      return self._objectToDom(subject);
    } else {
      throw Error("tools.toDom() only supports strings and objects");
    }
  },
  stringToDom: function(string) {
    var handler, parser;
    handler = new htmlparser.DomHandler;
    parser = new htmlparser.Parser(handler);
    parser.write(string);
    parser.end();
    return handler.dom;
  },
  _fixQuotesInDom: function(input) {
    var j, len, node;
    if (Array.isArray(input)) {
      for (j = 0, len = input.length; j < len; j++) {
        node = input[j];
        self._fixQuotesInDom(node);
      }
      return input;
    }
    node = input;
    if (node.type === 'text') {
      return node.data = self._quoteNodeText(node.data);
    } else {
      return self._fixQuotesInDom(node.children);
    }
  },
  objectToDom: function(o) {
    if (!Array.isArray(o)) {
      if (!object.isBareObject(o)) {
        throw Error("objectToDom() only accepts a bare object or an array");
      }
    }
    return self._fixQuotesInDom(objectToDom(o));
  },
  quote: function(str) {
    return String(str).replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;').replace(/\ /g, '&sp;').replace(/\n/g, '<br />');
  },
  _quoteNodeText: function(text) {
    return String(text).replace(/\&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;').replace(/\ /g, '&sp;').replace(/\n/g, "&nl;");
  },
  getCols: function() {
    var cols, tty;
    tty = require('tty');
    cols = (function() {
      try {
        if (tty.isatty(1) && tty.isatty(2)) {
          if (process.stdout.getWindowSize) {
            return process.stdout.getWindowSize(1)[0];
          } else if (tty.getWindowSize) {
            return tty.getWindowSize()[1];
          } else if (process.stdout.columns) {
            return process.stdout.columns;
          }
        }
      } catch (_error) {}
    })();
    if (typeof cols === 'number' && cols > 30) {
      return cols;
    } else {
      return 80;
    }
  }
};
