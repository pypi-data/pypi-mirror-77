!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?exports.AttachAddon=e():t.AttachAddon=e()}(window,(function(){return function(t){var e={};function n(o){if(e[o])return e[o].exports;var r=e[o]={i:o,l:!1,exports:{}};return t[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}return n.m=t,n.c=e,n.d=function(t,e,o){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:o})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var r in t)n.d(o,r,function(e){return t[e]}.bind(null,r));return o},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=0)}([function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.AttachAddon=void 0;var o=function(){function t(t,e){this._disposables=[],this._socket=t,this._socket.binaryType="arraybuffer",this._bidirectional=!e||!1!==e.bidirectional}return t.prototype.activate=function(t){var e=this;this._disposables.push(r(this._socket,"message",(function(e){var n=e.data;t.write("string"==typeof n?n:new Uint8Array(n))}))),this._bidirectional&&(this._disposables.push(t.onData((function(t){return e._sendData(t)}))),this._disposables.push(t.onBinary((function(t){return e._sendBinary(t)})))),this._disposables.push(r(this._socket,"close",(function(){return e.dispose()}))),this._disposables.push(r(this._socket,"error",(function(){return e.dispose()})))},t.prototype.dispose=function(){this._disposables.forEach((function(t){return t.dispose()}))},t.prototype._sendData=function(t){1===this._socket.readyState&&this._socket.send(t)},t.prototype._sendBinary=function(t){if(1===this._socket.readyState){for(var e=new Uint8Array(t.length),n=0;n<t.length;++n)e[n]=255&t.charCodeAt(n);this._socket.send(e)}},t}();function r(t,e,n){return t.addEventListener(e,n),{dispose:function(){n&&t.removeEventListener(e,n)}}}e.AttachAddon=o}])}));
//# sourceMappingURL=xterm-addon-attach.js.map