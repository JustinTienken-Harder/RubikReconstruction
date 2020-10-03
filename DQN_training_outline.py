"""
Deep Q-function Network a sketch for how training a reinforcement function to approximate the Q-function in a reinforcement problem.

Code will not run as is, but provides an outline for training, inspired by the deepmind's Atari paper.



Need to do:
    - Figure out what they mean by error clipping.
    -
"""
from collections import deque #list like container with faster appends and pops. Can set a fixed length so new appends drop first elements.
import time
import os
if not os.path.isdir("../models/"):
    os.makedirs("models")

MODEL_NAME = "deep_qube" #Name of the network
MIN_REWARD_TO_SAVE = 0           #Minimum amount of reward before you save a model
AGGREGATE_STATS_EVERY =  20 #How many cubes to solve before getting some aggregate stats/potentially saving a model


REPLAY_MEMORY_SIZE = 10_000 #Total amount of experiences to hold onto (I felt that)
MIN_EXPERIENCE_SIZE = 500 #Minimum number of experiences before you start training
MINIBATCH_SIZE = 64 #WHAT TO DO BRO

UPDATE_TARGET_MODEL_EVERY = 10 #Update the target model every 10 cubes?

epsilon = 1 #This is the exploration factor. Not necessarily constant, could be decayed. Essentially the probability of doing a random action.
MIN_EPSILON = 0.05 #the minimum amount of exploration you will allow
EPSILON_DECAY = 0.9 #Multiply your epsilon by this every episode or (variable) times: Deepmind actually uses linear decay.
DISCOUNT_FACTOR = 0.99 #Used throughout.

class DQNAgent:
    def __init__(self):
        #Main model_defined here. TODO: define create_model function
        self.model = self.create_model()

        #Target model. Generally a previous version of previously defined model.
        #We compare against it so that we can 1. reduce variance (?) of our estimation of the bellman equation (see paper)
        #                                     2. update weights without a recurrence relation.
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        #Define the size of our memory of "experiences"
        #An experience is a 4-tuple of (s,a,r,s'). We'll randomly sample from experiences
        #To update the model weights
        self.experience_memory = deque(maxlen = REPLAY_MEMORY_SIZE)
        #counter to determine when to update our target model "set our weights in stone" if you will
        self.target_update_counter = 0

    def create_model(self):
        '''
        Here is where we actually define (and potentially compile) our Deep Q-Function Network

        Make sure to use the global variables or environment's:
            - INPUT_SIZE/OBSERVATION_SPACE_SHAPE
            - OUTPUT_SIZE/ACTION_SPACE_SIZE
        '''
        pass

    def get_qs(self, state):
        '''
        Just return the q-values (might have some shape problems for batches?)
        '''
        return self.model.predict(np.array(state))

    def _hidden_train(self, terminal_state):
        '''
        Trains the network every step during an episode (as long as we have enough actions in memory).

        Gets a minibatch of experiences to train on. Uses a modified version of the Bellman Equation to update gradients.
        Ends up being a little bit complicated because as we train and update our network, our loss function needs to be updated
        (We essentially have a sequence of loss functions). Hope this isn't too confusing.

        Parameters:
            - terminal state: When we are in a completed state, this is when we might log some statistics about how we're doing.
            TRUE/FALSE


        We now have to reformulate the model loss in terms of the difference of our model's prediction (max q-value)
        and the temporary model's max q-values with observed reward.

        Model 1 output is [q_a1, q_a2, ..., q_an] = o
        We chose some action (for simplicity), q_a1.

        By the Bellman equation, we actually want q_a1 to be equal to the reward plus the dampened
        maximum value of our target_model's output on the subsequent state, s', (as the result of our action).
        q_a1 = r + DISCOUNT * max(target_model(s'))

        So our x will be the current state, but our "response", is actually:
        y = [r+discount * max(target_model(s')), q_a2, ..., q_an]

        Finally, the loss function of our model that we'll be fitting to is actually:
        loss = (y-o)^2 = [q*_a1, 0, ..., 0]

        Put another way, we're trying to make q_a1 = q*_a1. This loss is actually across the whole batch of experiences that we randomly sampled.
        '''
        # Get a minibatch of experiences
        minibatch = random.sample(self.experience_memory, MINIBATCH_SIZE)
        # Get the current states from a minibatch and query model for q-values
        current_states = np.array([experience[0] for experience in minibatch])
        current_qs_list = self.model.predict(current_states)

        #Get future states from minibatch, get the maximum argument of the target_model
        new_states = np.arrat([experience[3] for experience in minibatch])
        future_qs_list = self.target_model.predict(new_states)

        #We have the q's of our model for the current states, and the q's of the temporary model's next state.
        #Now we can build our X and Y described previously
        X = []
        y = []
        for index, (current_state, action, reward, new_state, done) in enumerate(minibatch):
            #If we're not in a terminal state, we get new_state to calculate expected future reward of the new state
            if not done:
                max_future_q = np.max(future_qs_list[index])
                y_i = reward + DISCOUNT * max_future_q
            #Otherwise, we use the reward as the y_i
            else:
                y_i = reward
            #Build the y_vector we saw in the
            qs_we_want = current_qs_list.copy()
            qs_we_want[index] = y_i
            #Finally, add them to our training data
            X.append(current_state)
            y.append(qs_we_want)
        #Now that we've done that mess, we can actually fit our model to this batch.
        #Could put tensorboard in here.
        self.model.fit(np.array(X), np.array(y), batch_size = MINIBATCH_SIZE, verbose=0)
        #Update your target update counter every episode (full rubik's cube you solve)
        if terminal_state:
            self.target_update_counter += 1
        #If update counter reaches threshold, you actually update the target model.
        if self.target_update_counter > UPDATE_TARGET_MODEL_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def train(self):
        '''
        An outline of the what training through episodes (e.g., one cube solve attempt) looks like.

        Conceptual issues:
            - How do we deal with terminal states (solved cubes) as next_states when we pass it into the _hidden_train.
        '''
        training_history = []
        for episode in range(1, EPISODES+1):
            #maybe update tensorboard, I've been looking at it, could be cool.
            #otherwise restart everything
            episode_reward = 0
            step = 1 #currently unused, but tracks how many training steps we've done.
            #PAPER: Initialize sequence s_1 =  {x_1}
            current_state = env.reset() #Restart and get the first, initial state
            #Restart finishing flag
            done = False
            while not done:
                if np.random.random() > epsilon:
                    #Get action from the Q-table
                    action = np.argmax(self.get_qs(current_state))
                else:
                    #Do a random action
                    action = np.random.randint(0, env.ACTION_SPACE_SIZE)
                #Perform action in the environment
                next_state, reward, done = env.do_action(action)
                episode_reward += reward
                #Save experience into  memory
                #TODO make sure that if new_state is solved that returned done is actually TRUE
                self.experience_memory.append( (current_state, action, reward, new_state, done) )
                if len(self.experience_memory) > MIN_EXPERIENCE_SIZE:
                    self._hidden_train(done)
                    step += 1
                current_state = new_state
            ep_rewards.append(episode_reward)
            #This is where you might aggregate stats here.
            #Plot your min/max/average episode rewards every something episodes
            #maybe save your model when your minimum episode rewards is greater than something
            if not episode % AGGREGATE_STATS_EVERY or episode == 1:
                average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:])/len(ep_rewards)
                min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
                max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
                training_history.append((max_reward, average_reward, min_reward))
                #Save it if we meet requirements
                if min_reward >= MIN_REWARD_TO_SAVE:
                    save_name = "../models/"+MODEL_NAME+"_"+str(max_reward)+ "max_"+str(average_reward)+"avg_"+min_reward+"min_"+str(int(time.time()))+".model"
                    self.model.save(save_name)
            if epsilon > MIN_EPSILON:
                epsilon *= EPSILON_DECAY
        print(training_history)
        return(training_history)
