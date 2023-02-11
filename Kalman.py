import numpy as np


# Kalman Filter
class KalmanFilter:

    def __init__(self, A_t, B_t, G, C_t, Q_t, covariance_matrix, mean):
        self.A_t = A_t
        self.B_t = B_t
        self.G = G
        self.C_t = C_t
        self.Q_t = Q_t

        self.covariance_matrix = covariance_matrix
        self.mean = mean


    # perform state prediction step of Kalman Filter
    def state_prediction(self, u_t, variance):
        # calculate the mean
        self.mean = np.matmul(self.A_t, self.mean) + np.matmul(self.B_t, u_t)

        # calculate the covariance
        A_squared = np.matmul(np.dot(self.A_t, self.covariance_matrix), np.transpose(self.A_t))
        R_t = np.dot(variance, np.matmul(self.G, np.transpose(self.G))) 

        self.covariance_matrix = A_squared + R_t

    
    # perform measurement update step of Kalman Filter
    def measurement_update(self, measurement):

        # we can only perform the update if we have a measurement
        if measurement is not None:
            # determine K
            K = np.dot(self.covariance_matrix, np.transpose(self.C_t))
            C_squared = np.linalg.inv(np.dot(np.dot(self.C_t, self.covariance_matrix), np.transpose(self.C_t)) + self.Q_t)
            K = np.dot(K, C_squared)

            # update mean
            self.mean = self.mean + np.dot(K, (measurement - np.dot(self.C_t, self.mean)))
            # update covariance    
            self.covariance_matrix = np.dot(np.identity(len(self.C_t)) - np.dot(K, self.C_t), self.covariance_matrix)


    def print_distribution(self):
        print("Mean: " + str(self.mean))
        print("Covariance: " + str(self.covariance_matrix))

    def get_mean(self):
        return self.mean
    
    def get_covariance(self):
        return self.covariance_matrix



  
 

