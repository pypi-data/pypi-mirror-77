import shutil

from genrl.agents import SAC
from genrl.environments import VectorEnv
from genrl.trainers import OffPolicyTrainer


def test_sac():
    env = VectorEnv("Pendulum-v0", 2)
    algo = SAC("mlp", env, batch_size=5, policy_layers=[1, 1], value_layers=[1, 1])

    trainer = OffPolicyTrainer(
        algo,
        env,
        log_mode=["csv"],
        logdir="./logs",
        epochs=5,
        max_ep_len=500,
        warmup_steps=10,
        start_update=10,
    )
    trainer.train()
    shutil.rmtree("./logs")
