script_path=$(readlink -f $BASH_SOURCE)
script_dir=$(dirname $script_path)

export PATH=$PATH:$script_dir/bin
export PYTHONPATH=$PYTHONPATH:$script_dir/python
