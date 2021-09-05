import os
import pdb

from doodad.wrappers.easy_launch import sweep_function, save_doodad_config

codepath = '/home/code'

def remote_fn(doodad_config, variant):
    kwarg_string = ' '.join([
        f'--{k} {v}' for k, v in variant.items()
    ])
    print(kwarg_string)

    d4rl_path = os.path.join(doodad_config.output_directory, 'datasets/')
    os.system(f'ls -a {codepath}')
    os.system(f'mv {codepath}/git {codepath}/.git')
    os.system(
        f'''export PYTHONPATH=$PYTHONPATH:{codepath} && '''
        f'''export CUDA_VISIBLE_DEVICES=0 && '''
        f'''export D4RL_DATASET_DIR={d4rl_path} && '''
        f'''python {codepath}/scripts/train.py '''
        f'''{kwarg_string}'''

    )
    save_doodad_config(doodad_config)

environments = ['halfcheetah', 'hopper', 'walker2d']
# buffers = ['medium-expert-v2', 'medium-v2', 'medium-replay-v2']
buffers = ['random-v2']
datasets = [f'{env}-{buf}' for env in environments for buf in buffers]

azure_logpath = 'defaults/'

if __name__ == "__main__":
    params_to_sweep = {
        'logbase': [os.path.join('/doodad_tmp', azure_logpath, 'logs')],
        'exp_name': ['gpt/azure'],
        'dataset': datasets,
    }

    sweep_function(
        remote_fn,
        params_to_sweep,
        config_path=os.path.abspath('azure/config.py'),
        log_path=azure_logpath,
        gpu_model='nvidia-tesla-v100',
        filter_dir=['logs'],
        use_gpu=True,
    )
