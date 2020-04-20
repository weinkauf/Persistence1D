from qpsolvers import solve_qp
import numpy as np

def  _BuildEqualityConstraints(InputData, AllExtremaIndices):
    """
    We constrain all (unfiltered) extrema to their original data values.
    """
    
    #~ We build a sparse matrix for the equalities with these number of rows and colums.
    NumRows = len(AllExtremaIndices)
    NumCols = InputData.size

    #~ We need to add a row if the leftmost or rightmost part of the data vector is NOT constrained
    #~ That means, we do not have an extremum (minimum only possible) there
    AddLeftEdge = 0
    if (AllExtremaIndices[0] != 0):
        AddLeftEdge = 1
        AllExtremaIndices = [0] + AllExtremaIndices
    AddRightEdge = 0
    if (AllExtremaIndices[-1] != InputData.size - 1):
        AddRightEdge = 1
        AllExtremaIndices = AllExtremaIndices + [InputData.size - 1]

    A = np.zeros((NumRows + AddRightEdge + AddLeftEdge, NumCols))
    for i in range(0, len(AllExtremaIndices)):
        A[i, AllExtremaIndices[i]] = 1

    b = InputData[AllExtremaIndices]

    return (A, b)


def  _BuildInequalityConstraints(AllExtremaIndices, DataLength):
    """
    To make sure we do not get other extrema than the ones provided by the user,
    we use inequality constrains: Consider a point x_i in the data vector with its two neighbors x_{i-1} and x_{i+1}.
    If x_i is a regular point, i.e., not an extremum, then we constrain it to be smaller
    than one of its neighbors and larger than the other neighbor. For example:
    x_{i-1} <= x_i <= x_{i+1}
    Hence, we have a monotonically increasing function here and x_i cannot be an extremum.
    
    Let us sketch a function:
    
    \
     \    /\  /
      \  /  \/
       \/
    nnnnpppnnpp
    
    Notice how the gradient between the samples is either negative (n) or positive (p),
    depending on whether we are in a section from a minimum to a maximum, or from a maximum to a minimum.
    We use this to gather all inequality constraints.
    We have one less inequality constraint than we have samples.
    
    For a positive gradient, i.e., the function values rise from left to right, we have this inequality:
    x_i - x_{i+1} <= 0
    For a negative gradient, i.e., the function values decrease from left to right, we have this inequality:
    -x_i + x_{i+1} <= 0
    The left part of these inequalities is implemented in the matrix G.
    The right part of these inequalities is implemented in the vector h.
    
    From a topological point of view, I do not like the equality part of the inequalities,
    but a quadratic program is typically run with <= instead of strict inequality.
    """

    #~ The matrix with the inequalities
    G = np.zeros([DataLength - 1, DataLength])

    #~ Note: The leftmost and rightmost extremum is always a minimum
    #~ We start at the left-most index by going down to the first minimum,
    #~ which we may encounter right there at the left-most index or some steps later
    PosGradientModifier = np.int_(-1)
    for i in range(0, DataLength - 1):
        if (i in AllExtremaIndices):
            PosGradientModifier *= np.int_(-1)
        G[i, i] = PosGradientModifier
        G[i, i+1] = np.int_(-1) * PosGradientModifier

    #~ The right side of the inequalities is simply a zero vector.
    h = np.zeros([DataLength - 1])

    return (G, h)


def _BuildEnergy(InputData, strSmoothness, DataWeight):
    """
    We use a biharmonic or triharmonic smoothness operator based on the Laplacian.
    The discrete Laplacian operator matrix is created with the assumption of uniformly spaced 1D data.
    The original data can be taken into account using the DataWeight factor between 0 and 1.
    """
    
    #~ How many items do we have?
    NumElements = len(InputData)

    #~ We start with the Laplacian.
    #~ We assume the original data is uniformly spaced.
    #~ If that is not the case, you need to get the geometry of the domain in here.
    LDiag = np.full(NumElements, 2)
    LDiag[0] = LDiag[-1] = 1
    LOff = -np.ones(NumElements-1)
    Laplacian = np.diag(LDiag, 0) + np.diag(LOff, -1) + np.diag(LOff, 1)

    if (strSmoothness == 'biharmonic'):
        P = np.dot(Laplacian, Laplacian)
    elif (strSmoothness == 'triharmonic'):
        P = np.dot(np.dot(Laplacian, Laplacian), Laplacian)
        P = (P + P.T) * 0.5
    else:
        raise ValueError("strSmoothness needs to be either 'biharmonic' or 'triharmonic'")
    
    #~ Right hand side if we do not have a data term
    q = np.zeros(NumElements)
    
    #~ Add data term weight to diagonal
    if (DataWeight != 0):
        DataDiag = np.full(NumElements, DataWeight)
        P = P + 2 * np.diag(DataDiag, 0)
        q = -2 * DataWeight * InputData

    return (P, q)


def _cmp(a, b):
    return -1 if (a < b) else 0 if (a == b) else 1

def _TestAlternating(L):
    return all(_cmp(a, b)*_cmp(b, c) == -1 for a, b, c in zip(L, L[1:], L[2:]))


def RunReconstruction(InputData, AllExtremaIndices, strSmoothness, DataWeight, Solver = 'quadprog'):
    """
    This function reconstructs a smooth function approximating the input data,
    but only containing the given minima/maxima.
    Adherence to the original data is controlled using the DataWeight term. 

    The reconstructed function can be C1 or C2 smooth.
    This is controlled by the smoothness parameter,
    which can be set to 'biharmonic' or 'triharmonic' accordingly.

    All extrema given to the function are used for reconstruction.
    Undesired extrema need to be filtered before using this function.
    This can be done using Persistence1D.

    This code just gets a list of indices representing the locations of extrema in the data.
    One may ask whether this is enough to determine their type and so on,
    since the type of the extrema is important for building the inequality constraints
    (which values should be larger than others etc.).
    The type of an extremum is inferable from a correct list of extrema:
    (1) The leftmost and rightmost extrema are always minima.
    (2) Minima and maxima alternate in the sequence (ordered from lowest to highest index).
    (3) Hence, we have an odd number of extrema.
    These statements are true for all 1D functions.
    We test for this here, to make sure the right input comes in.
    However, make sure you get your extrema indices from Persistence1D and you handle them correctly.

    @param[in] InputData
        Original data vector.
    @param[in] AllExtremaIndices
        Indices of (filtered) minima/maxima selected for reconstruction. 
    @param[in] strSmoothness
        Determines smoothness of result. Valid values are 'biharmonic' or 'triharmonic'
    @param[in] DataWeight
        Weight for data term. Affects how closely the reconstructed results adhere to the data. Valid range: 0.0-1.0
    @param[in] Solver
        Software for solving the Quadratic Programming problem. Possible values are 'cvxpy', 'ecos', 'quadprog', and others supported by the qpsolvers project: https://github.com/stephane-caron/qpsolvers

    @param[out] Solution
        Reconstructed data.
    
    The Matlab version of this code uses a different notation. Since it came first,
    we provide a translation here (Python code notation on the left side, Matlab on the right):
    Energy:
    P == operator
    q == f
    Inequalities:
    G == A
    h == b
    Equalities:
    A == Aeq
    b == beq    
    
    Author: Tino Weinkauf, based on code from Yeara Kozlov and Alec Jacobson
    """
 
    #~ Verify smoothness type is valid
    if (strSmoothness != 'biharmonic' and strSmoothness != 'triharmonic'):
        raise ValueError("unrecognized interpolation type: choose 'biharmonic' or 'triharmonic'")

    #~ Verify data weight is valid
    if (DataWeight < 0.0 or DataWeight > 1.0):
        raise ValueError('data term weight must be <= 1.0 and >= 0.0')

    #~ How many items do we have?
    NumElements = len(InputData)
    if (NumElements == 1):
        return InputData

    #~ Make sure to have an odd number of extrema
    if (len(AllExtremaIndices) % 2 != 1):
        raise ValueError("AllExtremaIndices needs to have an odd number of items.")

    #~ Sort the extrema indices from left to right.
    AllExtremaIndices.sort()

    #~ Make sure to have an alternating sequence of minima/maxima
    if not _TestAlternating(InputData[AllExtremaIndices]):
        raise ValueError("InputData and AllExtremaIndices need to define an alternating sequence of minima and maxima")

    #~ Do we start and end with a minimum?
    if (len(AllExtremaIndices) > 1):
        if (InputData[AllExtremaIndices[0]] > InputData[AllExtremaIndices[1]]):
            raise ValueError("InputData and AllExtremaIndices need to define a sequence of extrema starting with a minimum.")
        if (InputData[AllExtremaIndices[-1]] > InputData[AllExtremaIndices[-2]]):
            raise ValueError("InputData and AllExtremaIndices need to define a sequence of extrema ending with a minimum.")

    #~ Build equality constraints
    (A, b) = _BuildEqualityConstraints(InputData, AllExtremaIndices)
    #~ print("\nEquality:\n-------------------")
    #~ print("\nMatrix A:\nShape: %s\n%s" % (A.shape, A))
    #~ print("\nVector b:\nShape: %s\n%s" %(b.shape, b))

    #~ Build inequality constraints
    (G, h) = _BuildInequalityConstraints(AllExtremaIndices, NumElements)
    #~ print("\n\nInequality:\n-------------------")
    #~ print("\nMatrix G:\nShape: %s\n%s" % (G.shape, G))
    #~ print("\nVector h:\nShape: %s\n%s" %(h.shape, h))

    #~ Build energy to be minimized
    (P, q) = _BuildEnergy(InputData, strSmoothness, DataWeight)
    #~ print("\n\nEnergy:\n-------------------")
    #~ print("\nMatrix P:\nShape: %s\n%s" % (P.shape, P))
    #~ print("\nVector q:\nShape: %s\n%s" %(q.shape, q))

    #~ Solve the QP problem
    Solution = solve_qp(P, q, G, h, A, b, solver=Solver)
    #~ print("Solution", Solution)

    return Solution

