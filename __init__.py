"""H3 Long Video Manager. V3 migration by RAFOLIE, 2026-09-28."""
import logging
import os

from comfy_api.latest import ComfyExtension
from .comfyui.nodes import NODE_LIST
from .comfyui.server_api import register_h3lvm_routes
from .fork_guard import find_other_copy

logger = logging.getLogger(__name__)

_OTHER_COPY = find_other_copy(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.join("comfyui", "nodes.py"),
    "node_id='H3 Long Video Manager'",
)

if _OTHER_COPY:
    logger.warning(
        "[H3 LVM 熙云版] 检测到另一份 H3 Long Video Manager：%s。"
        "为避免同名节点、API 路由和前端互相覆盖，熙云版已跳过加载。"
        "要使用熙云版，请禁用或改名另一份（例如改成 H3-Long-Video-Manager.disabled）；"
        "确实需要强制同时加载时，设置环境变量 H3_XYIYUN_ALLOW_DUPLICATE=1（不推荐）。",
        _OTHER_COPY,
    )

# When another copy exists, serving this fork's web files would let its panels
# attach to the other copy's identically named nodes. Keep the fork inert.
WEB_DIRECTORY = None if _OTHER_COPY else "./web"


class H3LongVideoExtension(ComfyExtension):
    async def get_node_list(self):
        if _OTHER_COPY:
            return []
        return NODE_LIST


async def comfy_entrypoint():
    if not _OTHER_COPY:
        register_h3lvm_routes()
    return H3LongVideoExtension()
