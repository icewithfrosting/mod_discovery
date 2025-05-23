import logging
import os
from typing import Optional, List

import pandas as pd
from pandas import DataFrame
from tqdm import tqdm

from paths import OUT_DIR, WAVETABLES_DIR
from wavetables import CONTINUOUS_ABLETON_WTS

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))


def extract_test_vals(
    name: str, tsv_path: str, trial_col: str = "seed", x_col: str = "step", wt_names: Optional[List[str]] = None
) -> DataFrame:
    df = pd.read_csv(tsv_path, sep="\t", index_col=False)
    df = df[df["stage"] == "test"]
    if wt_names is not None:
        log.info(f"Including only {wt_names}, n_rows={len(df)} before")
        df = df[df["wt_name"].isin(wt_names)]
        log.info(f"Including only {wt_names}, n_rows={len(df)} after")
    df = df.drop(columns=["wt_name", "stage", "global_n"])
    df = df.groupby([trial_col, x_col]).mean().reset_index()
    df = df.drop(columns=[trial_col, x_col])
    df = pd.DataFrame(df.mean()).T
    df.insert(0, "name", name)
    return df


if __name__ == "__main__":
    tsv_names_and_paths = [
        # ("spline_n", os.path.join(OUT_DIR, f"out_curr/lfo/noise/mss__s24d3D__lfo__ase__ableton_13.tsv")),
        # ("8_hz_n", os.path.join(OUT_DIR, f"out_curr/lfo/noise/mss__frame_8_hz__lfo__ase__ableton_13.tsv")),
        # ("frame_n", os.path.join(OUT_DIR, f"out_curr/lfo/noise/mss__frame__lfo__ase__ableton_13.tsv")),
        # ("spline", os.path.join(OUT_DIR, f"out_curr/lfo/mss__s24d3D_nn__lfo__ase__ableton_13.tsv")),
        # ("8_hz", os.path.join(OUT_DIR, f"out_curr/lfo/mss__frame_8_hz_nn__lfo__ase__ableton_13.tsv")),
        # ("frame", os.path.join(OUT_DIR, f"out_curr/lfo/mss__frame_nn__lfo__ase__ableton_13.tsv")),
        ("spline", os.path.join(OUT_DIR, f"out_curr/lfo/mss__s24d3D_nn__lfo__ase__ableton_13__test.tsv")),
        ("8_hz", os.path.join(OUT_DIR, f"out_curr/lfo/mss__frame_8_hz_nn__lfo__ase__ableton_13__test.tsv")),
        ("frame", os.path.join(OUT_DIR, f"out_curr/lfo/mss__frame_nn__lfo__ase__ableton_13__test.tsv")),
        ("spline_v", os.path.join(OUT_DIR, f"out_curr/lfo/mss__s24d3D_nn__lfo__ase__ableton_13__vital_curves.tsv")),
        ("8_hz_v", os.path.join(OUT_DIR, f"out_curr/lfo/mss__frame_8_hz_nn__lfo__ase__ableton_13__vital_curves.tsv")),
        ("frame_v", os.path.join(OUT_DIR, f"out_curr/lfo/mss__frame_nn__lfo__ase__ableton_13__vital_curves.tsv")),

        # ("oracle", os.path.join(OUT_DIR, f"out_curr/sm/mss__oracle__sm_16_1024__ase__ableton_13.tsv")),
        # ("spline", os.path.join(OUT_DIR, f"out_curr/sm/mss__s24d3D__sm_16_1024__ase__ableton_13.tsv")),
        # ("8_hz", os.path.join(OUT_DIR, f"out_curr/sm/mss__frame_8_hz__sm_16_1024__ase__ableton_13.tsv")),
        # ("frame", os.path.join(OUT_DIR, f"out_curr/sm/mss__frame__sm_16_1024__ase__ableton_13.tsv")),
        # ("rand", os.path.join(OUT_DIR, f"out_curr/sm/mss__s24d3D_rand__sm__ase__ableton_13.tsv")),
        # ("rand_sm", os.path.join(OUT_DIR, f"out_curr/sm/mss__s24d3D_rand__sm_16_1024__ase__ableton_13.tsv")),
        # ("spline_nn", os.path.join(OUT_DIR, f"out_curr/sm/no_noise/mss__s24d3D_nn__sm_16_1024__ase__ableton_13.tsv")),
        # ("8_hz_nn", os.path.join(OUT_DIR, f"out_curr/sm/no_noise/mss__frame_8_hz_nn__sm_16_1024__ase__ableton_13.tsv")),
        # ("frame_nn", os.path.join(OUT_DIR, f"out_curr/sm/no_noise/mss__frame_nn__sm_16_1024__ase__ableton_13.tsv")),

        # ("spline", os.path.join(OUT_DIR, f"out_curr/serum/mss__s24d3D__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("8_hz", os.path.join(OUT_DIR, f"out_curr/serum/mss__frame_8_hz__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("frame", os.path.join(OUT_DIR, f"out_curr/serum/mss__frame__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("rand_sm", os.path.join(OUT_DIR, f"out_curr/serum/mss__s24d3D_rand__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("frame_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__frame_gran__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("spline_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__s24d3D_gran__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("8_hz_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__frame_8_hz_gran__sm_16_1024__serum__BA_both_lfo_10.tsv")),

        # ("spline", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_s24d3D__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("8_hz", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_frame_8_hz__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("frame", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_frame__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("rand_sm", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_s24d3D_rand__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("frame_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_frame_gran__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("spline_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_s24d3D_gran__sm_16_1024__serum__BA_both_lfo_10.tsv")),

        # ("spline", os.path.join(OUT_DIR, f"out_curr/serum/mss__ddsp_s24d3D__sm__serum__BA_both_lfo_10.tsv")),
        # ("8_hz", os.path.join(OUT_DIR, f"out_curr/serum/mss__ddsp_frame_8_hz__sm__serum__BA_both_lfo_10.tsv")),
        # ("frame", os.path.join(OUT_DIR, f"out_curr/serum/mss__ddsp_frame__sm__serum__BA_both_lfo_10.tsv")),
        # ("rand_sm", os.path.join(OUT_DIR, f"out_curr/serum/mss__ddsp_s24d3D_rand__sm__serum__BA_both_lfo_10.tsv")),
        # ("frame_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__ddsp_frame_gran__sm__serum__BA_both_lfo_10.tsv")),
        # ("spline_gran", os.path.join(OUT_DIR, f"out_curr/serum/mss__ddsp_s24d3D_gran__sm__serum__BA_both_lfo_10.tsv")),

        # ("rand_adapt", os.path.join(OUT_DIR, f"out_curr/serum/mss__s24d3D_rand_adapt__sm_16_1024__serum__BA_both_lfo_10.tsv")),
        # ("shan_100", os.path.join(OUT_DIR, f"out_curr/serum/mss__shan_100_not_sep_s24d3D__sm_16_1024__serum__BA_both_lfo_10.tsv")),
    ]

    wt_dir = os.path.join(WAVETABLES_DIR, "ableton")
    wt_names = [f[:-3] for f in os.listdir(wt_dir) if f.endswith(".pt")]
    wt_names = sorted(wt_names)
    filtered_wt_names = []
    for wt_name in wt_names:
        if any(wt_name.startswith(n) for n in CONTINUOUS_ABLETON_WTS):
            filtered_wt_names.append(wt_name)
    wt_names = filtered_wt_names
    # wt_names = None

    test_df_s = []
    for name, tsv_path in tqdm(tsv_names_and_paths):
        test_df = extract_test_vals(name, tsv_path, wt_names=wt_names)
        test_df_s.append(test_df)

    name_col = "name"
    df = pd.concat(test_df_s).reset_index(drop=True)
    rows = []
    for col in df.columns:
        if col == name_col:
            continue
        sort_ascending = True
        if "pcc" in col:
            sort_ascending = False
        data = df[[name_col, col]].sort_values([col], ascending=sort_ascending)
        sorted_names = data[name_col].tolist()
        sorted_names = [col] + sorted_names
        rows.append(sorted_names)
        sorted_vals = data[col].tolist()
        sorted_vals = [col] + sorted_vals
        rows.append(sorted_vals)

    sorted_cols = ["name"] + list(range(len(tsv_names_and_paths)))
    df = DataFrame(rows, columns=sorted_cols)
    # filter our rows where the name contains "_inv" or "_inv_all"
    # df = df[~df["name"].str.contains("audio__")]
    # df = df[~df["name"].str.contains("_inv__")]
    # df = df[~df["name"].str.contains("_inv_all")]
    df = df[~df["name"].str.contains("__esr")]
    df = df[~df["name"].str.contains("__mse")]
    df = df[~df["name"].str.contains("__fft")]
    # df = df[~df["name"].str.contains("__pcc")]
    df = df[~df["name"].str.contains("__cd")]
    df = df[~df["name"].str.contains("__dtw")]
    df = df[~df["name"].str.contains("_d2")]
    df = df[~df["name"].str.contains("__ent")]
    df = df[~df["name"].str.contains("__spec_ent")]
    df = df[~df["name"].str.contains("__tv")]
    df = df[~df["name"].str.contains("__tp")]
    df = df[~df["name"].str.contains("__range_mean")]
    df = df[~df["name"].str.contains("__min_val")]
    df = df[~df["name"].str.contains("__max_val")]
    # df = df[~df["name"].str.contains("fad__")]
    df = df[~df["name"].str.contains("__cf_8_hz")]

    nan_rows = df[df.isna().any(axis=1)].index
    for i in nan_rows:
        if i > 0:
            df = df.drop(i - 1)
            df = df.drop(i)

    # df = df[df["name"].str.contains("_inv_")]
    # df = df[df["name"].str.contains("__inv_all")]
    # df = df[df["name"].str.contains("__cf_8_hz__inv_all")]
    # df = df[df["name"].str.contains("audio__")]
    # df = df[df["name"].str.contains("__esr")]
    # df = df[df["name"].str.contains("__l1")]
    # df = df[df["name"].str.contains("__pcc")]
    # df = df[df["name"].str.contains("__fd")]
    # df = df[df["name"].str.contains("fad__")]
    print(df.to_string())
    print(f"len(df) = {len(df)}")

    # df = df[df[0] == "spline"]
    # df = df[df[0] == "cf_8"]
    # df = df[df[0] == "frame"]
    # df = df[df[0] == "rand"]
    # df = df[df[2] == "frame"]
    # df = df[df[0] == "oracle"]
    # df = df[(df[0] == "spline") | (df[1] == "spline")]
    df = df[(df[0] == "spline") | (df[0] == "8_hz")]
    print(df.to_string())
    print(f"len(df) = {len(df)}")
