from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session

from server import service
from server.context import database
from server.entity import schema
from server.entity.schema import R

router = APIRouter(prefix='/system/v1', tags=['System'])


@router.post(
    "/init",
    response_model=R[schema.DeviceInitReply],
    response_model_exclude_none=True
)
async def start_feedback(
        request: schema.DeviceBaseQuery,
        db: Session = Depends(database.session)
):
    owner, device = service.init(request, db)
    if not device or not owner:
        return R(code=status.HTTP_403_FORBIDDEN, msg="invalid_device")
    return R(data=schema.DeviceInitReply(
        device_id=device.device_id,
        owner_id=owner.owner_id
    ))
