from pathlib import Path
from socket import gethostname
from dask.distributed import Client, progress
from dask_jobqueue import HTCondorCluster

log_directory = Path('./logs') / gethostname()
if not log_directory.exists():
    log_directory.mkdir(parents=True)
for each in log_directory.glob('*'):
    each.unlink()

cluster = HTCondorCluster(
    cores=1,
    memory='2GB',
    disk='1GB',
    log_directory=log_directory
)
cluster.scale(n=10)
client = Client(cluster)
futures = client.map(lambda each: each + 1, range(100))
progress(futures)
result = client.gather(futures)
print(f'{result=}')
