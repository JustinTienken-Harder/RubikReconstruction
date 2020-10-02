"""
Deep Q-function Network a sketch for how training a reinforcement function to approximate the Q-function in a reinforcement problem.

Code will not run as is, but provides an outline for training, inspired by the deepmind's Atari paper.


"""

from collections import deque #list like container with faster appends and pops
REPLAY_MEMORY_SIZE = 10_000

epsilon = 1 #This is the exploration factor. Not necessarily constant, could be decayed. Essentially the probability of doing a random action.
MIN_EPSILON = 0.05 #the minimum amount of exploration you will allow
EPSILON_DECAY = 0.9 #Multiply your epsilon by this every episode or (variable) times

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

    def _hidden_train(self):
        pass

    def train(self):
        for episode in range(1, EPISODES+1):
            #maybe update tensorboard, I've been looking at it, could be cool.
            #otherwise restart everything
            episode_reward = 0
            step = 1
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
                self.experience_memory.append( (current_state, action, reward, new_state, done) )
                #Check your batch sizes and shiiiiit before you do the hidden training bro.
            ep_rewards.append(episode_reward)
            #This is where you might aggregate stats here.
            #Plot your min/max/average episode rewards every something episodes
            #maybe save your model when your minimum reward for blank episodes is greater than something
            if epsilon > MIN_EPSILON:
                epsilon *= EPSILON_DECAY
