#%%
import pandas as pd
from glob import glob
from plotnine import *

#%%
result_files = glob("exp_results_25/*/*")
result_files

#%%
result_file = result_files[1]
metadata_splits = result_file.split("/")[2].split(".")[0].split("_")
depth = int(metadata_splits[1].split("-")[1])
parallelism = int(metadata_splits[2].split("-")[1])
iters = int(metadata_splits[3].split("-")[1])

#%%
df = pd.read_csv(result_file, header=None)
df.columns = ["start", "end"]
df["depth"] = depth
df["parallelism"] = parallelism
df["iters"] = iters
df["duration"] = df["end"] - df["start"]
df

#%%
ggplot(df) +\
    geom_boxplot(aes(x="depth", y="duration"))

#%%
all_dfs = []
for result_file in result_files:
    metadata_splits = result_file.split("/")[2].split(".")[0].split("_")
    depth = int(metadata_splits[1].split("-")[1])
    parallelism = int(metadata_splits[2].split("-")[1])
    iters = int(metadata_splits[3].split("-")[1])
    df = pd.read_csv(result_file, header=None)
    df.columns = ["start", "end"]
    df["depth"] = depth
    df["parallelism"] = parallelism
    df["iters"] = iters
    df["duration"] = df["end"] - df["start"]
    all_dfs.append(df)
expdf = pd.concat(all_dfs)
expdf

#%%
d1df = expdf.loc[expdf["depth"] == 1].reset_index(drop=True)
d1df

#%%
ggplot(d1df) +\
    geom_boxplot(aes(x="parallelism", y="duration", group="parallelism"))

#%%
p16df = expdf.loc[expdf["parallelism"] == 16].reset_index(drop=True)
p16df

#%%
ggplot(p16df) +\
    geom_boxplot(aes(x="depth", y="duration", group="depth"))