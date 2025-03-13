from datetime import datetime

from sqlalchemy.orm import Session

from server.entity import schema, model
from .device import get_owner_by_code, get_device_by_key


def init(request: schema.DeviceBaseQuery, db: Session):
    try:
        # 开启事务
        with db.begin():
            # 验证归属者有效性
            owner = get_owner_by_code(request.code, db)
            if not owner or owner.status != "0":
                raise ValueError(f"无效的归属者代码: {request.code}")

            # 处理设备存在性验证
            if device := get_device_by_key(request.device_key, db):
                if device.status != '0':
                    raise ValueError(f"设备已禁用: {request.device_key}")
                return owner, device

            # 创建设备记录
            new_device = model.Device(
                device_key=request.device_key,
                status='0',
                create_by="system",
                create_time=datetime.now(),
                remark=""
            )
            db.add(new_device)
            db.flush()  # 立即生成设备ID

            # 创建关联关系
            db.add(model.DeviceOwner(
                device_id=new_device.device_id,
                owner_id=owner.owner_id
            ))

        db.commit()
        db.refresh(new_device)
        return owner, new_device

    except ValueError as ve:
        db.rollback()
        return None, None
    except Exception as e:
        db.rollback()
        return None, None