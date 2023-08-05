'use strict';

var GetIntrinsic = require('../GetIntrinsic');

var $TypeError = GetIntrinsic('%TypeError%');

var objectKeys = require('object-keys');

var callBound = require('../helpers/callBound');

var callBind = require('../helpers/callBind');

var $isEnumerable = callBound('Object.prototype.propertyIsEnumerable');
var $pushApply = callBind.apply(GetIntrinsic('%Array.prototype.push%'));

var forEach = require('../helpers/forEach');

var Type = require('./Type');

// https://www.ecma-international.org/ecma-262/8.0/#sec-enumerableownproperties

module.exports = function EnumerableOwnProperties(O, kind) {
	if (Type(O) !== 'Object') {
		throw new $TypeError('Assertion failed: Type(O) is not Object');
	}

	var keys = objectKeys(O);
	if (kind === 'key') {
		return keys;
	}
	if (kind === 'value' || kind === 'key+value') {
		var results = [];
		forEach(keys, function (key) {
			if ($isEnumerable(O, key)) {
				$pushApply(results, [
					kind === 'value' ? O[key] : [key, O[key]]
				]);
			}
		});
		return results;
	}
	throw new $TypeError('Assertion failed: "kind" is not "key", "value", or "key+value": ' + kind);
};
