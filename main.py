import numpy as np
import random
from Kalman import KalmanFilter
from World import WorldSimulation
import matplotlib.pyplot as plt

def main():

    # UNCOMMENT THESE LINES TO RUN CODE
    # ----------

    # one_point_three()
    # two_point_two()
    two_point_three()
    # three_point_zero()
    # extra_credit()


def one_point_three():
    # DEFINE THE INITIAL STATE OF THE WORLD
    # ----------

    # define the state vector (p_0 mean=0, v_0 mean=0)
    mean = np.matrix([[0], [0]])

    # define the covariance (initial covariance=0)
    covariance_matrix =  np.matrix([[0, 0], [0, 0]])

    # define the matrices A_t, B_t, and G (which are used in the state prediction step)
    A_t = np.matrix([[1, 1], [0, 1]])
    B_t = np.matrix([[1, 1], [0, 1]])# np.matrix([[0.5, 0], [0, 0]]) # TODO: Fill this in
    G = np.matrix([[0.5],[1]])

    # define matrices C_t and Q_t (which are used in measurement update step)
    C_t = np.matrix([[1, 0], [0, 1]])
    Q_t = np.matrix([[8, 0], [0, 8]])

    # define the control u_t as a matrix (initially, we have no control)
    u_t = np.matrix([[0], [0]])

    # define the measurement (initially, there is none)
    z_t = None


    # create a Kalman Filter for the drone (pass in the state vector, matrices A and B)
    drone = KalmanFilter(A_t, B_t, G, C_t, Q_t, covariance_matrix, mean)
    # create a world 
    world = WorldSimulation(A_t, mean)
    wind_variance = 1

    for t in range(1, 6):
        print("TIME STEP " + str(t))
        # state prediction step
        drone.state_prediction(u_t, wind_variance)
        drone.print_distribution()

def two_point_two():
    # DEFINE THE INITIAL STATE OF THE WORLD
    # ----------

    # define the state vector (p_0 mean=0, v_0 mean=0)
    mean = np.matrix([[0], [0]])

    # define the covariance (initial covariance=0)
    covariance_matrix =  np.matrix([[0, 0], [0, 0]])

    # define the matrices A_t, B_t, and G (which are used in the state prediction step)
    A_t = np.matrix([[1, 1], [0, 1]])
    B_t = np.matrix([[1, 1], [0, 1]])# np.matrix([[0.5, 0], [0, 0]]) # TODO: Fill this in
    G = np.matrix([[0.5],[1]])

    # define matrices C_t and Q_t (which are used in measurement update step)
    C_t = np.matrix([[1, 0], [0, 1]])
    Q_t = np.matrix([[8, 0], [0, 8]])

    # define the control u_t as a matrix (initially, we have no control)
    u_t = np.matrix([[0], [0]])


    # KALMAN FILTER
    # ----------
    # create a Kalman Filter for the drone (pass in the state vector, matrices A and B)
    drone = KalmanFilter(A_t, B_t, G, C_t, Q_t, covariance_matrix, mean)

    # create a world 
    world = WorldSimulation(A_t, mean)

    # implement the Kalman Filter for t = 1, 2, ..., 5
    for t in range(1, 6):
        print("\nTIME STEP " + str(t) + ":")

        wind_variance = 1
        z_t = None
        # PERFORM PREDICTION STEP
        # ----------

        # implement the state prediction step
        drone.state_prediction(u_t, wind_variance)


        # PERFORM MEASUREMENT UPDATE
        # ----------
        if t == 5:
            # z_t = np.matrix([[world.sample_position(8)], [0]])#10
            z_t = np.matrix([[10], [0]])#10
            print("\nMEASUREMENT UPDATE\nBefore Measurement")
            drone.print_distribution()
            print("\nAfter Measurement")

        drone.measurement_update(z_t)

        # print the result of the state prediction step
        drone.print_distribution()

def two_point_three():
    # DEFINE THE INITIAL STATE OF THE WORLD
    # ----------

    # define the state vector (p_0 mean=0, v_0 mean=0)
    mean = np.matrix([[0], [0]])

    # define the covariance (initial covariance=0)
    covariance_matrix =  np.matrix([[0, 0], [0, 0]])

    # define the matrices A_t, B_t, and G (which are used in the state prediction step)
    A_t = np.matrix([[1, 1], [0, 1]])
    B_t = np.matrix([[1, 1], [0, 1]])# np.matrix([[0.5, 0], [0, 0]]) # TODO: Fill this in
    G = np.matrix([[0.5],[1]])

    # define matrices C_t and Q_t (which are used in measurement update step)
    C_t = np.matrix([[1, 0], [0, 1]])
    Q_t = np.matrix([[8, 0], [0, 8]])

    # define the control u_t as a matrix (initially, we have no control)
    u_t = np.matrix([[0], [0]])

    # set N
    N = 500

    avg_error = []
    fig, ax = plt.subplots()
    probs = ['0.1', '0.5', '0.9']
    
    ax.set_title('Average error in position, given probability of failure')
    ax.set_ylabel('Average error (distance)')
    ax.set_xlabel('Probability of failure')

    # run for each probability
    for probability in [0.1, 0.5, 0.9]:

        # store the error between the true and estimated positions
        errors = []
        
        # repeat n times
        for time in range(0, N):
            # create a Kalman Filter for the drone (pass in the state vector, matrices A and B)
            drone = KalmanFilter(A_t, B_t, G, C_t, Q_t, covariance_matrix, mean)

            # create a world 
            world = WorldSimulation(A_t, mean)

            # go through each time step 
            for t in range (1, 21):
                variance = 1

                # perform state prediction for the given time step
                drone.state_prediction(u_t, variance) 
                world.update_states()

                # run measurement update step IF we have a measurement
                chance = random.random()
                # if the sensor works
                if not chance <= probability:
                    # perform a measurement update given the true position of the drone
                    drone.measurement_update(world.get_ground_truth().item(0))
            
            # at time step 20, get the ground truth position and expected position
            difference = abs(world.get_ground_truth().item(0) - drone.get_mean().item(0))
            print(drone.get_mean().item(0))
            errors.append(difference)

        avg_error.append(np.mean(errors))
    ax.bar(probs, avg_error, label=probs)        
    plt.show()

def three_point_zero():
    # DEFINE THE INITIAL STATE OF THE WORLD
    # ----------

    # define the state vector (p_0 mean=0, v_0 mean=0)
    mean = np.matrix([[0], [0]])

    # define the covariance (initial covariance=0)
    covariance_matrix =  np.matrix([[0, 0], [0, 0]])

    # define the matrices A_t, B_t, and G (which are used in the state prediction step)
    A_t = np.matrix([[1, 1], [0, 1]])
    B_t = np.matrix([[1, 1], [0, 1]])# np.matrix([[0.5, 0], [0, 0]]) # TODO: Fill this in
    G = np.matrix([[0.5],[1]])

    # define matrices C_t and Q_t (which are used in measurement update step)
    C_t = np.matrix([[1, 0], [0, 1]])
    Q_t = np.matrix([[8, 0], [0, 8]])

    # define the control u_t as a matrix (initially, we have no control)
    u_t = np.matrix([[0], [0]])

    # define the initial position and velocity to be 5.0 and 1.0
    mean = np.matrix([[5], [1]])
    # define the control 
    u_t = np.matrix([[0], [1]])

    # create a Kalman Filter for the drone (pass in the state vector, matrices A and B)
    drone = KalmanFilter(A_t, B_t, G, C_t, Q_t, covariance_matrix, mean)
    variation = 1

    # compute the mean estimate for the state at time t 
    drone.state_prediction(u_t, variation) # implement the state prediction step
    print(drone.get_mean())

def extra_credit():

    # define the mean (initially 0)
    mean = np.matrix([[0], [0], [0], [0]])

    # define the covariance (initial covariance=0)
    covariance_matrix =  np.matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    # define the matrices A_t, B_t, and G (which are used in the state prediction step)
    A_t = np.matrix([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
    B_t = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    G = np.matrix([[0.5],[0.5], [1], [1]])

    # define matrices C_t and Q_t (which are used in measurement update step)
    C_t = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    Q_t = np.matrix([[8, 0, 0, 0], [0, 8, 0, 0], [0, 0, 8, 0], [0, 0, 0, 8]])

    # define the control u_t as a matrix (initially, we have no control)
    u_t = np.matrix([[0], [0], [0], [0]])



    # create a Kalman Filter for the drone (pass in the state vector, matrices A and B)
    drone = KalmanFilter(A_t, B_t, G, C_t, Q_t, covariance_matrix, mean)

    # create a world 
    world = WorldSimulation(A_t, mean)

    actual_x_positions = []
    actual_y_positions = []
    predicted_x_positions = []
    predicted_y_positions = []
    timestamp = []

    # go through each time step 
    for t in range (1, 31):
        timestamp.append(t)
        variance = 1

        # perform state prediction for the given time step
        drone.state_prediction(u_t, variance) 
        world.update_states()

        # run measurement update step IF we have a measurement
        chance = random.random()
        # if the sensor works
        if not chance <= 0: # EDIT HERE TO CHANGE PROBABILITY OF SENSOR MALFUNCTION
            drone.measurement_update(np.matrix([[world.get_ground_truth().item(0)],[world.get_ground_truth().item(1)], [0], [0]]))

        # record the actual and predicted positions at each time step
        actual_x_positions.append(world.get_ground_truth().item(0))
        actual_y_positions.append(world.get_ground_truth().item(1))
        predicted_x_positions.append(drone.get_mean().item(0))
        predicted_y_positions.append(drone.get_mean().item(1))

    # Plot the results
    ax = plt.axes(projection="3d")
    ax.plot(actual_x_positions, actual_y_positions, timestamp, label="True Position", c="blue")
    ax.plot(predicted_x_positions, predicted_y_positions, timestamp, label="Predicted Position", c="red")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Time")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
