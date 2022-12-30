from gym_tron import *


def assign_player_pos(board_size):
    return [random.randint(1, board_size - 1),random.randint(1, board_size - 1)]

board_size = 150

p1_pos = board_size//2
p2_pos = board_size//4
# p1_pos = 5
# p1_pos = assign_player_pos(board_size)
# p2_pos = assign_player_pos(board_size)
# if (p1_pos == p2_pos):
#     p2_pos = assign_player_pos(board_size)

player1 = Cycle((150,50,200), 1, p1_pos, p1_pos, 2, [[py.K_a],[py.K_w],[py.K_s],[py.K_d]])
player2 = Cycle((100,64,0), 2, p2_pos, p2_pos, 4,  [[py.K_LEFT],[py.K_UP],[py.K_DOWN],[py.K_RIGHT]])

cycles = [player1, player2]

env = TronEnv(cycles, board_size, scale=4)

save_path = os.path.join('Training', 'Saved Models')
log_path = os.path.join('Training', 'Logs')
PPO_path = os.path.join('Training', 'Saved Models', 'PPO_model')
Best_path = os.path.join('Training', 'Saved Models', 'best_model')

stop_callback = StopTrainingOnRewardThreshold(reward_threshold=300, verbose=1)
eval_callback = EvalCallback(env, 
                             callback_on_new_best=stop_callback, 
                             eval_freq=100, 
                             best_model_save_path=save_path, 
                             verbose=1)
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

model.load(Best_path)

model.learn(total_timesteps=100000, callback=eval_callback, log_interval=100)

model.save(PPO_path)

evaluate_policy(model, env, n_eval_episodes=10)

episodes = 10
for episode in range(1, episodes + 1):
    obs = env.reset()
    done = False
    score = 0

    while not done:
        env.render()
        action, _ = model.predict(obs,deterministic=True)
        obs, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score{} '.format(episode, score))

env.close()
py.display.quit()
py.quit()