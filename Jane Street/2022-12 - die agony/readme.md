# [Die Agony](https://www.janestreet.com/puzzles/die-agony-index/)
The most agonizing part was trying to debug accidentally typing "186" on the grid as "168"

Things that I used:
* Linear Algebra (not needed, but fun)
* DFS (very useful but not necessary)

---

To start, I first needed some way to track the orientation of the die.  

I set the origin to $x = y = z = 0$, and all the faces are 1 away. 

Although this would still work like this, actually each face just needs to be represented by one point, so I ended up with 3 orthonormal points and their negatives  

For the sake of visualization, take a standard die and place it such that one is pointing right, the center of that face will be at $(1,0,0)$. Put 2 pointing away from you. Its position will be $(0,1,0)$. 3 should be facing up at the $(0,0,1)$ position. If it is 4, you have a left-handed die and need to swap the middle two columns of the following matrix:
```math
$D = \begin{bmatrix}
1 & 0 & 0 & 0 & 0 & -1 \\
0 & 1 & 0 & 0 & -1 & 0 \\
0 & 0 & 1 & -1 & 0 & 0
\end{bmatrix}$
```
where the face with a 1 represents the first column, 2 is the second up to the last column being the position of the face with a 6.

Now we can use the columns of the matrix to determine which of the faces is down. In the starting position, that would be 4th column.

In terms of the puzzle, we don't actually know what number each of the faces represents, so I gave each face a starting value of null.

now for tipping the die orthogonally:  
We have a rotation matrix $A$, such that  
```math
A \begin{bmatrix}a_1 & a_2 & a_3\end{bmatrix}=\begin{bmatrix}b_1 & b_2 & b_3\end{bmatrix}
```
where $a$ represents initial positions of faces and $b$ represents where they end up.

Now, if we choose $a = I_3$ (In linear algebra, multiplying by $I$ is the equivalent of multiplying a scalar by 1.) The interesting thing is that $I_3$ is the first 3 columns of $D$, so if you track where the 1, 2 and 3 faces go, you can generate the rotation matricies.

For example, tipping a die to the right changes these 3 faces reuluts in the following rotaional matrix:  
```math
R_r = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ -1 & 0 & 0 \end{bmatrix}
```

Now that we have this matrix, if you multiply your die matrix by this rotation matrix on the left, the output is the position of all the new faces.

Here are a few observations which are obvious geometrically:  
$R_r^4 = R_l^4 = R_u^4 = R_d^4 = I$  
$R_r^3 =R_l$  
$R_r^n * R_l^n = I $  
$(R_r * R_u)^3 = I $  
$|R_r|=|R_l|=...=1$ 

The rest is mostly computer science stuff. I used a DFS and performed a search where I assigned the faces of the die as needed (so that they would make the path valid). Each path went until it made a move that would either contradict an existing face, go off the grid, or until it reached the end.

From the correct path, I used the visited squares to figure out which ones had not been visited, and summed those squares up.
