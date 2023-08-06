# Equation Solver

This package can be used to solve linear equations encode in JSON.
Sample format is given below:  

```
{
    "op": "equal",
    "lhs": {
        "op": "add",
        "lhs": 1,
        "rhs": {
            "op": "multiply",
            "lhs": "x",
            "rhs": 10
        }
    },
    "rhs": 21
}

```

A driver program is included in the package to give an idea how to use the package.