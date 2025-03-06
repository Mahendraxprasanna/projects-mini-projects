import gymnasium as gym
import numpy as np
import pygame
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from gymnasium.spaces import Discrete, Box

# Create a custom Pong environment
class PongEnv(gym.Env):
    def __init__(self):
        super(PongEnv, self).__init__()
        
        # Define action and observation space
        self.action_space = Discrete(3)  # Move up, move down, stay
        self.observation_space = Box(low=-1, high=1, shape=(4,), dtype=np.float32)
        
        # Game variables
        self.paddle_y = 0.5
        self.ball_x, self.ball_y = 0.5, 0.5
        self.ball_dx, self.ball_dy = 0.01, 0.01
        
    def reset(self, seed=None, options=None):
        self.paddle_y = 0.5
        self.ball_x, self.ball_y = 0.5, 0.5
        self.ball_dx, self.ball_dy = 0.01, 0.01
        return np.array([self.paddle_y, self.ball_x, self.ball_y, self.ball_dx]), {}
    
    def step(self, action):
        if action == 0:  # Move up
            self.paddle_y = min(1.0, self.paddle_y + 0.05)
        elif action == 1:  # Move down
            self.paddle_y = max(0.0, self.paddle_y - 0.05)
        
        # Ball movement
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Wall bounce
        if self.ball_y <= 0 or self.ball_y >= 1:
            self.ball_dy *= -1
        
        # Paddle bounce
        if self.ball_x >= 0.95 and abs(self.ball_y - self.paddle_y) < 0.1:
            self.ball_dx *= -1
            reward = 1  # Reward for hitting the ball
        else:
            reward = -1 if self.ball_x > 1 else 0  # Negative reward if ball goes past paddle
        
        done = self.ball_x > 1
        obs = np.array([self.paddle_y, self.ball_x, self.ball_y, self.ball_dx])
        return obs, reward, done, False, {}

# Train RL model
def train_model():
    env = DummyVecEnv([lambda: PongEnv()])
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save("pong_dqn")
    print("✅ Training Complete!")

# Play against AI
def play_game():
    env = PongEnv()
    model = DQN.load("pong_dqn")
    
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()
    running = True
    obs, _ = env.reset()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        action, _ = model.predict(obs)
        obs, _, done, _, _ = env.step(action)
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (370, env.paddle_y * 400, 10, 50))
        pygame.draw.circle(screen, (255, 255, 255), (int(env.ball_x * 400), int(env.ball_y * 400)), 8)
        pygame.display.flip()
        clock.tick(30)
        
        if done:
            obs, _ = env.reset()
    
    pygame.quit()

# Run training or play the game
if __name__ == "__main__":
    train_model()
    play_game()
