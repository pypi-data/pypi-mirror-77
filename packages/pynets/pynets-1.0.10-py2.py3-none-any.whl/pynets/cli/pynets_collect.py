#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 10:40:07 2017
Copyright (C) 2017
@author: Derek Pisner (dPys)
"""
from nipype.interfaces import utility as niu
from nipype.pipeline import engine as pe
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def get_parser():
    """Parse command-line inputs"""
    import argparse
    from pynets.__about__ import __version__

    verstr = f"pynets v{__version__}"

    # Parse args
    parser = argparse.ArgumentParser(
        description="PyNets: A Fully-Automated Workflow for Reproducible"
                    " Functional and Structural Connectome Ensemble Learning")
    parser.add_argument(
        "-basedir",
        metavar="Output directory",
        help="Specify the path to the base output directory with group-level"
             " pynets derivatives.\n",
    )
    parser.add_argument(
        "-modality",
        nargs=1,
        choices=["dwi", "func"],
        help="Specify data modality from which to collect data. Options are"
             " `dwi` and `func`.",
    )
    parser.add_argument(
        "-dc",
        metavar="Column strings to exclude",
        default=None,
        nargs="+",
        help="Space-delimited list of strings.\n",
    )
    parser.add_argument(
        "-pm",
        metavar="Cores,memory",
        default="auto",
        help="Number of cores to use, number of GB of memory to use for single"
             " subject run, entered as two integers seperated by comma. "
             "Otherwise, default is `auto`, which uses all resources detected"
             " on the current compute node.\n",
    )
    parser.add_argument(
        "-plug",
        metavar="Scheduler type",
        default="MultiProc",
        nargs=1,
        choices=[
            "Linear",
            "MultiProc",
            "SGE",
            "PBS",
            "SLURM",
            "SGEgraph",
            "SLURMgraph",
            "LegacyMultiProc",
        ],
        help="Include this flag to specify a workflow plugin other than the"
             " default MultiProc.\n",
    )
    parser.add_argument(
        "-v",
        default=False,
        action="store_true",
        help="Verbose print for debugging.\n")
    parser.add_argument(
        "-work",
        metavar="Working directory",
        default="/tmp/work",
        help="Specify the path to a working directory for pynets to run."
             " Default is /tmp/work.\n",
    )
    parser.add_argument("--version", action="version", version=verstr)
    return parser


def load_pd_dfs(file_):
    import gc
    import os.path as op
    import pandas as pd
    import numpy as np
    from colorama import Fore, Style
    from pynets.cli.pynets_collect import summarize_missingness

    pd.set_option("display.float_format", lambda x: f"{x:.8f}")

    if file_:
        if op.isfile(file_) and not file_.endswith("_clean.csv"):
            df = pd.read_csv(file_, chunksize=100000, encoding="utf-8",
                             nrows=1, skip_blank_lines=False,
                             warn_bad_lines=True, error_bad_lines=False,
                             memory_map=True).read()
            if "Unnamed: 0" in df.columns:
                df.drop(df.filter(regex="Unnamed: 0"), axis=1, inplace=True)
            id = op.basename(file_).split("_topology")[0]
            if 'sub-sub-' in id:
                id = id.replace('topology_auc_sub-', '')
            else:
                id = id.replace('topology_auc_', '')
            if 'ses-ses-' in id:
                id = id.replace('ses-ses-', 'ses-')

            id = ('_').join(id.split('_')[0:2])

            if '.csv' in id:
                id = id.replace('.csv', '')

            #print(id)
            ID = id.split("_")[0].split("sub-")[1]
            ses = id.split("_")[1].split("ses-")[1]
            df["id"] = id
            df["id"] = df["id"].astype('str')
            df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
            bad_cols1 = df.columns[df.columns.str.endswith("_x")]
            if len(bad_cols1) > 0:
                for col in bad_cols1:
                    if np.isnan(df[col][0]) is False:
                        df.rename(columns=dict(zip(bad_cols1, [bad_col.split(
                            "_x")[0] for bad_col in bad_cols1])), inplace=True)
                    else:
                        df.drop(columns=[col], inplace=True)
                del col
            bad_cols2 = df.columns[df.columns.str.endswith("_y")]
            if len(bad_cols2) > 0:
                for col in bad_cols2:
                    if np.isnan(df[col][0]) is False:
                        df.rename(columns=dict(zip(bad_cols2, [bad_col.split(
                            "_y")[0] for bad_col in bad_cols2])),
                                  inplace=True)
                    else:
                        df.drop(columns=[col], inplace=True)
                del col

            df = df.loc[:, ~df.columns.str.contains(r".?\d{1}$", regex=True)]

            # Find empty duplicate columns
            df_dups = df.loc[:, df.columns.duplicated()]
            if df_dups.empty is False:
                empty_cols = [col for col in df.columns if
                              df_dups[col].isnull().all()]
                # Drop these columns from the dataframe
                print(f"{Fore.LIGHTYELLOW_EX}Dropping duplicated empty columns: {empty_cols}{Style.RESET_ALL}")
                df.drop(empty_cols,
                        axis=1,
                        inplace=True)
            if "Unnamed: 0" in df.columns:
                df.drop(df.filter(regex="Unnamed: 0"), axis=1, inplace=True)
            summarize_missingness(df)
            df.to_csv(f"{file_.split('.csv')[0]}{'_clean.csv'}", index=True)
            del bad_cols2, bad_cols1, id

        else:
            print(f"{Fore.RED}Cleaned {file_} missing...{Style.RESET_ALL}")
            df = pd.DataFrame()
    else:
        print(f"{Fore.RED}{file_} missing...{Style.RESET_ALL}")
        df = pd.DataFrame()
    gc.collect()

    return df


def df_concat(dfs, working_path, modality):
    import pandas as pd
    from colorama import Fore, Style

    pd.set_option("display.float_format", lambda x: f"{x:.8f}")

    def harmonize_dtypes(df):
        for i in [j for j in df.columns if j != 'id']:
            df[i] = df[i].astype("float32")
        return df

    dfs = [harmonize_dtypes(df) for df in dfs if df is not None and
           df.empty is False]

    frame = pd.concat(dfs, axis=0, join="outer", sort=True,
                      ignore_index=False)

    frame = frame.drop_duplicates(subset="id")
    frame = frame.loc[:, ~frame.columns.str.contains(r"thr_auc$", regex=True)]
    # frame = frame.loc[:, (frame == 0).mean() < .5]
    # frame = frame.loc[:, frame.isnull().mean() <= 0.1]
    cols = list(frame.columns)
    # Set ID to the first column
    cols = [cols[-1]] + cols[:-1]
    frame = frame[cols]
    #frame.dropna(thresh=0.50*len(frame.columns), inplace=True)
    missingness_dict = summarize_missingness(frame)[0]
    bad_cols = []
    for col in missingness_dict.keys():
        if missingness_dict[col] > 0.20:
            bad_cols.append(col)

    if len(bad_cols) > 0:
        print(f"{Fore.LIGHTYELLOW_EX}Dropping columns with excessive "
              f"missingness: {bad_cols}{Style.RESET_ALL}")
        frame = frame.drop(columns=bad_cols)

    frame.to_csv(f"{working_path}/all_subs_neat_{modality}.csv", index=False)

    # frame['missing'] = frame.apply(lambda x: x.count(), axis=1)
    # frame = frame.loc[frame['missing'] > np.mean(frame['missing'])]
    # frame = frame.sort_values(by=['missing'], ascending=False)

    return frame


def summarize_missingness(df):
    import numpy as np
    from colorama import Fore, Style
    missingness_dict = dict(df.apply(lambda x: x.isna().sum() /
                                                  (x.count() + x.isna().sum()),
                                        axis=0))
    missingness_mean = np.mean(list(missingness_dict.values()))
    if missingness_mean > 0.50:
        print(f"{Fore.RED} {df} missing {100*missingness_mean}% values!{Style.RESET_ALL}")

    return missingness_dict, missingness_mean


def load_pd_dfs_auc(atlas_name, prefix, auc_file, modality, drop_cols):
    from colorama import Fore, Style
    import pandas as pd
    import re

    pd.set_option("display.float_format", lambda x: f"{x:.8f}")

    df = pd.read_csv(
        auc_file, chunksize=100000, compression="gzip", encoding="utf-8",
        nrows=1, skip_blank_lines=False,
        warn_bad_lines=True, error_bad_lines=False,
        memory_map=True).read()
    #print(f"{'Atlas: '}{atlas_name}")
    prefix = f"{atlas_name}{'_'}{prefix}{'_'}"
    df_pref = df.add_prefix(prefix)
    if modality == 'dwi':
        df_pref = df_pref.rename(
            columns=lambda x: re.sub(
                "nodetype-parc_samples-\d{1,5}0000streams_tracktype-local_", "",
                x))
        df_pref = df_pref.rename(
            columns=lambda x: re.sub(
                "_tol-\d{1,20}", "",
                x))
    bad_cols = [i for i in df_pref.columns if any(ele in i for ele in
                                                  drop_cols)]
    print(f"{Fore.YELLOW} Dropping {len(bad_cols)}: {bad_cols} containing exclusionary strings...{Style.RESET_ALL}")
    df_pref.drop(columns=bad_cols, inplace=True)

    print(df_pref)
    # Find empty duplicate columns
    df_dups = df_pref.loc[:, df_pref.columns.duplicated()]
    if df_dups.empty is False:
        empty_cols = [col for col in df_pref.columns if
                      df_dups[col].isnull().all()]
        # Drop these columns from the dataframe
        df_pref.drop(empty_cols,
                axis=1,
                inplace=True)
    if "Unnamed: 0" in df_pref.columns:
        df_pref.drop(df_pref.filter(regex="Unnamed: 0"), axis=1, inplace=True)

    if df_pref.empty:
        print(f"{Fore.RED}Empty raw AUC: {df_pref} from {auc_file}...{Style.RESET_ALL}")
    return df_pref


def build_subject_dict(sub, working_path, modality, drop_cols):
    import shutil
    import os
    import glob
    from pathlib import Path
    from colorama import Fore, Style
    from pynets.cli.pynets_collect import load_pd_dfs_auc, summarize_missingness
    subject_dict = {}
    #print(sub)
    subject_dict[sub] = {}
    sessions = sorted(
        [i for i in os.listdir(f"{working_path}{'/'}{sub}") if i.startswith(
            "ses-")],
        key=lambda x: x.split("-")[1],
    )
    atlases = list(
        set(
            [
                os.path.basename(str(Path(i).parent.parent))
                for i in glob.glob(f"{working_path}{'/'}{sub}"
                                   f"/*/*/*/topology/*", recursive=True)
            ]
        )
    )
    #print(atlases)

    files_ = []
    for ses in sessions:
        #print(ses)
        subject_dict[sub][ses] = []
        for atlas in atlases:
            #atlas_name = "_".join(atlas.split("_")[1:])
            auc_csvs = glob.glob(
                f"{working_path}/{sub}/{ses}/{modality}/{atlas}/topology/auc/*"
            )
            for auc_file in auc_csvs:
                prefix = (
                    os.path.basename(auc_file)
                    .split(".csv")[0]
                    .split("model-")[1]
                    .split(modality)[0]
                )
                if os.path.isfile(auc_file):
                    df_sub = load_pd_dfs_auc(atlas, prefix, auc_file, modality, drop_cols)
                    if df_sub.empty:
                        continue
                    else:
                        subject_dict[sub][ses].append(df_sub)
                else:
                    print(f"{Fore.RED}Missing auc file for {sub} {ses}...{Style.RESET_ALL}")
                    continue
        list_ = subject_dict[sub][ses]
        if len(list_) > 0:
            df_base = list_[0][[c for c in list_[
                0].columns if c.endswith("auc")]]
            for m in range(len(list_))[1:]:
                df_base = df_base.merge(
                    list_[m][[c for c in list_[m].columns if c.endswith(
                        "auc")]],
                    how="right",
                    right_index=True,
                    left_index=True,
                )
            #df_base = pd.concat(list_, axis=1)
            summarize_missingness(df_base)
            if os.path.isdir(
                    f"{working_path}{'/'}{sub}{'/'}{ses}{'/'}{modality}"):
                out_path = (
                    f"{working_path}/{sub}/{ses}/{modality}/all_combinations"
                    f"_auc.csv"
                )
                df_base.to_csv(out_path, index=False)
                out_path_new = f"{str(Path(working_path))}/{modality}_" \
                               f"group_topology_auc/topology_auc_sub-{sub}_" \
                               f"ses-{ses}.csv"
                files_.append(out_path_new)
                shutil.copyfile(out_path, out_path_new)

            del df_base
        else:
            print(f"{Fore.RED}Missing data for {sub} {ses}...{Style.RESET_ALL}")
            continue
        del list_

    return files_


def collect_all(working_path, modality, drop_cols):
    from pathlib import Path
    import shutil
    import os

    import_list = [
        "import warnings",
        'warnings.filterwarnings("ignore")',
        "import os",
        "import numpy as np",
        "import indexed_gzip",
        "import nibabel as nib",
        "import glob",
        "import pandas as pd",
        "import shutil",
        "from pathlib import Path",
        "from colorama import Fore, Style"
    ]

    shutil.rmtree(f"{str(Path(working_path))}/{modality}_group_topology_auc",
                  ignore_errors=True)

    os.makedirs(f"{str(Path(working_path))}/{modality}_group_topology_auc")

    wf = pe.Workflow(name="load_pd_dfs")

    inputnode = pe.Node(
        niu.IdentityInterface(fields=["working_path", "modality", "drop_cols"]),
        name="inputnode"
    )
    inputnode.inputs.working_path = working_path
    inputnode.inputs.modality = modality
    inputnode.inputs.drop_cols = drop_cols

    build_subject_dict_node = pe.Node(
        niu.Function(
            input_names=["sub", "working_path", "modality", "drop_cols"],
            output_names=["files_"],
            function=build_subject_dict,
        ),
        name="build_subject_dict_node",
        imports=import_list,
    )
    build_subject_dict_node.iterables = (
        "sub",
        [i for i in os.listdir(working_path) if i.startswith("sub-")],
    )
    build_subject_dict_node.synchronize = True

    df_join_node = pe.JoinNode(
        niu.IdentityInterface(fields=["files_"]),
        name="df_join_node",
        joinfield=["files_"],
        joinsource=build_subject_dict_node,
    )

    load_pd_dfs_map = pe.MapNode(
        niu.Function(
            input_names=["file_"],
            outputs_names=["df"],
            function=load_pd_dfs),
        name="load_pd_dfs",
        imports=import_list,
        iterfield=["file_"],
        nested=True,
    )

    outputnode = pe.Node(
        niu.IdentityInterface(
            fields=["dfs"]),
        name="outputnode")

    wf.connect(
        [
            (inputnode, build_subject_dict_node,
             [("working_path", "working_path"), ('modality', 'modality'), ('drop_cols', 'drop_cols')]),
            (build_subject_dict_node, df_join_node, [("files_", "files_")]),
            (df_join_node, load_pd_dfs_map, [("files_", "file_")]),
            (load_pd_dfs_map, outputnode, [("df", "dfs")]),
        ]
    )

    return wf


def build_collect_workflow(args, retval):
    import os
    import glob
    import warnings
    warnings.filterwarnings("ignore")
    import ast
    import pkg_resources
    from pathlib import Path
    import yaml

    try:
        import pynets

        print(f"\n\nPyNets Version:\n{pynets.__version__}\n\n")
    except ImportError:
        print(
            "PyNets not installed! Ensure that you are using the correct"
            " python version."
        )

    # Set Arguments to global variables
    resources = args.pm
    if resources == "auto":
        from multiprocessing import cpu_count
        import psutil
        nthreads = cpu_count() - 1
        procmem = [int(nthreads),
                   int(list(psutil.virtual_memory())[4]/1000000000)]
    else:
        procmem = list(eval(str(resources)))
    plugin_type = args.plug
    if isinstance(plugin_type, list):
        plugin_type = plugin_type[0]
    verbose = args.v
    working_path = args.basedir
    work_dir = args.work
    modality = args.modality
    drop_cols = args.dc
    if isinstance(modality, list):
        modality = modality[0]

    os.makedirs(
        f"{str(Path(working_path))}/{modality}_group_topology_auc",
        exist_ok=True)

    wf = collect_all(working_path, modality, drop_cols)

    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        try:
            hardcoded_params = yaml.load(stream)
            runtime_dict = {}
            execution_dict = {}
            for i in range(len(hardcoded_params["resource_dict"])):
                runtime_dict[
                    list(hardcoded_params["resource_dict"][i].keys())[0]
                ] = ast.literal_eval(
                    list(hardcoded_params["resource_dict"][i].values())[0][0]
                )
            for i in range(len(hardcoded_params["execution_dict"])):
                execution_dict[
                    list(hardcoded_params["execution_dict"][i].keys())[0]
                ] = list(hardcoded_params["execution_dict"][i].values())[0][0]
        except FileNotFoundError:
            print("Failed to parse runconfig.yaml")

    os.makedirs(f"{work_dir}{'/pynets_out_collection'}", exist_ok=True)
    wf.base_dir = f"{work_dir}{'/pynets_out_collection'}"

    if verbose is True:
        from nipype import config, logging

        cfg_v = dict(
            logging={
                "workflow_level": "DEBUG",
                "utils_level": "DEBUG",
                "interface_level": "DEBUG",
                "filemanip_level": "DEBUG",
                "log_directory": str(wf.base_dir),
                "log_to_file": True,
            },
            monitoring={
                "enabled": True,
                "sample_frequency": "0.1",
                "summary_append": True,
                "summary_file": str(wf.base_dir),
            },
        )
        logging.update_logging(config)
        config.update_config(cfg_v)
        config.enable_debug_mode()
        config.enable_resource_monitor()

        import logging

        callback_log_path = f"{wf.base_dir}{'/run_stats.log'}"
        logger = logging.getLogger("callback")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(callback_log_path)
        logger.addHandler(handler)

    execution_dict["crashdump_dir"] = str(wf.base_dir)
    execution_dict["plugin"] = str(plugin_type)
    cfg = dict(execution=execution_dict)
    for key in cfg.keys():
        for setting, value in cfg[key].items():
            wf.config[key][setting] = value
    try:
        wf.write_graph(graph2use="colored", format="png")
    except BaseException:
        pass
    if verbose is True:
        from nipype.utils.profiler import log_nodes_cb

        plugin_args = {
            "n_procs": int(procmem[0]),
            "memory_gb": int(procmem[1]),
            "status_callback": log_nodes_cb,
            "scheduler": "mem_thread",
        }
    else:
        plugin_args = {
            "n_procs": int(procmem[0]),
            "memory_gb": int(procmem[1]),
            "scheduler": "mem_thread",
        }
    print("%s%s%s" % ("\nRunning with ", str(plugin_args), "\n"))
    wf.run(plugin=plugin_type, plugin_args=plugin_args)
    if verbose is True:
        from nipype.utils.draw_gantt_chart import generate_gantt_chart

        print("Plotting resource profile from run...")
        generate_gantt_chart(callback_log_path, cores=int(procmem[0]))
        handler.close()
        logger.removeHandler(handler)

    all_files = glob.glob(
        f"{str(Path(working_path))}/{modality}_group_topology_auc/*.csv"
    )

    files_ = [i for i in all_files if '_clean.csv' in i]

    dfs = []
    for file_ in files_:
        df = pd.read_csv(file_, chunksize=100000, encoding="utf-8",
            nrows=1, skip_blank_lines=False,
            warn_bad_lines=True, error_bad_lines=False,
            memory_map=True).read()
        if "Unnamed: 0" in df.columns:
            df.drop(df.filter(regex="Unnamed: 0"), axis=1, inplace=True)
        df.dropna(axis='columns', how='all', inplace=True)
        dfs.append(df)
        del df

    print("Aggregating dataframes...")
    frame = df_concat(dfs, working_path, modality)

    # Cleanup
    for j in all_files:
        if j not in files_:
            os.remove(j)

    print('\nDone!')
    return


def main():
    """Initializes collection of pynets outputs."""
    import gc
    import sys

    try:
        from pynets.core.utils import do_dir_path
    except ImportError:
        print(
            "PyNets not installed! Ensure that you are referencing the correct"
            " site-packages and using Python3.5+"
        )

    if len(sys.argv) < 1:
        print("\nMissing command-line inputs! See help options with the -h"
              " flag.\n")
        sys.exit()

    args = get_parser().parse_args()
    # args_dict_all = {}
    # args_dict_all['plug'] = 'MultiProc'
    # args_dict_all['v'] = False
    # args_dict_all['pm'] = '24,57'
    # args_dict_all['basedir'] = '/working/tuning_set/outputs_shaeffer/pynets'
    # args_dict_all['work'] = '/tmp'
    # args_dict_all['modality'] = 'func'
    # args_dict_all['drop_cols'] = [
    #                  'diversity_coefficient', 'participation_coefficient',
    #                  "_minlength-20", "_minlength-30", "_minlength-0",
    #                  "variance", "sum"]
    # from types import SimpleNamespace
    # args = SimpleNamespace(**args_dict_all)

    from multiprocessing import set_start_method, Process, Manager

    set_start_method("forkserver")
    with Manager() as mgr:
        retval = mgr.dict()
        p = Process(target=build_collect_workflow, args=(args, retval))
        p.start()
        p.join()

        if p.exitcode != 0:
            sys.exit(p.exitcode)

        # Clean up master process before running workflow, which may create
        # forks
        gc.collect()
    mgr.shutdown()


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen" \
               "_importlib.BuiltinImporter'>)"
    main()
