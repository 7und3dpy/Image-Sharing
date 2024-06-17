# ECDSA (Elliptic Curve Digital Signature Algorithm)

Signature algorithm is used for authenticating a device or a message sent by the device. For example consider two devices A and B. To authenticate a message sent by A, the device A **signs the message using its private key**. The device A sends the message and the signature to the device B. This signature can be **verified only by using the public key** of device A. Since the device B knows A’s public key, it can verify whether the message is indeed send by A or not.

ECDSA is a variant of the **Digital Signature Algorithm (DSA)** that operates on elliptic curve groups. For sending a signed message from A to B, both have to agree up on **Elliptic Curve domain parameters**. Sender ‘A’ have a key pair consisting of a private key $d_A$ (a randomly selected integer less than $n$, where $n$ is the order of the curve, an elliptic curve domain parameter) and a public key $Q_A = d_A * G$ ($G$ is the generator point, an elliptic curve domain parameter). An overview of ECDSA process is defined below.

ECDSA has three phases 

- **key generation**
- **signature generation**
- **signature verification**

# ECDSA Key Generation

An entity A's key pair is associated with a particular set of EC domain parameters $D = (CURVE, G, n, d_A, Q_A, m)$. 


- $CURVE$ is the elliptic curve field and equation used

- $G$ is elliptic curve base point, a point on the curve that generate a subgroup of large prime order n

- $n$ is the integer order of $G$, means that $n \times G = O$, where $O$ is the identity element. 

- $d_A$ is the private key (randomly selected)

- $Q_A$ is the public key $d_A \times G$ (calculated by elliptic curve)

- $m$ is the message to send. 

The order n of the base point G **must be prime**


1. Select the random integer $d$ in the interval $[1, n - 1]$

2. Compute $Q = d_A \times G$. We use $\times$ to denote elliptic curve point multiplication by a scalar. 

3. A's public key is Q, A's private key is $d$

# ECDSA Signature Generation



To sign a message $m$, an entity $A$ with domain parameters $D = (q, F_R, a, b, G, n, h)$ does the following

For Alice to sign a message $m$, she follows these steps: 

1. Calculate $e = $HASH(m). (Here HASH is a cryptographic hash function, such as SHA-2, with the output converted to integer)

2. Let $z$ be the $L_n$ leftmost bits of $e$, where $L_n$ is the bit length of the group order of $n$. (Note that $z$ can be *greater* than $n$ but not longer.)


3. Select a random or pseudorandom integer $k$ in the interval $[1, n-1]$

4. Calculate the curve point $(x_1, y_1) = k \times G$

5. Calculate $r = x_1 \mod n$. If $r = 0$, go back to step 3

6. Compute $s = k^{-1} (z + rd_A) \mod (n)$. If $s = 0$, go back to step 3. 

7. The signature is the pair $(r, s)$. (And ($r, -s \mod n$) is also a valid signature)

**Notes**: 

It is not only required for $k$ to be secret, but it is also crucial to select different $k$ for different signatures. Otherwise, the equation in step 6 can be solved for $d_A$, the private key: the given two signatures $(r, s)$ and $(r, s^\prime)$. If not, the equation is step 6 can be solved for $d_A$, the private key: given two signatures $(r, s)$ and $(r, s^\prime)$, employing the same unknown $k$ for different known message $m$ and $n^\prime$, an attacker can calculate $z$ and $z^\prime$, and since $s - s^\prime = k^{-1} (z - z^\prime)$ (all operations in this paragraph are done modulo $n$) the attacker can find $k = \frac{z - z^\prime}{s - s^\prime}$. Since $s = k^{-1}(z + rd_A)$, the attacker can now calculate the private key $d_A = \frac{sk - z}{r}$

![alt text](siggen.jpg)


# ECDSA Signature Verification


For Bob to authenticate Alice's signature, he must have a copy of her public-key curve point $Q_A$. Bob can verify $Q_A$ is a valid curve point as follows: 

1. Check that $Q_A$ is not equal to the identity element $O$, and its coordinates are otherwise valid. 

2. Check that $Q_A$ lies on the curve.

3. Check that $n \times Q_A = O$

After that, Bob follows these steps: 

1. Verify that $r$ and $s$ are integers in $[1, n - 1]$. If not, the signature is invalid

2. Calculate $e = HASH(m)$, where HASH is the same function used in the signature generation

3. Let $z$ be the $L_n$ leftmost bits of $e$. 

4. Calculate $u_1 = zs^{-1} \mod n$ and $u_2 = rs^{-1} \mod n$

5. Calculate the curve point $(x_1, y_1) = u_1 \times G + u_2 \times Q_A$. If $(x_1, y_1) = O$ then the signature is invalid

6. The signature is valid if $r \equiv x_1 (\mod n)$, invalid otherwise. 

Note that an efficient implementation would compute inverse $s^-1 \mod n$ only once. Also, using Shamir's trick, a sum of two scalar multiplications $u_1 \times G + u_2 \times Q_A$ can be calculated faster than two scalar multiplications done independently. 



![alt text](sigver.png)

### Correctness of the algorithm

It is not immediately obvious why verification even functions correctly. To see why, denote as $C$ the curve point computed in step 5 of verification, 

$$C = u_1 \times G + u_2 \times Q_A$$

From the definition of the public key as $Q_A = d_A \times G$, 

$$C = u_1 \times G + u_2d_A \times G$$

Because elliptic curve scalar multiplication distributes over addition, 


$$C = (u_1 + u_2d_A) \times G$$

Expanding the definition of $u_1$ and $u_2$ from verification step 4, 

$$C = (zs^{-1} + rd_As^{-1}) \times G$$

Collecting the common term $s^{-1}$, 

$$C = (z + rd_A)s^{-1} \times G$$

Since the inverse of an inverse is the original element, and the product of an element's inverse and the element is the identity, we are left with 

$$C = k \times G$$

(Q.E.D)

**Notes**: In public key cryptography each user or the device taking part in the communication generally have a pair of keys, a public key and a private key, and a set of operations associated with the keys to do the cryptographic operations. Only the particular user knows the private key whereas the public key is distributed to all users taking part in the communication.

The public key is a point on the curve and the private key is a random number. The public key is obtained by multiplying the private key with a generator point G in the curve.

The mathematical operations of ECC is defined over the elliptic curve y^2 = x^3 + ax + b, where 4a^3 + 27b^2 ≠ 0. Each value of the ‘a’ and ‘b’ gives a different elliptic curve.

One main advantage of ECC is its small key size. A 160-bit key in ECC is considered to be as secured as 1024-bit key in RSA.