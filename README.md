#  OpenEduQA

An Open Education Community

### Javascript Cheatshet

#### Set
```
    A Set is a collection of values, where each value may occur only once.

    Its main methods are:

    new Set(iterable) – creates the set, optionally from an array of values (any iterable will do).
    set.add(value) – adds a value, returns the set itself.
    set.delete(value) – removes the value, returns true if value existed at the moment of the call, otherwise false.
    set.has(value) – returns true if the value exists in the set, otherwise false.
    set.clear() – removes everything from the set.
    set.size – is the elements count.
```

We can use the Number(value) function to explicitly convert a value to a number

> Note: `set.has(value)` value have to be same type. i,e new Set([1,2,3]).has(1) return true but new Set(['1',2,3]).has(1)

