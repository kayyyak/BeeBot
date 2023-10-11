f np.equal(conv_to_a[0], W[0][j]) and np.equal(conv_to_a[1], W[1][j]):
                conv_to_p[0] = np.sum(save[0][2])
                conv_to_p[1] = np.sum(save[1][2])
                conv_to_a = np.matmul(variable_a, conv_to_p)
                conv_to_a[0] = np.round(conv_to_a[0])
                conv_to_a[1] = np.round(conv_to_a[1])
                update = save
            else:
                matrix_p = np.append(matrix_p, conv_to_p, axis = 1)
                matrix_a = np.append(matrix_a, conv_to_a, axis = 1)
                update = upd