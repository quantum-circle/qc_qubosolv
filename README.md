## Full contents

- [Installation Notes](#quick-summary)
- [A Minimal Example](#learn-how-qc_qubosolv-works)
- [Help and documentation](#help-and-documentation)
- [License](#license)

## Installation Notes

After downloading and unzipping the repository, you will be able to install the library using either native python setuptools: 
```
python setup.py install
```
or the pip package manager:
```
pip install .
```
This will also automatically download all required 3rd party packages.



## A Minimal Example
The following code snippet demonstrates how to use Quantum Circle's QUBO solver module `qc_qubosolv`. 

More detailed Jupyter notebook examples can be found in the `/examples` directory, including descriptions of the functionality and an introduction to simulated (quantum) annealing solvers.

```
>>> from qc_qubosolv import Solver
>>> 
>>> 
>>> # 1. Create the QUBO matrix to be solved
... qubo_matrix = [
...     [-1, 2], 
...     [2, -4]
... ]
>>> 
>>> # 2. Initialize the solver client
... solver = Solver(
...     username='YOUR_USERNAME_HERE', 
...     password='YOUR_PASSWORD_HERE'
... )
>>> 
>>> # 3. Solve the previously created QUBO problem
... result = solver.solve(qubo_matrix, algorithm='sqa')
>>> 
>>> # 4. Print the optimal bitstring and its corresponding objective function value
... print(f"Optimal bitstring: x = {result.optimal_bitstring}")
Optimal bitstring: x = [0 1]
>>> print(f"Optimal energy: f(x) = {result.optimal_energy}")
Optimal energy: f(x) = -4.0
```



## Help and documentation

If you're looking for help learning about the API, start with these resources:

- [API Documentation](https://docs.quantum-circle.com)



## License

[Apache](LICENSE).