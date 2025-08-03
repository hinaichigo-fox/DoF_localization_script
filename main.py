import asyncio
import time

from src import (
    logger,
    Paratranz,
    ProjectDOL,
    PARATRANZ_TOKEN,
    CHINESE_VERSION,
    SOURCE_TYPE,
)

from src.tools.process_variables import VariablesProcess as VP


async def process_common(dol_common: ProjectDOL, pt: Paratranz, chs_version: str):

    var = VP()
    var.fetch_all_file_paths()
    var.fetch_all_set_content()

    """ 创建生肉词典 """
    await dol_common.create_dicts()
    await dol_common.update_dicts()
    blacklist_dirs = [
        # "00-framework-tools",
        # "01-config",
        # "03-JavaScript",
        # "04-Variables",
        # "base-clothing",
        # "base-combat",
        # "base-debug",
        # "base-system",
        # "flavour-text-generators",
        # "fonts",
        # "overworld-forest",
        # "overworld-plains",
        # "overworld-town",
        # "overworld-underground",
        # "special-dance",
        # "special-exhibition",
        # "special-masturbation",
        # "special-templates"
    ]
    blacklist_files = []
    await dol_common.apply_dicts(blacklist_dirs, blacklist_files, debug_flag=False)


async def main():
    start = time.time()
    # =====
    dol_common = ProjectDOL(
        type_=SOURCE_TYPE
    )  # 改成 “dev” 则下载最新开发版分支的内容 common原版

    pt_common = Paratranz(type_=SOURCE_TYPE)
    #if not PARATRANZ_TOKEN:
        #logger.error("未填写 PARATRANZ_TOKEN, 汉化包下载可能失败，请前往 https://paratranz.cn/users/my 的设置栏中查看自己的 token, 并在 .env 中填写\n")
        #return

    await process_common(dol_common, pt_common, chs_version=CHINESE_VERSION)

    end = time.time()
    return end - start


if __name__ == "__main__":
    last = asyncio.run(main())
    logger.info(f"===== 总耗时 {last or -1:.2f}s =====")
    try:
        from win10toast import ToastNotifier
    except ImportError:
        pass
    else:
        ToastNotifier().show_toast(title="dol脚本运行完啦", msg=f"总耗时 {last or -1:.2f}s")
