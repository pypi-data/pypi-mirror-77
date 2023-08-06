import sys
import numpy as np
import pandas as pd
from collections import OrderedDict
from toolz import itemmap, keymap, valmap

from .utils import decode_escapes, decode_array


MAPPING = {
    "object": "String",
    "uint64": "UInt64",
    "uint32": "UInt32",
    "uint16": "UInt16",
    "uint8": "UInt8",
    "float64": "Float64",
    "float32": "Float32",
    "int64": "Int64",
    "int32": "Int32",
    "int16": "Int16",
    "int8": "Int8",
    "datetime64[D]": "Date",
    "datetime64[ns]": "DateTime",
}

PD2CH = keymap(np.dtype, MAPPING)

PD_INT_TYPES = [
    pd.Int8Dtype(),
    pd.Int16Dtype(),
    pd.Int32Dtype(),
    pd.Int64Dtype(),
    pd.UInt8Dtype(),
    pd.UInt16Dtype(),
    pd.UInt32Dtype(),
    pd.UInt64Dtype(),
]

for typ in PD_INT_TYPES:
    PD2CH[typ] = f"Nullable({typ.name})"

CH2PD = itemmap(reversed, MAPPING)
CH2PD["Null"] = "object"
CH2PD["Nothing"] = "object"

NULLABLE_COLS = [
    "Float64",
    "Float32",
    "String",
]

NULLABLE_COLS_INT = [
    "UInt64",
    "UInt32",
    "UInt16",
    "UInt8",
    "Int64",
    "Int32",
    "Int16",
    "Int8",
]

for col in NULLABLE_COLS:
    CH2PD[f"Nullable({col})"] = CH2PD[col]

for col in NULLABLE_COLS_INT:
    CH2PD[f"Nullable({col})"] = col

PY3 = sys.version_info[0] == 3


def normalize(df, index=True):
    if index:
        df = df.reset_index()

    for col in df.select_dtypes([bool]):
        df[col] = df[col].astype("uint8")

    dtypes = valmap(PD2CH.get, OrderedDict(df.dtypes))
    if None in dtypes.values():
        raise ValueError("Unknown type mapping in dtypes: {}".format(dtypes))

    return dtypes, df


def to_csv(df):
    data = df.to_csv(
        header=False, index=False, encoding="utf-8", na_rep="\\N", sep=",",
    )
    if PY3:
        return data.encode("utf-8")
    else:
        return data


def to_dataframe(lines, keep_default_na=False, **kwargs):
    names = lines.readline().decode("utf-8").strip().split("\t")
    types = lines.readline().decode("utf-8").strip().split("\t")

    dtypes, parse_dates, converters = {}, [], {}
    for name, chtype in zip(names, types):
        if chtype.startswith("DateTime("):
            # Parse time zoned DateTimes as DateTime
            chtype = "DateTime"

        dtype = CH2PD.get(chtype, "object")

        if chtype.startswith("Array("):
            converters[name] = decode_array
        elif dtype == "object":
            converters[name] = decode_escapes
        elif dtype.startswith("datetime"):
            parse_dates.append(name)
        else:
            dtypes[name] = dtype

    return pd.read_csv(
        lines,
        sep="\t",
        header=None,
        names=names,
        dtype=dtypes,
        parse_dates=parse_dates,
        converters=converters,
        na_values="\\N",
        keep_default_na=keep_default_na,
        **kwargs,
    )


def partition(df, chunksize=1000):
    nrows = df.shape[0]
    nchunks = int(nrows / chunksize) + 1
    for i in range(nchunks):
        start_i = i * chunksize
        end_i = min((i + 1) * chunksize, nrows)
        if start_i >= end_i:
            break

        chunk = df.iloc[start_i:end_i]
        yield chunk
