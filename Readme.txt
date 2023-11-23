The code is related to 'Related-Tweakey Boomerang and Rectangle Attacks on Reduced-Round Joltik-BC'.

./encrypt : includes the code for the encryption algorithm of Joltik-BC

./Sbox_modeling :  includes the code for describing the differential propagation property of the S-box with a small number of inequalities

./differential : includes the code for searching for the optimal differential characteristics with high probability

./boomerang_initial : includes the code for searching for boomerang distinguishers without considering the propagation of truncated differentials

./boomerang_final : includes the latest code for searching for boomerang distinguishers considering the propagation of truncated differentials

diff_instantion.py : instantiate bitwise differential characteristics based on the solution of model 

middle_probability.py : calculate the probability of the middle part

success_pro.py : Calculate the probability that recover key successfully