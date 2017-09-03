Given the binary chromosome with length 4, calculate the probability that no bits,
one bit and more than one bit will be flipped in a bit-flip mutation with \(p_m = \frac{1}{4}\).

No bits: (3 / 4)^4 = ~32%
One bit:

n! / k!(n -k)! * p^k * (1 - p)^(n-k)
(4 * 3 * 2) / (3 * 2) * 0.25 * (0.75)^(3)

0,421875

Alt:

(0.25 * 0.75 * 0.75 * 0.75) * 4 = 0,421875