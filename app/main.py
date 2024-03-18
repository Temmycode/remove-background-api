from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import rembg

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return HTMLResponse("<h1>Hello Man</h1>")


@app.post("/remove-background")
async def remove_background(image: UploadFile = File(...)):
    try:
        content = await image.read()
        output = rembg.remove(content)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(output)
        return FileResponse(
            path=temp_file.name, media_type="image/png", status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
