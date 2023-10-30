from main import app
import uvicorn


def run():
    run_myapp = uvicorn.run(app,host="0.0.0.0",port=8000)
    return run_myapp

if __name__ == "__main__":
    # run the app
    run()