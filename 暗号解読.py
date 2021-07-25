import pathlib

import src

# 目的の暗号文
text_target = (
    'kjqp wcai srxw qmas eupf oczo qzvg zgww'
    'kyez vtem tpzh vnot kzhr ccfq lvrp ccwl'
    'wpuy onfh ogdd mojx ggbh wwux njez axfu'
    'meys ecsm azfx nnas szgw rbdd mapg mrwt'
    'gxxz axlb xcph zbou yvrr vfdk hxmq ogyl'
    'yycu wqbt adrl bozk yxqp wuua fmiz tcea'
    'xbcr edhz jdop sqtn lihi qhnm jzuh smva'
    'hhqj lijr rxqz nfkh uiin zpmp aflh yonm'
    'rmda dfox tyop ewej geca hpyf vmci xaqd'
    'yiag zxld tfjw jqzm gbsn ermi pckp ovlt'
    'hzot uxql rsrz nqld hxhl ghyd nzkv bfdm'
    'xrzb romd prux hmfs hj'
).replace(' ', '').upper()


# スクランバーとリフレクターの設定
str_scramber1 = 'ajdk siru xblh wtmc qgzn pyfv oe'
str_scramber2 = 'ekmf lgdq vznt owyh xusp aibr cj'
str_scramber3 = 'bdfh jlcp rtxv znye iwga kmus qo'
strs_scramber = [str_scramber1, str_scramber2, str_scramber3]
str_reflector = 'yruh qsld pxng okmi ebfz cwvj at'

# 結果データの出力先
folder_result = pathlib.Path.cwd() / 'result'
name_file = '暗号解読_エニグマ'

slvr = src.solver.EnigmaSolver(
    'alphabet', strs_scramber, str_reflector, (2, 1, 3),
    folder_result, name_file
)
text_result, stdev = slvr.execute(text_target, 10)
print(f'result:\n{text_result}')
