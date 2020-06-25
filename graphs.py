#!/bin/python3
from typing import List, Dict

import pandas


def prepare_size_dataset(datasets: List[Dict[str, str]]) -> pandas.DataFrame:
    results_df = pandas.DataFrame()
    for dataset in datasets:
        lzma_df = pandas.read_csv(dataset['lzma_file'], sep=';', index_col='id of repetition', nrows=1)
        lzma_df.drop(columns=['decompressed'], inplace=True)
        lzma_df = pandas.concat([lzma_df], keys=['LZMA'], names=['algorithm'], axis=1)
        lzma_df = pandas.concat([lzma_df], keys=[dataset['dataset_name']], names=['dataset'])
        lzma_df.index = lzma_df.index.droplevel(level=1)

        bzip2_df = pandas.read_csv(dataset['bzip2_file'], sep=';', index_col='id of repetition', nrows=1)
        bzip2_df.drop(columns=['decompressed', 'uncompressed'], inplace=True)
        bzip2_df = pandas.concat([bzip2_df], keys=['bzip2'], names=['algorithm'], axis=1)
        bzip2_df = pandas.concat([bzip2_df], keys=[dataset['dataset_name']], names=['dataset'])
        bzip2_df.index = bzip2_df.index.droplevel(level=1)
        dataset_df = pandas.concat([lzma_df, bzip2_df], axis=1)
        results_df = pandas.concat([results_df, dataset_df])

    results_df.columns = pandas.MultiIndex.from_tuples([("-", 'uncompressed'),
                                                        ("LZMA", "compressed"),
                                                        ("bzip2", "compressed")],
                                                       names=("algorithm", ""))
    return results_df


def prepare_time_df(df: pandas.DataFrame, op: str, algo: str, dataset_name: str) -> pandas.DataFrame:
    df.drop(columns=["elapsed wall clock time[s]", "percentage CPU", "maximum resident set size[Kilobytes]",
                     "file system inputs", "file system outputs", "command exit code", "command"], inplace=True)
    df['CPU-time (system+user)[s]'] = df['CPU-time (system)[s]'] + df['CPU-time (user)[s]']
    df.drop(columns=['CPU-time (system)[s]', 'CPU-time (user)[s]'], inplace=True)
    df = pandas.concat([df], keys=[op], names=['operation'], axis=1)
    df = pandas.concat([df], keys=[algo], names=['algorithm'], axis=1)
    df = pandas.concat([df], keys=[dataset_name], names=['dataset'], axis=1)
    return df


def prepare_space_df(df: pandas.DataFrame, op: str, algo: str, dataset_name: str) -> pandas.DataFrame:
    df.drop(columns=["elapsed wall clock time[s]", "CPU-time (system)[s]", "CPU-time (user)[s]", "percentage CPU",
                     "file system inputs", "file system outputs", "command exit code", "command"], inplace=True)
    df = pandas.concat([df], keys=[op], names=['operation'], axis=1)
    df = pandas.concat([df], keys=[algo], names=['algorithm'], axis=1)
    df = pandas.concat([df], keys=[dataset_name], names=['dataset'], axis=1)
    return df


def prepare_time_dataset(datasets: List[Dict[str, str]]) -> pandas.DataFrame:
    results_df = pandas.DataFrame()

    for dataset in datasets:
        lzma_comp_df = prepare_time_df(
            pandas.read_csv(dataset['lzma_comp_file'], sep=';', index_col='id of repetition'),
            op='compression', algo='LZMA', dataset_name=dataset['dataset_name'])

        lzma_decomp_df = prepare_time_df(
            pandas.read_csv(dataset['lzma_decomp_file'], sep=';', index_col='id of repetition'),
            op='decompression', algo='LZMA', dataset_name=dataset['dataset_name'])

        bzip2_comp_df = prepare_time_df(
            pandas.read_csv(dataset['bzip2_comp_file'], sep=';', index_col='id of repetition'),
            op='compression', algo='bzip2', dataset_name=dataset['dataset_name'])

        bzip2_decomp_df = prepare_time_df(
            pandas.read_csv(dataset['bzip2_decomp_file'], sep=';', index_col='id of repetition'),
            op='decompression', algo='bzip2', dataset_name=dataset['dataset_name'])

        dataset_df = pandas.concat([lzma_comp_df, lzma_decomp_df, bzip2_comp_df, bzip2_decomp_df], axis=1)
        results_df = pandas.concat([results_df, dataset_df], axis=1)

    return results_df


def prepare_space_dataset(datasets: List[Dict[str, str]]) -> pandas.DataFrame:
    results_df = pandas.DataFrame()

    for dataset in datasets:
        lzma_comp_df = prepare_space_df(
            pandas.read_csv(dataset['lzma_comp_file'], sep=';', index_col='id of repetition'),
            op='compression', algo='LZMA', dataset_name=dataset['dataset_name'])

        lzma_decomp_df = prepare_space_df(
            pandas.read_csv(dataset['lzma_decomp_file'], sep=';', index_col='id of repetition'),
            op='decompression', algo='LZMA', dataset_name=dataset['dataset_name'])

        bzip2_comp_df = prepare_space_df(
            pandas.read_csv(dataset['bzip2_comp_file'], sep=';', index_col='id of repetition'),
            op='compression', algo='bzip2', dataset_name=dataset['dataset_name'])

        bzip2_decomp_df = prepare_space_df(
            pandas.read_csv(dataset['bzip2_decomp_file'], sep=';', index_col='id of repetition'),
            op='decompression', algo='bzip2', dataset_name=dataset['dataset_name'])

        dataset_df = pandas.concat([lzma_comp_df, lzma_decomp_df, bzip2_comp_df, bzip2_decomp_df], axis=1)
        results_df = pandas.concat([results_df, dataset_df], axis=1)

    return results_df


size_dataset = prepare_size_dataset([
    {
        'dataset_name': 'sample_vid.mp4',
        'lzma_file': 'results_70/result_sample_vid.mp4_size_lzma.csv',
        'bzip2_file': 'results_70/result_sample_vid.mp4_size_bzip2.csv'
    }, {
        'dataset_name': 'sample_music',
        'lzma_file': 'results_70/result_sample_music_size_lzma.csv',
        'bzip2_file': 'results_70/result_sample_music_size_bzip2.csv'
    }, {
        'dataset_name': 'sample_image-data',
        'lzma_file': 'results_70/result_sample_image-data_size_lzma.csv',
        'bzip2_file': 'results_70/result_sample_image-data_size_bzip2.csv'
    }, {
        'dataset_name': 'sample_enwik8',
        'lzma_file': 'results_70/result_sample_enwik8_size_lzma.csv',
        'bzip2_file': 'results_70/result_sample_enwik8_size_bzip2.csv'
    }, {
        'dataset_name': 'sample_config',
        'lzma_file': 'results_70/result_sample_config_size_lzma.csv',
        'bzip2_file': 'results_70/result_sample_config_size_bzip2.csv'
    }])

time_space_datasets = [
    {
        'dataset_name': 'sample_vid.mp4',
        'lzma_comp_file': 'results_70/result_sample_vid.mp4_compress_lzma.csv',
        'lzma_decomp_file': 'results_70/result_sample_vid.mp4_decompress_lzma.csv',
        'bzip2_comp_file': 'results_70/result_sample_vid.mp4_compress_bzip2.csv',
        'bzip2_decomp_file': 'results_70/result_sample_vid.mp4_decompress_bzip2.csv'
    }, {
        'dataset_name': 'sample_music',
        'lzma_comp_file': 'results_70/result_sample_music_compress_lzma.csv',
        'lzma_decomp_file': 'results_70/result_sample_music_decompress_lzma.csv',
        'bzip2_comp_file': 'results_70/result_sample_music_compress_bzip2.csv',
        'bzip2_decomp_file': 'results_70/result_sample_music_decompress_bzip2.csv'
    }, {
        'dataset_name': 'sample_image-data',
        'lzma_comp_file': 'results_70/result_sample_image-data_compress_lzma.csv',
        'lzma_decomp_file': 'results_70/result_sample_image-data_decompress_lzma.csv',
        'bzip2_comp_file': 'results_70/result_sample_image-data_compress_bzip2.csv',
        'bzip2_decomp_file': 'results_70/result_sample_image-data_decompress_bzip2.csv'
    }, {
        'dataset_name': 'sample_enwik8',
        'lzma_comp_file': 'results_70/result_sample_enwik8_compress_lzma.csv',
        'lzma_decomp_file': 'results_70/result_sample_enwik8_decompress_lzma.csv',
        'bzip2_comp_file': 'results_70/result_sample_enwik8_compress_bzip2.csv',
        'bzip2_decomp_file': 'results_70/result_sample_enwik8_decompress_bzip2.csv'
    }, {
        'dataset_name': 'sample_config',
        'lzma_comp_file': 'results_70/result_sample_config_compress_lzma.csv',
        'lzma_decomp_file': 'results_70/result_sample_config_decompress_lzma.csv',
        'bzip2_comp_file': 'results_70/result_sample_config_compress_bzip2.csv',
        'bzip2_decomp_file': 'results_70/result_sample_config_decompress_bzip2.csv'
    }]

time_dataset = prepare_time_dataset(time_space_datasets)

space_dataset = prepare_space_dataset(time_space_datasets)

# bar chart for compressed size per dataset two bars (lzma, bzip2) absolute file size of compressed data
size_dataset.rename(index={'sample_config': 'config', 'sample_enwik8': 'text', 'sample_image-data': 'image',
                           'sample_music': 'music', 'sample_vid.mp4': 'video'}, inplace=True)
ax = size_dataset.plot.bar(rot=45)
ax.legend(loc='lower left')
ax.set_ylabel("file size [bytes]")
ax.grid(axis='y')
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("size.png")

# bar chart for compressed size per dataset two bars (lzma, bzip2) space saving
size_dataset[("LZMA", "space_savings")] = (1 - (size_dataset[("LZMA", "compressed")] / size_dataset[("-", "uncompressed")])) * 100
size_dataset[("bzip2", "space_savings")] = (1 - (size_dataset[("bzip2", "compressed")] / size_dataset[("-", "uncompressed")])) * 100
space_savings = size_dataset.drop(columns=[("LZMA", "compressed"), ("-", "uncompressed"), ("bzip2", "compressed")])
space_savings.rename(index={'sample_config': 'config', 'sample_enwik8': 'text', 'sample_image-data': 'image',
                            'sample_music': 'music', 'sample_vid.mp4': 'video'}, inplace=True)
ax = space_savings.plot.bar(rot=45)
ax.legend(loc='upper left')
ax.set_ylabel("space savings [%]")
ax.grid(axis='y')
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("space_savings.png")


# boxplot cpu+user time per dataset two plots (lzma, bzip2) for compression
# print(time_dataset)
comp_time_dataset = time_dataset.loc[:, (slice(None), slice(None), ['compression'], slice(None))]
comp_time_dataset = comp_time_dataset.droplevel(2, axis=1)
comp_time_dataset = comp_time_dataset.droplevel(2, axis=1)
comp_time_dataset.columns.set_levels(['config', 'text', 'image', 'music', 'video'], level=0, inplace=True)
ax = comp_time_dataset.plot.box(rot=45)
# ax.legend(loc='upper left')
ax.set_ylabel("CPU-time (system+user) [s]")
ax.grid(axis='y')
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("comp_cpu.png")

# boxplot cpu+user time per dataset two plots (lzma, bzip2) for decompression
decomp_time_dataset = time_dataset.loc[:, (slice(None), slice(None), ['decompression'], slice(None))]
decomp_time_dataset = decomp_time_dataset.droplevel(2, axis=1)
decomp_time_dataset = decomp_time_dataset.droplevel(2, axis=1)
decomp_time_dataset.columns.set_levels(['config', 'text', 'image', 'music', 'video'], level=0, inplace=True)
ax = decomp_time_dataset.plot.box(rot=45)
# ax.legend(loc='upper left')
ax.set_ylabel("CPU-time (system+user) [s]")
ax.grid(axis='y')
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("decomp_cpu.png")


# boxplot max resident set size per dataset two plots (lzma, bzip2) for compression
comp_space_dataset = space_dataset.loc[:, (slice(None), slice(None), ['compression'], slice(None))]
comp_space_dataset = comp_space_dataset.droplevel(2, axis=1)
comp_space_dataset = comp_space_dataset.droplevel(2, axis=1)
comp_space_dataset.columns.set_levels(['config', 'text', 'image', 'music', 'video'], level=0, inplace=True)
ax = comp_space_dataset.plot.box(rot=45)
# ax.legend(loc='upper left')
ax.set_ylabel("maximum resident set size [Kilobytes]")
ax.grid(axis='y')
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("comp_mem.png")

# boxplot max resident set size per dataset two plots (lzma, bzip2) for decompression
decomp_space_dataset = space_dataset.loc[:, (slice(None), slice(None), ['decompression'], slice(None))]
decomp_space_dataset = decomp_space_dataset.droplevel(2, axis=1)
decomp_space_dataset = decomp_space_dataset.droplevel(2, axis=1)
decomp_space_dataset.columns.set_levels(['config', 'text', 'image', 'music', 'video'], level=0, inplace=True)
ax = decomp_space_dataset.plot.box(rot=45)
# ax.legend(loc='upper left')
ax.set_ylabel("maximum resident set size [Kilobytes]")
ax.grid(axis='y')
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("decomp_mem.png")
