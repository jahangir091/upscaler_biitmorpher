import os
import uvicorn
import time
from PIL import Image

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from codeformer.app import inference_app
from utils import UpscaleImageRequest, encode_pil_to_base64, save_image


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ai/api/v1/upscaler-server-test")
def upscaler_server_test():
    return "Upscale server is working fine. OK!"


@app.post("/ai/api/v1/upscale")
async def upscale_single_image(request: UpscaleImageRequest):
    stime = time.time()
    input_image = request.image
    if not input_image:
        return {
            "success": False,
            "message": "Input image not found",
            "server_process_time": '',
            "output_image_url": ''
        }
    image_path = save_image(input_image)
    restored_image_path = inference_app(
        image=image_path,
        background_enhance=True,
        face_upsample=True,
        upscale=2,
        codeformer_fidelity=0.5,
    )

    # out_pil_img = Image.open(restored_image_path)
    # upscaled_img_base64 = encode_pil_to_base64(out_pil_img)
    # os.remove(image_path)
    print('server process time: {0}'.format(time.time()-stime))
    return {
        "success": True,
        "message": "Returned output successfully",
        "server_process_time": time.time() - stime,
        "output_image_url": 'media' + '/upscaler_images/' + restored_image_path.split('/')[-1]
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)