'use strict';Object.defineProperty(exports,'__esModule',{value:true});exports.isSpaceSeparator=isSpaceSeparator;exports.isIdStartChar=isIdStartChar;exports.isIdContinueChar=isIdContinueChar;exports.isDigit=isDigit;exports.isHexDigit=isHexDigit;var _unicode=require('../lib/unicode');var unicode=_interopRequireWildcard(_unicode);function _interopRequireWildcard(obj){if(obj&&obj.__esModule){return obj}else{var newObj={};if(obj!=null){for(var key in obj){if(Object.prototype.hasOwnProperty.call(obj,key))newObj[key]=obj[key]}}newObj.default=obj;return newObj}}function isSpaceSeparator(c){return unicode.Space_Separator.test(c)}function isIdStartChar(c){return c>='a'&&c<='z'||c>='A'&&c<='Z'||c==='$'||c==='_'||unicode.ID_Start.test(c)}function isIdContinueChar(c){return c>='a'&&c<='z'||c>='A'&&c<='Z'||c>='0'&&c<='9'||c==='$'||c==='_'||c==='\u200C'||c==='\u200D'||unicode.ID_Continue.test(c)}function isDigit(c){return /[0-9]/.test(c)}function isHexDigit(c){return /[0-9A-Fa-f]/.test(c)}