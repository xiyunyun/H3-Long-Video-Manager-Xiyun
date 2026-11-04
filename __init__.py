"""H3 Long Video Manager. V3 migration by RAFOLIE, 2026-09-28."""
import logging
import os

from comfy_api.latest import ComfyExtension
from .comfyui.nodes import NODE_LIST
from .comfyui.ref_presets import migrate_input_media
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
        # Reference presets from before the dedicated input folder point at the input
        # root. Adopting copies keeps them loadable without breaking workflows that
        # still use the originals; the migration is idempotent and cheap after the
        # first run.
        try:
            report = migrate_input_media()
            if report["entries"]:
                logger.info("[H3 LVM 熙云版] 参考素材迁移完成：%d 个项目、%d 张卡片已指向 input/%s",
                            report["projects"], report["entries"], "h3-lvm-refs")
        except Exception:
            logger.warning("[H3 LVM 熙云版] 参考素材迁移失败（节点仍可使用）", exc_info=True)
        register_h3lvm_routes()
    return H3LongVideoExtension()
