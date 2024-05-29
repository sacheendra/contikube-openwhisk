#%%
import pandas as pd
from glob import glob
from plotnine import *

#%%
result_files = glob("exp_results*_50/*/*")
result_files

#%%
all_dfs = []
for result_file in result_files:
    filepath_splits = result_file.split("/")
    config = "default"
    if "opt" in filepath_splits[0]:
        config = "optimized"
    metadata_splits = filepath_splits[2].split(".")[0].split("_")
    depth = metadata_splits[1].split("-")[1]
    parallelism = metadata_splits[2].split("-")[1]
    iters = int(metadata_splits[3].split("-")[1])
    df = pd.read_csv(result_file, header=None)
    df.columns = ["start", "end"]
    df["depth"] = depth
    df["parallelism"] = parallelism
    df["iters"] = iters
    df["config"] = config
    df["duration"] = df["end"] - df["start"]
    all_dfs.append(df)
expdf = pd.concat(all_dfs)
expdf["parallelism"] = pd.Categorical(expdf["parallelism"], categories=["8","16","32","64"], ordered=True)
expdf["depth"] = expdf["depth"].str.replace("1", "length = 1")
expdf["depth"] = pd.Categorical(expdf["depth"], categories=["length = 1", "2", "4"], ordered=True)
expdf

#%%
summarized_df = (expdf.groupby(["parallelism", "depth", "config"])["duration"]
            .quantile([.25, .5, .75])
            .unstack()
            .reset_index()
            .rename(columns={
                0.25: "head", 0.5: "median", 0.75: "tail"
            }))
summarized_df

#%%
ggplot(summarized_df.loc[summarized_df["config"] == "default"]) +\
    geom_line(aes(x="parallelism", y="median", color="depth", group="depth")) +\
    geom_point(aes(x="parallelism", y="median", color="depth", group="depth"), size=3, position = position_dodge(width=0.1, preserve="total")) +\
    geom_linerange(aes(x="parallelism", ymin="head", ymax="tail", color="depth", group="depth"), position = position_dodge(width=0.1, preserve="total"))

#%%
ggplot(summarized_df.loc[summarized_df["config"] == "optimized"]) +\
    geom_line(aes(x="parallelism", y="median", color="depth", group="depth")) +\
    geom_point(aes(x="parallelism", y="median", color="depth", group="depth"), size=3, position = position_dodge(width=0.1, preserve="total")) +\
    geom_linerange(aes(x="parallelism", ymin="head", ymax="tail", color="depth", group="depth"), position = position_dodge(width=0.1, preserve="total"))

#%%
#%%
plt = ggplot(summarized_df) +\
    geom_line(aes(x="parallelism", y="median", color="config", group="config")) +\
    geom_point(aes(x="parallelism", y="median", color="config", group="config"), size=3, position = position_dodge(width=0.1, preserve="total")) +\
    geom_linerange(aes(x="parallelism", ymin="head", ymax="tail", color="config", group="config"), position = position_dodge(width=0.1, preserve="total")) +\
    facet_wrap("depth") +\
    theme_light(base_size=14) +\
    scale_color_manual(['#FFB200','#008837','#5e3c99']) +\
    guides(color=guide_legend(title="Kubernetes\nconfiguration")) +\
    theme(legend_position=(0.3, 0.7), legend_background=element_rect(fill=(0,0,0,0)), 
     figure_size=(6, 4), axis_text=element_text(size=13, rotation=0),
       panel_border=element_rect(color="black"), axis_line=element_line(color="black"), 
        legend_direction="vertical", strip_background=element_rect(fill="white", color="black"),
        strip_text=element_text(color="black"), legend_title=element_text(margin={"b":10}),
       axis_title_y=element_text(margin={"r":10})) +\
    xlab("Number of cores") + ylab("App latency [ms]")
plt.save("serverless_app_latency.pdf")
plt
