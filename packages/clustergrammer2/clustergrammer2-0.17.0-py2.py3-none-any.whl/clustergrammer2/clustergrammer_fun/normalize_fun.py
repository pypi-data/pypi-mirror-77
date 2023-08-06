import pandas as pd
import numpy as np
from copy import deepcopy

def run_norm(net, df=None, norm_type='zscore', axis='row', z_clip=None):
  '''
  A dataframe can be passed to run_norm and a normalization will be run (
  e.g. zscore) on either the rows or columns
  '''

  if df is None:
    df = net.dat_to_df()

  if norm_type == 'zscore':
    df, ser_mean, ser_std = zscore_df(df, axis, z_clip=z_clip)

    net.dat['pre_zscore'] = {}
    net.dat['pre_zscore']['mean'] = ser_mean.values.tolist()
    net.dat['pre_zscore']['std'] = ser_std.values.tolist()

  if norm_type == 'qn':
    df = qn_df(df, axis)

  if norm_type == 'umi':
    df = umi_norm(df)

  net.df_to_dat(df)

  # if norm_type == 'zscore' and axis == 'row':
  #   net.dat['pre_zscore'] = {}
  #   net.dat['pre_zscore']['mean'] = ser_mean
  #   net.dat['pre_zscore']['std'] = ser_std

def qn_df(df, axis='row'):
  '''
  do quantile normalization of a dataframe dictionary, does not write to net
  '''
  # using transpose to do row qn
  if axis == 'row':
    df = df.transpose()

  missing_values = df.isnull().values.any()

  # make mask of missing values
  if missing_values:

    # get nan mask
    missing_mask = pd.isnull(df)

    # tmp fill in na with zero, will not affect qn
    df = df.fillna(value=0)

  # calc common distribution
  common_dist = calc_common_dist(df)

  # swap in common distribution
  df = swap_in_common_dist(df, common_dist)

  # swap back in missing values
  if missing_values:
    df = df.mask(missing_mask, other=np.nan)

  # using transpose to do row qn
  if axis == 'row':
    df = df.transpose()

  df_qn = df

  return df_qn

def swap_in_common_dist(df, common_dist):

  col_names = df.columns.tolist()

  qn_arr = np.array([])
  orig_rows = df.index.tolist()

  # loop through each column
  for inst_col in col_names:

    # get the sorted list of row names for the given column
    tmp_series = deepcopy(df[inst_col])
    tmp_series = tmp_series.sort_values(ascending=False)
    sorted_names = tmp_series.index.tolist()

    qn_vect = np.array([])
    for inst_row in orig_rows:
      inst_index = sorted_names.index(inst_row)
      inst_val = common_dist[inst_index]
      qn_vect = np.hstack((qn_vect, inst_val))

    if qn_arr.shape[0] == 0:
      qn_arr = qn_vect
    else:
      qn_arr = np.vstack((qn_arr, qn_vect))

  # transpose (because of vstacking)
  qn_arr = qn_arr.transpose()

  qn_df = pd.DataFrame(data=qn_arr, columns=col_names, index=orig_rows)

  return qn_df

def calc_common_dist(df):
  '''
  calculate a common distribution (for col qn only) that will be used to qn
  '''

  # axis is col
  tmp_arr = np.array([])

  col_names = df.columns.tolist()

  for inst_col in col_names:

    # sort column
    tmp_vect = df[inst_col].sort_values(ascending=False).values

    # stacking rows vertically (will transpose)
    if tmp_arr.shape[0] == 0:
      tmp_arr = tmp_vect
    else:
      tmp_arr = np.vstack((tmp_arr, tmp_vect))

  tmp_arr = tmp_arr.transpose()

  common_dist = tmp_arr.mean(axis=1)

  return common_dist

def zscore_df(df, axis='row', z_clip=None):
  '''
  take the zscore of a dataframe dictionary, does not write to net (self)
  '''

  if axis == 'row':
    df = df.transpose()

  ser_mean = df.mean()
  ser_std = df.std()

  df_z = (df - ser_mean)/ser_std

  if axis == 'row':
    df_z = df_z.transpose()

  if z_clip is not None:
    df_z = z_clip_fun(df_z, lower=-z_clip, upper=z_clip)

  return df_z, ser_mean, ser_std

def umi_norm(df):
    # umi norm
    barcode_umi_sum = df.sum()
    df_umi = df.div(barcode_umi_sum)
    return df_umi


def z_clip_fun(df_z, lower=None, upper=None):
  '''
  Trim values at input thresholds using pandas function
  '''
  df_z = df_z.clip(lower=lower, upper=upper)

  return df_z