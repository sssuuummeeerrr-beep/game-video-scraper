"""飞书多维表格写入模块"""

import requests
import time
from config import FEISHU_APP_ID, FEISHU_APP_SECRET

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
BATCH_URL = "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"


class FeishuBitable:
    def __init__(self):
        self.token = None
        self.token_expire_at = 0
        self._auth()

    def _auth(self):
        """获取 tenant_access_token（有效期 2 小时，自动刷新）"""
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

    def append_records(
        self, app_token: str, table_id: str, records: list[dict]
    ) -> int:
        """批量追加记录到多维表格，返回成功写入条数"""
        self._auth()

        URL_FIELDS = {"url", "视频链接"}  # 需格式化为链接对象

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
        # 飞书单次最多 500 条，分批写入
        batch_size = 500
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            resp = requests.post(
                BATCH_URL.format(app_token=app_token, table_id=table_id),
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                json={"records": batch},
                timeout=30,
            )
            data = resp.json()
            if data.get("code") != 0:
                print(f"  写入失败 (batch {i}): {data.get('msg')}")
            else:
                count += len(batch)

        return count
