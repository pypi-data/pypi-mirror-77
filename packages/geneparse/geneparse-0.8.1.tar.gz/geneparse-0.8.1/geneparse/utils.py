"""Utilities"""

# This file is part of geneparse.
#
# The MIT License (MIT)
#
# Copyright (c) 2017 Pharmacogenomics Centre
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import urllib
import json
import logging
import warnings

import numpy as np
import pandas as pd

from .core import Variant
from . import parsers


logger = logging.getLogger(__name__)


warnings.simplefilter("once", DeprecationWarning)


def flip_alleles(genotypes):
    """Flip the alleles of an Genotypes instance."""
    warnings.warn("deprecated: use 'Genotypes.flip_coded'", DeprecationWarning)
    genotypes.reference, genotypes.coded = (genotypes.coded,
                                            genotypes.reference)
    genotypes.genotypes = 2 - genotypes.genotypes
    return genotypes


def code_minor(genotypes):
    """Encode the genotypes with respect to the minor allele.

    This confirms that "reference" is the major allele and that "coded" is
    the minor allele.

    In other words, this function can be used to make sure that the genotype
    value is the number of minor alleles for an individual.

    """
    warnings.warn("deprecated: use 'Genotypes.code_minor'", DeprecationWarning)
    _, minor_coded = maf(genotypes)
    if not minor_coded:
        return flip_alleles(genotypes)

    return genotypes


def maf(genotypes):
    """Computes the MAF and returns a boolean indicating if the minor allele
    is currently the coded allele.

    """
    warnings.warn("deprecated: use 'Genotypes.maf'", DeprecationWarning)
    g = genotypes.genotypes
    maf = np.nansum(g) / (2 * np.sum(~np.isnan(g)))
    if maf > 0.5:
        maf = 1 - maf
        return maf, False

    return maf, True


def rsids_to_variants(li):
    url = "http://grch37.rest.ensembl.org/variation/homo_sapiens"

    req = urllib.request.Request(
        url=url,
        data=json.dumps({"ids": li}).encode("utf-8"),
        headers={
            "Content-type": "application/json",
            "Accept": "application/json",
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read().decode("utf-8"))

    out = {}
    for name, info in data.items():
        # Check the mappings.
        found = False
        for mapping in info["mappings"]:
            chrom = mapping.get("seq_region_name")
            pos = mapping.get("start")
            alleles = mapping.get("allele_string").split("/")

            assembly = mapping.get("assembly_name")

            valid = (assembly == "GRCh37" and
                     chrom is not None and
                     pos is not None and
                     len(alleles) >= 2)

            if found and valid:
                logger.warning("Multiple mappings for '{}'.".format(name))
            elif valid:
                found = True
                out[name] = Variant(name, chrom, pos, alleles)

        if not found:
            logger.warning(
                "Could not find mappings for '{}'.".format(name)
            )

    return out


def genotype_to_df(g, samples, as_string=False):
    """Convert a genotype object to a pandas dataframe.

    By default, the encoded values are stored, but the as_string argument can
    be used to represent it as characters (alleles) instead.

    """
    name = g.variant.name if g.variant.name else "genotypes"
    df = pd.DataFrame(g.genotypes, index=samples, columns=[name])

    if as_string:
        df["alleles"] = None

        hard_calls = df[name].round()
        df.loc[hard_calls == 0, "alleles"] = "{0}/{0}".format(g.reference)
        df.loc[hard_calls == 1, "alleles"] = "{0}/{1}".format(g.reference,
                                                              g.coded)
        df.loc[hard_calls == 2, "alleles"] = "{0}/{0}".format(g.coded)

        df = df[["alleles"]]
        df.columns = [name]

    return df


def compute_ld(cur_geno, other_genotypes, r2=False):
    """Compute LD between a marker and a list of markers.

    Args:
        cur_geno (Genotypes): The genotypes of the marker.
        other_genotypes (list): A list of genotypes.

    Returns:
        numpy.array: An array containing the r or r**2 values between cur_geno
                     and other_genotypes.

    Note:
        The genotypes will automatically be normalized using (x - mean) / std.

    """
    # Normalizing the current genotypes
    norm_cur = normalize_genotypes(cur_geno)

    # Normalizing and creating the matrix for the other genotypes
    norm_others = np.stack(
        tuple(normalize_genotypes(g) for g in other_genotypes),
        axis=1,
    )

    # Making sure the size is the same
    assert norm_cur.shape[0] == norm_others.shape[0]

    # Getting the number of "samples" per marker (taking into account NaN)
    n = (
        ~np.isnan(norm_cur.reshape(norm_cur.shape[0], 1)) *
        ~np.isnan(norm_others)
    ).sum(axis=0)

    # Computing r (replacing NaN by 0)
    r = pd.Series(
        np.dot(
            np.nan_to_num(norm_cur), np.nan_to_num(norm_others) / n
        ),
        index=[g.variant.name for g in other_genotypes],
        name="r2" if r2 else "r",
    )

    # Checking no "invalid" values (i.e. < -1 or > 1)
    r.loc[r > 1] = 1
    r.loc[r < -1] = -1

    if r2:
        return r ** 2
    else:
        return r


def compute_ld_matrix(genotypes, r2=False):
    """Compute the pairwise LD matrix from a genotype matrix.

    Args:
        genotypes (numpy.array): An m x n matrix of m samples and n variants.
        r2 (bool): Whether to return the r or r2.

    Returns:
        numpy.array: The n x n LD matrix.

    """
    ns = (~np.isnan(genotypes)).astype(int)
    ns = np.dot(ns.T, ns)

    # Standardize the genotypes.
    g_std = (
        (genotypes - np.nanmean(genotypes, axis = 0)) /
        np.nanstd(genotypes, axis = 0)
    )

    g_std[np.isnan(g_std)] = 0

    # Compute the LD.
    # i,j needs to be divided by n_samples i and j
    r = np.dot(g_std.T, g_std) / ns

    if r2:
        return r ** 2
    else:
        return r


def normalize_genotypes(genotypes):
    """Normalize the genotypes.

    Args:
        genotypes (Genotypes): The genotypes to normalize.

    Returns:
        numpy.array: The normalized genotypes.

    """
    genotypes = genotypes.genotypes
    return (genotypes - np.nanmean(genotypes)) / np.nanstd(genotypes)


def add_arguments_to_parser(parser):
    """Add often used arguments to an argument parser.

    When reading genotype files some command-line arguments are almost
    systematically used. To avoid rewriting the code, this function adds
    these arguments to a Python argparse.ArgumentParser instance.

    Eventually, a well-formed reader can be constructed using this pattern:

        reader = geneparse.parsers[args.genotypes_format](
            args.genotypes,
            **geneparse.utils.parse_kwargs(args.genotypes_kwargs)
        )

    """
    parser.add_argument(
        "--genotypes", "-g",
        help="The genotypes file."
    )

    parser.add_argument(
        "--genotypes-format", "-f",
        help="The genotypes file format (one of: {})."
             "".format(", ".join(parsers.keys()))
    )

    parser.add_argument(
        "--genotypes-kwargs", "-kw",
        help="Keyword arguments to pass to the genotypes container. "
             "A string of the following format is expected: "
             "'key1=value1,key2=value2,...It is also possible to prefix"
             "the values by 'int:' or 'float:' to cast the them before "
             "passing them to the constructor."
    )


def parse_kwargs(s):
    """Parse command line arguments into Python arguments for parsers.

    Converts an arguments string of the form: key1=value1,key2=value2 into
    a dict of arguments that can be passed to Python initializers.

    This function also understands type prefixes and will cast values prefixed
    with 'int:' or 'float:'. For example magic_number=int:4 will be converted
    to {"magic_number": 4}.

    """
    if s is None:
        return {}

    kwargs = {}
    for argument in s.split(","):
        key, value = argument.strip().split("=")

        if value.startswith("int:"):
            value = int(value[4:])

        elif value.startswith("float:"):
            value = float(value[6:])

        kwargs[key] = value

    return kwargs
