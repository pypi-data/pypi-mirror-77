'use strict';

/* eslint global-require: 0 */
// https://www.ecma-international.org/ecma-262/10.0/#sec-abstract-operations
var ES2019 = {
	'Abstract Equality Comparison': require('./2019/AbstractEqualityComparison'),
	'Abstract Relational Comparison': require('./2019/AbstractRelationalComparison'),
	'Strict Equality Comparison': require('./2019/StrictEqualityComparison'),
	AddEntriesFromIterable: require('./2019/AddEntriesFromIterable'),
	AdvanceStringIndex: require('./2019/AdvanceStringIndex'),
	ArrayCreate: require('./2019/ArrayCreate'),
	ArraySetLength: require('./2019/ArraySetLength'),
	ArraySpeciesCreate: require('./2019/ArraySpeciesCreate'),
	Call: require('./2019/Call'),
	CanonicalNumericIndexString: require('./2019/CanonicalNumericIndexString'),
	CompletePropertyDescriptor: require('./2019/CompletePropertyDescriptor'),
	CopyDataProperties: require('./2019/CopyDataProperties'),
	CreateDataProperty: require('./2019/CreateDataProperty'),
	CreateDataPropertyOrThrow: require('./2019/CreateDataPropertyOrThrow'),
	CreateHTML: require('./2019/CreateHTML'),
	CreateIterResultObject: require('./2019/CreateIterResultObject'),
	CreateListFromArrayLike: require('./2019/CreateListFromArrayLike'),
	CreateMethodProperty: require('./2019/CreateMethodProperty'),
	DateFromTime: require('./2019/DateFromTime'),
	DateString: require('./2019/DateString'),
	Day: require('./2019/Day'),
	DayFromYear: require('./2019/DayFromYear'),
	DaysInYear: require('./2019/DaysInYear'),
	DayWithinYear: require('./2019/DayWithinYear'),
	DefinePropertyOrThrow: require('./2019/DefinePropertyOrThrow'),
	DeletePropertyOrThrow: require('./2019/DeletePropertyOrThrow'),
	EnumerableOwnPropertyNames: require('./2019/EnumerableOwnPropertyNames'),
	FlattenIntoArray: require('./2019/FlattenIntoArray'),
	FromPropertyDescriptor: require('./2019/FromPropertyDescriptor'),
	Get: require('./2019/Get'),
	GetIterator: require('./2019/GetIterator'),
	GetMethod: require('./2019/GetMethod'),
	GetOwnPropertyKeys: require('./2019/GetOwnPropertyKeys'),
	GetPrototypeFromConstructor: require('./2019/GetPrototypeFromConstructor'),
	GetSubstitution: require('./2019/GetSubstitution'),
	GetV: require('./2019/GetV'),
	HasOwnProperty: require('./2019/HasOwnProperty'),
	HasProperty: require('./2019/HasProperty'),
	HourFromTime: require('./2019/HourFromTime'),
	InLeapYear: require('./2019/InLeapYear'),
	InstanceofOperator: require('./2019/InstanceofOperator'),
	Invoke: require('./2019/Invoke'),
	IsAccessorDescriptor: require('./2019/IsAccessorDescriptor'),
	IsArray: require('./2019/IsArray'),
	IsCallable: require('./2019/IsCallable'),
	IsConcatSpreadable: require('./2019/IsConcatSpreadable'),
	IsConstructor: require('./2019/IsConstructor'),
	IsDataDescriptor: require('./2019/IsDataDescriptor'),
	IsExtensible: require('./2019/IsExtensible'),
	IsGenericDescriptor: require('./2019/IsGenericDescriptor'),
	IsInteger: require('./2019/IsInteger'),
	IsPromise: require('./2019/IsPromise'),
	IsPropertyKey: require('./2019/IsPropertyKey'),
	IsRegExp: require('./2019/IsRegExp'),
	IsStringPrefix: require('./2019/IsStringPrefix'),
	IterableToList: require('./2019/IterableToList'),
	IteratorClose: require('./2019/IteratorClose'),
	IteratorComplete: require('./2019/IteratorComplete'),
	IteratorNext: require('./2019/IteratorNext'),
	IteratorStep: require('./2019/IteratorStep'),
	IteratorValue: require('./2019/IteratorValue'),
	MakeDate: require('./2019/MakeDate'),
	MakeDay: require('./2019/MakeDay'),
	MakeTime: require('./2019/MakeTime'),
	MinFromTime: require('./2019/MinFromTime'),
	modulo: require('./2019/modulo'),
	MonthFromTime: require('./2019/MonthFromTime'),
	msFromTime: require('./2019/msFromTime'),
	NumberToString: require('./2019/NumberToString'),
	ObjectCreate: require('./2019/ObjectCreate'),
	OrdinaryDefineOwnProperty: require('./2019/OrdinaryDefineOwnProperty'),
	OrdinaryGetOwnProperty: require('./2019/OrdinaryGetOwnProperty'),
	OrdinaryGetPrototypeOf: require('./2019/OrdinaryGetPrototypeOf'),
	OrdinarySetPrototypeOf: require('./2019/OrdinarySetPrototypeOf'),
	OrdinaryHasInstance: require('./2019/OrdinaryHasInstance'),
	OrdinaryHasProperty: require('./2019/OrdinaryHasProperty'),
	PromiseResolve: require('./2019/PromiseResolve'),
	RegExpExec: require('./2019/RegExpExec'),
	RequireObjectCoercible: require('./2019/RequireObjectCoercible'),
	SameValue: require('./2019/SameValue'),
	SameValueNonNumber: require('./2019/SameValueNonNumber'),
	SameValueZero: require('./2019/SameValueZero'),
	SecFromTime: require('./2019/SecFromTime'),
	Set: require('./2019/Set'),
	SetFunctionName: require('./2019/SetFunctionName'),
	SetIntegrityLevel: require('./2019/SetIntegrityLevel'),
	SpeciesConstructor: require('./2019/SpeciesConstructor'),
	SymbolDescriptiveString: require('./2019/SymbolDescriptiveString'),
	TestIntegrityLevel: require('./2019/TestIntegrityLevel'),
	thisBooleanValue: require('./2019/thisBooleanValue'),
	thisNumberValue: require('./2019/thisNumberValue'),
	thisStringValue: require('./2019/thisStringValue'),
	thisSymbolValue: require('./2019/thisSymbolValue'),
	thisTimeValue: require('./2019/thisTimeValue'),
	TimeClip: require('./2019/TimeClip'),
	TimeFromYear: require('./2019/TimeFromYear'),
	TimeString: require('./2019/TimeString'),
	TimeWithinDay: require('./2019/TimeWithinDay'),
	ToBoolean: require('./2019/ToBoolean'),
	ToDateString: require('./2019/ToDateString'),
	ToIndex: require('./2019/ToIndex'),
	ToInt16: require('./2019/ToInt16'),
	ToInt32: require('./2019/ToInt32'),
	ToInt8: require('./2019/ToInt8'),
	ToInteger: require('./2019/ToInteger'),
	ToLength: require('./2019/ToLength'),
	ToNumber: require('./2019/ToNumber'),
	ToObject: require('./2019/ToObject'),
	ToPrimitive: require('./2019/ToPrimitive'),
	ToPropertyDescriptor: require('./2019/ToPropertyDescriptor'),
	ToPropertyKey: require('./2019/ToPropertyKey'),
	ToString: require('./2019/ToString'),
	ToUint16: require('./2019/ToUint16'),
	ToUint32: require('./2019/ToUint32'),
	ToUint8: require('./2019/ToUint8'),
	ToUint8Clamp: require('./2019/ToUint8Clamp'),
	TrimString: require('./2019/TrimString'),
	Type: require('./2019/Type'),
	ValidateAndApplyPropertyDescriptor: require('./2019/ValidateAndApplyPropertyDescriptor'),
	WeekDay: require('./2019/WeekDay'),
	YearFromTime: require('./2019/YearFromTime')
};

module.exports = ES2019;
