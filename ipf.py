def ipf(a, b, tolerance=1e-4, target=[0.7, 0.3]):
        '''
        a, b, c, d - total scores of the four factors
        tolerance - the error threshold for convergence
        target - desired target proportions for the contributions of the factors
        '''
        weights = target.copy()  # Start with current weights
        while True:
            c_i = [a * weights[0], b * weights[1]]
            c_total = sum(c_i)
            p_i = [c_i[i] / c_total for i in range(len(c_i))]

            # Update weights
            weights = [weights[i] * target[i] / p_i[i] for i in range(len(weights))]

            # Normalize the new weights
            denom = sum(weights)
            weights = [w / denom for w in weights]

            # Check convergence (compare p_i to target)
            diff = sum(abs(p_i[i] - target[i]) for i in range(len(target)))
            if diff < tolerance:
                break

        return weights
 
print(ipf(2326.225052861417, 991.8335624858058))