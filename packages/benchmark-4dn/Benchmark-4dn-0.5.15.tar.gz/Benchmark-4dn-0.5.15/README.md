The repo contains a benchmarking script for some of the CWL workflows used by 4DN-DCIC (https://github.com/4dn-dcic/pipelines-cwl), that returns total space, mem and CPUs required per given input size and a recommended AWS EC2 instance type.

[![Build Status](https://travis-ci.org/SooLee/Benchmark.svg?branch=master)](https://travis-ci.org/SooLee/Benchmark)

### Example usage of benchmarking script
* importing the module
```python
from Benchmark import run as B
```

* md5
```python
app_name = 'md5'
input_json = {'input_size_in_bytes': {'input_file': 20000}}
B.benchmark(app_name, input_json)
```
```
{'aws': {'recommended_instance_type': 't2.xlarge', 'EBS_optimized': False, 'cost_in_usd': 0.188, 'EBS_optimization_surcharge': None, 'mem_in_gb': 16.0, 'cpu': 4}, 'total_size_in_GB': 14.855186462402344, 'total_mem_in_MB': 13142.84375, 'min_CPU': 4}
```

* fastqc-0-11-4-1
```python
app_name = 'fastqc-0-11-4-1'
input_json = {'input_size_in_bytes': {'input_fastq':20000},
              'parameters': {'threads': 2}}
B.benchmark(app_name, input_json)
```
```
{'recommended_instance_type': 't2.nano', 'EBS_optimized': False, 'cost_in_usd': 0.006, 'EBS_optimization_surcharge': None, 'mem_in_gb': 0.5, 'cpu': 1}
```

* bwa-mem
```python
app_name = 'bwa-mem'
input_json = {'input_size_in_bytes': {'fastq1':93520000,
                                      'fastq2':97604000,
                                      'bwa_index':3364568000},
              'parameters': {'nThreads': 4}}
B.benchmark(app_name, input_json)
```
```
{'aws': {'cost_in_usd': 0.188, 'EBS_optimization_surcharge': None, 'EBS_optimized': False, 'cpu': 4, 'mem_in_gb': 16.0, 'recommended_instance_type': 't2.xlarge'}, 'total_mem_in_MB': 12834.808349609375, 'total_size_in_GB': 15.502477258443832, 'min_CPU': 4}
```

To use Benchmark in from other places, install it as below.
```
pip install Benchmark-4dn
```
or
```
pip install git+git://github.com/SooLee/Benchmark.git
```


---

Note: From `0.5.3` we have a new function that takes in cpu and memory and returns a sorted list of instance dictionaries.
```
get_instance_types(cpu=1, mem_in_gb=0.5, instances=instance_list(), top=10, rank='cost_in_usd')
```

Keys in each instance dictionary:
```
'cost_in_usd', 'mem_in_gb', 'cpu', 'instance_type', 'EBS_optimized', 'EBS_optimization_surcharge'
```
