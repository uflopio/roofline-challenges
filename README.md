<!-- vale write-good.E-Prime = YES -->
# Roofline Challenges

A collection of challenge for [roofline.dev](https://roofline.dev).

## Normative Keywords

- **MUST / MUST NOT**. Mandatory, no exceptions under any circumstanced.
- **SHOULD / SHOULD NOT**. Exceptions allowed, but discouraged.
- **MAY / MAY NOT**. Soft preference, needed for style and consistency.

## Style

### Problems

<!-- vale write-good.TooWordy = NO -->
- The problem _must_ support multiple valid solutions with differing performance characteristics.
<!-- vale write-good.TooWordy = YES -->
- The problem _must_ allow constructing a complete baseline solution from the problem statement alone.
- The problem _must_ remain self-contained and _must_ not reference external materials that define implementation details. It _should_ not have links, references to textbooks, blogs or YouTube videos, or anything else.
<!-- vale write-good.Passive = NO -->
<!-- vale write-good.E-Prime = NO -->
- The problem _must_ have a section that can be sped up by cleverly applying optimisation techniques.
<!-- vale write-good.E-Prime = YES -->
<!-- vale write-good.Passive = YES -->
- The problem _may_ expect results within some numerical tolerance.

### Text

- The text _must_ $\LaTeX$ for mathematical formulae. Learn to use it here: [Learn LaTeX](https://www.overleaf.com/learn).

- The text _should_ use underlines to denote vectors, like $\underline{a}$, $\underline{b}$ and $\underline{c}$.
- The text _should_ use letters from the beginning of the alphabet for vectors, so $\underline{a}$, $\underline{b}$, $\underline{c}$ and so on.
- The text _should_ use capitals to denote matrices, like $A$, $B$ and $C$.
- The text _should_ use letters from the beginning of the alphabet for matrices, so $A$, $B$, $C$ and so on.
- The text _should_ use the letters $i$, $j$, $k$ for indexing dimensions 1 to 3.
- The text _must_ use capitals for hyper-parameters and constants that don't change across runs of the same family of algorithms, like $N$, $X$ or $Q$.
<!-- vale write-good.Passive = NO -->
<!-- vale write-good.E-Prime = NO -->
- The text _must_ pose the problems in terms that do not hint at how it can be accelerated in hardware.
<!-- vale write-good.E-Prime = YES -->
<!-- vale write-good.Passive = YES -->
- The text _should_ state numerical tolerances for the results, if applicable.
- The text _should_ state 
