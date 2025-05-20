from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from ..services.color_analysis import process_image, change_image_skin_tone
import io

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    
    image, skin_tone, palette = process_image(file)
    
    return {
        "skin_tone": skin_tone.tolist(),
        "color_palette": palette
    }

@router.post("/change-skin-tone")
async def change_skin_tone(file: UploadFile = File(...), target_tone: str):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image")
    
    try:
        target_tone = [int(x) for x in target_tone.split(',')]
        if len(target_tone) != 3:
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid target tone format. Use 'R,G,B'")
    
    adjusted_image = change_image_skin_tone(file, target_tone)
    
    return StreamingResponse(io.BytesIO(adjusted_image.getvalue()), media_type="image/png")