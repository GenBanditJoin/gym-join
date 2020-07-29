from datetime import datetime
import yaml
from gym_join.envs.db_models import Table
import gym

OUTER_TABLE_PATH = "outer_table_path"
INNER_TABLE_PATH = "inner_table_path"
PAGE_SIZE = "page_size"
R_SEED = "r_random_seed"
S_SEED = "s_random_seed"


def nested_loop_join(config):
    env_config = config["env"]
    r_table = Table(env_config[OUTER_TABLE_PATH], env_config[PAGE_SIZE], env_config[R_SEED], True)
    k = env_config["k"]
    result_set = set()
    while True:

        r_page = r_table.next_page()
        if r_page == None:
            break
        s_table = Table(env_config[INNER_TABLE_PATH], env_config[PAGE_SIZE], env_config[S_SEED], False, False)
        count = 0
        while True:
            s_page = s_table.next_page()
            if s_page == None:
                break
            for s_tuple in s_page:

                if s_tuple.id1 in r_page.id1_set:
                    result_set.add(s_tuple.id1 + "-" + s_tuple.id2)
                    count += 1
                    if len(result_set) >= k:
                        return result_set
        # print(count)

def start_experiment(config, iters):
  
    env_id = 'gym_join:join-v0'
   
    total_time = 0
    results = 0
    for _ in range(iters):
        env = gym.make(env_id)
        env.set_config(config)
        start = datetime.now().timestamp()
        env.reset()
        done = False
        while not done:
            _, reward, done = env.step(0)
        total_time += (datetime.now().timestamp() - start)
        results += len(env.results)

    return total_time / iters, results / iters
    
if __name__ == "__main__":
    with open('config.yml') as f:
        config = yaml.safe_load(f)
    
    print("Block Nested Loop Join")

    # page_sizes = [32, 64, 128, 256, 512]
    # k_size = [50, 100, 500, 1000, 5000, 10000, 50000]

    page_sizes = [64, 128, 256, 512]
    k_size = [1000, 5000, 10000]

    # n_array = 2
    for k in k_size:
        config["env"]["k"] = k
        for page_size in page_sizes:
            config["env"]["page_size"] = page_size
            time, avg_results = start_experiment(config, 3)
            print(k, page_size, time, avg_results)

