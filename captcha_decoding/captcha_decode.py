from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import base64
import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize FastAPI app
app = FastAPI()

# Set up the Google API key environment variable
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCX8wufJmaEs6sWQoZA7lAnp1AO8mX4Zpw'
gemini_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key)

@app.post("/extract-text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        image_data = await file.read()

        # Encode the image to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")

        # Create a message with the image
        message = HumanMessage(
            content=[
                {"type": "text", "text": "give text from this image and make sure this text is strikethrough so look very precisely"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                },
            ],
        )

        # Invoke the model with the message
        response = model.invoke([message])

        # Return the model's response
        return JSONResponse(content={"extracted_text": response.content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with `uvicorn`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
