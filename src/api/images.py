import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image_path

router = APIRouter(prefix="/images", tags=["Изображения отелей"])

@router.post("")
def upload_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image_path.delay(image_path)
