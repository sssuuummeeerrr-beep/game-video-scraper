"""飞书多维表格写入模块"""

import requests
import time
from datetime import datetime
from config import FEISHU_APP_ID, FEISHU_APP_SECRET

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
BITABLE_API = "https://open.feishu.cn/open-apis/bitable/v1/apps"

FIELDS = [
    ("来源", 1),
    ("视频ID", 1),
    ("视频标题", 1),
    ("UP主", 1),
    ("播放量", 2),
    ("点赞量", 2),
    ("评论数", 2),
    ("分享数", 2),
    ("收藏数", 2),
    ("时长(秒)", 2),
    ("标签", 1),
    ("视频链接", 15),
    ("抓取时间", 1),
    ("爆款原因", 1),
    ("优化建议", 1),
]


class FeishuBitable:
    def __init__(self):
        self.token = None
        self.token_expire_at = 0
        self._auth()

    def _auth(self):
        if time.time() < self.token_expire_at - 60:
            return
        resp = requests.post(TOKEN_URL, json={
            "app_id": FEISHU_APP_ID,
            "app_secret": FEISHU_APP_SECRET,
        }, timeout=15)
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"飞书认证失败: {data.get('msg')}")
        self.token = data["tenant_access_token"]
        self.token_expire_at = time.time() + data.get("expire", 7200)

    @property
    def _headers(self):
        self._auth()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _list_tables(self, app_token: str) -> dict:
        """返回 {表名: table_id} 映射"""
        resp = requests.get(
            f"{BITABLE_API}/{app_token}/tables",
            headers=self._headers, timeout=15,
        )
        data = resp.json()
        tables = {}
        if data.get("code") == 0:
            for item in data["data"]["items"]:
                tables[item["name"]] = item["table_id"]
        return tables

    def _create_table(self, app_token: str, name: str) -> str:
        """创建子表并初始化字段，返回 table_id"""
        # 创建子表
        resp = requests.post(
            f"{BITABLE_API}/{app_token}/tables",
            headers=self._headers,
            json={"table": {"name": name}},
            timeout=15,
        )
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"创建子表失败: {data.get('msg')}")
        table_id = data["data"]["table_id"]

        # 获取默认字段并删除多余的，保留第一个文本字段重命名为"来源"
        resp = requests.get(
            f"{BITABLE_API}/{app_token}/tables/{table_id}/fields",
            headers=self._headers, timeout=15,
        )
        fields_data = resp.json()
        existing = fields_data.get("data", {}).get("items", [])
        primary_field_id = None
        to_delete = []

        for f in existing:
            fid = f["field_id"]
            if f.get("is_primary"):
                primary_field_id = fid
            elif f["field_name"] in ("单选", "日期", "附件", "多选", "人员", "复选框", "电话", "邮箱"):
                to_delete.append(fid)

        # 删多余字段
        for fid in to_delete:
            requests.delete(
                f"{BITABLE_API}/{app_token}/tables/{table_id}/fields/{fid}",
                headers=self._headers, timeout=15,
            )
            time.sleep(0.15)

        # 重命名主字段为"来源"
        if primary_field_id:
            requests.put(
                f"{BITABLE_API}/{app_token}/tables/{table_id}/fields/{primary_field_id}",
                headers=self._headers,
                json={"field_name": "来源", "type": 1},
                timeout=15,
            )
            time.sleep(0.15)

        # 添加业务字段（跳过"来源"因为已有）
        url = f"{BITABLE_API}/{app_token}/tables/{table_id}/fields"
        for field_name, field_type in FIELDS:
            if field_name == "来源":
                continue
            requests.post(url, headers=self._headers, json={
                "field_name": field_name,
                "type": field_type,
            }, timeout=15)
            time.sleep(0.15)

        return table_id

    def get_or_create_table(self, app_token: str, table_name: str) -> str:
        """获取或创建指定名称的子表，返回 table_id"""
        tables = self._list_tables(app_token)
        if table_name in tables:
            return tables[table_name]
        return self._create_table(app_token, table_name)

    def write_records(
        self, app_token: str, table_id: str, records: list[dict]
    ) -> int:
        """批量写入记录到指定子表，返回成功写入条数"""
        URL_FIELDS = {"url", "视频链接"}

        items = []
        for r in records:
            fields = {}
            for key, val in r.items():
                if isinstance(val, int):
                    fields[key] = val
                elif val is None:
                    fields[key] = ""
                elif key in URL_FIELDS:
                    fields[key] = {"link": str(val), "text": str(val)}
                else:
                    fields[key] = str(val)
            items.append({"fields": fields})

        count = 0
        batch_size = 500
        url = f"{BITABLE_API}/{app_token}/tables/{table_id}/records/batch_create"
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            resp = requests.post(url, headers=self._headers, json={"records": batch}, timeout=30)
            data = resp.json()
            if data.get("code") != 0:
                print(f"  写入失败 (batch {i}): {data.get('msg')}")
            else:
                count += len(batch)

        return count

    def delete_table(self, app_token: str, table_id: str) -> bool:
        """删除子表（用于清理）"""
        resp = requests.delete(
            f"{BITABLE_API}/{app_token}/tables/{table_id}",
            headers=self._headers, timeout=15,
        )
        return resp.json().get("code") == 0
