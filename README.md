<!-- vale write-good.E-Prime = YES -->
# Roofline Challenges

A collection of challenge for [roofline.dev](https://roofline.dev).

## Normative Keywords

- **MUST / MUST NOT**. Mandatory, no exceptions under any circumstanced.
- **SHOULD / SHOULD NOT**. Exceptions allowed, but discouraged.
- **MAY / MAY NOT**. Soft preference, needed for style and consistency.

## Rules

- You must not override the input if it is provided as `const`.
- The text _must not_ use libraries like cuBLAS, cuDNN and similar unless explicitly stated.

## Style

The list below describes the stylistic criteria to keep in mind when designing problems for **Roofline**.

### Design

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
- The problem _must_ expect the datatype with the same precision for input as for output and vice versa.  
- The problem _must_ come with a reference implementation used for correctness checking.
- The problem _must not_ use `long double`.

### Text

- The text _must_ $\LaTeX$ for mathematical formulae. Learn to use it here: [Learn LaTeX](https://www.overleaf.com/learn).

- The text _should_ use underlines to denote vectors, like $\underline{v}$, $\underline{u}$ and $\underline{w}$.
- The text _should_ use letters like $\underline{v}$, $\underline{u}$, $\underline{w}$ for individual vectors.
- The text _should_ use letters from the beginning of the alphabet for scalar inputs, so $a$, $b$ and $c$.
- The text _should_ use capitals to denote matrices, like $A$, $B$ and $C$.
- The text _should_ use letters from the beginning of the alphabet for matrices, so $A$, $B$, $C$ and so on.
- The text _should_ use the letters $i$, $j$, $k$ for indexing dimensions 1 to 3.
- The text _should_ use $\Sigma$- and $\Pi$-notation without specifying a starting iteration number when summing over a vector, so $\Sigma^N_i$ is the same as $\Sigma^{N - 1}_{i=0}$, same as $\Sigma^N_{i=1}$. 

- The text _must not_ use latex for showing indexing, don't use "$\text{for } i = 0, 1, \dots, N - 1$."
- The text _should avoid_ set membership for indices, like $i \in [0; N)$, unless the problem statement is more clearly stated mathematically.
- The text _should_ use brackets $[a; b]$ for inclusive bounds and parentheses $(a; b)$ for exclusive bounds.
- The text _should_ use implicit multiplication $ab$ over "$a \cdot b$" or "$a \times b$."
- The text _must_ use $4 \text{ mod } 3$ instead of `4 % 3` to talk about modular arithmetic.

- The text _must_ use a different family of letters for constants than it does for inputs. If the inputs are $\underline{a}$ and $\underline{b}$, the constant must not be $c$, but can be $n$.
<!-- vale write-good.E-Prime = NO -->
<!-- vale write-good.Passive = NO -->
- The text _should_ pose the problems in terms that do not hint at how it can be accelerated in hardware.
<!-- vale write-good.Passive = YES -->
- The text _must_ state whether the layout is row-major or column-major, if applicable. 
<!-- vale write-good.E-Prime = YES -->
- The text _should_ state numerical tolerances for the results, if applicable.
- The text _must_ explicitly state the method for computing tolerances: absolute, relative, element-wise max and so on.
- The text _should_ stay the distribution if the inputs.
- The text _should_ state whether the harness uses adversarial inputs.
- The text _may_ include an example of indexing with the appropriate strides.
- The text _must not_ put any delimiters between the subscript indices, instead of $A_{i,j}$ (`A_{i,j}`), use $A_{ij}$ (`A_{i,j}`). 
- The text _must_ put a thin space between numerical indices, instead of $A_{11}$ (`A_{11}`), use $A_{1\,1}$ (`A_{1\,1}`).
