from nonebot.adapters.onebot.v11 import MessageEvent as ME
from nonebot.adapters.onebot.v11 import MessageSegment as MS

from nonebot.typing import T_State
from nonebot.params import ArgPlainText

from .base import(
    cmd_session,
    get_sessions_list,
    get_session_id,
    session_delete,
    session_select,
    fl_group_at
)

from ...config import Config
from nonebot import get_plugin_config
conf = get_plugin_config(Config)
command = conf.sparkapi_commands["session_delete"]

matcher_session_delete = cmd_session.command(command)
@matcher_session_delete.handle()
async def _(event:ME):
    session_id = get_session_id(event)
    session_list = get_sessions_list(session_id)
    msg = f"{session_list}\n\n输入序号选择会话，回复其他内容取消删除"
    await matcher_session_delete.send(MS.text(msg), at_sender=fl_group_at)

@matcher_session_delete.got("index")
async def _(event:ME, state:T_State, index=ArgPlainText()):
    if not index.isdigit():
        await matcher_session_delete.finish(MS.text("已取消删除"), at_sender=fl_group_at)
    session_id = get_session_id(event)
    session_list = get_sessions_list(session_id)
    idx = int(index)
    if idx not in range(len(session_list)) or idx == 0:
        await matcher_session_delete.reject(MS.text("序号不合法，请重新输入"), at_sender=fl_group_at)
    session = session_select(session_id, index=idx)
    msg = f"{session.get_info()}\n\n确认删除该会话？\n回复“确认”确认删除，回复其他内容取消删除"
    await matcher_session_delete.send(MS.text(msg), at_sender=fl_group_at)
    state["index"] = idx

@matcher_session_delete.got("check")
async def _(event:ME, state:T_State, check=ArgPlainText()):
    if check!="确认":
        await matcher_session_delete.finish(MS.text("已取消删除"), at_sender=fl_group_at)
    session_id = get_session_id(event)
    index = state["index"]
    try:
        session_delete(session_id, index=index)
    except Exception as e:
        await matcher_session_delete.finish(MS.text(f"删除失败！请联系开发者。\n错误信息：{type(e)}:{e}"), at_sender=fl_group_at)
    await matcher_session_delete.finish(MS.text("会话删除成功！"), at_sender=fl_group_at)
