'use strict';

var GetIntrinsic = require('../GetIntrinsic');

var $TypeError = GetIntrinsic('%TypeError%');

var IsPropertyKey = require('./IsPropertyKey');
var SameValue = require('./SameValue');
var Type = require('./Type');

// IE 9 does not throw in strict mode when writability/configurability/extensibility is violated
var noThrowOnStrictViolation = (function () {
	try {
		delete [].length;
		return true;
	} catch (e) {
		return false;
	}
}());

// https://ecma-international.org/ecma-262/6.0/#sec-set-o-p-v-throw

module.exports = function Set(O, P, V, Throw) {
	if (Type(O) !== 'Object') {
		throw new $TypeError('Assertion failed: `O` must be an Object');
	}
	if (!IsPropertyKey(P)) {
		throw new $TypeError('Assertion failed: `P` must be a Property Key');
	}
	if (Type(Throw) !== 'Boolean') {
		throw new $TypeError('Assertion failed: `Throw` must be a Boolean');
	}
	if (Throw) {
		O[P] = V; // eslint-disable-line no-param-reassign
		if (noThrowOnStrictViolation && !SameValue(O[P], V)) {
			throw new $TypeError('Attempted to assign to readonly property.');
		}
		return true;
	} else {
		try {
			O[P] = V; // eslint-disable-line no-param-reassign
			return noThrowOnStrictViolation ? SameValue(O[P], V) : true;
		} catch (e) {
			return false;
		}
	}
};
