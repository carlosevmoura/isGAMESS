# isGAMESS
A script to automate calculation of inner-shell electronic excited states using IS-MCSCF method in GAMESS

## About the Inner-Shell Multiconfigurational Self-Consistent (IS-MCSCF) Method
The IS-MCSCF method is a *double-loop* MCSCF procedure. The active space is splitted in two orbital groups: one containing the core orbitals to be analysed and another containing the remaining orbitals used for the groud-state reference calculation. The electronic occupation of these groups is contrained, in order to avoid the variational collapse found when trying to obtain high-energy excited states. While one of the groups is optimzed, the other is kept frozen. The *double-loop* is repeated until the energy convergence is achieved.

## Usage
```sh
~ $ isGAMESS.py <input-file>
```

## Environment Setup
```sh
~ $ export GMSPATH='<GAMESS FULL PATH>'
```

## Next Implementations
- Add automation when running IS-MRMP method;
- Automate the construction of HEADER files;
- Include options for mor than two ORMAS groups;

## References

Rocha, A. (2011). Potential curves for inner-shell states of CO calculated at multiconfigurational self-consistent field level The Journal of Chemical Physics  134(2), 024107. [Link](https://dx.doi.org/10.1063/1.3528725)

Rocha, A., Moura, C. (2011). The problem of hole localization in inner-shell states of $N_2$ and $CO_2$ revisited with complete active space self-consistent field approach The Journal of Chemical Physics, 135(22), 224112. [Link](https://dx.doi.org/10.1063/1.3666016)

Moura, C., Oliveira, R., Rocha, A. (2013). Transition energy and potential energy curves for ionized inner-shell states of CO, O2 and N2 calculated by several inner-shell multiconfigurational approaches Journal of Molecular Modeling  19(5), 2027-2033. [Link](https://dx.doi.org/10.1007/s00894-012-1622-x)

Varas, L., Coutinho, L., Bernini, R., Betancourt, A., Moura, C., Rocha, A., Souza, G. (2017). Breaking the disulfide chemical bond using high energy photons: the dimethyl disulfide and methyl propyl disulfide molecules RSC Advances  7(58), 36525-36532. [Link](https://dx.doi.org/10.1039/c7ra05001a)
