""" app control """
import time

import pandas as pd

# from src.pkl import load_pkl
from src.execution_time import Execution

from src.beam_name import load_beam_name, init_beam_name
from src.beam import init_beam, put_column_order
from src.e2k import load_e2k
from src.etabs_design import load_etabs_design, post_e2k
from src.stirrups import calc_stirrups, calc_stirrups_3
from src.bar_size_num import calc_db
from src.bar_ld import calc_ld, add_ld, add_max_d_12db
from src.bar_cut import cut_optimization
from src.bar_cut_v1 import cut_optimization as cut_optimization_v1
from src.bar_traditional import cut_traditional

# 不管是物件導向設計還是函數式編程 只要能解決問題的就是好方法
# 現在還只是看的不爽 所以並沒有造成問題
# 物件導向是對於真實世界的物體的映射
# 函數式編程是對於資料更好的操控


def cut_multiple(etabs_design, const, vc, by='BayID', group_num=3):
    """
    多點斷筋
    """
    # 初始化輸出表格
    beam = init_beam(etabs_design)
    # 計算箍筋
    beam, etabs_design = calc_stirrups_3(beam, etabs_design, const, vc)
    # 計算主筋
    etabs_design = calc_db(by, etabs_design, const)
    # 計算延伸長度
    etabs_design = calc_ld(etabs_design, const)
    # 加上延伸長度
    etabs_design = add_ld(etabs_design, 'Ld', const)
    etabs_design = add_max_d_12db(etabs_design, const)
    # 多點斷筋
    beam = cut_optimization_v1(beam, etabs_design, const, group_num)

    beam = put_column_order(beam)

    return beam, etabs_design


def cut_trational(etabs_design, const, vc, by='BayID'):
    """
    傳統斷筋
    """
    # 初始化輸出表格
    beam = init_beam(etabs_design)
    # 計算箍筋
    beam, etabs_design = calc_stirrups(beam, etabs_design, const, vc)
    # 計算主筋
    etabs_design = calc_db(by, etabs_design, const)
    # 計算延伸長度
    etabs_design = calc_ld(etabs_design, const)
    # 傳統斷筋
    beam = cut_traditional(beam, etabs_design, const['rebar'])

    beam = put_column_order(beam)

    return beam, etabs_design


def cut_by_beam(const, group_num=3):
    """ run by beam, no need beam name ID"""
    execution = Execution()

    # get input data
    e2k = load_e2k(const['e2k_path'])
    etabs_design = load_etabs_design(const['etabs_design_path'])
    etabs_design = post_e2k(etabs_design, e2k)

    # output path
    writer = pd.ExcelWriter(
        f'{const["output_dir"]}/'
        f'{time.strftime("%Y%m%d %H%M%S", time.localtime())} '
        f'Cut {group_num - 1}.xlsx'
    )

    execution.time('傳統斷筋')
    beam_tra, etabs_design_tra = cut_trational(
        etabs_design, const, vc=False, by='BayID')
    execution.time()

    execution.time('多點斷筋')
    beam, etabs_design = cut_multiple(
        etabs_design, const, vc=False, by='BayID', group_num=group_num)
    execution.time()

    beam_name_empty = init_beam_name(etabs_design)

    beam_name_empty, beam, beam_tra, etabs_design, etabs_design_tra = load_pkl(
    #     const['output_dir'] + '/design.pkl')

    # 輸出成表格
    execution.time('Output Result')
    beam_name_empty.to_excel(writer, '梁名編號')
    beam.to_excel(writer, '多點斷筋')
    beam_tra.to_excel(writer, '傳統斷筋')
    etabs_design.to_excel(writer, 'etabs_design')
    etabs_design_tra.to_excel(writer, 'etabs_design_trational')
    pd.DataFrame.from_dict(const, orient='index').to_excel(writer, 'config')
    writer.save()
    execution.time()


def cut_by_frame(const, moment=3):
    pass
# 晚一點在做 目前不重要
# def cut_by_frame(const, moment=3):
#     """ run by frame, need beam name ID"""
#     e2k_path, etabs_design_path, beam_name_path, output_dir = const[
#         'e2k_path'], const['etabs_design_path'], const['beam_name_path'], const['output_dir']

#     execution = Execution()

#     # get input data
#     e2k = load_e2k(e2k_path, e2k_path + '.pkl')
#     etabs_design = load_beam_design(
#         etabs_design_path, etabs_design_path + '.pkl')
#     beam_name = load_beam_name(beam_name_path, beam_name_path + '.pkl')

#     # output path
#     writer = pd.ExcelWriter(
#         output_dir + '/' + time.strftime("%Y%m%d %H%M%S", time.localtime()) + ' SmartCut.xlsx')

#     # 初始化輸出表格
#     execution.time('Initialize Output Table')
#     beam_traditional = init_beam(etabs_design, e2k)
#     beam = init_beam(etabs_design, e2k, moment=moment)
#     # no change tradition beam id
#     beam, etabs_design = add_and_alter_beam_id(
#         beam, beam_name, etabs_design)
#     execution.time()

#     # 計算箍筋
#     execution.time('Calculate Stirrup Size and Spacing')
#     beam, dh_design = calc_stirrups(
#         beam, etabs_design, e2k, const, consider_vc=False)
#     beam_traditional, _ = calc_stirrups(
#         beam_traditional, etabs_design, e2k, const, consider_vc=False)
    (beam, beam_traditional, dh_design) = load_pkl(
#         output_dir + '/dh_design.pkl', (beam, beam_traditional, dh_design))
#     execution.time()

#     # 以一台梁為單位 計算主筋
#     execution.time('Calculate Rebar Size and Number by Frame')
#     db_design = calc_db('FrameID', dh_design, e2k, const)
    db_design = load_pkl(output_dir + '/db_design.pkl', db_design)
#     execution.time()

#     # 計算延伸長度
#     execution.time('Calculate Ld')
#     ld_design = calc_ld(db_design, e2k, const)
#     execution.time()

#     # 加上延伸長度
#     execution.time('Add Ld')
#     ld_design = add_ld(ld_design, 'Ld', const)
    ld_design = load_pkl(output_dir + '/ld_design.pkl', ld_design)
#     execution.time()

#     # 傳統斷筋
#     execution.time('Traditional Cut')
#     beam_traditional = cut_traditional(
#         beam_traditional, ld_design, const['rebar'])
#     execution.time()

#     # 多點斷筋
#     execution.time('Multi Smart Cut')
#     beam = cut_optimization(moment, beam, ld_design, const)
#     execution.time()

#     # 輸出成表格
#     execution.time('Output Result')
#     beam.to_excel(writer, '多點斷筋')
#     beam_traditional.to_excel(writer, '傳統斷筋')
#     ld_design.to_excel(writer, 'etabs_design')
#     beam_name.to_excel(writer, '梁名編號')
#     writer.save()
#     execution.time()


if __name__ == "__main__":
    from tests.const import const as constants

    cut_by_beam(constants, 3)
    # cut_by_frame(constants)
