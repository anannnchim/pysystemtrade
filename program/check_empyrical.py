if __name__ == '__main__':
    import numpy as np
    from empyrical import max_drawdown, alpha_beta

    returns = np.array([.01, .02, .03, -.4, -.06, -.02])
    benchmark_returns = np.array([.02, .02, .03, -.35, -.05, -.01])

    # calculate the max drawdown
    max_drawdown(returns)

    # calculate alpha and beta
    alpha, beta = alpha_beta(returns, benchmark_returns)
    print(alpha)
